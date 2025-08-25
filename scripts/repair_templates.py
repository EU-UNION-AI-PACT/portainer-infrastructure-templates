#!/usr/bin/env python3

import json
import sys

def fix_template_errors(templates_data):
    """Fix critical errors in templates"""
    templates = templates_data['templates']
    fixes_applied = 0
    
    for i, template in enumerate(templates):
        original_template = template.copy()
        
        # Fix missing or empty descriptions
        if 'description' not in template or not template['description']:
            title = template.get('title', 'Unknown')
            
            # Default descriptions based on title patterns
            descriptions = {
                'SyncThing': 'Syncthing is a continuous file synchronization program. It synchronizes files between two or more computers in real time, safely protected from prying eyes.',
                'SmokePing': 'SmokePing is a deluxe latency measurement tool. It can measure, store and display latency, latency distribution and packet loss.',
                'UniFi Controller': 'The UniFi Controller software is a powerful, enterprise wireless software engine ideal for high-density client deployments requiring low latency and high uptime performance.',
                'Headphones': 'Automated music downloader for NZB and Torrent, written in Python. It supports SABnzbd, NZBget, Transmission, μTorrent, Deluge and Blackhole.',
            }
            
            if title in descriptions:
                template['description'] = descriptions[title]
                fixes_applied += 1
            elif 'Stack' in title:
                template['description'] = f'{title} - Complete infrastructure deployment with Docker Compose for easy container orchestration.'
                fixes_applied += 1
            else:
                template['description'] = f'{title} - Self-hosted application for Docker deployment.'
                fixes_applied += 1
        
        # Fix missing images for stacks
        if 'image' not in template or not template['image']:
            title = template.get('title', 'Unknown')
            
            # Default images
            images = {
                'Invoice Ninja': 'invoiceninja/invoiceninja:latest',
                'Nextcloud': 'nextcloud:latest',
                'Seafile': 'seafileltd/seafile-mc:latest',
                'Monitoring-Only Stack': 'alpine:latest',  # Dummy image for compose stack
                'Complete Security Infrastructure Stack': 'alpine:latest',  # Dummy image for compose stack
                'Security-Only Stack': 'alpine:latest',  # Dummy image for compose stack
            }
            
            if title in images:
                template['image'] = images[title]
                fixes_applied += 1
            elif 'Stack' in title:
                # For compose stacks, we use a dummy image
                template['image'] = 'alpine:latest'
                template['note'] = 'This is a Docker Compose stack. The image field is required but not used.'
                fixes_applied += 1
        
        # Fix port formats
        if 'ports' in template and template['ports']:
            for j, port in enumerate(template['ports']):
                if isinstance(port, str) and port.endswith('/tcp') and ':' in port:
                    # Fix format like "80/tcp" to "80:80/tcp"
                    if not port.split('/')[0].count(':'):
                        port_num = port.split('/')[0]
                        protocol = port.split('/')[1] if '/' in port else 'tcp'
                        template['ports'][j] = f"{port_num}:{port_num}/{protocol}"
                        fixes_applied += 1
        
        # Ensure type is set
        if 'type' not in template:
            template['type'] = 1  # Default to container
            fixes_applied += 1
        
        # Ensure platform is set
        if 'platform' not in template:
            template['platform'] = 'linux'
            fixes_applied += 1
    
    return fixes_applied

def main():
    # Read the template file
    with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
        templates_data = json.load(f)
    
    print(f"📊 Original templates: {len(templates_data.get('templates', []))}")
    
    # Apply fixes
    fixes = fix_template_errors(templates_data)
    
    # Create backup
    with open('web/portainer-template.json.backup4', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    # Write fixed version
    with open('web/portainer-template.json', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    # Also update the fixed version
    with open('web/portainer-template-v3-fixed.json', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    print(f"🔧 Applied {fixes} fixes")
    print("✅ Templates repaired!")
    print("📄 Backup created: web/portainer-template.json.backup4")

if __name__ == "__main__":
    main()