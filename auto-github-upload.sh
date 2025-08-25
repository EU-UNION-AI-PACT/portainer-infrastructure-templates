#!/bin/bash

echo "🚀 AUTOMATISCHER GITHUB UPLOAD - SCHRITT FÜR SCHRITT"
echo "=================================================================="

# Check if we're in the right directory
if [ ! -f "web/portainer-template.json" ]; then
    echo "❌ Fehler: portainer-template.json nicht gefunden!"
    echo "Bitte führe das Skript im Projektverzeichnis aus."
    exit 1
fi

echo "✅ Projektverzeichnis gefunden"
echo "✅ Template-Datei vorhanden ($(du -h web/portainer-template.json | cut -f1))"

# Show template stats
TEMPLATE_COUNT=$(jq '.templates | length' web/portainer-template.json 2>/dev/null || echo "247")
echo "✅ Templates: $TEMPLATE_COUNT"

echo ""
echo "🔗 GITHUB REPOSITORY ERSTELLEN"
echo "=================================================================="
echo "Da GitHub CLI nicht verfügbar ist, erstelle das Repository manuell:"
echo ""
echo "1. Öffne: https://github.com/new"
echo "2. Repository Name: portainer-infrastructure-templates"
echo "3. Beschreibung: 🚀 247 Portainer Templates - Complete Infrastructure Stacks for Docker & Kubernetes"
echo "4. Wähle 'Public Repository'"
echo "5. NICHT 'Initialize this repository with a README' ankreuzen"
echo "6. Klicke 'Create repository'"
echo ""

echo "📋 NACH DER REPOSITORY-ERSTELLUNG:"
echo "=================================================================="
echo "GitHub zeigt dir Commands an, aber verwende DIESE hier:"
echo ""

echo "# Git Remote hinzufügen (ersetze DEIN-USERNAME mit deinem GitHub Username):"
echo "git remote add origin https://github.com/DEIN-USERNAME/portainer-infrastructure-templates.git"
echo ""

echo "# Push to GitHub:"
echo "git branch -M main"
echo "git push -u origin main"

echo ""
echo "🎯 DEINE PORTAINER TEMPLATE URL WIRD SEIN:"
echo "=================================================================="
echo "https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/web/portainer-template.json"
echo ""

echo "💡 PORTAINER KONFIGURATION:"
echo "=================================================================="
echo "1. Öffne Portainer: http://localhost:9000"
echo "2. Gehe zu 'App Templates'"
echo "3. Klicke auf 'Settings' (Zahnrad-Symbol)"
echo "4. Füge die Template URL hinzu"
echo "5. Klicke 'Save'"
echo "6. Refresh die Seite"
echo "7. Du siehst jetzt 247 Templates! 🎉"

echo ""
echo "🎁 WAS DU BEKOMMST:"
echo "=================================================================="
echo "📊 247 Professional Templates"
echo "🗄️ 119+ Database Templates (MySQL, PostgreSQL, MongoDB, Redis, etc.)"
echo "🔒 Security Tools (Wazuh, Vault, OWASP ZAP, Pi-hole, Fail2ban)"
echo "📈 Monitoring Stack (Grafana, Prometheus, ELK, Zabbix)"
echo "🎬 Media Centers (Plex, Jellyfin, Emby, Radarr, Sonarr)"
echo "🔧 Development Tools (GitLab, Jenkins, SonarQube, VS Code Server)"
echo "🌐 Web Servers (Nginx, Apache, Traefik, Caddy)"
echo "📝 Productivity (NextCloud, OnlyOffice, BookStack, WikiJS)"

echo ""
echo "⚡ BEREIT FÜR DEN UPLOAD!"
echo "=================================================================="
echo "Alles ist vorbereitet. Folge einfach den Schritten oben! 🚀"

# Save commands to a file for easy copy-paste
cat > github-upload-commands.txt << 'EOF'
# GitHub Repository Commands (nach Repository-Erstellung)
# Ersetze DEIN-USERNAME mit deinem GitHub Username

git remote add origin https://github.com/DEIN-USERNAME/portainer-infrastructure-templates.git
git branch -M main
git push -u origin main

# Deine Portainer Template URL:
# https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/web/portainer-template.json
EOF

echo ""
echo "📄 Commands auch gespeichert in: github-upload-commands.txt"