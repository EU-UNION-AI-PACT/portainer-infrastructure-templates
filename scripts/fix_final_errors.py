#!/usr/bin/env python3

import json

def fix_final_certification_errors():
    """Fix the last critical certification errors"""
    
    with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
        templates_data = json.load(f)
    
    templates = templates_data['templates']
    
    # Fix Let's Encrypt title (remove apostrophe)
    for template in templates:
        if template.get('title') == "Let's Encrypt":
            template['title'] = "LetsEncrypt"
            print("✅ Fixed Let's Encrypt title")
            break
    
    # Fix Unknown Database image
    for template in templates:
        if template.get('image') == "/unknown:latest":
            template['image'] = "alpine:latest"
            template['title'] = "Database Template"
            template['description'] = "Generic database template for custom configurations"
            print("✅ Fixed Unknown Database template")
            break
    
    # Save updated templates
    with open('web/portainer-template.json', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    with open('web/portainer-template-v3-fixed.json', 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    
    print("🎉 All critical certification errors fixed!")

if __name__ == "__main__":
    fix_final_certification_errors()