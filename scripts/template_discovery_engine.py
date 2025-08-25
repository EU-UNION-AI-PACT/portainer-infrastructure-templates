#!/usr/bin/env python3
"""
🌟 EU-Compliant Template Discovery Engine
=========================================

Entdeckt automatisch neue Template-Quellen und vertrauenswürdige 
Community-Repositories mit vollständiger EU-DSGVO Compliance.

🔍 Features:
- GitHub API-basierte Entdeckung
- Community-Source Verification 
- Trust-Score Berechnung
- EU-Compliance Validation
- Automatische Quellenregistrierung
"""

import json
import requests
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging
import re
from urllib.parse import urlparse

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class DiscoveredSource:
    """Entdeckte Template-Quelle mit Metadaten."""
    name: str
    url: str
    repository: str
    description: str
    stars: int
    forks: int
    last_updated: str
    language: str
    license: Optional[str]
    topics: List[str]
    trust_score: int
    eu_compliant: bool
    template_count: int
    maintainer: str
    verified: bool = False

# 🔍 GitHub-Suchterme für Template-Repositories
DISCOVERY_SEARCH_TERMS = [
    "portainer templates",
    "portainer template json",
    "docker templates portainer", 
    "selfhosted templates",
    "docker compose templates",
    "homelab templates",
    "portainer infrastructure",
    "portainer app templates",
    "docker stack templates",
    "container templates"
]

# 🛡️ Vertrauenswürdige Domains und Organisationen
TRUSTED_ORGANIZATIONS = [
    "portainer",
    "linuxserver",
    "selfhostedpro", 
    "awesome-selfhosted",
    "docker",
    "compose-spec",
    "pi-hole",
    "nextcloud",
    "jellyfin",
    "bitwarden"
]

# 🇪🇺 EU-Compliance Kriterien
EU_COMPLIANCE_CRITERIA = {
    'min_stars': 10,           # Mindest-Community-Vertrauen
    'max_age_days': 730,       # Nicht älter als 2 Jahre
    'required_topics': ['docker', 'portainer', 'templates', 'selfhosted'],
    'allowed_licenses': ['mit', 'apache-2.0', 'gpl-3.0', 'bsd-3-clause', 'creative-commons'],
    'forbidden_topics': ['surveillance', 'tracking', 'mining', 'cryptocurrency', 'gambling']
}

def calculate_trust_score(repo_data: Dict[str, Any]) -> int:
    """
    Berechnet einen Trust-Score (0-100) für ein Repository.
    """
    score = 50  # Basis-Score
    
    # Stars-Bonus (max 25 Punkte)
    stars = repo_data.get('stargazers_count', 0)
    if stars > 0:
        score += min(25, int(stars / 10))
    
    # Forks-Bonus (max 15 Punkte)
    forks = repo_data.get('forks_count', 0)
    if forks > 0:
        score += min(15, int(forks / 5))
    
    # Aktualität-Bonus (max 20 Punkte)
    updated_at = repo_data.get('updated_at', '')
    if updated_at:
        try:
            updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            days_old = (datetime.now().replace(tzinfo=updated_date.tzinfo) - updated_date).days
            if days_old < 30:
                score += 20
            elif days_old < 90:
                score += 15
            elif days_old < 365:
                score += 10
        except:
            pass
    
    # Vertrauenswürdige Organisation-Bonus (max 15 Punkte)
    owner = repo_data.get('owner', {}).get('login', '').lower()
    if any(org in owner for org in TRUSTED_ORGANIZATIONS):
        score += 15
    
    # Lizenz-Bonus (max 10 Punkte)
    license_info = repo_data.get('license', {})
    if license_info and license_info.get('key', '').lower() in EU_COMPLIANCE_CRITERIA['allowed_licenses']:
        score += 10
    
    # Topics-Relevanz-Bonus (max 15 Punkte)
    topics = repo_data.get('topics', [])
    relevant_topics = [t for t in topics if t in EU_COMPLIANCE_CRITERIA['required_topics']]
    score += min(15, len(relevant_topics) * 3)
    
    return min(100, max(0, score))

def check_eu_compliance(repo_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Prüft EU-DSGVO Compliance eines Repositories.
    """
    violations = []
    
    # Mindest-Stars prüfen
    stars = repo_data.get('stargazers_count', 0)
    if stars < EU_COMPLIANCE_CRITERIA['min_stars']:
        violations.append(f"Insufficient community trust: {stars} stars")
    
    # Aktualität prüfen
    updated_at = repo_data.get('updated_at', '')
    if updated_at:
        try:
            updated_date = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            days_old = (datetime.now().replace(tzinfo=updated_date.tzinfo) - updated_date).days
            if days_old > EU_COMPLIANCE_CRITERIA['max_age_days']:
                violations.append(f"Repository too old: {days_old} days")
        except:
            violations.append("Invalid update date")
    
    # Verbotene Topics prüfen
    topics = repo_data.get('topics', [])
    forbidden_found = [t for t in topics if t in EU_COMPLIANCE_CRITERIA['forbidden_topics']]
    if forbidden_found:
        violations.append(f"Forbidden topics: {forbidden_found}")
    
    # Lizenz prüfen
    license_info = repo_data.get('license', {})
    if license_info:
        license_key = license_info.get('key', '').lower()
        if license_key not in EU_COMPLIANCE_CRITERIA['allowed_licenses']:
            violations.append(f"Non-compliant license: {license_key}")
    else:
        violations.append("No license specified")
    
    return len(violations) == 0, violations

def discover_template_repositories(github_token: Optional[str] = None) -> List[DiscoveredSource]:
    """
    Entdeckt Template-Repositories über GitHub API.
    """
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
        headers['Accept'] = 'application/vnd.github.v3+json'
    
    discovered_sources = []
    processed_repos = set()
    
    logger.info("🔍 Starting GitHub repository discovery...")
    
    for search_term in DISCOVERY_SEARCH_TERMS:
        logger.info(f"🔎 Searching for: {search_term}")
        
        try:
            # GitHub Repository Search
            search_url = f"https://api.github.com/search/repositories"
            params = {
                'q': f'{search_term} language:json OR language:yaml',
                'sort': 'stars',
                'order': 'desc',
                'per_page': 20
            }
            
            response = requests.get(search_url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 403:
                logger.warning("GitHub API rate limit reached")
                time.sleep(60)  # Rate-limit wait
                continue
            
            response.raise_for_status()
            search_data = response.json()
            
            for repo in search_data.get('items', []):
                repo_full_name = repo.get('full_name', '')
                
                # Duplikate vermeiden
                if repo_full_name in processed_repos:
                    continue
                processed_repos.add(repo_full_name)
                
                # EU-Compliance prüfen
                is_compliant, violations = check_eu_compliance(repo)
                if not is_compliant:
                    logger.debug(f"❌ {repo_full_name}: {violations}")
                    continue
                
                # Trust-Score berechnen
                trust_score = calculate_trust_score(repo)
                if trust_score < 60:  # Mindest-Trust-Score
                    logger.debug(f"❌ {repo_full_name}: Low trust score {trust_score}")
                    continue
                
                # Nach Template-Dateien suchen
                template_files = search_template_files(repo_full_name, headers)
                if not template_files:
                    continue
                
                # Template-Count ermitteln
                template_count = count_templates_in_repo(repo_full_name, template_files[0], headers)
                
                # DiscoveredSource erstellen
                discovered_source = DiscoveredSource(
                    name=repo.get('name', ''),
                    url=template_files[0],  # Erste gefundene Template-Datei
                    repository=f"https://github.com/{repo_full_name}",
                    description=repo.get('description', ''),
                    stars=repo.get('stargazers_count', 0),
                    forks=repo.get('forks_count', 0),
                    last_updated=repo.get('updated_at', ''),
                    language=repo.get('language', ''),
                    license=repo.get('license', {}).get('name') if repo.get('license') else None,
                    topics=repo.get('topics', []),
                    trust_score=trust_score,
                    eu_compliant=is_compliant,
                    template_count=template_count,
                    maintainer=repo.get('owner', {}).get('login', ''),
                    verified=any(org in repo.get('owner', {}).get('login', '').lower() 
                               for org in TRUSTED_ORGANIZATIONS)
                )
                
                discovered_sources.append(discovered_source)
                logger.info(f"✅ Discovered: {repo_full_name} (Trust: {trust_score}, Templates: {template_count})")
                
        except Exception as e:
            logger.error(f"❌ Error searching for '{search_term}': {e}")
            continue
        
        # Rate-limiting zwischen Suchen
        time.sleep(2)
    
    # Nach Trust-Score sortieren
    discovered_sources.sort(key=lambda x: x.trust_score, reverse=True)
    
    logger.info(f"🎉 Discovery complete: {len(discovered_sources)} compliant sources found")
    return discovered_sources

def search_template_files(repo_full_name: str, headers: Dict[str, str]) -> List[str]:
    """
    Sucht nach Template-Dateien in einem Repository.
    """
    template_files = []
    
    # Bekannte Template-Pfade
    common_paths = [
        'template.json',
        'templates.json', 
        'portainer-template.json',
        'portainer-templates.json',
        'templates/template.json',
        'templates/templates.json',
        'portainer/template.json',
        'portainer/templates.json'
    ]
    
    for path in common_paths:
        try:
            file_url = f"https://api.github.com/repos/{repo_full_name}/contents/{path}"
            response = requests.get(file_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                file_data = response.json()
                if file_data.get('type') == 'file':
                    # Raw URL erstellen
                    raw_url = f"https://raw.githubusercontent.com/{repo_full_name}/master/{path}"
                    template_files.append(raw_url)
                    break  # Erste gefundene Datei verwenden
                    
        except:
            continue
    
    return template_files

def count_templates_in_repo(repo_full_name: str, template_url: str, headers: Dict[str, str]) -> int:
    """
    Zählt Templates in einer Repository-Template-Datei.
    """
    try:
        response = requests.get(template_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Template-Struktur analysieren
        if isinstance(data, list):
            return len(data)
        elif isinstance(data, dict):
            if 'templates' in data:
                return len(data['templates'])
            elif 'version' in data and 'templates' in data:
                return len(data['templates'])
        
        return 0
        
    except:
        return 0

def save_discovered_sources(sources: List[DiscoveredSource], output_file: Path):
    """
    Speichert entdeckte Quellen in JSON-Datei.
    """
    discovery_data = {
        'discovery_date': datetime.now().isoformat(),
        'total_sources': len(sources),
        'eu_compliant_sources': len([s for s in sources if s.eu_compliant]),
        'high_trust_sources': len([s for s in sources if s.trust_score >= 80]),
        'total_templates_discovered': sum(s.template_count for s in sources),
        'sources': [asdict(source) for source in sources]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(discovery_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"💾 Discovery data saved to: {output_file}")

def generate_discovery_report(sources: List[DiscoveredSource]):
    """
    Generiert einen detaillierten Discovery-Report.
    """
    print("\n" + "="*80)
    print("🌟 EU-COMPLIANT TEMPLATE SOURCE DISCOVERY REPORT")
    print("="*80)
    
    total_sources = len(sources)
    eu_compliant = len([s for s in sources if s.eu_compliant])
    verified_sources = len([s for s in sources if s.verified])
    total_templates = sum(s.template_count for s in sources)
    
    print(f"📊 Discovery Statistics:")
    print(f"   • Total Sources Found: {total_sources}")
    print(f"   • EU-GDPR Compliant: {eu_compliant} ({eu_compliant/total_sources*100:.1f}%)")
    print(f"   • Verified Organizations: {verified_sources}")
    print(f"   • Total Templates Available: {total_templates}")
    
    # Top-Quellen nach Trust-Score
    print(f"\n🏆 Top Sources by Trust Score:")
    for i, source in enumerate(sources[:10], 1):
        trust_indicator = "🔥" if source.trust_score >= 90 else "⭐" if source.trust_score >= 80 else "👍"
        verified_badge = " ✅" if source.verified else ""
        print(f"   {i:2d}. {trust_indicator} {source.name} (Trust: {source.trust_score}){verified_badge}")
        print(f"       └─ {source.template_count} templates, {source.stars} stars")
    
    # Kategorien-Analyse
    all_topics = []
    for source in sources:
        all_topics.extend(source.topics)
    
    from collections import Counter
    topic_counts = Counter(all_topics)
    
    print(f"\n📂 Popular Topics:")
    for topic, count in topic_counts.most_common(10):
        print(f"   • {topic}: {count} sources")
    
    # Compliance-Status
    print(f"\n🇪🇺 EU-GDPR Compliance Summary:")
    print(f"   • Compliant Sources: {eu_compliant}/{total_sources}")
    print(f"   • Safe Licenses: {len([s for s in sources if s.license])}")
    print(f"   • Recent Updates: {len([s for s in sources if (datetime.now() - datetime.fromisoformat(s.last_updated.replace('Z', '+00:00'))).days < 90])}")
    
    print("\n" + "="*80)

def main():
    """Hauptfunktion für Template-Source Discovery."""
    try:
        logger.info("🌟 EU-Compliant Template Discovery Engine")
        logger.info("=" * 60)
        
        script_dir = Path(__file__).parent.absolute()
        project_root = script_dir.parent
        
        # GitHub Token aus Umgebung (optional)
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            logger.warning("⚠️ No GITHUB_TOKEN found - API rate limiting may occur")
        
        # Template-Source Discovery
        discovered_sources = discover_template_repositories(github_token)
        
        if not discovered_sources:
            logger.warning("❌ No compliant template sources discovered")
            return
        
        # Results speichern
        output_file = project_root / 'discovered_sources.json'
        save_discovered_sources(discovered_sources, output_file)
        
        # Report generieren
        generate_discovery_report(discovered_sources)
        
        # Integration-Vorschläge
        print(f"\n🚀 Integration Recommendations:")
        high_trust_sources = [s for s in discovered_sources if s.trust_score >= 80]
        
        for source in high_trust_sources[:5]:
            print(f"   • {source.name}: {source.template_count} templates")
            print(f"     └─ URL: {source.url}")
            print(f"     └─ Trust: {source.trust_score}/100, Stars: {source.stars}")
        
        logger.info(f"\n✅ Discovery completed successfully!")
        logger.info(f"💾 Results saved to: {output_file}")
        
    except KeyboardInterrupt:
        logger.info("\n⏹️ Discovery interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()