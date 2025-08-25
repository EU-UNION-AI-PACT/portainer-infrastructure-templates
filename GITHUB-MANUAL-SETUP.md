# 🚀 GitHub Manual Setup Guide

## Schritt 1: GitHub Repository erstellen

1. Gehe zu https://github.com/new
2. Repository Name: `portainer-infrastructure-templates`
3. Description: `🚀 Complete infrastructure stacks for instant deployment via Portainer. 247+ templates with Docker Compose stacks for Security, Monitoring, VPN, and Development.`
4. Wähle "Public" aus
5. Klicke "Create repository"

## Schritt 2: Repository URL kopieren

Nach der Erstellung kopiere die Repository URL (sollte so aussehen):
```
https://github.com/DEIN-USERNAME/portainer-infrastructure-templates.git
```

## Schritt 3: Remote Origin setzen und pushen

Führe diese Befehle in deinem Terminal aus:

```bash
cd "/home/holythreekingstreescrowns/Schreibtisch/Portainer Template"

# Remote origin setzen (ersetze DEIN-USERNAME mit deinem GitHub Username)
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/DEIN-USERNAME/portainer-infrastructure-templates.git

# Push to GitHub
git push -u origin main
```

## Schritt 4: Portainer Template URL

Nach erfolgreichem Upload ist deine Portainer Template URL:

```
https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/web/portainer-template.json
```

## Schritt 5: In Portainer konfigurieren

1. Öffne Portainer: http://localhost:9000
2. Gehe zu "App Templates" → "Settings"
3. Füge die Template URL hinzu (von Schritt 4)
4. Klicke "Save"
5. Refresh die Seite

## 🎉 Fertig!

Du hast jetzt 247 professionelle Templates verfügbar in Portainer!

### Template Kategorien:
- 🗄️ **119 Databases** (PostgreSQL, MySQL, MongoDB, etc.)
- 🔒 **Security Tools** (Wazuh, OWASP ZAP, Vault, etc.)
- 📊 **Monitoring** (Grafana, Prometheus, ELK Stack)
- 🎬 **Media Centers** (Plex, Jellyfin, Emby)
- 🔧 **Development Tools** (GitLab, Jenkins, SonarQube)
- 🌐 **Web Servers** (Nginx, Apache, Traefik)
- 📝 **Productivity** (NextCloud, OnlyOffice, BookStack)

### Alternative URLs (falls benötigt):
- Complete Stack: `https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/docker-compose.yml`
- Security Only: `https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/stacks/security-only.yml`
- Monitoring Only: `https://raw.githubusercontent.com/DEIN-USERNAME/portainer-infrastructure-templates/main/stacks/monitoring-only.yml`