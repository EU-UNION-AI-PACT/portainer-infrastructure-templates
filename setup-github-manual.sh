#!/bin/bash

echo "🚀 Portainer Infrastructure Templates - Manual GitHub Setup"
echo "=================================================================="
echo ""
echo "📋 ANLEITUNG:"
echo "1. Erstelle ein neues Repository auf GitHub:"
echo "   - Gehe zu: https://github.com/new"
echo "   - Name: portainer-infrastructure-templates"
echo "   - Beschreibung: 🚀 Complete infrastructure stacks for instant deployment via Portainer. 247+ templates"
echo "   - Wähle 'Public' aus"
echo "   - Klicke 'Create repository'"
echo ""
echo "2. Kopiere die Repository URL (z.B.: https://github.com/DEIN-USERNAME/portainer-infrastructure-templates.git)"
echo ""
echo "3. Führe dann diese Befehle aus:"
echo ""

# Check current git status
echo "🔍 Aktueller Git Status:"
git status --short

echo ""
echo "📝 BEFEHLE ZUM KOPIEREN:"
echo "=================================================================="
echo "# Remote origin setzen (ersetze DEIN-USERNAME mit deinem GitHub Username)"
echo "git remote remove origin 2>/dev/null || true"
echo "git remote add origin https://github.com/DEIN-USERNAME/portainer-infrastructure-templates.git"
echo ""
echo "# Push to GitHub"
echo "git push -u origin main"
echo ""
echo "=================================================================="
echo ""
echo "🎯 DEINE PORTAINER TEMPLATE URL (nach GitHub Upload):"
echo "https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/web/portainer-template.json"
echo ""
echo "💡 Diese URL dann in Portainer unter 'App Templates → Settings' einfügen!"
echo ""
echo "📊 TEMPLATE STATISTIKEN:"
echo "=================================================================="

# Check template file
if [ -f "web/portainer-template.json" ]; then
    TEMPLATE_COUNT=$(jq '.templates | length' web/portainer-template.json 2>/dev/null || echo "?)") 
    echo "✅ Template Datei gefunden: web/portainer-template.json"
    echo "📈 Anzahl Templates: $TEMPLATE_COUNT"
    echo "📁 Dateigröße: $(du -h web/portainer-template.json | cut -f1)"
else
    echo "❌ Template Datei nicht gefunden!"
fi

echo ""
echo "🔗 NACH DEM GITHUB UPLOAD:"
echo "=================================================================="
echo "1. Öffne Portainer: http://localhost:9000"
echo "2. App Templates → Settings"
echo "3. Template URL hinzufügen"
echo "4. Save & Enjoy 247 Templates! 🎉"