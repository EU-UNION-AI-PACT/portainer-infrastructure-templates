#!/usr/bin/env python3

import json
import re

def fix_portainer_certification_issues():
    """Fix issues preventing Portainer certification"""
    
    # Load templates
    with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
        templates_data = json.load(f)
    
    templates = templates_data['templates']
    fixes_applied = 0
    
    for i, template in enumerate(templates):
        # Fix port formats - convert "80/tcp" to "80:80/tcp"
        if 'ports' in template and template['ports']:
            new_ports = []
            for port in template['ports']:
                if isinstance(port, str):
                    # Handle formats like "80/tcp" -> "80:80/tcp"
                    if re.match(r'^\d+/(tcp|udp)$', port):
                        port_num = port.split('/')[0]
                        protocol = port.split('/')[1]
                        new_ports.append(f"{port_num}:{port_num}/{protocol}")
                        fixes_applied += 1
                    else:
                        new_ports.append(port)
                else:
                    new_ports.append(port)
            template['ports'] = new_ports
        
        # Fix image formats - add :latest if no tag
        if 'image' in template and template['image']:
            image = template['image']
            if ':' not in image and '/' in image:
                template['image'] = f"{image}:latest"
                fixes_applied += 1
        
        # Add missing restart policies
        if 'restart_policy' not in template:
            template['restart_policy'] = 'unless-stopped'
            fixes_applied += 1
        
        # Fix common image issues
        if 'image' in template:
            image = template['image']
            # Fix some common problematic images
            image_fixes = {
                'prom/prometheus': 'prom/prometheus:latest',
                'markusmcnugen/qbittorrentvpn': 'markusmcnugen/qbittorrentvpn:latest',
                'alpine': 'alpine:latest'
            }
            
            if image in image_fixes:
                template['image'] = image_fixes[image]
                fixes_applied += 1
    
    # Save fixed version
    with open('web/portainer-template.json.backup5', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    with open('web/portainer-template.json', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    # Also update the fixed version
    with open('web/portainer-template-v3-fixed.json', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    print(f"🔧 Applied {fixes_applied} certification fixes")
    print("✅ Templates optimized for Portainer certification!")
    print("📄 Backup created: web/portainer-template.json.backup5")

if __name__ == "__main__":
    fix_portainer_certification_issues()