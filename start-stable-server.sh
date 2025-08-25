#!/bin/bash

# Stable Template Server für Portainer
set -euo pipefail

# Verzeichnis erstellen falls nicht vorhanden
mkdir -p web

# Template kopieren
cp portainer-template.json web/

# Port prüfen und freigeben falls belegt
if lsof -Pi :8091 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "🔄 Port 8091 ist belegt - beende alte Prozesse..."
    lsof -ti:8091 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Server starten
echo "🚀 Starte Template Server auf Port 8091..."
cd web

# Server im Hintergrund starten
nohup python3 -m http.server 8091 > ../template-server.log 2>&1 &
SERVER_PID=$!

# Kurz warten bis Server bereit ist
sleep 3

# Testen ob Server läuft
if curl -s http://localhost:8091/portainer-template.json >/dev/null 2>&1; then
    echo "✅ Template Server erfolgreich gestartet!"
    echo "📋 Template URL: http://localhost:8091/portainer-template.json"
    echo "🌐 Web Interface: http://localhost:8091"
    echo "🔢 Server PID: $SERVER_PID"
    echo "$SERVER_PID" > ../template-server.pid
else
    echo "❌ Template Server konnte nicht gestartet werden!"
    exit 1
fi