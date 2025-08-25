#!/usr/bin/env python3
"""
SelfhostedPro Templates Integration Script
=====================================

Dieses Script integriert die umfangreichen SelfhostedPro Templates in unsere bestehende
Portainer Template Collection. Es lädt die Original-Templates und fügt sie mit
korrekter Quellenattribution und erweiterten Metadaten hinzu.

URLs zu den SelfhostedPro Template-Dateien:
- https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/template.json
- https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/portainer-v2.json
- https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/portainer-v1.json
- https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/yacht.json
"""

import json
import requests
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Template-URLs von SelfhostedPro
SELFHOSTEDPRO_TEMPLATE_URLS = {
    'main': 'https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/template.json',
    'portainer-v2': 'https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/portainer-v2.json',
    'portainer-v1': 'https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/portainer-v1.json',
    'yacht': 'https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/yacht.json',
    'omv-v1': 'https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/omv-v1.json',
    'omv-v2': 'https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/omv-v2.json'
}

# Standard-Logo-URLs für bekannte Apps
LOGO_MAPPING = {
    'nextcloud': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/nextcloud.png',
    'jellyfin': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/jellyfin.png',
    'bitwarden': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/bitwarden.png',
    'vaultwarden': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/vaultwarden.png',
    'heimdall': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/heimdall.png',
    'plex': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/plex.png',
    'sonarr': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/sonarr.png',
    'radarr': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/radarr.png',
    'portainer': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/portainer.png',
    'gitea': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/gitea.png',
    'nginx': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/nginx.png',
    'mariadb': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/mariadb.png',
    'photoprism': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/photoprism.png',
    'pi-hole': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/pi-hole.png',
    'adguard': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/adguard-home.png',
    'calibre-web': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/calibre-web.png',
    'bookstack': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/bookstack.png',
    'freshrss': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/freshrss.png',
    'tautulli': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/tautulli.png',
    'organizr': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/organizr.png',
    'ombi': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/ombi.png',
    'jackett': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/jackett.png',
    'transmission': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/transmission.png',
    'qbittorrent': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/qbittorrent.png',
    'syncthing': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/syncthing.png',
    'filebrowser': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/filebrowser.png',
    'guacamole': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/guacamole.png',
    'code-server': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/code-server.png',
    'yacht': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/yacht.png'
}

def fetch_template_data(url: str) -> Dict[str, Any]:
    """Lädt Template-Daten von einer URL."""
    try:
        print(f"📥 Lade Template-Daten von: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Prüfe Content-Type
        content_type = response.headers.get('content-type', '')
        if 'application/json' not in content_type and 'text/plain' not in content_type:
            print(f"⚠️  Unerwarteter Content-Type: {content_type}")
        
        data = response.json()
        
        # SelfhostedPro Templates haben unterschiedliche Strukturen
        if isinstance(data, list):
            # template.json ist eine direkte Liste von Templates
            templates = data
            data = {'templates': templates}
        elif isinstance(data, dict) and 'templates' in data:
            # portainer-v2.json hat bereits die richtige Struktur
            templates = data['templates']
        else:
            print(f"⚠️  Unbekannte Template-Struktur in {url}")
            return {'templates': []}
        
        print(f"✅ Template-Daten erfolgreich geladen ({len(templates)} Templates)")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Fehler beim Laden von {url}: {e}")
        return {'templates': []}
    except json.JSONDecodeError as e:
        print(f"❌ JSON-Parsing Fehler für {url}: {e}")
        return {'templates': []}

def enhance_template(template: Dict[str, Any], source_name: str, source_url: str) -> Dict[str, Any]:
    """Erweitert ein Template mit zusätzlichen Metadaten und Quellenattribution."""
    enhanced = template.copy()
    
    # Name normalisieren für Logo-Mapping
    template_name = template.get('name', '').lower()
    title = template.get('title', '').lower()
    
    # Logo optimieren
    current_logo = template.get('logo', '')
    if template_name in LOGO_MAPPING:
        enhanced['logo'] = LOGO_MAPPING[template_name]
    elif title in LOGO_MAPPING:
        enhanced['logo'] = LOGO_MAPPING[title]
    elif current_logo and not current_logo.startswith('https://cdn.jsdelivr.net'):
        # Behalte Original-Logo wenn keine bessere Variante verfügbar
        enhanced['logo'] = current_logo
    
    # Quelle hinzufügen
    enhanced['source'] = {
        'name': source_name,
        'url': source_url,
        'repository': 'https://github.com/SelfhostedPro/selfhosted_templates'
    }
    
    # Maintainer-Informationen
    enhanced['maintainer'] = {
        'name': 'SelfhostedPro Community',
        'email': 'community@selfhosted.pro',
        'url': 'https://github.com/SelfhostedPro'
    }
    
    # Deployment-Notizen basierend auf Template-Typ
    deployment_notes = []
    
    # Type 1 = Container Template
    if template.get('type') == 1:
        deployment_notes.append("🐳 Single Container Deployment")
        if template.get('env'):
            deployment_notes.append("⚙️  Environment variables configuration required")
        if template.get('volumes'):
            deployment_notes.append("💾 Persistent storage volumes configured")
        if template.get('ports'):
            deployment_notes.append("🌐 Network ports will be exposed")
    
    # Type 2 = Swarm Service
    elif template.get('type') == 2:
        deployment_notes.append("🐙 Docker Swarm Service")
        deployment_notes.append("⚠️  Requires Docker Swarm mode")
    
    # Type 3 = Compose/Stack
    elif template.get('type') == 3:
        deployment_notes.append("📚 Docker Compose Stack")
        deployment_notes.append("🔗 Multi-container orchestrated deployment")
        if template.get('repository'):
            deployment_notes.append("📁 Stack file will be fetched from repository")
    
    # Spezielle App-Hinweise
    app_name = template.get('name', '').lower()
    if 'nextcloud' in app_name:
        deployment_notes.append("☁️  Self-hosted cloud storage solution")
        deployment_notes.append("🔒 Configure HTTPS for production use")
    elif 'jellyfin' in app_name:
        deployment_notes.append("🎬 Media server for movies and TV shows")
        deployment_notes.append("🎵 Supports music and photo libraries")
    elif 'bitwarden' in app_name or 'vaultwarden' in app_name:
        deployment_notes.append("🔐 Password manager - secure your master password")
        deployment_notes.append("🛡️  Consider enabling 2FA")
    elif 'pihole' in app_name:
        deployment_notes.append("🚫 Network-wide ad blocker")
        deployment_notes.append("⚡ Configure your router to use Pi-hole as DNS")
    elif 'portainer' in app_name:
        deployment_notes.append("🚀 Docker management interface")
        deployment_notes.append("🔧 Web-based container administration")
    
    enhanced['deployment_notes'] = deployment_notes
    
    # Kategorien erweitern
    categories = enhanced.get('categories', [])
    if source_name == 'SelfhostedPro':
        if 'SelfhostedPro' not in categories:
            categories.append('SelfhostedPro')
    
    # Besondere Kategorien hinzufügen
    if template.get('type') == 3:
        if 'Multi-Container' not in categories:
            categories.append('Multi-Container')
    
    enhanced['categories'] = categories
    
    # Verification Badge für bekannte, stabile Apps
    stable_apps = ['nextcloud', 'jellyfin', 'bitwarden', 'vaultwarden', 'heimdall', 
                   'plex', 'sonarr', 'radarr', 'portainer', 'gitea', 'nginx', 'mariadb']
    
    if any(app in template_name for app in stable_apps):
        enhanced['verified'] = True
        enhanced['verification_badge'] = 'Community Verified'
    
    # Installation Complexity
    if template.get('type') == 1 and not template.get('env'):
        enhanced['complexity'] = 'Simple'
    elif template.get('type') == 3 or (template.get('env') and len(template.get('env', [])) > 5):
        enhanced['complexity'] = 'Advanced'
    else:
        enhanced['complexity'] = 'Intermediate'
    
    return enhanced

def integrate_selfhostedpro_templates():
    """Integriert SelfhostedPro Templates in unsere bestehende Collection."""
    
    # Arbeitsverzeichnis setzen
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent
    template_file = project_root / 'web' / 'portainer-template.json'
    
    print("🚀 SelfhostedPro Templates Integration")
    print("=" * 50)
    print(f"📁 Arbeitsverzeichnis: {project_root}")
    print(f"📄 Template-Datei: {template_file}")
    
    # Bestehende Templates laden
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
        print(f"✅ Bestehende Templates geladen ({len(existing_data.get('templates', []))} Templates)")
    except FileNotFoundError:
        print("❌ Template-Datei nicht gefunden!")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Fehler beim Laden der Template-Datei: {e}")
        return False
    
    # Bestehende Template-Namen sammeln (um Duplikate zu vermeiden)
    existing_names = {t.get('name', '').lower() for t in existing_data.get('templates', [])}
    print(f"📋 Bestehende Template-Namen: {len(existing_names)}")
    
    # SelfhostedPro Templates von verschiedenen URLs laden
    all_new_templates = []
    total_loaded = 0
    
    for source_name, url in SELFHOSTEDPRO_TEMPLATE_URLS.items():
        print(f"\n📡 Lade {source_name} Templates...")
        template_data = fetch_template_data(url)
        
        if not template_data.get('templates'):
            print(f"⚠️  Keine Templates in {source_name} gefunden")
            continue
        
        loaded_count = 0
        for template in template_data['templates']:
            template_name = template.get('name', '').lower()
            
            # Duplikate überspringen
            if template_name in existing_names:
                continue
            
            # Template erweitern
            enhanced_template = enhance_template(template, 'SelfhostedPro', url)
            all_new_templates.append(enhanced_template)
            existing_names.add(template_name)  # Für weitere Duplikat-Prüfungen
            loaded_count += 1
        
        print(f"✅ {loaded_count} neue Templates aus {source_name} hinzugefügt")
        total_loaded += loaded_count
    
    if not all_new_templates:
        print("\n⚠️  Keine neuen Templates zum Hinzufügen gefunden")
        return True
    
    # Templates zur bestehenden Collection hinzufügen
    existing_data['templates'].extend(all_new_templates)
    
    # Metadaten aktualisieren
    if 'metadata' not in existing_data:
        existing_data['metadata'] = {}
    
    existing_data['metadata'].update({
        'last_selfhostedpro_integration': datetime.now().isoformat(),
        'selfhostedpro_templates_added': total_loaded,
        'selfhostedpro_sources': list(SELFHOSTEDPRO_TEMPLATE_URLS.keys()),
        'total_templates': len(existing_data['templates'])
    })
    
    # Backup erstellen
    backup_file = template_file.with_suffix('.backup.json')
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Backup erstellt: {backup_file}")
    except Exception as e:
        print(f"⚠️  Backup-Erstellung fehlgeschlagen: {e}")
    
    # Erweiterte Template-Datei speichern
    try:
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 SelfhostedPro Integration erfolgreich!")
        print(f"📊 Statistik:")
        print(f"   • Neue Templates hinzugefügt: {total_loaded}")
        print(f"   • Gesamte Templates: {len(existing_data['templates'])}")
        print(f"   • Quellen integriert: {len(SELFHOSTEDPRO_TEMPLATE_URLS)}")
        print(f"   • Datei aktualisiert: {template_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Speichern: {e}")
        return False

def main():
    """Hauptfunktion."""
    try:
        success = integrate_selfhostedpro_templates()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Integration abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()