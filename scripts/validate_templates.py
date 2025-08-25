#!/usr/bin/env python3
"""
Portainer Template Validator

Validates template files for format compliance, missing fields, and best practices.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from urllib.parse import urlparse
import re
import argparse

class TemplateValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
        # Required fields for a valid template
        self.required_fields = ['name', 'image']
        self.recommended_fields = ['title', 'description', 'categories', 'logo']
        
        # Valid platform values
        self.valid_platforms = ['linux', 'windows']
        
        # Valid restart policies
        self.valid_restart_policies = ['no', 'on-failure', 'always', 'unless-stopped']
    
    def validate_url(self, url: str) -> bool:
        """Validate if URL is properly formatted."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def validate_port_format(self, port: str) -> bool:
        """Validate port format (e.g., '8080:80/tcp')."""
        port_pattern = r'^\d+:\d+(/tcp|/udp)?$|^\d+(/tcp|/udp)?$'
        return bool(re.match(port_pattern, str(port)))
    
    def validate_template_structure(self, template: Dict, template_index: int = 0) -> List[Dict]:
        """Validate a single template's structure and content."""
        issues = []
        
        # Check required fields
        for field in self.required_fields:
            if field not in template or not template[field]:
                issues.append({
                    'type': 'error',
                    'field': field,
                    'message': f"Required field '{field}' is missing or empty",
                    'template_index': template_index
                })
        
        # Check recommended fields
        for field in self.recommended_fields:
            if field not in template or not template[field]:
                issues.append({
                    'type': 'warning',
                    'field': field,
                    'message': f"Recommended field '{field}' is missing or empty",
                    'template_index': template_index
                })
        
        # Validate specific fields
        
        # Name validation
        if 'name' in template:
            name = template['name']
            if not isinstance(name, str) or len(name.strip()) == 0:
                issues.append({
                    'type': 'error',
                    'field': 'name',
                    'message': "Name must be a non-empty string",
                    'template_index': template_index
                })
            elif len(name) > 100:
                issues.append({
                    'type': 'warning',
                    'field': 'name',
                    'message': "Name is very long (>100 characters)",
                    'template_index': template_index
                })
        
        # Image validation
        if 'image' in template:
            image = template['image']
            if not isinstance(image, str) or len(image.strip()) == 0:
                issues.append({
                    'type': 'error',
                    'field': 'image',
                    'message': "Image must be a non-empty string",
                    'template_index': template_index
                })
            elif ':' not in image:
                issues.append({
                    'type': 'warning',
                    'field': 'image',
                    'message': "Image should specify a tag (e.g., 'nginx:latest')",
                    'template_index': template_index
                })
        
        # Platform validation
        if 'platform' in template:
            platform = template['platform']
            if platform not in self.valid_platforms:
                issues.append({
                    'type': 'warning',
                    'field': 'platform',
                    'message': f"Platform '{platform}' not in recommended values: {self.valid_platforms}",
                    'template_index': template_index
                })
        
        # Restart policy validation
        if 'restart_policy' in template:
            restart_policy = template['restart_policy']
            if restart_policy not in self.valid_restart_policies:
                issues.append({
                    'type': 'warning',
                    'field': 'restart_policy',
                    'message': f"Restart policy '{restart_policy}' not in valid values: {self.valid_restart_policies}",
                    'template_index': template_index
                })
        
        # Categories validation
        if 'categories' in template:
            categories = template['categories']
            if not isinstance(categories, list):
                issues.append({
                    'type': 'error',
                    'field': 'categories',
                    'message': "Categories must be a list",
                    'template_index': template_index
                })
            elif len(categories) == 0:
                issues.append({
                    'type': 'warning',
                    'field': 'categories',
                    'message': "Template should have at least one category",
                    'template_index': template_index
                })
        
        # Ports validation
        if 'ports' in template:
            ports = template['ports']
            if not isinstance(ports, list):
                issues.append({
                    'type': 'error',
                    'field': 'ports',
                    'message': "Ports must be a list",
                    'template_index': template_index
                })
            else:
                for i, port in enumerate(ports):
                    if not self.validate_port_format(port):
                        issues.append({
                            'type': 'warning',
                            'field': 'ports',
                            'message': f"Port '{port}' at index {i} has invalid format",
                            'template_index': template_index
                        })
        
        # Environment variables validation
        if 'env' in template:
            env = template['env']
            if not isinstance(env, list):
                issues.append({
                    'type': 'error',
                    'field': 'env',
                    'message': "Environment variables must be a list",
                    'template_index': template_index
                })
            else:
                for i, env_var in enumerate(env):
                    if not isinstance(env_var, dict):
                        issues.append({
                            'type': 'error',
                            'field': 'env',
                            'message': f"Environment variable at index {i} must be an object",
                            'template_index': template_index
                        })
                    elif 'name' not in env_var:
                        issues.append({
                            'type': 'error',
                            'field': 'env',
                            'message': f"Environment variable at index {i} missing 'name' field",
                            'template_index': template_index
                        })
        
        # Logo URL validation
        if 'logo' in template and template['logo']:
            logo = template['logo']
            if not self.validate_url(logo):
                issues.append({
                    'type': 'warning',
                    'field': 'logo',
                    'message': "Logo URL appears to be invalid",
                    'template_index': template_index
                })
        
        # Description length check
        if 'description' in template and template['description']:
            description = template['description']
            if len(description) > 1000:
                issues.append({
                    'type': 'warning',
                    'field': 'description',
                    'message': "Description is very long (>1000 characters)",
                    'template_index': template_index
                })
        
        return issues
    
    def validate_template_file(self, file_path: Path) -> Dict:
        """Validate a single template file."""
        validation_result = {
            'file': str(file_path),
            'status': 'unknown',
            'issues': [],
            'template_count': 0,
            'error': None
        }
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Extract templates from different formats
            templates = []
            if 'templates' in data:
                templates = data['templates']
            elif isinstance(data, list):
                templates = data
            else:
                templates = [data]
            
            validation_result['template_count'] = len(templates)
            
            # Validate each template
            all_issues = []
            for i, template in enumerate(templates):
                if isinstance(template, dict):
                    template_issues = self.validate_template_structure(template, i)
                    all_issues.extend(template_issues)
                else:
                    all_issues.append({
                        'type': 'error',
                        'field': 'structure',
                        'message': f"Template at index {i} is not a valid object",
                        'template_index': i
                    })
            
            validation_result['issues'] = all_issues
            
            # Determine overall status
            has_errors = any(issue['type'] == 'error' for issue in all_issues)
            has_warnings = any(issue['type'] == 'warning' for issue in all_issues)
            
            if has_errors:
                validation_result['status'] = 'error'
            elif has_warnings:
                validation_result['status'] = 'warning'
            else:
                validation_result['status'] = 'valid'
        
        except json.JSONDecodeError as e:
            validation_result['status'] = 'error'
            validation_result['error'] = f"Invalid JSON: {e}"
        except Exception as e:
            validation_result['status'] = 'error'
            validation_result['error'] = f"Validation error: {e}"
        
        return validation_result
    
    def validate_all_templates(self, templates_dir: str = "templates/individual") -> Dict:
        """Validate all template files in a directory."""
        templates_path = Path(templates_dir)
        
        if not templates_path.exists():
            return {
                'status': 'error',
                'error': f"Templates directory not found: {templates_dir}",
                'results': []
            }
        
        results = []
        total_templates = 0
        total_errors = 0
        total_warnings = 0
        
        print(f"🔍 Validating templates in {templates_dir}...")
        
        for file_path in templates_path.glob("*.json"):
            print(f"  Validating {file_path.name}...")
            result = self.validate_template_file(file_path)
            results.append(result)
            
            total_templates += result['template_count']
            
            errors = len([i for i in result['issues'] if i['type'] == 'error'])
            warnings = len([i for i in result['issues'] if i['type'] == 'warning'])
            
            total_errors += errors
            total_warnings += warnings
            
            # Print summary for this file
            if result['status'] == 'error':
                print(f"    ❌ {errors} errors")
            elif result['status'] == 'warning':
                print(f"    ⚠️  {warnings} warnings")
            else:
                print(f"    ✅ Valid")
        
        summary = {
            'total_files': len(results),
            'total_templates': total_templates,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'files_with_errors': len([r for r in results if r['status'] == 'error']),
            'files_with_warnings': len([r for r in results if r['status'] == 'warning']),
            'valid_files': len([r for r in results if r['status'] == 'valid'])
        }
        
        return {
            'status': 'complete',
            'summary': summary,
            'results': results
        }
    
    def save_validation_report(self, validation_results: Dict, output_path: str = "reports/validation_report.json") -> None:
        """Save validation results to a file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_file, 'w') as f:
                json.dump(validation_results, f, indent=2)
            print(f"📄 Validation report saved to {output_file}")
        except Exception as e:
            print(f"❌ Failed to save validation report: {e}")
    
    def print_validation_summary(self, validation_results: Dict) -> None:
        """Print a human-readable validation summary."""
        if validation_results['status'] != 'complete':
            print(f"❌ Validation failed: {validation_results.get('error', 'Unknown error')}")
            return
        
        summary = validation_results['summary']
        
        print("\n📊 Validation Summary:")
        print(f"  Total files: {summary['total_files']}")
        print(f"  Total templates: {summary['total_templates']}")
        print(f"  Valid files: {summary['valid_files']}")
        print(f"  Files with warnings: {summary['files_with_warnings']}")
        print(f"  Files with errors: {summary['files_with_errors']}")
        print(f"  Total errors: {summary['total_errors']}")
        print(f"  Total warnings: {summary['total_warnings']}")
        
        if summary['files_with_errors'] > 0:
            print("\n❌ Files with errors:")
            for result in validation_results['results']:
                if result['status'] == 'error':
                    print(f"  - {Path(result['file']).name}: {result.get('error', 'Template validation errors')}")
        
        if summary['files_with_warnings'] > 0:
            print("\n⚠️  Files with warnings:")
            for result in validation_results['results']:
                if result['status'] == 'warning':
                    warning_count = len([i for i in result['issues'] if i['type'] == 'warning'])
                    print(f"  - {Path(result['file']).name}: {warning_count} warnings")

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Validate Portainer template files')
    parser.add_argument('--input', '-i', default='templates/individual',
                       help='Directory containing template files to validate')
    parser.add_argument('--output', '-o', default='reports/validation_report.json',
                       help='Output file for validation report')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed validation issues')
    
    args = parser.parse_args()
    
    validator = TemplateValidator()
    results = validator.validate_all_templates(args.input)
    
    # Print summary
    validator.print_validation_summary(results)
    
    # Show detailed issues if verbose
    if args.verbose and results['status'] == 'complete':
        print("\n🔍 Detailed Issues:")
        for result in results['results']:
            if result['issues']:
                print(f"\n📄 {Path(result['file']).name}:")
                for issue in result['issues']:
                    icon = "❌" if issue['type'] == 'error' else "⚠️"
                    print(f"  {icon} Template {issue['template_index']}: {issue['message']} (field: {issue['field']})")
    
    # Save report
    validator.save_validation_report(results, args.output)

if __name__ == "__main__":
    main()