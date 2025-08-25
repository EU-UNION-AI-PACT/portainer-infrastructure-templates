#!/usr/bin/env python3
"""
🔍 DATABASE DISCOVERY ENGINE
Deep Search für alle verfügbaren Datenbanken mit Docker Images
Automatische Integration in Portainer Templates
"""

import asyncio
import aiohttp
import json
import re
from typing import Dict, List, Set
from dataclasses import dataclass
import yaml

@dataclass
class DatabaseInfo:
    name: str
    category: str
    docker_image: str
    github_repo: str
    description: str
    ports: List[int]
    environment_vars: Dict[str, str]
    volumes: List[str]
    license: str = "Unknown"
    tags: List[str] = None

class DatabaseDiscovery:
    """Deep Search Engine für Database Discovery"""
    
    def __init__(self):
        self.session = None
        self.discovered_databases = []
        
        # Bekannte Database Kategorien für Deep Search
        self.database_categories = {
            "relational": ["postgresql", "mysql", "mariadb", "sqlite", "cockroachdb", "yugabytedb", "tidb"],
            "nosql": ["mongodb", "couchdb", "rethinkdb", "orientdb", "arangodb"],
            "key_value": ["redis", "keydb", "dragonflydb", "etcd", "consul", "hazelcast"],
            "graph": ["neo4j", "dgraph", "janusgraph", "memgraph", "hugegraph"],
            "timeseries": ["influxdb", "questdb", "timescaledb", "victoriametrics", "prometheus"],
            "search": ["elasticsearch", "opensearch", "solr", "typesense", "meilisearch", "vespa"],
            "vector": ["milvus", "weaviate", "qdrant", "pinecone", "chroma"],
            "analytics": ["clickhouse", "druid", "pinot", "duckdb", "monetdb"],
            "cache": ["memcached", "varnish", "squid", "nginx-cache"],
            "embedded": ["h2", "hsqldb", "derby", "firebird", "perst"]
        }
        
        # Docker Hub API Search Patterns
        self.search_patterns = [
            "database", "db", "sql", "nosql", "cache", "search-engine", 
            "timeseries", "graph-database", "vector-database", "analytics"
        ]

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def search_docker_hub(self, query: str, limit: int = 100) -> List[Dict]:
        """Docker Hub API Deep Search"""
        try:
            url = f"https://hub.docker.com/v2/search/repositories/"
            params = {
                "query": query,
                "page_size": limit,
                "ordering": "pull_count"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("results", [])
        except Exception as e:
            print(f"❌ Docker Hub Search Error für '{query}': {e}")
        return []

    async def search_github_repos(self, query: str) -> List[Dict]:
        """GitHub API für Repository Discovery"""
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": f"{query} database docker language:dockerfile",
                "sort": "stars",
                "order": "desc",
                "per_page": 50
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("items", [])
        except Exception as e:
            print(f"❌ GitHub Search Error für '{query}': {e}")
        return []

    def extract_database_info(self, docker_result: Dict, github_data: Dict = None) -> DatabaseInfo:
        """Extrahiert Database-Info aus Docker/GitHub Daten"""
        name = docker_result.get("name", "unknown")
        description = docker_result.get("short_description", "")
        docker_image = f"{docker_result.get('repo_owner', '')}/{name}"
        
        # Kategorie bestimmen
        category = self.determine_category(name, description)
        
        # Standard Ports basierend auf Database-Typ
        ports = self.get_default_ports(name, category)
        
        # Standard Environment Variables
        env_vars = self.get_default_env_vars(name, category)
        
        # Standard Volumes
        volumes = self.get_default_volumes(name, category)
        
        # GitHub Repo falls verfügbar
        github_repo = ""
        if github_data:
            github_repo = github_data.get("html_url", "")
        
        return DatabaseInfo(
            name=name,
            category=category,
            docker_image=docker_image,
            github_repo=github_repo,
            description=description,
            ports=ports,
            environment_vars=env_vars,
            volumes=volumes
        )

    def determine_category(self, name: str, description: str) -> str:
        """Bestimmt Database-Kategorie basierend auf Name/Description"""
        name_lower = name.lower()
        desc_lower = description.lower()
        
        for category, keywords in self.database_categories.items():
            if any(keyword in name_lower or keyword in desc_lower for keyword in keywords):
                return category
        
        # Fallback basierend auf Keywords
        if any(word in desc_lower for word in ["graph", "neo4j", "cypher"]):
            return "graph"
        elif any(word in desc_lower for word in ["time series", "metrics", "monitoring"]):
            return "timeseries"
        elif any(word in desc_lower for word in ["search", "index", "lucene", "elastic"]):
            return "search"
        elif any(word in desc_lower for word in ["vector", "embedding", "similarity"]):
            return "vector"
        elif any(word in desc_lower for word in ["cache", "memory", "redis"]):
            return "key_value"
        elif any(word in desc_lower for word in ["nosql", "document", "json"]):
            return "nosql"
        else:
            return "relational"

    def get_default_ports(self, name: str, category: str) -> List[int]:
        """Standard Ports für Database-Typen"""
        port_mapping = {
            "postgresql": [5432], "mysql": [3306], "mariadb": [3306],
            "mongodb": [27017], "redis": [6379], "elasticsearch": [9200, 9300],
            "neo4j": [7474, 7687], "influxdb": [8086], "cassandra": [9042],
            "clickhouse": [8123, 9000], "memcached": [11211]
        }
        
        name_lower = name.lower()
        for db_name, ports in port_mapping.items():
            if db_name in name_lower:
                return ports
        
        # Fallback basierend auf Kategorie
        category_ports = {
            "relational": [5432], "nosql": [27017], "key_value": [6379],
            "graph": [7474], "timeseries": [8086], "search": [9200],
            "vector": [8080], "analytics": [8123], "cache": [11211]
        }
        
        return category_ports.get(category, [8080])

    def get_default_env_vars(self, name: str, category: str) -> Dict[str, str]:
        """Standard Environment Variables"""
        name_lower = name.lower()
        
        if "postgres" in name_lower:
            return {
                "POSTGRES_DB": "database",
                "POSTGRES_USER": "admin",
                "POSTGRES_PASSWORD": "secure_password"
            }
        elif "mysql" in name_lower or "mariadb" in name_lower:
            return {
                "MYSQL_ROOT_PASSWORD": "secure_password",
                "MYSQL_DATABASE": "database",
                "MYSQL_USER": "admin",
                "MYSQL_PASSWORD": "secure_password"
            }
        elif "mongo" in name_lower:
            return {
                "MONGO_INITDB_ROOT_USERNAME": "admin",
                "MONGO_INITDB_ROOT_PASSWORD": "secure_password",
                "MONGO_INITDB_DATABASE": "database"
            }
        elif "redis" in name_lower:
            return {"REDIS_PASSWORD": "secure_password"}
        elif "elastic" in name_lower:
            return {
                "discovery.type": "single-node",
                "ES_JAVA_OPTS": "-Xms512m -Xmx512m"
            }
        
        return {"DB_PASSWORD": "secure_password"}

    def get_default_volumes(self, name: str, category: str) -> List[str]:
        """Standard Volume Mappings"""
        name_lower = name.lower()
        
        if "postgres" in name_lower:
            return ["/var/lib/postgresql/data"]
        elif "mysql" in name_lower or "mariadb" in name_lower:
            return ["/var/lib/mysql"]
        elif "mongo" in name_lower:
            return ["/data/db"]
        elif "redis" in name_lower:
            return ["/data"]
        elif "elastic" in name_lower:
            return ["/usr/share/elasticsearch/data"]
        elif "neo4j" in name_lower:
            return ["/data", "/logs"]
        elif "influx" in name_lower:
            return ["/var/lib/influxdb"]
        
        return ["/data"]

    async def discover_all_databases(self) -> List[DatabaseInfo]:
        """Main Discovery Engine - findet alle verfügbaren Datenbanken"""
        print("🔍 STARTE DATABASE DEEP SEARCH...")
        
        all_databases = []
        discovered_names = set()
        
        # 1. Suche nach bekannten Database-Kategorien
        for category, db_names in self.database_categories.items():
            print(f"🔍 Durchsuche {category.upper()} Datenbanken...")
            
            for db_name in db_names:
                # Docker Hub Search
                docker_results = await self.search_docker_hub(db_name)
                
                for result in docker_results[:5]:  # Top 5 pro DB
                    name = result.get("name", "")
                    if name not in discovered_names:
                        db_info = self.extract_database_info(result)
                        all_databases.append(db_info)
                        discovered_names.add(name)
                
                await asyncio.sleep(0.5)  # Rate limiting
        
        # 2. Deep Search mit allgemeinen Patterns
        print("🔍 Deep Search mit allgemeinen Database-Patterns...")
        for pattern in self.search_patterns:
            docker_results = await self.search_docker_hub(pattern, limit=50)
            
            for result in docker_results:
                name = result.get("name", "")
                description = result.get("short_description", "")
                
                # Filter für echte Datenbanken
                if self.is_database_related(name, description) and name not in discovered_names:
                    db_info = self.extract_database_info(result)
                    all_databases.append(db_info)
                    discovered_names.add(name)
            
            await asyncio.sleep(1)  # Rate limiting
        
        print(f"✅ DISCOVERED: {len(all_databases)} Datenbanken gefunden!")
        return all_databases

    def is_database_related(self, name: str, description: str) -> bool:
        """Filtert echte Database-Container"""
        db_keywords = [
            "database", "db", "sql", "nosql", "store", "cache", "search",
            "index", "graph", "timeseries", "analytics", "warehouse"
        ]
        
        text = f"{name} {description}".lower()
        return any(keyword in text for keyword in db_keywords)

    async def generate_portainer_templates(self, databases: List[DatabaseInfo]) -> Dict:
        """Generiert Portainer Templates aus discovered databases"""
        templates = []
        
        for db in databases:
            template = {
                "type": 1,
                "title": f"{db.name.title()} Database",
                "description": f"{db.description or f'{db.name} database container'} (Category: {db.category})",
                "categories": [db.category, "database", "storage"],
                "platform": "linux",
                "logo": f"https://raw.githubusercontent.com/docker-library/docs/master/{db.name}/logo.png",
                "image": db.docker_image,
                "ports": [f"{port}:{port}" for port in db.ports],
                "volumes": [{"container": vol, "bind": f"./data/{db.name}{vol}"} for vol in db.volumes],
                "env": [{"name": k, "label": k, "default": v} for k, v in db.environment_vars.items()],
                "restart_policy": "unless-stopped",
                "network_mode": "bridge"
            }
            
            if db.github_repo:
                template["repository"] = {"url": db.github_repo}
            
            templates.append(template)
        
        return {
            "version": "2",
            "templates": templates
        }

    async def generate_docker_compose(self, databases: List[DatabaseInfo]) -> str:
        """Generiert Docker Compose für alle Datenbanken"""
        services = {}
        
        for db in databases:
            service_name = db.name.replace("/", "_").replace("-", "_")
            
            service = {
                "image": db.docker_image,
                "container_name": f"{service_name}",
                "restart": "unless-stopped",
                "environment": db.environment_vars,
                "ports": [f"{port}:{port}" for port in db.ports],
                "volumes": [f"./data/{service_name}{vol}:{vol}" for vol in db.volumes],
                "networks": ["database_network"]
            }
            
            services[service_name] = service
        
        compose_data = {
            "version": "3.8",
            "services": services,
            "networks": {
                "database_network": {
                    "driver": "bridge"
                }
            },
            "volumes": {f"{service}_data": None for service in services.keys()}
        }
        
        return yaml.dump(compose_data, default_flow_style=False)

async def main():
    """Main Discovery Prozess"""
    async with DatabaseDiscovery() as discovery:
        # Deep Search für alle Datenbanken
        databases = await discovery.discover_all_databases()
        
        # Sortiere nach Kategorie und Popularität
        databases.sort(key=lambda x: (x.category, x.name))
        
        # Generiere Portainer Templates
        templates = await discovery.generate_portainer_templates(databases)
        
        # Speichere Templates
        with open("templates/database/discovered_databases.json", "w") as f:
            json.dump(templates, f, indent=2)
        
        # Generiere Docker Compose
        compose_content = await discovery.generate_docker_compose(databases)
        
        with open("stacks/database-complete.yml", "w") as f:
            f.write(compose_content)
        
        # Generiere Statistiken
        stats = {}
        for db in databases:
            category = db.category
            if category not in stats:
                stats[category] = []
            stats[category].append(db.name)
        
        with open("reports/database_discovery_stats.json", "w") as f:
            json.dump({
                "total_databases": len(databases),
                "categories": {k: len(v) for k, v in stats.items()},
                "databases_by_category": stats,
                "discovery_timestamp": "2025-08-25T03:30:00Z"
            }, f, indent=2)
        
        print("\n🎯 DATABASE DISCOVERY COMPLETE!")
        print(f"✅ {len(databases)} Datenbanken entdeckt")
        print(f"✅ {len(stats)} Kategorien erstellt")
        print("✅ Portainer Templates generiert: templates/database/discovered_databases.json")
        print("✅ Docker Compose erstellt: stacks/database-complete.yml")
        print("✅ Statistiken: reports/database_discovery_stats.json")

if __name__ == "__main__":
    asyncio.run(main())