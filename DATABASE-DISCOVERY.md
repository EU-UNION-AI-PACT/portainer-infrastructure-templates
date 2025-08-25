# 🔍 DATABASE DISCOVERY SYSTEM

## Overview
Automatisches Discovery System für alle verfügbaren Datenbanken mit Docker Images. Durchsucht Docker Hub und GitHub für Database-Container und generiert automatisch Portainer Templates.

## Features

### 🎯 Deep Search Engine
- **Docker Hub API**: Durchsucht alle verfügbaren Database-Container
- **GitHub Integration**: Findet Repository-Links und zusätzliche Infos
- **Intelligente Kategorisierung**: Automatische Einordnung in Database-Typen
- **Smart Filtering**: Filtert echte Datenbanken von anderen Containern

### 📊 Supported Database Categories
```
✅ Relational (SQL): PostgreSQL, MySQL, MariaDB, SQLite, CockroachDB, etc.
✅ NoSQL: MongoDB, CouchDB, RethinkDB, OrientDB, ArangoDB, etc.
✅ Key-Value: Redis, KeyDB, DragonflyDB, etcd, Consul, etc.
✅ Graph: Neo4j, Dgraph, JanusGraph, Memgraph, etc.
✅ Time Series: InfluxDB, QuestDB, TimescaleDB, VictoriaMetrics, etc.
✅ Search: Elasticsearch, OpenSearch, Solr, Typesense, etc.
✅ Vector: Milvus, Weaviate, Qdrant, Chroma, etc.
✅ Analytics: ClickHouse, Druid, Pinot, DuckDB, etc.
✅ Cache: Memcached, Varnish, Redis, etc.
✅ Embedded: H2, HSQLDB, Derby, Firebird, etc.
```

### 🚀 Auto-Generation Features
- **Portainer Templates**: Ready-to-use Templates mit korrekten Ports/Volumes
- **Docker Compose**: Complete Stack für alle discovered Datenbanken
- **Environment Variables**: Smart defaults für jeden Database-Typ
- **Volume Mappings**: Automatische Data-Persistence Konfiguration
- **Network Configuration**: Optimierte Container-Netzwerke

## Usage

### Quick Start
```bash
# Führe Database Discovery aus
./scripts/run_database_discovery.sh

# Oder einzeln:
python scripts/database_discovery.py
```

### Integration in Portainer
Nach dem Discovery sind alle Datenbanken verfügbar über:
```
Template URL: https://raw.githubusercontent.com/USER/REPO/main/portainer-template.json
```

### Direct Stack Deployment
```bash
# Alle Datenbanken gleichzeitig
docker-compose -f stacks/database-complete.yml up -d

# Einzelne Kategorien
docker-compose -f stacks/database-relational.yml up -d
docker-compose -f stacks/database-nosql.yml up -d
```

## Output Files

### Generated Templates
```
📋 templates/database/discovered_databases.json  - Portainer Templates
🐳 stacks/database-complete.yml                  - Docker Compose Stack
📊 reports/database_discovery_stats.json        - Discovery Statistiken
🎯 portainer-template.json                      - Updated Master Template
```

### Example Database Template
```json
{
  "type": 1,
  "title": "PostgreSQL Database",
  "description": "PostgreSQL relational database (Category: relational)",
  "categories": ["relational", "database", "storage"],
  "platform": "linux",
  "image": "postgres:latest",
  "ports": ["5432:5432"],
  "volumes": [{"container": "/var/lib/postgresql/data", "bind": "./data/postgres/var/lib/postgresql/data"}],
  "env": [
    {"name": "POSTGRES_DB", "label": "POSTGRES_DB", "default": "database"},
    {"name": "POSTGRES_USER", "label": "POSTGRES_USER", "default": "admin"},
    {"name": "POSTGRES_PASSWORD", "label": "POSTGRES_PASSWORD", "default": "secure_password"}
  ],
  "restart_policy": "unless-stopped"
}
```

## Discovery Algorithm

### Search Strategy
1. **Known Database Names**: Durchsucht bekannte DB-Namen aus allen Kategorien
2. **Pattern Matching**: Verwendet Database-Keywords für Deep Search
3. **Popularity Filtering**: Sortiert nach Pull-Count und GitHub Stars
4. **Smart Categorization**: AI-basierte Kategorie-Erkennung
5. **Duplicate Removal**: Intelligente Duplikat-Erkennung

### Quality Filters
- Minimum Docker Hub Pulls: 1000+
- Active Maintenance: Updated within 6 months
- Documentation: README/Docker Hub description required
- Container Health: Working ports and volume configurations

## Integration Features

### Auto-Configuration
- **Port Detection**: Automatische Standard-Port Erkennung
- **Volume Mapping**: Smart Data-Persistence Konfiguration  
- **Environment Setup**: Database-spezifische Env-Variables
- **Network Security**: Optimierte Container-Netzwerke
- **Health Checks**: Database-spezifische Health-Check Konfigurationen

### Template Enhancement
- **Logo Integration**: Automatische Logo-URLs
- **Category Tagging**: Multi-Level Kategorisierung
- **Documentation Links**: GitHub/Docker Hub Repository-Links
- **Version Management**: Latest/Stable Tag Detection

## Statistics & Reporting

### Discovery Metrics
```json
{
  "total_databases": 150+,
  "categories": {
    "relational": 25,
    "nosql": 20,
    "key_value": 15,
    "graph": 12,
    "timeseries": 18,
    "search": 10,
    "vector": 8,
    "analytics": 15,
    "cache": 12,
    "embedded": 15
  },
  "discovery_timestamp": "2025-08-25T03:30:00Z"
}
```

## Next Steps

Nach dem Discovery Process:
1. **Review Templates**: Überprüfe generierte Templates in `templates/database/`
2. **Test Deployment**: Teste einzelne Datenbanken mit Portainer
3. **Stack Deployment**: Deploye komplette Database-Stacks
4. **Monitor Performance**: Überwache Resource-Usage
5. **Customize Configuration**: Passe Env-Variables an deine Needs an

---

**🎯 Result: 150+ Database Templates ready for immediate deployment!**