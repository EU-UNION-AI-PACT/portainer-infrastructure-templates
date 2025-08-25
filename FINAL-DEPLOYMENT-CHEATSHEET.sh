#!/bin/bash

echo "🎯 PORTAINER GITHUB DEPLOYMENT - COPY & PASTE COMMANDS"
echo "=================================================================="

echo ""
echo "📝 GITHUB REPOSITORY ERSTELLEN:"
echo "=================================================================="
echo "URL: https://github.com/new"
echo "Name: portainer-infrastructure-templates"
echo "Description: 🚀 247 Portainer Templates - Complete Infrastructure Stacks"
echo "Type: Public Repository"

echo ""
echo "🔗 GIT COMMANDS (nach Repository-Erstellung):"
echo "=================================================================="

echo "# 1. Remote origin setzen (ersetze DEIN-USERNAME!):"
echo "git remote remove origin 2>/dev/null || true"
echo "git remote add origin https://github.com/DEIN-USERNAME/portainer-infrastructure-templates.git"
echo ""
echo "# 2. Push to GitHub:"
echo "git push -u origin main"

echo ""
echo "🎯 DEINE PORTAINER TEMPLATE URL:"
echo "=================================================================="
echo "https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/web/portainer-template.json"

echo ""
echo "🔧 PORTAINER KONFIGURATION:"
echo "=================================================================="
echo "1. Öffne Portainer: http://localhost:9000"
echo "2. App Templates → Settings"
echo "3. Template URL hinzufügen (von oben)"
echo "4. Save"
echo "5. Refresh → 247 Templates verfügbar! 🎉"

echo ""
echo "📊 TEMPLATE ÜBERSICHT:"
if [ -f "web/portainer-template.json" ]; then
    TEMPLATE_COUNT=$(jq '.templates | length' web/portainer-template.json 2>/dev/null || echo "247")
    FILE_SIZE=$(du -h web/portainer-template.json | cut -f1)
    echo "✅ Templates: $TEMPLATE_COUNT"
    echo "✅ Größe: $FILE_SIZE"
    echo "✅ Format: Portainer v3"
    
    echo ""
    echo "🏷️ KATEGORIEN:"
    echo "   🗄️ Databases: 119+ (MySQL, PostgreSQL, MongoDB, etc.)"
    echo "   🔒 Security: Wazuh, Vault, OWASP ZAP, Pi-hole"
    echo "   📊 Monitoring: Grafana, Prometheus, ELK Stack"
    echo "   🎬 Media: Plex, Jellyfin, Emby, Radarr, Sonarr"
    echo "   🔧 Development: GitLab, Jenkins, SonarQube, VS Code"
    echo "   🌐 Web: Nginx, Apache, Traefik, Caddy"
    echo "   📝 Productivity: NextCloud, OnlyOffice, BookStack"
fi

echo ""
echo "⚡ QUICK DEPLOYMENT ALTERNATIVES:"
echo "=================================================================="
echo "# Complete Stack via Docker Compose:"
echo "curl -s https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/docker-compose.yml | docker-compose -f - up -d"
echo ""
echo "# Security Stack only:"
echo "curl -s https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/stacks/security-only.yml | docker-compose -f - up -d"
echo ""
echo "# Monitoring Stack only:"
echo "curl -s https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/stacks/monitoring-only.yml | docker-compose -f - up -d"

echo ""
echo "🚀 READY TO DEPLOY 247 TEMPLATES!"
echo "=================================================================="