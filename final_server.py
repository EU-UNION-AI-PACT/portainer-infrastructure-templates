#!/usr/bin/env python3
"""
Final Portainer Template Server - With CORS Headers
This server will work with Portainer's CORS requirements
"""

import http.server
import socketserver
from http.server import SimpleHTTPRequestHandler
import os
import socket

PORT = 8091

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()

    def guess_type(self, path):
        if path.endswith('.json'):
            return 'application/json', None
        return super().guess_type(path)

class DualStackTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        # Try IPv6 dual-stack first
        try:
            self.address_family = socket.AF_INET6
            socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=False)
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            self.allow_reuse_address = True
            self.server_bind()
            self.server_activate()
            print("✅ Dual-stack IPv6 server (accepts IPv4+IPv6)")
        except Exception as e:
            print(f"IPv6 failed ({e}), trying IPv4...")
            try:
                self.server_close()
            except:
                pass
            self.address_family = socket.AF_INET
            socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
            print("✅ IPv4 server started")

def main():
    os.chdir('/home/holythreekingstreescrowns/Schreibtisch/Portainer Template/web')
    
    print(f"🚀 Starting Final Portainer Template Server")
    print(f"📂 Serving from: {os.getcwd()}")
    
    try:
        with DualStackTCPServer(("", PORT), CORSRequestHandler) as httpd:
            print(f"🔗 IPv4 URL: http://localhost:{PORT}/portainer-template.json")
            print(f"🔗 IPv6 URL: http://[::1]:{PORT}/portainer-template.json")
            print("✅ CORS headers enabled for Portainer compatibility")
            print("🔄 Server running... (Ctrl+C to stop)")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()