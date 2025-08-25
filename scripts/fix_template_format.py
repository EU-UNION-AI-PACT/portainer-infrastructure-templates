#!/usr/bin/env python3

import json
import sys

def fix_ports_format(template):
    """Convert ports from object format to string array format"""
    if 'ports' in template and template['ports']:
        new_ports = []
        for port in template['ports']:
            if isinstance(port, dict):
                # Convert {"WebUI": "9090:9090/tcp"} to "9090:9090/tcp"
                for key, value in port.items():
                    new_ports.append(value)
            elif isinstance(port, str):
                # Already correct format
                new_ports.append(port)
        template['ports'] = new_ports
    return template

def fix_template_format(templates_data):
    """Fix all templates to ensure proper Portainer v3 format"""
    if 'templates' in templates_data:
        for i, template in enumerate(templates_data['templates']):
            # Fix ports format
            templates_data['templates'][i] = fix_ports_format(template)
            
            # Ensure required fields are present
            if 'platform' not in template:
                templates_data['templates'][i]['platform'] = 'linux'
            
            # Ensure type is correct
            if 'type' not in template:
                templates_data['templates'][i]['type'] = 1  # Container type
            
            # Fix any malformed environment variables
            if 'env' in template and template['env']:
                env_fixed = []
                for env_var in template['env']:
                    if isinstance(env_var, dict) and all(key in env_var for key in ['name', 'label']):
                        env_fixed.append(env_var)
                    else:
                        print(f"Warning: Skipping malformed env var in {template.get('title', 'Unknown')}: {env_var}")
                templates_data['templates'][i]['env'] = env_fixed
    
    return templates_data

def main():
    # Read the template file
    with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
        templates_data = json.load(f)
    
    print(f"Original templates: {len(templates_data.get('templates', []))}")
    
    # Fix the format
    fixed_data = fix_template_format(templates_data)
    
    # Create backup
    with open('web/portainer-template.json.backup3', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    # Write fixed version
    with open('web/portainer-template.json', 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=2, ensure_ascii=False)
    
    print(f"Fixed templates: {len(fixed_data.get('templates', []))}")
    print("✅ Template format fixed!")
    print("📄 Backup created: web/portainer-template.json.backup3")

if __name__ == "__main__":
    main()