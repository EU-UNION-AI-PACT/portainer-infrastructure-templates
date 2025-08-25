#!/usr/bin/env python3
"""
Portainer Template Server - IPv4/IPv6 Compatible
Simple server that works with both IPv4 and IPv6 connections
"""

import http.server
import socketserver
import json
import socket
from pathlib import Path

PORT = 8091

class PortainerHandler(http.server.SimpleHTTPRequestHandler):
    """Handler with CORS headers for Portainer"""
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def guess_type(self, path):
        if path.endswith('.json'):
            return 'application/json', None
        return super().guess_type(path)

class DualStackServer(socketserver.TCPServer):
    """Server that accepts both IPv4 and IPv6 connections"""
    
    def __init__(self, server_address, RequestHandlerClass):
        # Try IPv6 with dual-stack first (accepts both IPv4 and IPv6)
        try:
            self.address_family = socket.AF_INET6
            super().__init__(server_address, RequestHandlerClass, bind_and_activate=False)
            # Enable dual-stack (IPv4 and IPv6)
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            self.allow_reuse_address = True
            self.server_bind()
            self.server_activate()
            print("✅ Dual-stack server (IPv4+IPv6) started")
        except Exception as e:
            print(f"IPv6 dual-stack failed: {e}, falling back to IPv4...")
            # Fallback to IPv4 only
            self.server_close()
            self.address_family = socket.AF_INET
            super().__init__(server_address, RequestHandlerClass)
            print("✅ IPv4 server started")

def main():
    # Validate setup
    web_dir = Path(__file__).parent / "web"
    template_file = web_dir / "portainer-template.json"
    
    if not template_file.exists():
        print("❌ Template file not found!")
        return
    
    # Validate JSON
    with open(template_file) as f:
        data = json.load(f)
        count = len(data.get('templates', []))
        print(f"✅ {count} templates loaded")
    
    # Change to web directory
    import os
    os.chdir(web_dir)
    
    print(f"🚀 Starting Portainer Template Server on port {PORT}")
    print(f"🔗 URL: http://localhost:{PORT}/portainer-template.json")
    
    try:
        with DualStackServer(("", PORT), PortainerHandler) as server:
            print("🔄 Server running... (Ctrl+C to stop)")
            server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()