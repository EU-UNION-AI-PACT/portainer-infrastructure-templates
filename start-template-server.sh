#!/bin/bash

# Portainer Template URL Server
# Macht das portainer-template.json über lokale URL verfügbar

set -euo pipefail

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔗 PORTAINER TEMPLATE URL SERVER${NC}"
echo -e "${BLUE}=================================${NC}"

# Check if template exists
if [ ! -f "portainer-template.json" ]; then
    echo "❌ portainer-template.json nicht gefunden!"
    exit 1
fi

# Create web directory
mkdir -p web

# Copy template to web directory
cp portainer-template.json web/

# Create simple index page
cat > web/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Portainer Template URL Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        .url-box { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; font-family: monospace; }
        .copy-btn { background: #007bff; color: white; border: none; padding: 10px 20px; cursor: pointer; }
        .step { margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; background: #f8f9fa; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 Portainer Template URL Server</h1>
        
        <div class="step">
            <h3>📋 Schritt 1: Portainer öffnen</h3>
            <p>Gehe zu deiner Portainer Instanz und melde dich an.</p>
        </div>

        <div class="step">
            <h3>⚙️ Schritt 2: App Templates Settings</h3>
            <p>Klicke auf <strong>Settings</strong> → <strong>App Templates</strong></p>
        </div>

        <div class="step">
            <h3>🔗 Schritt 3: Template URL hinzufügen</h3>
            <p>Füge diese URL in Portainer ein:</p>
            <div class="url-box">
                <strong>http://localhost:8091/portainer-template.json</strong>
                <button class="copy-btn" onclick="copyUrl()">📋 Kopieren</button>
            </div>
        </div>

        <div class="step">
            <h3>✅ Schritt 4: Templates laden</h3>
            <p>Klicke auf <strong>Save Settings</strong> → Gehe zu <strong>App Templates</strong></p>
            <p><strong>🎉 Alle 125+ Templates sind sofort verfügbar!</strong></p>
        </div>

        <h2>📊 Template Statistiken</h2>
        <ul>
            <li><strong>Total Templates:</strong> 125+</li>
            <li><strong>Database Engines:</strong> 118+</li>
            <li><strong>Security Stacks:</strong> 7</li>
            <li><strong>Categories:</strong> 10</li>
        </ul>

        <h2>🔗 Direct Links</h2>
        <ul>
            <li><a href="/portainer-template.json">📄 Template JSON anzeigen</a></li>
            <li><a href="http://localhost:9000" target="_blank">🐳 Portainer öffnen</a></li>
            <li><a href="http://localhost:8090" target="_blank">🔒 GDPR Compliance Portal</a></li>
        </ul>
    </div>

    <script>
        function copyUrl() {
            navigator.clipboard.writeText('http://localhost:8091/portainer-template.json');
            alert('URL kopiert! 📋');
        }
    </script>
</body>
</html>
EOF

echo -e "${GREEN}✅ Web-Verzeichnis erstellt${NC}"

# Start Python HTTP server
echo -e "${YELLOW}🚀 Starte Template URL Server...${NC}"
echo ""
echo -e "${GREEN}📋 Portainer Template URL:${NC}"
echo -e "${BLUE}http://localhost:8091/portainer-template.json${NC}"
echo ""
echo -e "${GREEN}🌐 Web Interface:${NC}"
echo -e "${BLUE}http://localhost:8091${NC}"
echo ""
echo -e "${YELLOW}⚡ Server läuft... (Strg+C zum Stoppen)${NC}"
echo ""

cd web
python3 -m http.server 8091