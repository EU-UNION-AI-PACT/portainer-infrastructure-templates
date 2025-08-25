#!/bin/bash

# 🔍 DATABASE DISCOVERY & INTEGRATION SCRIPT
# Deep Search alle verfügbaren Datenbanken und automatische Template-Integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔍 DATABASE DISCOVERY ENGINE"
echo "=============================="
echo ""

# Erstelle notwendige Verzeichnisse
mkdir -p "$PROJECT_ROOT/templates/database"
mkdir -p "$PROJECT_ROOT/stacks"
mkdir -p "$PROJECT_ROOT/reports"

echo "📁 Verzeichnisse erstellt..."

# Aktiviere Python Environment
if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
    echo "🐍 Python Environment aktiviert"
else
    echo "❌ Python Environment nicht gefunden!"
    exit 1
fi

# Installiere zusätzliche Dependencies für Discovery
echo "📦 Installiere Discovery Dependencies..."
pip install aiohttp pyyaml requests beautifulsoup4 lxml

echo ""
echo "🚀 STARTE DATABASE DEEP SEARCH..."
echo "=================================="

# Führe Database Discovery aus
cd "$PROJECT_ROOT"
python scripts/database_discovery.py

echo ""
echo "🔄 INTEGRIERE DISCOVERED DATABASES..."
echo "====================================="

# Füge discovered databases zu haupte portainer-template.json hinzu
python3 << 'EOF'
import json
import os

# Lade discovered databases
try:
    with open("templates/database/discovered_databases.json", "r") as f:
        db_templates = json.load(f)
    
    # Lade existing portainer template
    with open("portainer-template.json", "r") as f:
        main_templates = json.load(f)
    
    # Füge Database-Templates hinzu
    main_templates["templates"].extend(db_templates["templates"])
    
    # Entferne Duplikate basierend auf title
    seen_titles = set()
    unique_templates = []
    
    for template in main_templates["templates"]:
        title = template.get("title", "")
        if title not in seen_titles:
            seen_titles.add(title)
            unique_templates.append(template)
    
    main_templates["templates"] = unique_templates
    
    # Speichere updated template
    with open("portainer-template.json", "w") as f:
        json.dump(main_templates, f, indent=2)
    
    print(f"✅ {len(db_templates['templates'])} Database-Templates integriert")
    print(f"✅ Total Templates: {len(unique_templates)}")
    
except Exception as e:
    print(f"❌ Integration Error: {e}")
EOF

echo ""
echo "📊 GENERIERE DATABASE STATISTIKEN..."
echo "===================================="

# Erstelle Database-Übersicht
python3 << 'EOF'
import json

try:
    with open("reports/database_discovery_stats.json", "r") as f:
        stats = json.load(f)
    
    print("🎯 DATABASE DISCOVERY ERGEBNISSE:")
    print("=================================")
    print(f"📊 Total Datenbanken: {stats['total_databases']}")
    print("")
    print("📂 Kategorien:")
    for category, count in stats["categories"].items():
        print(f"   {category.upper()}: {count} Datenbanken")
    
    print("")
    print("🔍 Top Datenbanken pro Kategorie:")
    for category, databases in stats["databases_by_category"].items():
        print(f"   {category.upper()}: {', '.join(databases[:5])}")
        if len(databases) > 5:
            print(f"      ... und {len(databases) - 5} weitere")
    
except Exception as e:
    print(f"❌ Stats Error: {e}")
EOF

echo ""
echo "✅ DATABASE DISCOVERY COMPLETE!"
echo "==============================="
echo ""
echo "📁 Generierte Files:"
echo "   📋 templates/database/discovered_databases.json"
echo "   🐳 stacks/database-complete.yml"
echo "   📊 reports/database_discovery_stats.json"
echo "   🎯 portainer-template.json (updated)"
echo ""
echo "🚀 Ready für GitHub Upload!"