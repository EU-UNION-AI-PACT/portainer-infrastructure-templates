#!/usr/bin/env python3
"""
Generate comprehensive report of collected Portainer templates
"""

import json
from collections import defaultdict, Counter

def analyze_templates(file_path: str):
    """Analyze and generate report of templates"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    templates = data.get("templates", [])
    total_count = len(templates)
    
    print("📊 COMPREHENSIVE PORTAINER TEMPLATE COLLECTION REPORT")
    print("=" * 60)
    print(f"📈 Total Templates: {total_count}")
    print(f"🔧 Template Version: {data.get('version', 'unknown')}")
    print()
    
    # Analyze by categories
    print("📂 TEMPLATES BY CATEGORY:")
    print("-" * 40)
    category_counts = defaultdict(int)
    for template in templates:
        categories = template.get("categories", ["Other"])
        if isinstance(categories, list):
            for category in categories:
                category_counts[category] += 1
        else:
            category_counts[categories] += 1
    
    # Sort categories by count
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    for category, count in sorted_categories:
        print(f"  {category:20} {count:3d} templates")
    
    print()
    
    # Analyze by type
    print("🏗️  TEMPLATES BY TYPE:")
    print("-" * 40)
    type_counts = Counter([t.get("type", "unknown") for t in templates])
    type_names = {1: "Container", 3: "Stack", 2: "Swarm"}
    
    for type_id, count in type_counts.items():
        type_name = type_names.get(type_id, f"Type {type_id}")
        print(f"  {type_name:15} {count:3d} templates")
    
    print()
    
    # Popular applications
    print("🌟 POPULAR SELFHOSTED APPLICATIONS:")
    print("-" * 40)
    popular_apps = [
        "Nextcloud", "Jellyfin", "Bitwarden", "AdGuard", "Pi-Hole", 
        "Nginx Proxy Manager", "Portainer", "Heimdall", "Sonarr", "Radarr",
        "Plex", "Emby", "BookStack", "Gitea", "FreshRSS", "Photoprism",
        "Vaultwarden", "Authelia", "Traefik", "Grafana", "Prometheus",
        "MariaDB", "PostgreSQL", "Redis", "InfluxDB", "MongoDB"
    ]
    
    found_apps = []
    for template in templates:
        title = template.get("title", "").lower()
        for app in popular_apps:
            if app.lower() in title:
                found_apps.append(template.get("title", "Unknown"))
                break
    
    # Remove duplicates and sort
    unique_found = sorted(list(set(found_apps)))
    for app in unique_found[:20]:  # Show first 20
        print(f"  ✅ {app}")
    
    if len(unique_found) > 20:
        print(f"  ... and {len(unique_found) - 20} more popular apps")
    
    print()
    
    # Database templates
    print("🗄️  DATABASE TEMPLATES:")
    print("-" * 40)
    db_templates = [t for t in templates if any(cat.lower() in ['database', 'analytics', 'timeseries', 'nosql', 'relational', 'cache', 'search', 'graph', 'vector', 'key_value'] 
                                               for cat in t.get("categories", []))]
    
    db_categories = defaultdict(int)
    for template in db_templates:
        for category in template.get("categories", []):
            if category.lower() in ['database', 'analytics', 'timeseries', 'nosql', 'relational', 'cache', 'search', 'graph', 'vector', 'key_value']:
                db_categories[category] += 1
    
    for category, count in sorted(db_categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category:15} {count:3d} databases")
    
    print(f"\n  Total database templates: {len(db_templates)}")
    
    print()
    
    # Security and monitoring
    print("🔒 SECURITY & MONITORING:")
    print("-" * 40)
    security_templates = [t for t in templates if any(cat.lower() in ['security', 'monitoring', 'vpn', 'proxy', 'authentication'] 
                                                     for cat in t.get("categories", []))]
    
    security_categories = defaultdict(int)
    for template in security_templates:
        for category in template.get("categories", []):
            if category.lower() in ['security', 'monitoring', 'vpn', 'proxy', 'authentication']:
                security_categories[category] += 1
    
    for category, count in sorted(security_categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category:15} {count:3d} templates")
    
    print(f"\n  Total security/monitoring: {len(security_templates)}")
    
    print()
    
    # Sources
    print("📦 TEMPLATE SOURCES:")
    print("-" * 40)
    sources = defaultdict(int)
    for template in templates:
        note = template.get("note", "")
        if "Source:" in note:
            source = note.split("Source:")[-1].strip().split(")")[0].strip()
            sources[source] += 1
        else:
            sources["Original/Custom"] += 1
    
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source:25} {count:3d} templates")
    
    print()
    print("🎉 COLLECTION COMPLETE!")
    print(f"✅ Ready to serve {total_count} templates via Portainer")
    print(f"🌐 Server URL: http://localhost:8091/portainer-template.json")

def main():
    """Main function"""
    import os
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_file = os.path.join(base_dir, "web", "portainer-template.json")
    
    analyze_templates(template_file)

if __name__ == "__main__":
    main()