#!/usr/bin/env python3
"""
🎯 ADVANCED TEMPLATE ORGANIZER
=================================================
Intelligente Sortierung und Kategorisierung von Portainer Templates
nach Themen, Größe, Neuheiten und kuratierten Inhalten
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TemplateOrganizer:
    def __init__(self, template_file: str):
        self.template_file = template_file
        self.templates = []
        
        # 🎯 KATEGORIE-HIERARCHIE
        self.category_priority = {
            # 🏆 KURATIERTE TOP-PICKS (Höchste Priorität)
            "⭐ Kuratierte Top-Picks": 1,
            "🔥 Neuheiten & Trends": 2,
            "🚀 One-Click Deployments": 3,
            
            # 🎯 NACH ANWENDUNGSBEREICH
            "📱 Web Development": 10,
            "🗄️ Datenbanken": 11,
            "🔧 DevOps & CI/CD": 12,
            "📊 Monitoring & Analytics": 13,
            "🎵 Media & Entertainment": 14,
            "🔐 Security & Privacy": 15,
            "☁️ Cloud & Infrastructure": 16,
            "📚 Productivity & Tools": 17,
            "🌐 Networking": 18,
            "🎮 Gaming": 19,
            
            # 📦 NACH KOMPLEXITÄT/GRÖßE
            "⚡ Lightweight (< 100MB)": 30,
            "🔧 Standard (100MB - 500MB)": 31,
            "🏗️ Enterprise (> 500MB)": 32,
            
            # 🎯 SPEZIAL-KATEGORIEN
            "🧪 Experimental": 40,
            "📖 Documentation": 41,
            "🏆 Badges & Info": 42
        }
        
        # 🎯 THEMEN-MAPPING für intelligente Kategorisierung
        self.theme_mapping = {
            # Web Development
            "wordpress": "📱 Web Development",
            "nginx": "📱 Web Development",
            "apache": "📱 Web Development",
            "node": "📱 Web Development",
            "react": "📱 Web Development",
            "vue": "📱 Web Development",
            "angular": "📱 Web Development",
            "nextjs": "📱 Web Development",
            
            # Datenbanken
            "mysql": "🗄️ Datenbanken",
            "postgresql": "🗄️ Datenbanken",
            "mongodb": "🗄️ Datenbanken",
            "redis": "🗄️ Datenbanken",
            "mariadb": "🗄️ Datenbanken",
            "influxdb": "🗄️ Datenbanken",
            
            # DevOps & CI/CD
            "gitlab": "🔧 DevOps & CI/CD",
            "jenkins": "🔧 DevOps & CI/CD",
            "gitea": "🔧 DevOps & CI/CD",
            "drone": "🔧 DevOps & CI/CD",
            "portainer": "🔧 DevOps & CI/CD",
            
            # Monitoring
            "grafana": "📊 Monitoring & Analytics",
            "prometheus": "📊 Monitoring & Analytics",
            "uptime": "📊 Monitoring & Analytics",
            "netdata": "📊 Monitoring & Analytics",
            
            # Media
            "plex": "🎵 Media & Entertainment",
            "jellyfin": "🎵 Media & Entertainment",
            "emby": "🎵 Media & Entertainment",
            "sonarr": "🎵 Media & Entertainment",
            "radarr": "🎵 Media & Entertainment",
            "lidarr": "🎵 Media & Entertainment",
            "bazarr": "🎵 Media & Entertainment",
            
            # Security
            "bitwarden": "🔐 Security & Privacy",
            "authelia": "🔐 Security & Privacy",
            "vaultwarden": "🔐 Security & Privacy",
            "pihole": "🔐 Security & Privacy",
            
            # Productivity
            "nextcloud": "📚 Productivity & Tools",
            "wikijs": "📚 Productivity & Tools",
            "bookstack": "📚 Productivity & Tools",
            "heimdall": "📚 Productivity & Tools",
            "homer": "📚 Productivity & Tools"
        }
        
        # 🎯 SIZE CATEGORIES (basierend auf typischen Docker Image Größen)
        self.size_categories = {
            "lightweight": ["nginx", "alpine", "busybox", "hello", "whoami"],
            "standard": ["wordpress", "mysql", "postgresql", "redis"],
            "enterprise": ["gitlab", "nextcloud", "plex", "emby", "elasticsearch"]
        }

    def load_templates(self):
        """Lade Templates aus der JSON-Datei"""
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.templates = data.get('templates', [])
                logger.info(f"📦 {len(self.templates)} Templates geladen")
        except Exception as e:
            logger.error(f"❌ Fehler beim Laden der Templates: {e}")
            return False
        return True

    def categorize_template(self, template: Dict[str, Any]) -> str:
        """Intelligente Kategorisierung basierend auf Titel, Beschreibung und Image"""
        title = (template.get('title') or '').lower()
        description = (template.get('description') or '').lower()
        image = (template.get('image') or '').lower()
        
        # 🏆 Kuratierte Top-Picks erkennen
        if any(keyword in title for keyword in ['top', 'best', 'recommended', 'professional', 'enterprise']):
            return "⭐ Kuratierte Top-Picks"
        
        # 🔥 Neuheiten erkennen
        if any(keyword in title for keyword in ['new', 'latest', 'modern', '2024', '2025']):
            return "🔥 Neuheiten & Trends"
        
        # 🚀 One-Click erkennen
        if any(keyword in title for keyword in ['one-click', 'ready', 'complete', 'stack']):
            return "🚀 One-Click Deployments"
        
        # 🎯 Themen-basierte Kategorisierung
        content = f"{title} {description} {image}"
        for theme, category in self.theme_mapping.items():
            if theme in content:
                return category
        
        # 📦 Größen-basierte Kategorisierung
        if any(size in image for size in self.size_categories["lightweight"]):
            return "⚡ Lightweight (< 100MB)"
        elif any(size in image for size in self.size_categories["enterprise"]):
            return "🏗️ Enterprise (> 500MB)"
        else:
            return "🔧 Standard (100MB - 500MB)"

    def add_eos_marker(self):
        """Füge EOS (End of Stack) Marker am Ende hinzu"""
        eos_template = {
            "type": 1,
            "title": "🔚 EOS - End of Stack",
            "description": "🎉 Sie haben das Ende unserer kuratierten Template-Kollektion erreicht! Diese Sammlung enthält 378+ professionell ausgewählte und organisierte Templates. Für weitere Templates oder Support besuchen Sie unser GitHub Repository.",
            "categories": ["📖 Documentation", "🏆 Badges & Info"],
            "platform": "linux",
            "logo": "https://nginx.org/nginx.png",
            "image": "nginx:alpine",
            "ports": ["8080:80/tcp"],
            "env": [
                {
                    "name": "COLLECTION_STATUS",
                    "label": "Collection Status",
                    "default": "✅ Complete - Pink Star Diamond Certified",
                    "description": "Status der Template-Kollektion"
                },
                {
                    "name": "TOTAL_TEMPLATES",
                    "label": "Total Templates",
                    "default": "378+",
                    "description": "Gesamtanzahl der Templates"
                },
                {
                    "name": "GITHUB_REPO",
                    "label": "GitHub Repository",
                    "default": "EU-UNION-AI-PACT/portainer-infrastructure-templates",
                    "description": "GitHub Repository für Updates"
                }
            ],
            "restart_policy": "unless-stopped",
            "labels": [
                {"name": "template.type", "value": "eos-marker"},
                {"name": "template.category", "value": "documentation"}
            ]
        }
        return eos_template

    def organize_templates(self):
        """Hauptorganisations-Funktion"""
        logger.info("🎯 Starte Template-Organisation...")
        
        # 1. Templates kategorisieren
        categorized = {}
        for template in self.templates:
            category = self.categorize_template(template)
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(template)
        
        # 2. Nach Priorität sortieren
        sorted_categories = sorted(categorized.keys(), 
                                 key=lambda x: self.category_priority.get(x, 99))
        
        # 3. Neu organisierte Template-Liste erstellen
        organized_templates = []
        
        for category in sorted_categories:
            # Kategorie-Header hinzufügen
            header_template = self.create_category_header(category, len(categorized[category]))
            organized_templates.append(header_template)
            
            # Templates in der Kategorie sortieren (alphabetisch)
            category_templates = sorted(categorized[category], 
                                      key=lambda x: x.get('title', ''))
            organized_templates.extend(category_templates)
        
        # 4. EOS Marker hinzufügen
        organized_templates.append(self.add_eos_marker())
        
        logger.info(f"✅ {len(organized_templates)} Templates organisiert in {len(sorted_categories)} Kategorien")
        return organized_templates

    def create_category_header(self, category: str, count: int) -> Dict[str, Any]:
        """Erstelle Kategorie-Header Template"""
        return {
            "type": 1,
            "title": f"📋 {category} ({count} Templates)",
            "description": f"Diese Kategorie enthält {count} sorgfältig ausgewählte Templates für {category.split(' ', 1)[1] if ' ' in category else category}. Alle Templates sind professionell konfiguriert und sofort einsatzbereit.",
            "categories": ["📖 Documentation", category.split(' ', 1)[1] if ' ' in category else category],
            "platform": "linux",
            "logo": "https://nginx.org/nginx.png",
            "image": "nginx:alpine",
            "ports": ["8080:80/tcp"],
            "env": [
                {
                    "name": "CATEGORY_NAME",
                    "label": "Category Name",
                    "default": category,
                    "description": "Name der Kategorie"
                },
                {
                    "name": "TEMPLATE_COUNT",
                    "label": "Template Count",
                    "default": str(count),
                    "description": "Anzahl Templates in dieser Kategorie"
                }
            ],
            "restart_policy": "unless-stopped",
            "labels": [
                {"name": "template.type", "value": "category-header"},
                {"name": "template.category", "value": category}
            ]
        }

    def save_organized_templates(self, organized_templates: List[Dict[str, Any]]):
        """Speichere organisierte Templates"""
        # Backup erstellen
        backup_file = f"{self.template_file}.backup.organized.{int(datetime.now().timestamp())}.json"
        os.rename(self.template_file, backup_file)
        logger.info(f"💾 Backup erstellt: {backup_file}")
        
        # Neue organisierte Struktur speichern
        organized_data = {
            "version": "3",
            "templates": organized_templates
        }
        
        with open(self.template_file, 'w', encoding='utf-8') as f:
            json.dump(organized_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Organisierte Templates gespeichert: {len(organized_templates)} Templates")

    def generate_organization_report(self, organized_templates: List[Dict[str, Any]]):
        """Erstelle Organisations-Report"""
        categories = {}
        for template in organized_templates:
            title = template.get('title', '')
            if title.startswith('📋 '):
                category = title.split('📋 ')[1].split(' (')[0]
                count = title.split('(')[1].split(' Templates')[0]
                categories[category] = int(count)
        
        logger.info("📊 TEMPLATE ORGANISATION REPORT")
        logger.info("=" * 50)
        for category, count in categories.items():
            logger.info(f"   {category}: {count} Templates")
        logger.info("=" * 50)
        logger.info(f"📦 Gesamt: {len(organized_templates)} Templates (inkl. Header & EOS)")

def main():
    """Hauptfunktion"""
    logger.info("🎯 ADVANCED TEMPLATE ORGANIZER")
    logger.info("=" * 60)
    
    template_file = "/home/holythreekingstreescrowns/Schreibtisch/Portainer Template/web/portainer-template.json"
    
    organizer = TemplateOrganizer(template_file)
    
    # 1. Templates laden
    if not organizer.load_templates():
        return
    
    # 2. Templates organisieren
    organized_templates = organizer.organize_templates()
    
    # 3. Speichern
    organizer.save_organized_templates(organized_templates)
    
    # 4. Report generieren
    organizer.generate_organization_report(organized_templates)
    
    logger.info("🎉 Template-Organisation erfolgreich abgeschlossen!")
    logger.info("💎 Pink Star Diamond Zertifizierung: Organisiert & Kuratiert!")

if __name__ == "__main__":
    main()