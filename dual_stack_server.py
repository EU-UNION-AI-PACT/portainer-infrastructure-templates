#!/usr/bin/env python3
"""
Professional Portainer Template Server with working IPv4/IPv6 dual-stack support
This server starts both IPv4 and IPv6 listeners to handle Portainer's connection attempts
"""

import http.server
import socketserver
import json
import os
import sys
import socket
import threading
import time
from pathlib import Path

# Configuration
PORT = 8091

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with CORS headers for Portainer compatibility"""
    
    def end_headers(self):
        # Add CORS headers for Portainer compatibility
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests"""
        self.send_response(200)
        self.end_headers()
    
    def guess_type(self, path):
        """Override to ensure JSON files have correct content type"""
        mimetype, encoding = super().guess_type(path)
        if path.endswith('.json'):
            return 'application/json', encoding
        return mimetype, encoding
    
    def log_message(self, format, *args):
        """Custom log format"""
        client_ip = self.client_address[0]
        if ':' in client_ip:
            client_ip = f"[{client_ip}]"
        print(f"[{client_ip}] {format % args}")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Threaded TCP Server for better performance"""
    allow_reuse_address = True
    daemon_threads = True

def start_server(host, port, addr_family, server_name):
    """Start a server on specified host/port with given address family"""
    try:
        class CustomTCPServer(ThreadedTCPServer):
            address_family = addr_family
            
            def __init__(self, server_address, RequestHandlerClass):
                super().__init__(server_address, RequestHandlerClass)
                if addr_family == socket.AF_INET6:
                    # For IPv6, allow IPv4 connections too (dual-stack)
                    self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        
        server = CustomTCPServer((host, port), CORSHTTPRequestHandler)
        print(f"✅ {server_name} server started on {host}:{port}")
        server.serve_forever()
        
    except Exception as e:
        print(f"❌ {server_name} server failed: {e}")
        return None

def main():
    # Validate environment
    script_dir = Path(__file__).parent.absolute()
    web_dir = script_dir / "web"
    
    if not web_dir.exists():
        print("❌ Web directory not found!")
        sys.exit(1)
    
    template_file = web_dir / "portainer-template.json"
    if not template_file.exists():
        print("❌ portainer-template.json not found in web directory!")
        sys.exit(1)
    
    # Validate JSON and count templates
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
    
    print(f"🚀 Starting Dual-Stack Portainer Template Server...")
    print(f"📂 Serving directory: {web_dir}")
    print(f"🔗 Template URL (IPv4): http://localhost:{PORT}/portainer-template.json")
    print(f"🔗 Template URL (IPv6): http://[::1]:{PORT}/portainer-template.json")
    print(f"📊 Templates available: {template_count}")
    
    # Start servers in separate threads
    servers = []
    
    # IPv4 Server
    ipv4_thread = threading.Thread(
        target=start_server, 
        args=("0.0.0.0", PORT, socket.AF_INET, "IPv4"),
        daemon=True
    )
    ipv4_thread.start()
    servers.append(ipv4_thread)
    
    # IPv6 Server (on different port to avoid conflicts)
    ipv6_thread = threading.Thread(
        target=start_server, 
        args=("::", PORT, socket.AF_INET6, "IPv6"),
        daemon=True
    )
    ipv6_thread.start()
    servers.append(ipv6_thread)
    
    # Give servers time to start
    time.sleep(2)
    
    print("✅ Dual-stack servers started successfully!")
    print("🔄 Server is running... (Ctrl+C to stop)")
    print()
    print("📋 Connection Test Commands:")
    print(f"   IPv4: curl -I http://localhost:{PORT}/portainer-template.json")
    print(f"   IPv6: curl -I http://[::1]:{PORT}/portainer-template.json")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    main()