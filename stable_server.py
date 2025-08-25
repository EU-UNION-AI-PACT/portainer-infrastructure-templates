#!/usr/bin/env python3
"""
Stable Portainer Template Server - IPv4/IPv6 Compatible
Robust server that stays running and handles both connection types
"""

import http.server
import socketserver
import json
import socket
import threading
import time
from pathlib import Path

PORT = 8091

class StableHandler(http.server.SimpleHTTPRequestHandler):
    """Stable handler that doesn't crash on requests"""
    
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
    
    def log_message(self, format, *args):
        """Quiet logging to prevent crashes"""
        pass

class StableTCPServer(socketserver.ThreadingTCPServer):
    """Stable TCP server with proper error handling"""
    allow_reuse_address = True
    daemon_threads = True
    
    def __init__(self, server_address, RequestHandlerClass):
        # Try dual-stack IPv6 first (accepts both IPv4 and IPv6)
        try:
            self.address_family = socket.AF_INET6
            super().__init__(server_address, RequestHandlerClass, bind_and_activate=False)
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            self.server_bind()
            self.server_activate()
            print("✅ Dual-stack server (IPv4+IPv6) bound successfully")
        except Exception as e:
            # Fallback to IPv4 only
            try:
                self.server_close()
            except:
                pass
            self.address_family = socket.AF_INET
            super().__init__(server_address, RequestHandlerClass)
            print("✅ IPv4 server bound successfully")

def main():
    # Setup and validation
    web_dir = Path(__file__).parent / "web"
    template_file = web_dir / "portainer-template.json"
    
    if not template_file.exists():
        print("❌ Template file not found!")
        return
    
    with open(template_file) as f:
        data = json.load(f)
        count = len(data.get('templates', []))
        print(f"✅ {count} templates loaded")
    
    import os
    os.chdir(web_dir)
    
    print(f"🚀 Starting Stable Portainer Template Server")
    print(f"🔗 IPv4 URL: http://localhost:{PORT}/portainer-template.json")
    print(f"🔗 IPv6 URL: http://[::1]:{PORT}/portainer-template.json")
    
    try:
        server = StableTCPServer(("", PORT), StableHandler)
        print(f"✅ Server running on port {PORT}")
        print("🔄 Serving requests... (Ctrl+C to stop)")
        
        # Start server in daemon thread so it doesn't block
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        server.shutdown()
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()