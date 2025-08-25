#!/usr/bin/env python3
"""
Portainer Template JSON Format Fixer
Fixes the labels format issue that causes Go unmarshal errors in Portainer
"""

import json
import os
from datetime import datetime

def fix_labels_format():
    """Fix labels format from object to array of pairs"""
    
    print("🔧 Fixing Portainer Template JSON Format Issues...")
    
    try:
        # Load current template
        with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Processing {len(data.get('templates', []))} templates...")
        
        fixed_count = 0
        
        # Process each template
        for i, template in enumerate(data.get('templates', [])):
            if 'labels' in template:
                labels = template['labels']
                
                # Check if labels is a dict (object) instead of array
                if isinstance(labels, dict):
                    # Convert dict to array of key-value pairs
                    labels_array = []
                    for key, value in labels.items():
                        labels_array.append({
                            "name": key,
                            "value": str(value)
                        })
                    
                    template['labels'] = labels_array
                    fixed_count += 1
                    
                    print(f"  ✅ Fixed template {i+1}: {template.get('title', 'Unknown')}")
            
            # Remove non-standard fields that might cause issues
            non_standard_fields = ['cosmic_enhancement', 'note']
            for field in non_standard_fields:
                if field in template:
                    del template[field]
                    print(f"  🗑️ Removed non-standard field '{field}' from {template.get('title', 'Unknown')}")
        
        # Remove metadata section if it exists (not part of Portainer v3 spec)
        if 'metadata' in data:
            del data['metadata']
            print("🗑️ Removed metadata section (not part of Portainer v3 spec)")
        
        # Create backup
        backup_path = f'web/portainer-template.json.backup-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Save fixed template
        with open('web/portainer-template.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ JSON Format Fix Complete!")
        print(f"📊 Fixed {fixed_count} templates with label format issues")
        print(f"💾 Backup saved to: {backup_path}")
        print(f"🎯 Template should now work correctly with Portainer")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing template format: {e}")
        return False

def validate_json_structure():
    """Validate that the JSON structure is correct for Portainer"""
    
    print("\n🔍 Validating JSON structure...")
    
    try:
        with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check required fields
        if 'version' not in data:
            print("❌ Missing 'version' field")
            return False
        
        if 'templates' not in data:
            print("❌ Missing 'templates' field")
            return False
        
        if not isinstance(data['templates'], list):
            print("❌ 'templates' must be an array")
            return False
        
        # Check each template structure
        for i, template in enumerate(data['templates']):
            required_fields = ['type', 'title', 'description', 'categories', 'platform', 'image']
            
            for field in required_fields:
                if field not in template:
                    print(f"❌ Template {i+1} missing required field: {field}")
                    return False
            
            # Check labels format
            if 'labels' in template:
                labels = template['labels']
                if not isinstance(labels, list):
                    print(f"❌ Template {i+1} has incorrect labels format (should be array)")
                    return False
                
                for label in labels:
                    if not isinstance(label, dict) or 'name' not in label or 'value' not in label:
                        print(f"❌ Template {i+1} has invalid label structure")
                        return False
        
        print("✅ JSON structure is valid for Portainer v3")
        return True
        
    except Exception as e:
        print(f"❌ JSON validation error: {e}")
        return False

def create_simplified_template():
    """Create a simplified version for testing"""
    
    print("\n🧪 Creating simplified test template...")
    
    try:
        simplified_template = {
            "version": "3",
            "templates": [
                {
                    "type": 1,
                    "title": "Test Template - Nginx",
                    "description": "Simple nginx test template to verify Portainer compatibility",
                    "categories": ["Web", "Test"],
                    "platform": "linux",
                    "logo": "https://img.shields.io/badge/Test-Nginx-green?style=for-the-badge&logo=nginx",
                    "image": "nginx:alpine",
                    "ports": ["8080:80/tcp"],
                    "env": [
                        {
                            "name": "TEST_VAR",
                            "label": "Test Variable",
                            "default": "test",
                            "description": "Test environment variable"
                        }
                    ],
                    "restart_policy": "unless-stopped",
                    "labels": [
                        {
                            "name": "test.template",
                            "value": "true"
                        },
                        {
                            "name": "version",
                            "value": "1.0"
                        }
                    ]
                }
            ]
        }
        
        with open('web/portainer-template-test.json', 'w', encoding='utf-8') as f:
            json.dump(simplified_template, f, indent=2, ensure_ascii=False)
        
        print("✅ Test template created: web/portainer-template-test.json")
        return True
        
    except Exception as e:
        print(f"❌ Error creating test template: {e}")
        return False

def main():
    """Main execution"""
    print("🔧 Portainer Template JSON Format Fixer")
    print("=" * 50)
    
    # Fix the main template
    if fix_labels_format():
        # Validate the fixed template
        if validate_json_structure():
            # Create test template
            create_simplified_template()
            
            print(f"\n🎉 All fixes completed successfully!")
            print(f"🚀 Your template should now work with Portainer")
            print(f"\n📋 Integration Steps:")
            print(f"1. Use this URL in Portainer:")
            print(f"   https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template.json")
            print(f"2. Or test with the simplified version first:")
            print(f"   https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template-test.json")
        else:
            print("❌ Template validation failed")
    else:
        print("❌ Template fix failed")

if __name__ == "__main__":
    main()