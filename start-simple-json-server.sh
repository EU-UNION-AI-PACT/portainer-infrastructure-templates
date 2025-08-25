#!/bin/bash
# Simple Portainer Template Server für JSON-only
# Serves only the portainer-template.json file

cd "/home/holythreekingstreescrowns/Schreibtisch/Portainer Template/web"

echo "🚀 Starting Simple JSON Template Server..."
echo "📂 Serving from: $(pwd)"
echo "📋 Template file: portainer-template.json"

# Check if template file exists
if [ ! -f "portainer-template.json" ]; then
    echo "❌ portainer-template.json not found!"
    exit 1
fi

# Validate JSON
if ! jq empty portainer-template.json 2>/dev/null; then
    echo "❌ Invalid JSON in template file!"
    exit 1
fi

TEMPLATE_COUNT=$(jq '.templates | length' portainer-template.json)
echo "✅ $TEMPLATE_COUNT templates validated"

echo "🔗 Template URL: http://localhost:8091/portainer-template.json"
echo "🔗 IPv6 URL: http://[::1]:8091/portainer-template.json"
echo "✅ CORS headers will be added automatically"
echo "🔄 Starting server... (Ctrl+C to stop)"
echo ""

# Start simple HTTP server with IPv6 dual-stack
# The --bind :: enables both IPv4 and IPv6
exec python3 -m http.server 8091 --bind ::