#!/usr/bin/env python3
"""
Portainer Template ID Fix
Fixes the id field issue that causes Go unmarshal errors in Portainer
Converts string IDs to integer IDs as expected by Portainer
"""

import json
import os
import re
from datetime import datetime

def fix_template_ids():
    """Fix template ID format from string to integer"""
    
    print("🔧 Fixing Portainer Template ID Format Issues...")
    
    try:
        # Load current template
        with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Processing {len(data.get('templates', []))} templates...")
        
        fixed_count = 0
        removed_count = 0
        
        # Process each template
        for i, template in enumerate(data.get('templates', [])):
            # Check if template has string ID
            if 'id' in template:
                current_id = template['id']
                
                # If it's a string ID, convert to integer or remove
                if isinstance(current_id, str):
                    # Try to extract number from string ID
                    match = re.search(r'(\d+)', current_id)
                    if match:
                        # Convert to integer
                        template['id'] = int(match.group(1))
                        fixed_count += 1
                        print(f"  ✅ Fixed ID for template {i+1}: '{current_id}' → {template['id']}")
                    else:
                        # Remove invalid ID
                        del template['id']
                        removed_count += 1
                        print(f"  🗑️ Removed invalid ID for template {i+1}: '{current_id}'")
                
                # Ensure ID is unique
                elif isinstance(current_id, int):
                    # ID is already integer, just log
                    print(f"  ✅ Template {i+1} already has integer ID: {current_id}")
            
            # If no ID exists, add sequential integer ID
            if 'id' not in template:
                template['id'] = i + 1
                print(f"  ➕ Added ID for template {i+1}: {template['id']}")
                fixed_count += 1
        
        # Ensure all IDs are unique
        used_ids = set()
        for i, template in enumerate(data.get('templates', [])):
            original_id = template.get('id', i + 1)
            
            # If ID is already used, find next available
            if original_id in used_ids:
                new_id = max(used_ids) + 1 if used_ids else 1
                template['id'] = new_id
                print(f"  🔄 Changed duplicate ID for template {i+1}: {original_id} → {new_id}")
            
            used_ids.add(template['id'])
        
        # Create backup
        backup_path = f'web/portainer-template.json.backup-id-fix-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Save fixed template
        with open('web/portainer-template.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ ID Format Fix Complete!")
        print(f"📊 Fixed {fixed_count} template IDs")
        print(f"🗑️ Removed {removed_count} invalid IDs")
        print(f"💾 Backup saved to: {backup_path}")
        print(f"🎯 All template IDs are now integers as required by Portainer")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing template IDs: {e}")
        return False

def validate_template_ids():
    """Validate that all template IDs are integers"""
    
    print("\n🔍 Validating Template IDs...")
    
    try:
        with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check each template ID
        errors = []
        for i, template in enumerate(data.get('templates', [])):
            if 'id' in template:
                template_id = template['id']
                
                # Check if ID is integer
                if not isinstance(template_id, int):
                    errors.append(f"Template {i+1}: ID '{template_id}' is not an integer")
                
                # Check if ID is positive
                elif template_id <= 0:
                    errors.append(f"Template {i+1}: ID {template_id} is not positive")
            else:
                errors.append(f"Template {i+1}: Missing ID field")
        
        if errors:
            print("❌ ID validation errors found:")
            for error in errors:
                print(f"  • {error}")
            return False
        else:
            print("✅ All template IDs are valid integers")
            return True
        
    except Exception as e:
        print(f"❌ ID validation error: {e}")
        return False

def check_id_uniqueness():
    """Check that all template IDs are unique"""
    
    print("\n🔍 Checking ID Uniqueness...")
    
    try:
        with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        ids = []
        for template in data.get('templates', []):
            if 'id' in template:
                ids.append(template['id'])
        
        # Check for duplicates
        unique_ids = set(ids)
        if len(ids) == len(unique_ids):
            print(f"✅ All {len(ids)} template IDs are unique")
            return True
        else:
            duplicates = [id for id in ids if ids.count(id) > 1]
            print(f"❌ Found duplicate IDs: {set(duplicates)}")
            return False
        
    except Exception as e:
        print(f"❌ ID uniqueness check error: {e}")
        return False

def create_test_template_with_ids():
    """Create a test template with proper integer IDs"""
    
    print("\n🧪 Creating test template with integer IDs...")
    
    try:
        test_template = {
            "version": "3",
            "templates": [
                {
                    "id": 1,
                    "type": 1,
                    "title": "Test Template - Nginx",
                    "description": "Simple nginx test template with integer ID",
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
                },
                {
                    "id": 2,
                    "type": 1,
                    "title": "Test Template - Apache",
                    "description": "Simple apache test template with integer ID",
                    "categories": ["Web", "Test"],
                    "platform": "linux",
                    "logo": "https://img.shields.io/badge/Test-Apache-red?style=for-the-badge&logo=apache",
                    "image": "httpd:alpine",
                    "ports": ["8081:80/tcp"],
                    "restart_policy": "unless-stopped",
                    "labels": [
                        {
                            "name": "test.template",
                            "value": "true"
                        },
                        {
                            "name": "version",
                            "value": "2.0"
                        }
                    ]
                }
            ]
        }
        
        with open('web/portainer-template-id-test.json', 'w', encoding='utf-8') as f:
            json.dump(test_template, f, indent=2, ensure_ascii=False)
        
        print("✅ Test template with integer IDs created: web/portainer-template-id-test.json")
        return True
        
    except Exception as e:
        print(f"❌ Error creating test template: {e}")
        return False

def main():
    """Main execution"""
    print("🔧 Portainer Template ID Format Fixer")
    print("=" * 45)
    
    # Fix the template IDs
    if fix_template_ids():
        # Validate the fixed IDs
        if validate_template_ids() and check_id_uniqueness():
            # Create test template
            create_test_template_with_ids()
            
            print(f"\n🎉 All ID fixes completed successfully!")
            print(f"🚀 Template IDs are now properly formatted for Portainer")
            print(f"\n📋 Integration URLs:")
            print(f"Main: https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template.json")
            print(f"Test: https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template-id-test.json")
        else:
            print("❌ ID validation failed")
    else:
        print("❌ ID fix failed")

if __name__ == "__main__":
    main()