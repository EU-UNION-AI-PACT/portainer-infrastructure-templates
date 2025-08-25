#!/usr/bin/env python3

import json

def final_fixes():
    # Read the template file
    with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
        templates_data = json.load(f)
    
    templates = templates_data['templates']
    
    # Fix remaining templates
    for i, template in enumerate(templates):
        title = template.get('title', '')
        
        # Fix specific templates
        if i == 106 and '🆓 Kostenlose Security Alternativen' in title:
            template['image'] = 'alpine:latest'  # Compose stack
            template['note'] = 'Docker Compose stack with multiple security services'
        elif i == 107 and '🔧 Extended Security Tools' in title:
            template['image'] = 'alpine:latest'  # Compose stack
            template['note'] = 'Docker Compose stack with extended security tools'
        elif title == 'Pritunl':
            template['image'] = 'pritunl/pritunl:latest'
        elif title == 'Bookstack':
            template['image'] = 'lscr.io/linuxserver/bookstack:latest'
    
    # Write updated version
    with open('web/portainer-template.json', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    # Also update the fixed version
    with open('web/portainer-template-v3-fixed.json', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Final fixes applied!")

if __name__ == "__main__":
    final_fixes()