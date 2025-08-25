#!/bin/bash

# Portainer Template Server - Docker Compose Deployment
# Einfache und zuverlässige Bereitstellung von 247 Portainer Templates

set -e

echo "🚀 Starting Portainer Template Server with Docker Compose..."

# Farben für bessere Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Prüfe ob Docker läuft
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker ist nicht verfügbar oder läuft nicht!${NC}"
    echo "Bitte starte Docker und versuche es erneut."
    exit 1
fi

# Prüfe ob docker-compose verfügbar ist
if ! command -v docker-compose >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  docker-compose nicht gefunden, verwende 'docker compose'${NC}"
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Prüfe Template-Datei
if [ ! -f "web/portainer-template.json" ]; then
    echo -e "${RED}❌ Template-Datei nicht gefunden: web/portainer-template.json${NC}"
    exit 1
fi

# Zähle Templates
TEMPLATE_COUNT=$(python3 -c "import json; data=json.load(open('web/portainer-template.json')); print(len(data['templates']))" 2>/dev/null || echo "unknown")

echo -e "${BLUE}📊 Template Info:${NC}"
echo -e "   📄 Template-Datei: web/portainer-template.json"
echo -e "   📈 Anzahl Templates: ${TEMPLATE_COUNT}"
echo ""

# Stoppe eventuell laufende Container
echo -e "${YELLOW}🔄 Stoppe vorhandene Template-Server...${NC}"
$COMPOSE_CMD -f docker-compose.templates.yml down --remove-orphans >/dev/null 2>&1 || true

# Erstelle notwendige Verzeichnisse
mkdir -p config data logs

# Starte die Services
echo -e "${BLUE}🐳 Starte Docker Compose Services...${NC}"
$COMPOSE_CMD -f docker-compose.templates.yml up -d

# Warte auf Services
echo -e "${YELLOW}⏳ Warte auf Services...${NC}"
sleep 10

# Prüfe Service Status
echo -e "${BLUE}📋 Service Status:${NC}"

# Nginx Server
if curl -s http://localhost:8091/health >/dev/null 2>&1; then
    echo -e "   ✅ Nginx Template Server: ${GREEN}RUNNING${NC} (Port 8091)"
else
    echo -e "   ❌ Nginx Template Server: ${RED}FAILED${NC} (Port 8091)"
fi

# Python Server
if curl -s http://localhost:8093/portainer-template.json >/dev/null 2>&1; then
    echo -e "   ✅ Python Backup Server: ${GREEN}RUNNING${NC} (Port 8093)"
else
    echo -e "   ❌ Python Backup Server: ${RED}FAILED${NC} (Port 8093)"
fi

# Load Balancer
if curl -s http://localhost:8090/health >/dev/null 2>&1; then
    echo -e "   ✅ Load Balancer: ${GREEN}RUNNING${NC} (Port 8090)"
else
    echo -e "   ❌ Load Balancer: ${RED}FAILED${NC} (Port 8090)"
fi

echo ""
echo -e "${GREEN}🎉 Portainer Template Server erfolgreich gestartet!${NC}"
echo ""
echo -e "${BLUE}📡 Verfügbare Endpunkte:${NC}"
echo -e "   🌐 Haupt-URL (Load Balanced): ${GREEN}http://localhost:8090/portainer-template.json${NC}"
echo -e "   🔧 Nginx Server: http://localhost:8091/portainer-template.json"
echo -e "   🐍 Python Backup: http://localhost:8093/portainer-template.json"
echo -e "   📊 HAProxy Stats: http://localhost:8404/stats"
echo ""
echo -e "${YELLOW}🔧 Für Portainer verwende:${NC}"
echo -e "   Template URL: ${GREEN}http://localhost:8090/portainer-template.json${NC}"
echo ""
echo -e "${BLUE}📝 Befehle:${NC}"
echo -e "   Logs anzeigen: ${COMPOSE_CMD} -f docker-compose.templates.yml logs -f"
echo -e "   Services stoppen: ${COMPOSE_CMD} -f docker-compose.templates.yml down"
echo -e "   Status prüfen: ${COMPOSE_CMD} -f docker-compose.templates.yml ps"

# Test Template-Endpunkt
echo ""
echo -e "${BLUE}🧪 Teste Template-Endpunkt...${NC}"
if TEMPLATE_TEST=$(curl -s http://localhost:8090/portainer-template.json | python3 -c "import json,sys; data=json.load(sys.stdin); print(f'✅ {len(data[\"templates\"])} Templates verfügbar')" 2>/dev/null); then
    echo -e "   ${TEMPLATE_TEST}"
else
    echo -e "   ❌ Template-Test fehlgeschlagen"
fi

echo ""
echo -e "${GREEN}🚀 Setup abgeschlossen! Der Template-Server ist bereit.${NC}"