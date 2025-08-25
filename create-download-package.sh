#!/bin/bash

# 📦 PORTAINER TEMPLATE SERVER - COMPLETE SETUP PACKAGE
# Creates a complete, portable template server setup

set -e

echo "📦 Creating Complete Portainer Template Server Package..."

# Farben
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Zielverzeichnis
PACKAGE_DIR="$HOME/Downloads/portainer-template-server"
mkdir -p "$PACKAGE_DIR"

echo -e "${BLUE}📁 Package Directory: ${PACKAGE_DIR}${NC}"

# 1. Kopiere Haupt-Compose-Datei
echo -e "${YELLOW}📋 Copying Docker Compose files...${NC}"
cp docker-compose-complete.yml "$PACKAGE_DIR/docker-compose.yml"
cp docker-compose.templates.yml "$PACKAGE_DIR/docker-compose-simple.yml"

# 2. Kopiere Template-Datei
echo -e "${YELLOW}📄 Copying template files...${NC}"
mkdir -p "$PACKAGE_DIR/web"
cp web/portainer-template.json "$PACKAGE_DIR/web/"

# 3. Kopiere Konfigurationsdateien
echo -e "${YELLOW}⚙️  Copying configuration files...${NC}"
mkdir -p "$PACKAGE_DIR/config"
cp config/nginx.conf "$PACKAGE_DIR/config/"
cp config/haproxy.cfg "$PACKAGE_DIR/config/"

# 4. Kopiere Dockerfile
echo -e "${YELLOW}🐳 Copying Docker files...${NC}"
cp Dockerfile.simple "$PACKAGE_DIR/"

# 5. Erstelle Monitoring-Konfigurationen
echo -e "${YELLOW}📊 Creating monitoring configurations...${NC}"
mkdir -p "$PACKAGE_DIR/monitoring"

# Prometheus config
cat > "$PACKAGE_DIR/monitoring/prometheus.yml" << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'template-server'
    static_configs:
      - targets: ['portainer-template-server:80', 'python-template-server:8000']
    scrape_interval: 30s
    metrics_path: '/health'

  - job_name: 'haproxy'
    static_configs:
      - targets: ['template-loadbalancer:8404']
    scrape_interval: 30s
EOF

# Loki config
cat > "$PACKAGE_DIR/monitoring/loki-config.yml" << 'EOF'
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory

query_range:
  results_cache:
    cache:
      embedded_cache:
        enabled: true
        max_size_mb: 100

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

ruler:
  alertmanager_url: http://localhost:9093

limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: false
  retention_period: 0s

compactor:
  working_directory: /loki/boltdb-shipper-compactor
  shared_store: filesystem
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150
EOF

# Promtail config
cat > "$PACKAGE_DIR/monitoring/promtail-config.yml" << 'EOF'
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: containers
    static_configs:
      - targets:
          - localhost
        labels:
          job: containerlogs
          __path__: /var/lib/docker/containers/*/*log

    pipeline_stages:
      - json:
          expressions:
            output: log
            stream: stream
            attrs:
      - json:
          expressions:
            tag:
          source: attrs
      - regex:
          expression: (?P<container_name>(?:[^|]){1,12})
          source: tag
      - timestamp:
          format: RFC3339Nano
          source: time
      - labels:
          stream:
          container_name:
      - output:
          source: output
EOF

# 6. Erstelle Start-Scripts
echo -e "${YELLOW}🚀 Creating start scripts...${NC}"

# Einfaches Start-Script
cat > "$PACKAGE_DIR/start.sh" << 'EOF'
#!/bin/bash
# Simple start script for Portainer Template Server

echo "🚀 Starting Portainer Template Server..."

# Basic setup (ohne Monitoring)
docker-compose up -d portainer-template-server python-template-server template-loadbalancer

echo "✅ Template Server started!"
echo "🌐 Main URL: http://localhost:8090/portainer-template.json"
echo "📊 Stats: http://localhost:8404/stats"
EOF

# Erweiteres Start-Script mit Monitoring
cat > "$PACKAGE_DIR/start-with-monitoring.sh" << 'EOF'
#!/bin/bash
# Start script with full monitoring stack

echo "🚀 Starting Portainer Template Server with Monitoring..."

# Mit Monitoring
docker-compose --profile monitoring up -d

echo "✅ Template Server with monitoring started!"
echo "🌐 Main URL: http://localhost:8090/portainer-template.json"
echo "📊 HAProxy Stats: http://localhost:8404/stats"
echo "📈 Grafana: http://localhost:3000 (admin/admin123)"
echo "🔍 Prometheus: http://localhost:9090"
echo "📝 Loki: http://localhost:3100"
EOF

# Stop-Script
cat > "$PACKAGE_DIR/stop.sh" << 'EOF'
#!/bin/bash
# Stop all template server services

echo "🛑 Stopping Portainer Template Server..."

docker-compose down

echo "✅ Template Server stopped!"
EOF

# Status-Script
cat > "$PACKAGE_DIR/status.sh" << 'EOF'
#!/bin/bash
# Check status of template server

echo "📊 Portainer Template Server Status:"
echo "======================================"

docker-compose ps

echo ""
echo "📡 Testing endpoints:"

# Test main endpoint
if curl -s http://localhost:8090/portainer-template.json >/dev/null 2>&1; then
    TEMPLATE_COUNT=$(curl -s http://localhost:8090/portainer-template.json | python3 -c "import json,sys; data=json.load(sys.stdin); print(len(data['templates']))" 2>/dev/null || echo "unknown")
    echo "✅ Main URL (Port 8090): Working - $TEMPLATE_COUNT templates"
else
    echo "❌ Main URL (Port 8090): Failed"
fi

# Test individual servers
if curl -s http://localhost:8091/portainer-template.json >/dev/null 2>&1; then
    echo "✅ Nginx Server (Port 8091): Working"
else
    echo "❌ Nginx Server (Port 8091): Failed"
fi

if curl -s http://localhost:8093/portainer-template.json >/dev/null 2>&1; then
    echo "✅ Python Server (Port 8093): Working"
else
    echo "❌ Python Server (Port 8093): Failed"
fi
EOF

# 7. README erstellen
echo -e "${YELLOW}📚 Creating README...${NC}"
cat > "$PACKAGE_DIR/README.md" << 'EOF'
# 🚀 Portainer Template Server - Complete Package

Professional Docker-based template server with **247+ templates** for Portainer.

## ✅ What's Included

- **247 Professional Templates** (Portainer v3 format)
- **High Availability Setup** (Nginx + Python backup + Load Balancer)
- **IPv4/IPv6 Dual Stack Support**
- **CORS Headers** for Portainer compatibility
- **Health Checks & Auto Restart**
- **Optional Monitoring Stack** (Prometheus, Grafana, Loki)
- **Professional Logging**

## 🚀 Quick Start

### 1. Basic Setup (Template Server Only)
```bash
chmod +x start.sh
./start.sh
```

### 2. With Full Monitoring
```bash
chmod +x start-with-monitoring.sh
./start-with-monitoring.sh
```

### 3. Check Status
```bash
chmod +x status.sh
./status.sh
```

### 4. Stop Services
```bash
chmod +x stop.sh
./stop.sh
```

## 📡 Endpoints

### For Portainer Configuration
**Primary URL (Use this):** `http://localhost:8090/portainer-template.json`

### Individual Servers
- Nginx Server: `http://localhost:8091/portainer-template.json`
- Python Backup: `http://localhost:8093/portainer-template.json`

### Monitoring (if enabled)
- HAProxy Stats: `http://localhost:8404/stats`
- Grafana Dashboard: `http://localhost:3000` (admin/admin123)
- Prometheus: `http://localhost:9090`
- Loki Logs: `http://localhost:3100`

## 🎯 Portainer Setup

1. Open Portainer web interface
2. Go to **Settings** → **App Templates**
3. Set template URL to: `http://localhost:8090/portainer-template.json`
4. Save and browse **247 templates** in App Templates!

## 📂 File Structure

```
portainer-template-server/
├── docker-compose.yml              # Complete setup with monitoring
├── docker-compose-simple.yml       # Simple 3-container setup
├── Dockerfile.simple               # Python backup server
├── start.sh                        # Quick start script
├── start-with-monitoring.sh        # Start with monitoring
├── stop.sh                         # Stop all services
├── status.sh                       # Check status
├── web/
│   └── portainer-template.json     # 247 templates
├── config/
│   ├── nginx.conf                  # Nginx configuration
│   └── haproxy.cfg                 # Load balancer config
├── monitoring/
│   ├── prometheus.yml              # Prometheus config
│   ├── loki-config.yml             # Loki config
│   └── promtail-config.yml         # Log collector config
└── README.md                       # This file
```

## 🔧 Manual Commands

```bash
# Start basic services
docker-compose up -d portainer-template-server python-template-server template-loadbalancer

# Start with monitoring
docker-compose --profile monitoring up -d

# View logs
docker-compose logs -f

# Stop all
docker-compose down

# Check container status
docker-compose ps
```

## 🌟 Features

- ✅ **247 Professional Templates** covering all major self-hosted apps
- ✅ **Database Universe** (119 databases: SQL, NoSQL, Vector, Graph, etc.)
- ✅ **Security Stack** (Authelia, Vault, VPN, Monitoring)
- ✅ **Media Center** (Jellyfin, Plex, Sonarr, Radarr)
- ✅ **Productivity** (Nextcloud, BookStack, Gitea)
- ✅ **High Availability** with automatic failover
- ✅ **IPv6 Support** for modern networks
- ✅ **Professional Monitoring** with Grafana dashboards

## 🎉 Success!

Your Portainer template server is now ready with **247 professional templates**!

The collection includes everything from simple utilities to complex infrastructure stacks, with special emphasis on databases and security applications.

**Template Server URL for Portainer:** `http://localhost:8090/portainer-template.json`
EOF

# 8. Executable machen
chmod +x "$PACKAGE_DIR"/*.sh

# 9. Archive erstellen (optional)
echo -e "${YELLOW}📦 Creating archive...${NC}"
cd "$HOME/Downloads"
tar -czf "portainer-template-server-complete.tar.gz" portainer-template-server/

echo -e "${GREEN}🎉 Complete package created successfully!${NC}"
echo ""
echo -e "${BLUE}📁 Package Location:${NC}"
echo "   Directory: $PACKAGE_DIR"
echo "   Archive: $HOME/Downloads/portainer-template-server-complete.tar.gz"
echo ""
echo -e "${BLUE}📋 Package Contents:${NC}"
echo "   ✅ Docker Compose files (simple + complete)"
echo "   ✅ 247 Templates (portainer-template.json)"
echo "   ✅ Nginx & HAProxy configurations"
echo "   ✅ Monitoring stack configs"
echo "   ✅ Start/Stop/Status scripts"
echo "   ✅ Complete documentation"
echo ""
echo -e "${GREEN}🚀 Ready to deploy anywhere!${NC}"