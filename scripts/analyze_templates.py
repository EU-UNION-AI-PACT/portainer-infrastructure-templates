#!/usr/bin/env python3

import json
import sys
import re
from collections import defaultdict

def validate_template(template, index):
    """Validate a single template and return list of issues"""
    issues = []
    warnings = []
    
    # Required fields
    required_fields = ['type', 'title', 'description', 'platform', 'image']
    for field in required_fields:
        if field not in template:
            issues.append(f"Missing required field: {field}")
        elif not template[field]:
            issues.append(f"Empty required field: {field}")
    
    # Validate type
    if 'type' in template and template['type'] not in [1, 2, 3]:
        issues.append(f"Invalid type: {template['type']} (should be 1, 2, or 3)")
    
    # Validate platform
    if 'platform' in template and template['platform'] not in ['linux', 'windows']:
        warnings.append(f"Unusual platform: {template['platform']}")
    
    # Validate ports format
    if 'ports' in template and template['ports']:
        for i, port in enumerate(template['ports']):
            if isinstance(port, dict):
                issues.append(f"Port {i} is object format (should be string): {port}")
            elif isinstance(port, str):
                # Check if port format is valid
                if not re.match(r'^\d+:\d+(/tcp|/udp)?$', port):
                    warnings.append(f"Unusual port format: {port}")
            else:
                issues.append(f"Port {i} has invalid type: {type(port)}")
    
    # Validate environment variables
    if 'env' in template and template['env']:
        for i, env_var in enumerate(template['env']):
            if not isinstance(env_var, dict):
                issues.append(f"Env var {i} is not an object")
            else:
                if 'name' not in env_var:
                    issues.append(f"Env var {i} missing 'name' field")
                if 'label' not in env_var:
                    warnings.append(f"Env var {i} missing 'label' field")
    
    # Validate volumes
    if 'volumes' in template and template['volumes']:
        for i, volume in enumerate(template['volumes']):
            if not isinstance(volume, dict):
                issues.append(f"Volume {i} is not an object")
            else:
                if 'container' not in volume:
                    issues.append(f"Volume {i} missing 'container' field")
    
    # Validate image format
    if 'image' in template:
        image = template['image']
        if ':' not in image:
            warnings.append(f"Image missing tag: {image}")
        elif image.endswith(':'):
            issues.append(f"Image has empty tag: {image}")
    
    # Check for common issues
    if 'title' in template and template['title']:
        title = template['title']
        if len(title) > 100:
            warnings.append(f"Title very long ({len(title)} chars)")
        if not title[0].isupper():
            warnings.append(f"Title should start with capital letter: {title}")
    
    if 'description' in template and template['description']:
        desc = template['description']
        if len(desc) < 20:
            warnings.append(f"Description very short ({len(desc)} chars)")
        elif len(desc) > 500:
            warnings.append(f"Description very long ({len(desc)} chars)")
    
    return issues, warnings

def analyze_templates(file_path):
    """Analyze all templates in the file"""
    print(f"🔍 ANALYZING TEMPLATES: {file_path}")
    print("="*80)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON PARSE ERROR: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ FILE NOT FOUND: {file_path}")
        return False
    
    if 'templates' not in data:
        print("❌ NO 'templates' FIELD FOUND")
        return False
    
    templates = data['templates']
    total_templates = len(templates)
    
    print(f"📊 TOTAL TEMPLATES: {total_templates}")
    print(f"📄 FILE VERSION: {data.get('version', 'Unknown')}")
    print()
    
    # Statistics
    stats = {
        'valid': 0,
        'warnings': 0,
        'errors': 0,
        'categories': defaultdict(int),
        'platforms': defaultdict(int),
        'types': defaultdict(int)
    }
    
    error_templates = []
    warning_templates = []
    
    # Analyze each template
    for i, template in enumerate(templates):
        issues, warnings = validate_template(template, i)
        
        # Collect statistics
        if 'categories' in template:
            for cat in template['categories']:
                stats['categories'][cat] += 1
        
        if 'platform' in template:
            stats['platforms'][template['platform']] += 1
        
        if 'type' in template:
            stats['types'][template['type']] += 1
        
        # Categorize template status
        if issues:
            stats['errors'] += 1
            error_templates.append({
                'index': i,
                'title': template.get('title', f'Template {i}'),
                'issues': issues,
                'warnings': warnings
            })
        elif warnings:
            stats['warnings'] += 1
            warning_templates.append({
                'index': i,
                'title': template.get('title', f'Template {i}'),
                'warnings': warnings
            })
        else:
            stats['valid'] += 1
    
    # Print results
    print("🎯 VALIDATION RESULTS:")
    print("="*80)
    print(f"✅ VALID TEMPLATES: {stats['valid']}")
    print(f"⚠️  TEMPLATES WITH WARNINGS: {stats['warnings']}")
    print(f"❌ TEMPLATES WITH ERRORS: {stats['errors']}")
    print()
    
    # Platform distribution
    print("🖥️  PLATFORM DISTRIBUTION:")
    for platform, count in stats['platforms'].items():
        percentage = (count / total_templates) * 100
        print(f"   {platform}: {count} ({percentage:.1f}%)")
    print()
    
    # Type distribution
    print("📦 TYPE DISTRIBUTION:")
    type_names = {1: "Container", 2: "Swarm", 3: "Compose"}
    for type_id, count in stats['types'].items():
        type_name = type_names.get(type_id, f"Unknown({type_id})")
        percentage = (count / total_templates) * 100
        print(f"   {type_name}: {count} ({percentage:.1f}%)")
    print()
    
    # Top categories
    print("🏷️  TOP CATEGORIES:")
    sorted_cats = sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True)
    for cat, count in sorted_cats[:10]:
        print(f"   {cat}: {count}")
    print()
    
    # Show errors
    if error_templates:
        print("❌ TEMPLATES WITH ERRORS:")
        print("="*80)
        for template in error_templates[:10]:  # Show first 10
            print(f"🔸 #{template['index']} - {template['title']}")
            for issue in template['issues']:
                print(f"   ❌ {issue}")
            for warning in template['warnings']:
                print(f"   ⚠️  {warning}")
            print()
        
        if len(error_templates) > 10:
            print(f"... and {len(error_templates) - 10} more templates with errors")
    
    # Show warnings (if no errors)
    elif warning_templates:
        print("⚠️  TEMPLATES WITH WARNINGS:")
        print("="*80)
        for template in warning_templates[:10]:  # Show first 10
            print(f"🔸 #{template['index']} - {template['title']}")
            for warning in template['warnings']:
                print(f"   ⚠️  {warning}")
            print()
        
        if len(warning_templates) > 10:
            print(f"... and {len(warning_templates) - 10} more templates with warnings")
    
    # Final assessment
    print("🏆 FINAL ASSESSMENT:")
    print("="*80)
    if stats['errors'] == 0:
        if stats['warnings'] == 0:
            print("🎉 PERFECT! All templates are valid and ready for production!")
        else:
            print(f"✅ GOOD! All templates are functional. {stats['warnings']} have minor warnings.")
        print("🚀 READY FOR PORTAINER DEPLOYMENT!")
    else:
        print(f"⚠️  NEEDS ATTENTION: {stats['errors']} templates have critical errors.")
        print("🔧 Fix errors before production deployment.")
    
    return stats['errors'] == 0

if __name__ == "__main__":
    success = analyze_templates('web/portainer-template.json')
    sys.exit(0 if success else 1)