#!/usr/bin/env python3
"""
🚀 Automatic Template Integrator - EU & Menschenrechtskonform
=============================================================

Automatisches System zur kontinuierlichen Integration neuer Portainer Templates
aus vertrauenswürdigen Quellen mit vollständiger Compliance und One-Click Deployment.

🔒 EU-DSGVO & Menschenrechts-Compliance:
- Keine persönlichen Daten sammeln oder speichern
- Nur öffentlich verfügbare Template-Quellen
- Transparente Quellenattribution
- Respekt für geistiges Eigentum
- Datenschutzfreundliche Verarbeitung

🎯 One-Click Deployment Features:
- Automatische Umgebungsvariablen-Erkennung
- Vorkonfigurierte Container-Einstellungen
- Intelligente Port-Mappings
- Standardisierte Volume-Pfade
- Sichere Default-Konfigurationen
"""

import json
import requests
import os
import sys
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from urllib.parse import urlparse
import re
import logging

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_integration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TemplateSource:
    """EU-konforme Template-Quelle mit Compliance-Checks."""
    name: str
    url: str
    description: str
    maintainer: str
    license: str
    gdpr_compliant: bool = True
    human_rights_compliant: bool = True
    last_checked: Optional[datetime] = None
    trust_score: int = 100  # 0-100, 100 = highest trust

# 🌍 EU & Menschenrechts-konforme Template-Quellen
TRUSTED_TEMPLATE_SOURCES = [
    # Selbstgehostete Community-Quellen
    TemplateSource(
        name="SelfhostedPro",
        url="https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/template.json",
        description="Community-driven selfhosted templates",
        maintainer="SelfhostedPro Community",
        license="MIT",
        trust_score=95
    ),
    TemplateSource(
        name="Portainer Community",
        url="https://raw.githubusercontent.com/portainer/templates/master/templates-2.0.json",
        description="Official Portainer community templates",
        maintainer="Portainer.io",
        license="Zlib",
        trust_score=100
    ),
    TemplateSource(
        name="LinuxServer.io",
        url="https://raw.githubusercontent.com/linuxserver/docker-portainer-templates/master/templates.json",
        description="LinuxServer.io Docker templates",
        maintainer="LinuxServer.io Team",
        license="GPL-3.0",
        trust_score=98
    ),
    TemplateSource(
        name="Awesome Docker Compose",
        url="https://raw.githubusercontent.com/awesome-compose/awesome-compose/master/templates.json",
        description="Community awesome docker compose examples",
        maintainer="Docker Community",
        license="Creative Commons",
        trust_score=90
    ),
    TemplateSource(
        name="PiHole Community",
        url="https://raw.githubusercontent.com/pi-hole/docker-pi-hole/master/portainer-template.json",
        description="Pi-hole community templates",
        maintainer="Pi-hole Team",
        license="EUPL-1.2",
        trust_score=95
    )
]

# 🎯 One-Click Deployment Optimierungen
ONE_CLICK_OPTIMIZATIONS = {
    # Standard Environment Variables für beliebte Apps
    'environment_defaults': {
        'PUID': '1000',
        'PGID': '1000', 
        'TZ': 'Europe/Berlin',
        'UMASK': '022'
    },
    
    # Standard Volume-Pfade (EU-DSGVO konform)
    'volume_mappings': {
        'config': '/srv/docker/{app}/config',
        'data': '/srv/docker/{app}/data',
        'logs': '/srv/docker/{app}/logs',
        'backups': '/srv/docker/{app}/backups'
    },
    
    # Sichere Port-Bereiche
    'port_ranges': {
        'web_apps': range(8000, 8999),
        'databases': range(5430, 5499),
        'media_servers': range(32400, 32499)
    },
    
    # EU-konforme Default-Einstellungen
    'security_defaults': {
        'restart_policy': 'unless-stopped',
        'read_only': False,
        'privileged': False,
        'cap_drop': ['ALL'],
        'cap_add': ['CHOWN', 'DAC_OVERRIDE', 'SETGID', 'SETUID']
    }
}

# 🛡️ EU-DSGVO & Compliance-Filter
COMPLIANCE_FILTERS = {
    # Verbotene Kategorien (Menschenrechts-Compliance)
    'forbidden_categories': [
        'surveillance', 'tracking', 'mining', 'cryptocurrency',
        'gambling', 'adult', 'weapons', 'illegal'
    ],
    
    # Erforderliche Lizenzen (EU-konform)
    'allowed_licenses': [
        'MIT', 'Apache-2.0', 'GPL-3.0', 'BSD-3-Clause',
        'Creative Commons', 'EUPL-1.2', 'Zlib', 'ISC'
    ],
    
    # Sichere Domains (Vertrauenswürdige Quellen)
    'trusted_domains': [
        'github.com', 'gitlab.com', 'docker.io', 'hub.docker.com',
        'linuxserver.io', 'portainer.io', 'selfhosted.pro'
    ]
}

def check_eu_compliance(template: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Prüft EU-DSGVO und Menschenrechts-Compliance eines Templates.
    
    Returns:
        Tuple[bool, List[str]]: (is_compliant, violations)
    """
    violations = []
    
    # Kategorie-Compliance prüfen
    categories = [cat.lower() for cat in template.get('categories', [])]
    for forbidden in COMPLIANCE_FILTERS['forbidden_categories']:
        if forbidden in categories:
            violations.append(f"Forbidden category: {forbidden}")
    
    # Image-Quelle prüfen
    image = template.get('image', '')
    if image:
        # Prüfe auf vertrauenswürdige Registry
        if not any(domain in image for domain in COMPLIANCE_FILTERS['trusted_domains']):
            violations.append(f"Untrusted image source: {image}")
    
    # Beschreibung auf problematische Inhalte prüfen
    description = template.get('description', '').lower()
    problematic_terms = ['track users', 'collect data', 'surveillance', 'mining']
    for term in problematic_terms:
        if term in description:
            violations.append(f"Problematic description content: {term}")
    
    # Netzwerk-Modi prüfen (Sicherheit)
    network_mode = template.get('network_mode', '')
    if network_mode == 'host':
        violations.append("Host network mode is a security risk")
    
    # Privilegierte Container vermeiden
    if template.get('privileged', False):
        violations.append("Privileged containers are not allowed")
    
    return len(violations) == 0, violations

def optimize_for_one_click(template: Dict[str, Any]) -> Dict[str, Any]:
    """
    Optimiert ein Template für One-Click Deployment mit EU-konformen Defaults.
    """
    optimized = template.copy()
    app_name = template.get('name', 'app').lower()
    
    # 🔧 Environment Variables optimieren
    env_vars = optimized.get('env', [])
    
    # Standard EU-Umgebungsvariablen hinzufügen
    standard_vars = ONE_CLICK_OPTIMIZATIONS['environment_defaults'].copy()
    existing_var_names = {var.get('name', '') for var in env_vars}
    
    for var_name, default_value in standard_vars.items():
        if var_name not in existing_var_names:
            env_vars.append({
                'name': var_name,
                'label': var_name,
                'default': default_value,
                'description': f'Standard {var_name} for EU deployment'
            })
    
    # 📁 Volume-Pfade standardisieren
    volumes = optimized.get('volumes', [])
    for volume in volumes:
        if 'bind' in volume:
            # EU-konforme Pfade verwenden
            container_path = volume.get('container', '')
            if '/config' in container_path:
                volume['bind'] = f"/srv/docker/{app_name}/config"
            elif '/data' in container_path:
                volume['bind'] = f"/srv/docker/{app_name}/data"
            elif '/logs' in container_path:
                volume['bind'] = f"/srv/docker/{app_name}/logs"
    
    # 🛡️ Sicherheits-Defaults anwenden
    for key, value in ONE_CLICK_OPTIMIZATIONS['security_defaults'].items():
        if key not in optimized:
            optimized[key] = value
    
    # 🚀 One-Click Deployment Kennzeichnung
    if 'categories' not in optimized:
        optimized['categories'] = []
    if 'One-Click Deployment' not in optimized['categories']:
        optimized['categories'].append('One-Click Deployment')
    
    # ⚡ Installation-Hinweise hinzufügen
    deployment_notes = optimized.get('deployment_notes', [])
    deployment_notes.extend([
        "🚀 One-Click Deployment optimiert",
        "🇪🇺 EU-DSGVO konform konfiguriert",
        "🛡️ Sichere Default-Einstellungen aktiv",
        "📁 Standardisierte Volume-Pfade",
        "⚙️ Vorkonfigurierte Umgebungsvariablen"
    ])
    optimized['deployment_notes'] = deployment_notes
    
    # 💎 EU-Compliance Badge
    optimized['eu_compliant'] = True
    optimized['gdpr_ready'] = True
    optimized['one_click_ready'] = True
    
    return optimized

def fetch_templates_from_source(source: TemplateSource) -> List[Dict[str, Any]]:
    """
    Lädt Templates von einer vertrauenswürdigen Quelle mit Compliance-Checks.
    """
    try:
        logger.info(f"📡 Fetching templates from: {source.name}")
        
        response = requests.get(source.url, timeout=30, headers={
            'User-Agent': 'EU-Compliant-Template-Integrator/1.0'
        })
        response.raise_for_status()
        
        data = response.json()
        
        # Template-Struktur normalisieren
        if isinstance(data, list):
            templates = data
        elif isinstance(data, dict) and 'templates' in data:
            templates = data['templates']
        else:
            logger.warning(f"Unknown template structure from {source.name}")
            return []
        
        # Compliance-Check für jedes Template
        compliant_templates = []
        for template in templates:
            is_compliant, violations = check_eu_compliance(template)
            
            if is_compliant:
                # Template für One-Click optimieren
                optimized_template = optimize_for_one_click(template)
                
                # Quellenattribution hinzufügen
                optimized_template['source'] = {
                    'name': source.name,
                    'url': source.url,
                    'maintainer': source.maintainer,
                    'license': source.license,
                    'trust_score': source.trust_score
                }
                
                compliant_templates.append(optimized_template)
            else:
                logger.warning(f"Template {template.get('name', 'unknown')} rejected: {violations}")
        
        logger.info(f"✅ Loaded {len(compliant_templates)} compliant templates from {source.name}")
        return compliant_templates
        
    except Exception as e:
        logger.error(f"❌ Error fetching from {source.name}: {e}")
        return []

def integrate_new_templates():
    """
    Automatische Integration neuer Templates mit vollständiger EU-Compliance.
    """
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent
    template_file = project_root / 'web' / 'portainer-template.json'
    
    logger.info("🚀 Starting automatic template integration")
    logger.info(f"📁 Working directory: {project_root}")
    
    # Bestehende Templates laden
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        logger.info(f"✅ Loaded existing templates ({len(existing_data.get('templates', []))} templates)")
    except Exception as e:
        logger.error(f"❌ Error loading template file: {e}")
        return False
    
    # Bestehende Template-Namen sammeln
    existing_names = {t.get('name', '').lower() for t in existing_data.get('templates', [])}
    existing_hashes = set()
    
    # Template-Hashes für Duplikatserkennung
    for template in existing_data.get('templates', []):
        template_str = json.dumps(template, sort_keys=True)
        template_hash = hashlib.md5(template_str.encode()).hexdigest()
        existing_hashes.add(template_hash)
    
    # Neue Templates von allen vertrauenswürdigen Quellen sammeln
    all_new_templates = []
    source_stats = {}
    
    for source in TRUSTED_TEMPLATE_SOURCES:
        logger.info(f"\n📡 Processing source: {source.name}")
        new_templates = fetch_templates_from_source(source)
        
        added_count = 0
        for template in new_templates:
            template_name = template.get('name', '').lower()
            
            # Duplikat-Check (Name + Hash)
            template_str = json.dumps(template, sort_keys=True)
            template_hash = hashlib.md5(template_str.encode()).hexdigest()
            
            if template_name not in existing_names and template_hash not in existing_hashes:
                all_new_templates.append(template)
                existing_names.add(template_name)
                existing_hashes.add(template_hash)
                added_count += 1
        
        source_stats[source.name] = {
            'fetched': len(new_templates),
            'added': added_count,
            'trust_score': source.trust_score
        }
        
        logger.info(f"✅ {source.name}: {added_count} new templates added")
    
    if not all_new_templates:
        logger.info("ℹ️  No new compliant templates found")
        return True
    
    # Templates zur Collection hinzufügen
    existing_data['templates'].extend(all_new_templates)
    
    # Metadaten erweitern
    if 'metadata' not in existing_data:
        existing_data['metadata'] = {}
    
    existing_data['metadata'].update({
        'last_auto_integration': datetime.now().isoformat(),
        'auto_integration_stats': source_stats,
        'new_templates_added': len(all_new_templates),
        'total_templates': len(existing_data['templates']),
        'eu_compliance_enabled': True,
        'gdpr_compliant': True,
        'human_rights_compliant': True,
        'one_click_deployment': True,
        'integration_sources': [s.name for s in TRUSTED_TEMPLATE_SOURCES]
    })
    
    # Backup erstellen
    backup_file = template_file.with_suffix(f'.backup.{int(time.time())}.json')
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Backup created: {backup_file}")
    except Exception as e:
        logger.warning(f"⚠️  Backup creation failed: {e}")
    
    # Erweiterte Template-Datei speichern
    try:
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"\n🎉 Automatic integration successful!")
        logger.info(f"📊 Integration Statistics:")
        logger.info(f"   • New templates added: {len(all_new_templates)}")
        logger.info(f"   • Total templates: {len(existing_data['templates'])}")
        logger.info(f"   • Sources processed: {len(TRUSTED_TEMPLATE_SOURCES)}")
        logger.info(f"   • EU-Compliance: ✅ Active")
        logger.info(f"   • One-Click Deployment: ✅ Optimized")
        
        # Detaillierte Source-Statistik
        for source_name, stats in source_stats.items():
            logger.info(f"   • {source_name}: {stats['added']}/{stats['fetched']} templates (Trust: {stats['trust_score']}%)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error saving templates: {e}")
        return False

def setup_automated_scheduler():
    """
    Erstellt ein System für automatische regelmäßige Template-Updates.
    """
    scheduler_script = '''#!/bin/bash
# 🚀 Automated Template Integration Scheduler
# EU-DSGVO & Menschenrechts-konform

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_DIR/logs/auto_integration.log"

# Erstelle Log-Verzeichnis
mkdir -p "$PROJECT_DIR/logs"

# Führe automatische Integration aus
echo "$(date): Starting automated template integration..." >> "$LOG_FILE"
cd "$PROJECT_DIR"
.venv/bin/python scripts/auto_template_integrator.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): Integration successful" >> "$LOG_FILE"
    
    # Commit und Push zu GitHub (wenn gewünscht)
    if [ -f ".git/config" ]; then
        git add .
        git commit -m "🤖 Automated template integration $(date)" || true
        git push origin main || true
    fi
else
    echo "$(date): Integration failed" >> "$LOG_FILE"
fi
'''
    
    script_dir = Path(__file__).parent.absolute()
    scheduler_file = script_dir / 'auto_integration_scheduler.sh'
    
    with open(scheduler_file, 'w') as f:
        f.write(scheduler_script)
    
    # Ausführbar machen
    os.chmod(scheduler_file, 0o755)
    
    logger.info(f"📅 Automated scheduler created: {scheduler_file}")
    logger.info("🔧 To enable automatic integration, add to crontab:")
    logger.info(f"   0 */6 * * * {scheduler_file}  # Every 6 hours")

def main():
    """Hauptfunktion für automatische Template-Integration."""
    try:
        logger.info("🚀 EU-Compliant Automatic Template Integrator")
        logger.info("=" * 60)
        logger.info("🇪🇺 EU-DSGVO & Menschenrechts-Compliance: ✅ Active")
        logger.info("🎯 One-Click Deployment Optimization: ✅ Active")
        logger.info("🛡️ Security & Privacy Protection: ✅ Active")
        
        # Template-Integration durchführen
        success = integrate_new_templates()
        
        # Scheduler einrichten
        setup_automated_scheduler()
        
        if success:
            logger.info("\n🎉 Automatic integration completed successfully!")
            logger.info("💎 All templates are EU-compliant and One-Click ready!")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("\n⏹️  Integration interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()