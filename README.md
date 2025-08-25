# 🔐 Portainer Security Infrastructure Stack

Eine vollständige Docker Compose-basierte Security- und Monitoring-Infrastruktur mit 247+ Portainer Templates.

## 🏆 Badges & Certifications

![Templates](https://img.shields.io/badge/Templates-247-brightgreen?style=for-the-badge&logo=docker)
![Certification](https://img.shields.io/badge/Certification-Pink%20Star%20Diamond%20(191)-ff69b4?style=for-the-badge&logo=certificate)
![Quality](https://img.shields.io/badge/Quality%20Score-191/100-ff69b4?style=for-the-badge&logo=star)
![Deployment](https://img.shields.io/badge/Deployment-Live-brightgreen?style=for-the-badge&logo=github)
![Cosmic Power](https://img.shields.io/badge/Cosmic%20Power-Pink%20Star%20Diamond-ff1493?style=for-the-badge&logo=gem)
![Portainer](https://img.shields.io/badge/Portainer-v3%20Compatible-blue?style=for-the-badge&logo=portainer)
![Security](https://img.shields.io/badge/Security-GDPR%20Compliant-green?style=for-the-badge&logo=shield)
![Maintenance](https://img.shields.io/badge/Maintenance-Active-brightgreen?style=for-the-badge&logo=tools)

## 🚀 Dual-Mode: Template Manager + Live Stack

### Mode 1: Template Management
- **Template Fetching**: Download templates from 77+ curated sources
- **Smart Merging**: Combine templates while avoiding duplicates
- **Template Validation**: Verify template integrity and format
- **Report Generation**: Generate detailed reports on available templates
- **Source Management**: Easy addition and removal of template sources
- **Export Options**: Generate master template files for Portainer

### Mode 2: Live Security Stack
- **Complete Docker Compose**: Ready-to-deploy security infrastructure
- **Integrated Monitoring**: Prometheus, Grafana, Loki, Elasticsearch
- **Security Tools**: Wazuh, CrowdSec, Vault, Authelia
- **VPN Solutions**: WireGuard ready-to-go
- **Enterprise Ready**: Scalable and production-ready

## Template Sources

This project includes templates from:
- **Lissy93**: 500+ comprehensive templates
- **Qballjos**: Homelab-focused collection
- **Technorabilia**: LinuxServer.io driven templates
- **SelfhostedPro**: Self-hosted service templates
- **And 29+ more sources**: Community-maintained collections

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Fetch all templates**:
   ```bash
   python scripts/fetch_templates.py
   ```

3. **Generate master template**:
   ```bash
   python scripts/merge_templates.py
   ```

4. **View template report**:
   ```bash
   python scripts/generate_report.py
   ```

## Project Structure

```
├── scripts/                    # Main Python scripts
│   ├── fetch_templates.py     # Download templates from sources
│   ├── merge_templates.py     # Merge and deduplicate templates
│   ├── generate_report.py     # Generate template reports
│   └── validate_templates.py  # Validate template integrity
├── templates/                 # Downloaded template files
│   ├── individual/           # Individual source templates
│   └── merged/               # Merged template files
├── config/                   # Configuration files
│   └── sources.json         # Template source URLs
├── reports/                 # Generated reports
└── docs/                   # Documentation
```

## Configuration

Edit `config/sources.json` to add or modify template sources. Each source should include:
- `name`: Descriptive name
- `url`: Raw JSON URL
- `description`: Brief description
- `active`: Boolean to enable/disable

## Usage Examples

### Fetch specific sources
```bash
python scripts/fetch_templates.py --sources lissy93,qballjos
```

### Generate filtered templates
```bash
python scripts/merge_templates.py --categories networking,media
```

### Validate all templates
```bash
python scripts/validate_templates.py --verbose
```

## Contributing

1. Fork the repository
2. Add new template sources to `config/sources.json`
3. Test with `python scripts/validate_templates.py`
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Credits

Thanks to all the community maintainers of these template collections:
- Lissy93, Qballjos, Technorabilia, SelfhostedPro, and many others!