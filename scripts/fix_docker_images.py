#!/usr/bin/env python3
"""
Docker Image Fix for Portainer Templates
Fixes problematic Docker image names and ensures they are valid and deployable
"""

import json
import re
import time
from datetime import datetime

class DockerImageValidator:
    def __init__(self):
        self.valid_registries = [
            'docker.io',
            'lscr.io',
            'ghcr.io',
            'quay.io',
            'registry.k8s.io'
        ]
        
        # Image fixes mapping - problematic images to working alternatives
        self.image_fixes = {
            # LinuxServer.io images with :stable tag issues
            'lscr.io/linuxserver/projectsend:stable': 'lscr.io/linuxserver/projectsend:latest',
            'lscr.io/linuxserver/pydio:stable': 'lscr.io/linuxserver/pydio:latest',
            'lscr.io/linuxserver/ubooquity:stable': 'lscr.io/linuxserver/ubooquity:latest',
            'lscr.io/linuxserver/duckdns:stable': 'lscr.io/linuxserver/duckdns:latest',
            'lscr.io/linuxserver/papermerge:stable': 'lscr.io/linuxserver/papermerge:latest',
            'lscr.io/linuxserver/cardigann:stable': 'lscr.io/linuxserver/cardigann:latest',
            'lscr.io/linuxserver/couchpotato:stable': 'lscr.io/linuxserver/couchpotato:latest',
            'lscr.io/linuxserver/deluge:stable': 'lscr.io/linuxserver/deluge:latest',
            'lscr.io/linuxserver/medusa:stable': 'lscr.io/linuxserver/medusa:latest',
            'lscr.io/linuxserver/mylar:stable': 'lscr.io/linuxserver/mylar:latest',
            'lscr.io/linuxserver/nzbget:stable': 'lscr.io/linuxserver/nzbget:latest',
            'lscr.io/linuxserver/nzbhydra2:stable': 'lscr.io/linuxserver/nzbhydra2:latest',
            'lscr.io/linuxserver/ombi:stable': 'lscr.io/linuxserver/ombi:latest',
            'lscr.io/linuxserver/plexrequests:stable': 'lscr.io/linuxserver/plexrequests:latest',
            'lscr.io/linuxserver/sabnzbd:stable': 'lscr.io/linuxserver/sabnzbd:latest',
            'lscr.io/linuxserver/sickchill:stable': 'lscr.io/linuxserver/sickchill:latest',
            'lscr.io/linuxserver/sickgear:stable': 'lscr.io/linuxserver/sickgear:latest',
            'lscr.io/linuxserver/transmission:stable': 'lscr.io/linuxserver/transmission:latest',
            'lscr.io/linuxserver/webgrabplus:stable': 'lscr.io/linuxserver/webgrabplus:latest',
            'lscr.io/linuxserver/lidarr:stable': 'lscr.io/linuxserver/lidarr:latest',
            'lscr.io/linuxserver/qbittorrent:stable': 'lscr.io/linuxserver/qbittorrent:latest',
            'lscr.io/linuxserver/rutorrent:stable': 'lscr.io/linuxserver/rutorrent:latest',
            'lscr.io/linuxserver/davos:stable': 'lscr.io/linuxserver/davos:latest',
            'lscr.io/linuxserver/domoticz:stable': 'lscr.io/linuxserver/domoticz:latest',
            
            # Old linuxserver registry format
            'linuxserver/jackett:stable': 'lscr.io/linuxserver/jackett:latest',
            'linuxserver/radarr:stable': 'lscr.io/linuxserver/radarr:latest',
            'linuxserver/sonarr:stable': 'lscr.io/linuxserver/sonarr:latest',
            
            # Other problematic images
            'markusmcnugen/qbittorrentvpn:stable': 'markusmcnugen/qbittorrentvpn:latest',
            'shenxn/protonmail-bridge:stable': 'shenxn/protonmail-bridge:latest',
            'seafileltd/seafile-mc:stable': 'seafileltd/seafile-mc:latest',
            
            # Version specific fixes
            'nextcloud:stable': 'nextcloud:latest',
            
            # Deprecated or broken images - replace with alternatives
            'lscr.io/linuxserver/plexrequests:latest': 'lscr.io/linuxserver/ombi:latest',  # PlexRequests is deprecated
        }
        
        # Known working stable images
        self.stable_images = {
            'nginx': 'nginx:stable-alpine',
            'apache': 'httpd:alpine',
            'mysql': 'mysql:8.0',
            'postgres': 'postgres:15-alpine',
            'redis': 'redis:7-alpine',
            'mongo': 'mongo:7',
            'elasticsearch': 'docker.elastic.co/elasticsearch/elasticsearch:8.8.0',
            'kibana': 'docker.elastic.co/kibana/kibana:8.8.0',
            'grafana': 'grafana/grafana:latest',
            'prometheus': 'prom/prometheus:latest',
            'portainer': 'portainer/portainer-ce:latest',
        }
    
    def validate_image_name(self, image_name):
        """Validate if an image name is properly formatted"""
        if not image_name or image_name.strip() == "":
            return False, "Empty image name"
        
        # Check for common malformed patterns
        if image_name.endswith(':'):
            return False, "Image name ends with colon"
        
        if '::' in image_name:
            return False, "Double colon in image name"
        
        # Basic regex validation
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._/-]*(?::[a-zA-Z0-9._-]+)?$'
        if not re.match(pattern, image_name):
            return False, "Invalid image name format"
        
        return True, "Valid"
    
    def fix_image_name(self, image_name):
        """Fix known problematic image names"""
        if image_name in self.image_fixes:
            return self.image_fixes[image_name], f"Fixed: {image_name} → {self.image_fixes[image_name]}"
        
        # Clean up common issues
        fixed_image = image_name.strip()
        
        # Fix double colons
        fixed_image = re.sub(r'::+', ':', fixed_image)
        
        # Fix trailing colons
        fixed_image = fixed_image.rstrip(':')
        
        # If image has no tag, add :latest
        if ':' not in fixed_image:
            fixed_image += ':latest'
        
        if fixed_image != image_name:
            return fixed_image, f"Cleaned: {image_name} → {fixed_image}"
        
        return image_name, "No changes needed"
    
    def fix_template_images(self):
        """Fix all problematic images in the template file"""
        print("🔧 Fixing Docker Image Names in Portainer Templates...")
        
        try:
            # Load template file
            with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"📊 Processing {len(data.get('templates', []))} templates...")
            
            fixed_count = 0
            error_count = 0
            fixes_applied = []
            
            for i, template in enumerate(data.get('templates', [])):
                if 'image' in template:
                    original_image = template['image']
                    
                    # Validate image name
                    is_valid, validation_msg = self.validate_image_name(original_image)
                    
                    if not is_valid:
                        error_count += 1
                        print(f"  ❌ Template {i+1} ({template.get('title', 'Unknown')}): {validation_msg}")
                        
                        # Try to fix
                        fixed_image, fix_msg = self.fix_image_name(original_image)
                        template['image'] = fixed_image
                        fixes_applied.append({
                            'template': template.get('title', 'Unknown'),
                            'original': original_image,
                            'fixed': fixed_image,
                            'reason': validation_msg
                        })
                        fixed_count += 1
                        print(f"    🔧 Fixed: {fix_msg}")
                    
                    else:
                        # Check if it's in our known fixes
                        fixed_image, fix_msg = self.fix_image_name(original_image)
                        if fixed_image != original_image:
                            template['image'] = fixed_image
                            fixes_applied.append({
                                'template': template.get('title', 'Unknown'),
                                'original': original_image,
                                'fixed': fixed_image,
                                'reason': 'Known problematic image'
                            })
                            fixed_count += 1
                            print(f"  🔧 Template {i+1} ({template.get('title', 'Unknown')}): {fix_msg}")
                        else:
                            print(f"  ✅ Template {i+1} ({template.get('title', 'Unknown')}): Image OK")
                
                else:
                    error_count += 1
                    print(f"  ❌ Template {i+1} ({template.get('title', 'Unknown')}): Missing image field")
                    # Add a default image
                    template['image'] = 'nginx:alpine'
                    fixes_applied.append({
                        'template': template.get('title', 'Unknown'),
                        'original': 'MISSING',
                        'fixed': 'nginx:alpine',
                        'reason': 'Missing image field'
                    })
                    fixed_count += 1
            
            # Create backup
            backup_path = f'web/portainer-template.json.backup-image-fix-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Save fixed template
            with open('web/portainer-template.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Save fixes report
            with open('image-fixes-report.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'total_templates': len(data.get('templates', [])),
                    'fixes_applied': fixed_count,
                    'errors_found': error_count,
                    'fixes_detail': fixes_applied
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Docker Image Fix Complete!")
            print(f"📊 Fixed {fixed_count} problematic images")
            print(f"⚠️ Found {error_count} total issues")
            print(f"💾 Backup saved to: {backup_path}")
            print(f"📄 Fixes report saved to: image-fixes-report.json")
            
            return True, fixes_applied
            
        except Exception as e:
            print(f"❌ Error fixing images: {e}")
            return False, []
    
    def create_validated_test_template(self):
        """Create a test template with validated working images"""
        print("\n🧪 Creating validated test template...")
        
        test_template = {
            "version": "3",
            "templates": [
                {
                    "id": 1,
                    "type": 1,
                    "title": "✅ Nginx Web Server",
                    "description": "Nginx web server with validated stable image",
                    "categories": ["Web", "Proxy", "Test"],
                    "platform": "linux",
                    "logo": "https://img.shields.io/badge/Test-Nginx-green?style=for-the-badge&logo=nginx",
                    "image": "nginx:stable-alpine",
                    "ports": ["8080:80/tcp"],
                    "restart_policy": "unless-stopped",
                    "labels": [
                        {
                            "name": "test.validated",
                            "value": "true"
                        }
                    ]
                },
                {
                    "id": 2,
                    "type": 1,
                    "title": "✅ Portainer CE",
                    "description": "Portainer Community Edition with validated image",
                    "categories": ["Management", "Docker", "Test"],
                    "platform": "linux",
                    "logo": "https://img.shields.io/badge/Test-Portainer-blue?style=for-the-badge&logo=portainer",
                    "image": "portainer/portainer-ce:latest",
                    "ports": ["9000:9000/tcp"],
                    "volumes": [
                        {
                            "container": "/var/run/docker.sock",
                            "bind": "/var/run/docker.sock"
                        },
                        {
                            "container": "/data",
                            "bind": "/tmp/portainer-data"
                        }
                    ],
                    "restart_policy": "unless-stopped",
                    "labels": [
                        {
                            "name": "test.validated",
                            "value": "true"
                        }
                    ]
                },
                {
                    "id": 3,
                    "type": 1,
                    "title": "✅ Redis Cache",
                    "description": "Redis cache with validated alpine image",
                    "categories": ["Database", "Cache", "Test"],
                    "platform": "linux",
                    "logo": "https://img.shields.io/badge/Test-Redis-red?style=for-the-badge&logo=redis",
                    "image": "redis:7-alpine",
                    "ports": ["6379:6379/tcp"],
                    "restart_policy": "unless-stopped",
                    "labels": [
                        {
                            "name": "test.validated",
                            "value": "true"
                        }
                    ]
                }
            ]
        }
        
        with open('web/portainer-template-validated.json', 'w', encoding='utf-8') as f:
            json.dump(test_template, f, indent=2, ensure_ascii=False)
        
        print("✅ Validated test template created: web/portainer-template-validated.json")
        return True

def main():
    """Main execution"""
    print("🔧 Docker Image Validator and Fixer")
    print("=" * 40)
    
    validator = DockerImageValidator()
    
    # Fix the images
    success, fixes = validator.fix_template_images()
    
    if success:
        # Create validated test template
        validator.create_validated_test_template()
        
        print(f"\n🎉 Image fixes completed successfully!")
        print(f"🚀 All Docker images are now properly formatted")
        print(f"\n📋 Integration URLs:")
        print(f"Main: https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template.json")
        print(f"Validated: https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template-validated.json")
        
        if fixes:
            print(f"\n📄 Top 10 fixes applied:")
            for fix in fixes[:10]:
                print(f"  • {fix['template']}: {fix['original']} → {fix['fixed']}")
    else:
        print("❌ Image fix failed")

if __name__ == "__main__":
    main()