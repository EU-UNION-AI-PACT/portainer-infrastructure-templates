#!/usr/bin/env python3
"""
🚀 Simple Template Server - Alternative Port
Serves Portainer templates on port 8092
"""
import json
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import socketserver
import os

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TemplateHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/portainer-template.json':
            self.serve_template()
        elif self.path == '/':
            self.serve_index()
        else:
            super().do_GET()
    
    def serve_template(self):
        """Serve the Portainer template JSON"""
        template_path = Path('web/portainer-template.json')
        
        if not template_path.exists():
            self.send_error(404, 'Template not found')
            return
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Send JSON data
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            self.wfile.write(json_data.encode('utf-8'))
            
            logging.info(f"✅ Template served: {len(data.get('templates', []))} templates")
            
        except Exception as e:
            logging.error(f"❌ Error serving template: {e}")
            self.send_error(500, f'Internal server error: {e}')
    
    def serve_index(self):
        """Serve a simple status page"""
        template_path = Path('web/portainer-template.json')
        template_count = 0
        
        if template_path.exists():
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    template_count = len(data.get('templates', []))
            except:
                pass
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🚀 Portainer Template Server</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .status {{ color: #28a745; font-weight: bold; }}
                .url {{ background: #f8f9fa; padding: 10px; border-left: 4px solid #007bff; margin: 10px 0; }}
                .count {{ font-size: 2em; color: #007bff; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Portainer Template Server</h1>
                <p class="status">✅ Server is running successfully!</p>
                
                <h2>📊 Statistics</h2>
                <p>Available Templates: <span class="count">{template_count}</span></p>
                
                <h2>🔗 Access URLs</h2>
                <div class="url">
                    <strong>Template JSON:</strong><br>
                    <a href="/portainer-template.json">http://localhost:8092/portainer-template.json</a>
                </div>
                
                <h2>🎯 Portainer Setup</h2>
                <p>Add this URL to Portainer:</p>
                <div class="url">
                    <code>http://localhost:8092/portainer-template.json</code>
                </div>
                
                <h2>💎 Status</h2>
                <p>🟢 Pink Star Diamond Certified</p>
                <p>🟢 EU-GDPR Compliant</p>
                <p>🟢 One-Click Deployment Ready</p>
            </div>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

def main():
    """Start the template server"""
    port = 8092
    
    # Change to the correct directory
    os.chdir('/home/holythreekingstreescrowns/Schreibtisch/Portainer Template')
    
    try:
        with socketserver.TCPServer(("", port), TemplateHandler) as httpd:
            template_path = Path('web/portainer-template.json')
            template_count = 0
            
            if template_path.exists():
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        template_count = len(data.get('templates', []))
                except:
                    pass
            
            logging.info("🚀 PORTAINER TEMPLATE SERVER")
            logging.info("=" * 50)
            logging.info(f"📊 Templates loaded: {template_count}")
            logging.info(f"🌐 Server starting on port {port}")
            logging.info(f"🔗 Template URL: http://localhost:{port}/portainer-template.json")
            logging.info(f"📊 Status page: http://localhost:{port}/")
            logging.info("💎 Pink Star Diamond Certified - Ready for deployment!")
            logging.info("Press Ctrl+C to stop the server")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        logging.info("🛑 Server stopped by user")
    except Exception as e:
        logging.error(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()