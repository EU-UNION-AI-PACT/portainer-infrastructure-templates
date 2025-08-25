# 🎯 QUICK START URLs - Nach GitHub Upload sofort nutzbar!

## 🚀 MASTER TEMPLATE URL (In Portainer einfügen)
```
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/portainer-template.json
```

## 🔥 ONE-LINER DEPLOYMENTS

### Alle Services (Complete Infrastructure)
```bash
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/docker-compose.yml | docker-compose -f - up -d
```

### Kostenlose Alternativen (Keeper→Vaultwarden, Auth0→Keycloak)
```bash
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/free-alternatives.yml | docker-compose -f - up -d
```

### Extended Security Tools (SIEM, DevSecOps, Privacy)
```bash
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/extended-security-tools.yml | docker-compose -f - up -d
```

## 📱 MASTER ALL-IN-ONE INSTALLER
```bash
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/all-in-one-deploy.sh | bash
```

## 🌐 INSTANT ACCESS (Nach Deployment)

| Service | URL | Stack |
|---------|-----|-------|
| **Vaultwarden** (Keeper Alternative) | http://localhost:8080 | Free Alternatives |
| **Keycloak** (Auth0 Alternative) | http://localhost:8081 | Free Alternatives |
| **Authentik** (Authy Alternative) | http://localhost:8082 | Free Alternatives |
| **FusionAuth** (Okta Alternative) | http://localhost:8084 | Free Alternatives |
| **Wazuh Manager** (SIEM) | http://localhost:55000 | Extended Security |
| **OWASP ZAP** (Security Scanner) | http://localhost:8080 | Extended Security |
| **Pi-hole** (DNS Filter) | http://localhost:8082 | Extended Security |
| **TheHive** (Incident Response) | http://localhost:9000 | Extended Security |
| **Grafana** (Monitoring) | http://localhost:3000 | Monitoring |
| **Prometheus** (Metrics) | http://localhost:9090 | Monitoring |
| **Portainer** (Container Management) | http://localhost:9000 | Always Available |

## 🎯 3-MINUTE SETUP

1. **Add Template to Portainer:**
   ```
   http://localhost:9000 → App Templates → Settings → Add URL:
   https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/portainer-template.json
   ```

2. **Deploy Stack:** Click any template → Deploy

3. **Access Services:** Use URLs from table above

## 🔧 CUSTOMIZATION

### Environment Variables
```bash
# Download and customize
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/.env.example > .env
# Edit .env with your passwords and settings
```

### Specific Stack Deployment
```bash
# Security Only
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/security-only.yml | docker-compose -f - up -d

# Monitoring Only  
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/monitoring-only.yml | docker-compose -f - up -d

# VPN Only
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/vpn-only.yml | docker-compose -f - up -d
```

---

**🚀 Ready to deploy enterprise-grade infrastructure in minutes!**