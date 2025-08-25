#!/bin/bash
# Simple start script for Portainer Template Server

cd "/home/holythreekingstreescrowns/Schreibtisch/Portainer Template/web"

echo "🚀 Starting Portainer Template Server..."
echo "📂 Serving from: $(pwd)"
echo "🔗 Template URL: http://localhost:8091/portainer-template.json"
echo "🔗 IPv6 URL: http://[::1]:8091/portainer-template.json"
echo "✅ Server ready for Portainer integration"
echo "🔄 Starting server... (Ctrl+C to stop)"
echo ""

# Start simple HTTP server with IPv6 dual-stack support
exec python3 -m http.server 8091 --bind ::