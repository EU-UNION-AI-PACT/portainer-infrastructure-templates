#!/usr/bin/env python3
"""
Dedicated JSON-only Portainer Template Server
Only serves JSON content with proper CORS headers
"""

import http.server
import socketserver
import json
import socket
from pathlib import Path

PORT = 8091

class JSONOnlyHandler(http.server.BaseHTTPRequestHandler):
    """Handler that only serves JSON with proper headers"""
    
    def do_GET(self):
        # Only serve the portainer-template.json file
        template_file = Path("portainer-template.json")
        
        if not template_file.exists():
            self.send_error(404, "Template file not found")
            return
        
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Validate JSON
            json.loads(content)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Cache-Control', 'no-cache, must-revalidate')
            self.send_header('Content-Length', str(len(content.encode('utf-8'))))
            self.end_headers()
            
            self.wfile.write(content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error reading template: {e}")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"🔗 [JSON Server] {format % args}")

class DualStackTCPServer(socketserver.TCPServer):
    """TCP Server with IPv4/IPv6 dual-stack support"""
    allow_reuse_address = True
    
    def __init__(self, server_address, RequestHandlerClass):
        # Try IPv6 with dual-stack first
        try:
            self.address_family = socket.AF_INET6
            super().__init__(server_address, RequestHandlerClass, bind_and_activate=False)
            # Enable dual-stack (IPv4 and IPv6)
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            self.server_bind()
            self.server_activate()
            print("✅ Dual-stack server (IPv4+IPv6) bound")
        except Exception as e:
            print(f"IPv6 failed ({e}), falling back to IPv4...")
            try:
                self.server_close()
            except:
                pass
            self.address_family = socket.AF_INET
            super().__init__(server_address, RequestHandlerClass)
            print("✅ IPv4 server bound")

def main():
    # Change to web directory where the template file is
    import os
    web_dir = "/home/holythreekingstreescrowns/Schreibtisch/Portainer Template/web"
    os.chdir(web_dir)
    
    # Validate template file exists and is valid JSON
    template_file = Path("portainer-template.json")
    if not template_file.exists():
        print("❌ portainer-template.json not found!")
        return
    
    try:
        with open(template_file, 'r') as f:
            data = json.load(f)
            template_count = len(data.get('templates', []))
            print(f"✅ {template_count} templates validated")
    except Exception as e:
        print(f"❌ Template validation failed: {e}")
        return
    
    print(f"🚀 Starting JSON-only Portainer Template Server")
    print(f"📂 Serving from: {web_dir}")
    print(f"🔗 Template URL: http://localhost:{PORT}/")
    print(f"🔗 IPv6 URL: http://[::1]:{PORT}/")
    print(f"📊 Templates: {template_count}")
    print("✅ CORS headers enabled for Portainer")
    
    try:
        with DualStackTCPServer(("", PORT), JSONOnlyHandler) as httpd:
            print(f"🔄 Server running on port {PORT}... (Ctrl+C to stop)")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()