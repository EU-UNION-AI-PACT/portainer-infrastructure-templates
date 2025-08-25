#!/usr/bin/env python3
"""
Professional Portainer Template Server with IPv4/IPv6 dual-stack support
Serves Portainer templates with proper CORS headers for web integration
"""

import http.server
import socketserver
import json
import os
import sys
import socket
import threading
from pathlib import Path

# Configuration
PORT = 8091
BIND_HOST_V4 = "0.0.0.0"  # IPv4 binding
BIND_HOST_V6 = "::"       # IPv6 binding

class IPv4Server(socketserver.TCPServer):
    """IPv4 TCP Server"""
    address_family = socket.AF_INET
    allow_reuse_address = True

class IPv6Server(socketserver.TCPServer):
    """IPv6 TCP Server with dual-stack support"""
    address_family = socket.AF_INET6
    allow_reuse_address = True
    
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=False)
        try:
            # Allow IPv4 connections on IPv6 socket (dual-stack)
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        except:
            pass  # IPv6 might not be available
        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise

class DualStackTCPServer(socketserver.TCPServer):
    """TCP Server that supports both IPv4 and IPv6"""
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        # Try IPv4 first, then IPv6
        try:
            self.address_family = socketserver.socket.AF_INET
            super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        except Exception as e:
            print(f"IPv4 binding failed: {e}")
            try:
                self.address_family = socketserver.socket.AF_INET6
                super().__init__(server_address, RequestHandlerClass, bind_and_activate)
            except Exception as e2:
                print(f"IPv6 binding also failed: {e2}")
                raise

class PortainerTemplateHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with CORS headers for Portainer compatibility"""
    
    def end_headers(self):
        # Add CORS headers for cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.address_string()}] {format % args}")

def main():
    # Ensure we're in the correct directory and find web folder
    script_dir = Path(__file__).parent.absolute()
    web_dir = script_dir / "web"
    if not web_dir.exists():
        print("❌ Web directory not found!")
        sys.exit(1)
    
    # Check if template file exists
    template_file = web_dir / "portainer-template.json"
    if not template_file.exists():
        print("❌ portainer-template.json not found in web directory!")
        sys.exit(1)
    
    # Validate JSON
    try:
        with open(template_file, 'r') as f:
            data = json.load(f)
            template_count = len(data.get('templates', []))
            print(f"✅ Template validation successful - {template_count} templates found")
    except Exception as e:
        print(f"❌ Template validation failed: {e}")
        sys.exit(1)
    
    # Change to web directory
    os.chdir(str(web_dir))
    
    print(f"🚀 Starting Portainer Template Server...")
    print(f"📂 Serving directory: {web_dir.absolute()}")
    print(f"🌐 IPv4 Server: http://{BIND_HOST_V4}:{PORT}")
    print(f"🌐 IPv6 Server: http://[{BIND_HOST_V6}]:{PORT}")
    print(f"🔗 Template URL: http://localhost:{PORT}/portainer-template.json")
    print(f"📊 Templates available: {template_count}")
    
    servers = []
    threads = []
    
    try:
        # Start IPv4 server
        try:
            ipv4_server = IPv4Server((BIND_HOST_V4, PORT), PortainerTemplateHandler)
            servers.append(ipv4_server)
            ipv4_thread = threading.Thread(target=ipv4_server.serve_forever, daemon=True)
            ipv4_thread.start()
            threads.append(ipv4_thread)
            print(f"✅ IPv4 server started on {BIND_HOST_V4}:{PORT}")
        except Exception as e:
            print(f"⚠️ IPv4 server failed: {e}")
        
        # Start IPv6 server
        try:
            ipv6_server = IPv6Server((BIND_HOST_V6, PORT), PortainerTemplateHandler)
            servers.append(ipv6_server)
            ipv6_thread = threading.Thread(target=ipv6_server.serve_forever, daemon=True)
            ipv6_thread.start()
            threads.append(ipv6_thread)
            print(f"✅ IPv6 server started on [{BIND_HOST_V6}]:{PORT}")
        except Exception as e:
            print(f"⚠️ IPv6 server failed: {e}")
        
        if not servers:
            print("❌ No servers could be started!")
            sys.exit(1)
        
        print(f"✅ Server(s) started successfully on port {PORT}")
        print("🔄 Server is running... (Ctrl+C to stop)")
        
        # Keep main thread alive
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
    
    finally:
        # Clean shutdown
        for server in servers:
            server.shutdown()
            server.server_close()
        sys.exit(1)

if __name__ == "__main__":
    main()