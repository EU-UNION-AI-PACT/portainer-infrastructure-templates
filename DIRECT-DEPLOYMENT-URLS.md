# 🚀 PORTAINER INFRASTRUCTURE TEMPLATES - DEPLOYMENT URLs

## 📋 Nach GitHub Upload sofort verfügbar:

### 🎯 **MASTER TEMPLATE URL** (Alle Templates in einem)
```
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/portainer-template.json
```
**👆 Diese URL in Portainer App Templates einfügen für Zugriff auf alle 6+ Stacks!**

---

## 🐳 **DIREKTE STACK DEPLOYMENT URLs**

### 1. 🛡️ **Complete Security Infrastructure** (Alles in einem)
```bash
# Docker Compose URL
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/docker-compose.yml

# Deployment Command
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/docker-compose.yml | docker-compose -f - up -d
```

### 2. 🆓 **Kostenlose Alternativen** (Keeper→Vaultwarden, Auth0→Keycloak, etc.)
```bash
# Docker Compose URL
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/free-alternatives.yml

# Deployment Command
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/free-alternatives.yml | docker-compose -f - up -d
```

### 3. 🔧 **Extended Security Tools** (SIEM, DevSecOps, Privacy)
```bash
# Docker Compose URL
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/extended-security-tools.yml

# Deployment Command
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/extended-security-tools.yml | docker-compose -f - up -d
```

### 4. 🛡️ **Security Only** (Wazuh, CrowdSec, Vault)
```bash
# Docker Compose URL
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/security-only.yml

# Deployment Command
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/security-only.yml | docker-compose -f - up -d
```

### 5. 📊 **Monitoring Only** (Prometheus, Grafana, Loki)
```bash
# Docker Compose URL
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/monitoring-only.yml

# Deployment Command
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/monitoring-only.yml | docker-compose -f - up -d
```

### 6. 🔐 **VPN Only** (WireGuard, OpenVPN, Tailscale)
```bash
# Docker Compose URL
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/vpn-only.yml

# Deployment Command
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/vpn-only.yml | docker-compose -f - up -d
```

### 7. 💻 **Development Stack** (GitLab, Jenkins, SonarQube)
```bash
# Docker Compose URL
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/development.yml

# Deployment Command
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/development.yml | docker-compose -f - up -d
```

---

## 🎯 **ONE-CLICK DEPLOYMENT Optionen**

### Option 1: **Portainer Integration** (Empfohlen)
1. Öffne Portainer: `http://localhost:9000`
2. Gehe zu **App Templates** → **Settings**
3. Füge Template URL hinzu:
   ```
   https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/portainer-template.json
   ```
4. **Save** und Template-Liste aktualisieren
5. **Deploy with one click!** 🚀

### Option 2: **Direct GitHub Import**
1. Öffne Portainer: `http://localhost:9000`
2. Gehe zu **Stacks** → **Add stack**
3. Wähle **Repository** Tab
4. Repository URL: `https://github.com/YOUR_USERNAME/portainer-infrastructure-templates`
5. Compose file path: `docker-compose.yml` (oder einen der `stacks/*.yml`)
6. **Deploy the stack**

### Option 3: **Terminal One-Liner**
```bash
# Gesamte Infrastruktur
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/docker-compose.yml | docker-compose -f - up -d

# Oder spezifischer Stack (Beispiel: Free Alternatives)
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/free-alternatives.yml | docker-compose -f - up -d
```

---

## 📚 **KOMPLETTE DOKUMENTATION URLs**

### Setup & Installation Guides
```
# Hauptdokumentation
https://github.com/YOUR_USERNAME/portainer-infrastructure-templates/blob/main/README.md

# Deployment Guide
https://github.com/YOUR_USERNAME/portainer-infrastructure-templates/blob/main/DEPLOYMENT-README.md

# Environment Konfiguration
https://github.com/YOUR_USERNAME/portainer-infrastructure-templates/blob/main/.env.example
```

### Template Sammlungen
```
# Kostenlose Alternativen
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/templates/security/free-alternatives.json

# Extended Docker Tools
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/templates/security/extended-docker-tools.json

# Security Templates
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/templates/security/security-templates.json
```

---

## 🌐 **INSTANT INFRASTRUCTURE ACCESS** (nach Deployment)

### 🆓 Kostenlose Alternativen Stack
```bash
Vaultwarden (Keeper):     http://localhost:8080
Keycloak (Auth0):         http://localhost:8081
Authentik (Authy):        http://localhost:8082
Authelia (FrontEgg):      http://localhost:8083
FusionAuth (Okta):        http://localhost:8084
Passbolt (Team Pass):     http://localhost:8085
```

### 🔧 Extended Security Tools Stack
```bash
Wazuh Manager:            http://localhost:55000
FusionAuth:               http://localhost:9011
Trivy Scanner:            http://localhost:4954
OWASP ZAP:                http://localhost:8080
Roundcube Mail:           http://localhost:8081
Pi-hole:                  http://localhost:8082
Passbolt:                 http://localhost:8083
MISP:                     http://localhost:8084
TheHive:                  http://localhost:9000
PrivacyIDEA:              http://localhost:5001
```

### 📊 Monitoring Stack
```bash
Grafana:                  http://localhost:3000
Prometheus:               http://localhost:9090
Kibana:                   http://localhost:5601
AlertManager:             http://localhost:9093
```

### 🔐 VPN Stack
```bash
OpenVPN Admin:            https://localhost:943
pfSense:                  https://localhost:8443
Nginx Proxy Manager:      http://localhost:81
```

---

## 🔄 **AUTOMATISCHE UPDATES**

### Template Manager (Python)
```bash
# Alle 77+ Templates aktualisieren
python portainer_manager.py update

# Reports generieren
python portainer_manager.py report

# Templates validieren
python portainer_manager.py validate
```

### GitHub Sync
```bash
# Repository aktualisieren
git pull origin main

# Neue Templates pullen
docker-compose pull

# Services neu starten
docker-compose up -d
```

---

## 🎯 **QUICK START COMMANDS**

### 1-Minute Deployment
```bash
# Template URL zu Portainer hinzufügen
curl -X POST http://localhost:9000/api/settings \
  -H "Content-Type: application/json" \
  -d '{"templatesURL": "https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/portainer-template.json"}'

# Sofort deploybare Infrastruktur
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/docker-compose.yml | docker-compose -f - up -d
```

### Backup & Migration
```bash
# Alle Volumes sichern
docker run --rm -v portainer_data:/data -v $(pwd):/backup alpine tar czf /backup/portainer-backup.tar.gz /data

# Configuration exportieren
docker-compose config > current-infrastructure.yml
```

---

## 🚀 **READY TO GO!**

**Nach GitHub Upload sind sofort verfügbar:**
✅ **Master Template URL** für Portainer Integration  
✅ **6+ direkte Stack URLs** für spezifische Deployments  
✅ **One-Click Commands** für Terminal Deployment  
✅ **Komplette Dokumentation** mit Setup-Guides  
✅ **Instant Access URLs** für alle Services  
✅ **Automatische Updates** über GitHub Integration  

**Einfach `./deploy-to-github.sh` ausführen und alle URLs sind live! 🎯**