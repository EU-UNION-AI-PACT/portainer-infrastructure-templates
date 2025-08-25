# Portainer Infrastructure Templates
Complete infrastructure stacks for instant deployment via Portainer.

## Quick Deploy URLs

### For Portainer Template Integration
```
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/portainer-template.json
```

### Direct Stack Deployment URLs
```bash
# Complete Infrastructure (All Services)
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/docker-compose.yml

# Security-Only Stack
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/security-only.yml

# Monitoring-Only Stack
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/monitoring-only.yml

# VPN-Only Stack
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/vpn-only.yml

# Development Stack
https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/stacks/development.yml
```

## Available Stacks

### 🛡️ Security Stack
- **Wazuh SIEM**: Complete security monitoring (Manager + Indexer + Dashboard)
- **CrowdSec**: Behavioral detection and IP blocking
- **Vault**: HashiCorp secret management
- **Vaultwarden**: Bitwarden-compatible password manager
- **Authelia**: Advanced authentication and authorization

### 📊 Monitoring Stack
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboards
- **Loki**: Log aggregation
- **Elasticsearch + Kibana**: Advanced log analysis
- **Node Exporter**: System metrics
- **cAdvisor**: Container metrics
- **AlertManager**: Alert routing and management

### 🔐 VPN Stack
- **WireGuard**: Modern VPN solution
- **OpenVPN Access Server**: Enterprise VPN
- **Tailscale**: Zero-config VPN mesh network
- **ZeroTier**: Software-defined networking
- **pfSense**: Firewall and router
- **Nginx Proxy Manager**: SSL certificates and reverse proxy

### 💻 Development Stack
- **Code Server**: VS Code in browser
- **Gitea**: Git service with web interface
- **GitLab CE**: Complete DevOps platform
- **Jenkins**: CI/CD automation
- **Docker Registry**: Private container registry
- **SonarQube**: Code quality analysis

## Instant Deployment

### Method 1: Via Portainer Templates
1. Open Portainer
2. Go to **App Templates**
3. Click **Settings** → **Add custom template**
4. Paste template URL from above
5. Save and refresh
6. Deploy any stack with one click

### Method 2: Direct Stack Import
1. Open Portainer
2. Go to **Stacks**
3. Click **Add stack**
4. Choose **Repository** tab
5. Paste any stack URL from above
6. Click **Deploy the stack**

### Method 3: Local Docker Compose
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/portainer-infrastructure-templates.git
cd portainer-infrastructure-templates

# Deploy complete infrastructure
docker-compose up -d

# Or deploy specific stack
docker-compose -f stacks/security-only.yml up -d
docker-compose -f stacks/monitoring-only.yml up -d
docker-compose -f stacks/vpn-only.yml up -d
docker-compose -f stacks/development.yml up -d
```

## Access Information

### Security Stack Endpoints
- **Wazuh Dashboard**: https://localhost:443
- **CrowdSec**: http://localhost:8080
- **Vault**: http://localhost:8200
- **Vaultwarden**: http://localhost:8081

### Monitoring Stack Endpoints
- **Grafana**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090
- **Kibana**: http://localhost:5601
- **AlertManager**: http://localhost:9093

### VPN Stack Endpoints
- **OpenVPN Admin**: https://localhost:943
- **pfSense**: https://localhost:8443
- **Nginx Proxy Manager**: http://localhost:81

### Development Stack Endpoints
- **Code Server**: https://localhost:8443
- **Gitea**: http://localhost:3001
- **GitLab**: http://localhost:8083
- **Jenkins**: http://localhost:8082
- **SonarQube**: http://localhost:9000

## Environment Variables

Create `.env` file for custom passwords:
```bash
# Security Stack
WAZUH_PASSWORD=your-secure-password
VAULTWARDEN_ADMIN_TOKEN=your-admin-token
VAULT_TOKEN=hvs.your-root-token

# Monitoring Stack
GRAFANA_PASSWORD=your-grafana-password

# VPN Stack
WIREGUARD_SERVER_URL=your-domain.com
TAILSCALE_AUTHKEY=your-tailscale-key
NPM_DB_PASSWORD=your-npm-password
NPM_DB_ROOT_PASSWORD=your-root-password

# Development Stack
CODE_SERVER_PASSWORD=your-code-password
GITEA_DB_PASSWORD=your-gitea-password
SONAR_DB_PASSWORD=your-sonar-password
```

## Template Management

This repository also includes a Python-based template management system for collecting and merging Portainer templates from 77+ sources.

### Quick Start
```bash
# Install dependencies
./setup.sh

# Update all templates
python portainer_manager.py update

# Generate reports
python portainer_manager.py report
```

### Features
- **77+ Template Sources**: Comprehensive collection from major providers
- **Automatic Validation**: JSON schema validation and duplicate detection
- **Category Organization**: Templates organized by application type
- **Detailed Reporting**: Statistics and analysis of template collections
- **Async Processing**: Fast parallel template fetching

## Contributing

1. Fork the repository
2. Add your template sources to `config/sources.json`
3. Create new stack configurations in `stacks/`
4. Update `portainer-template.json` with new templates
5. Submit a pull request

## License

MIT License - Feel free to use and modify for your infrastructure needs.

## Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Documentation**: Complete setup guides in `/docs`
- **Community**: Join discussions in GitHub Discussions

---

🚀 **Ready to deploy enterprise infrastructure in seconds!**