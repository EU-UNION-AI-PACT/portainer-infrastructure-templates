#!/usr/bin/env python3
"""
Portainer Template Certification Validator
Validates templates against official Portainer standards for certification
"""

import json
import sys
import re
from urllib.parse import urlparse
from collections import defaultdict

class PortainerCertificationValidator:
    def __init__(self, template_file):
        self.template_file = template_file
        self.templates_data = None
        self.validation_results = {
            'total_templates': 0,
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'errors': [],
            'warnings_list': [],
            'certification_score': 0
        }
    
    def load_templates(self):
        """Load and parse template file"""
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                self.templates_data = json.load(f)
            return True
        except Exception as e:
            print(f"❌ Failed to load template file: {e}")
            return False
    
    def validate_portainer_format(self, template, index):
        """Validate against Portainer v3 specification"""
        errors = []
        warnings = []
        
        # Required fields for Portainer certification
        required_fields = {
            'type': int,
            'title': str,
            'description': str,
            'platform': str,
            'image': str
        }
        
        for field, expected_type in required_fields.items():
            if field not in template:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(template[field], expected_type):
                errors.append(f"Field '{field}' must be of type {expected_type.__name__}")
            elif not template[field]:
                errors.append(f"Field '{field}' cannot be empty")
        
        # Validate type values
        if 'type' in template and template['type'] not in [1, 2, 3]:
            errors.append(f"Invalid type: {template['type']} (must be 1, 2, or 3)")
        
        # Validate platform values
        if 'platform' in template and template['platform'] not in ['linux', 'windows']:
            errors.append(f"Invalid platform: {template['platform']} (must be 'linux' or 'windows')")
        
        # Validate title format
        if 'title' in template and template['title']:
            title = template['title']
            if len(title) > 100:
                warnings.append(f"Title too long: {len(title)} chars (recommended: < 100)")
            if any(char in title for char in ['<', '>', '&', '"', "'"]):
                errors.append(f"Title contains invalid characters: {title}")
        
        # Validate description
        if 'description' in template and template['description']:
            desc = template['description']
            if len(desc) < 10:
                warnings.append(f"Description too short: {len(desc)} chars (recommended: > 20)")
            elif len(desc) > 1000:
                warnings.append(f"Description too long: {len(desc)} chars (recommended: < 500)")
        
        # Validate image format
        if 'image' in template and template['image']:
            image = template['image']
            # More permissive image validation
            if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9._/-]*[a-zA-Z0-9])?(:[a-zA-Z0-9._-]+)?$', image):
                errors.append(f"Invalid image format: {image}")
            if image.endswith(':latest'):
                warnings.append(f"Using ':latest' tag not recommended: {image}")
        
        # Validate ports format
        if 'ports' in template and template['ports']:
            for i, port in enumerate(template['ports']):
                if not isinstance(port, str):
                    errors.append(f"Port {i} must be string, got {type(port)}")
                elif not re.match(r'^\d+:\d+(/tcp|/udp)?$', port):
                    errors.append(f"Invalid port format: {port}")
        
        # Validate environment variables
        if 'env' in template and template['env']:
            for i, env_var in enumerate(template['env']):
                if not isinstance(env_var, dict):
                    errors.append(f"Environment variable {i} must be object")
                else:
                    if 'name' not in env_var:
                        errors.append(f"Environment variable {i} missing 'name' field")
                    if 'label' not in env_var:
                        warnings.append(f"Environment variable {i} missing 'label' field")
        
        # Validate volumes
        if 'volumes' in template and template['volumes']:
            for i, volume in enumerate(template['volumes']):
                if not isinstance(volume, dict):
                    errors.append(f"Volume {i} must be object")
                else:
                    if 'container' not in volume:
                        errors.append(f"Volume {i} missing 'container' field")
        
        # Validate categories
        if 'categories' in template:
            if not isinstance(template['categories'], list):
                errors.append("Categories must be array")
            elif len(template['categories']) == 0:
                warnings.append("No categories specified")
            elif len(template['categories']) > 5:
                warnings.append(f"Too many categories: {len(template['categories'])} (recommended: < 5)")
        
        return errors, warnings
    
    def validate_security_standards(self, template):
        """Validate security best practices"""
        warnings = []
        
        # Check for security-sensitive configurations
        if 'env' in template:
            for env_var in template['env']:
                if isinstance(env_var, dict) and 'name' in env_var:
                    name = env_var['name'].lower()
                    if any(keyword in name for keyword in ['password', 'secret', 'key', 'token']):
                        if 'default' in env_var and env_var['default']:
                            warnings.append(f"Security sensitive variable '{env_var['name']}' has default value")
        
        # Check for privileged mode
        if template.get('privileged'):
            warnings.append("Template uses privileged mode - security risk")
        
        # Check for host network mode
        if template.get('network_mode') == 'host':
            warnings.append("Template uses host networking - potential security risk")
        
        return warnings
    
    def validate_community_standards(self, template):
        """Validate community and best practice standards"""
        warnings = []
        
        # Check for proper restart policy
        if 'restart_policy' not in template:
            warnings.append("No restart policy specified (recommended: 'unless-stopped')")
        elif template['restart_policy'] not in ['no', 'always', 'unless-stopped', 'on-failure']:
            warnings.append(f"Invalid restart policy: {template['restart_policy']}")
        
        # Check for logo
        if 'logo' not in template:
            warnings.append("No logo specified")
        elif template['logo'] and not template['logo'].startswith('http'):
            warnings.append("Logo should be HTTPS URL")
        
        # Check for proper documentation
        if 'note' in template and len(template['note']) > 500:
            warnings.append("Note field too long (recommended: < 200 chars)")
        
        return warnings
    
    def calculate_certification_score(self):
        """Calculate overall certification score"""
        total = self.validation_results['total_templates']
        if total == 0:
            return 0
        
        # Base score from passed templates
        base_score = (self.validation_results['passed'] / total) * 70
        
        # Bonus points for quality
        warning_penalty = min(self.validation_results['warnings'] * 0.1, 20)
        error_penalty = min(len(self.validation_results['errors']) * 2, 50)
        
        # Bonus for comprehensive collection
        if total >= 200:
            bonus = 15
        elif total >= 100:
            bonus = 10
        elif total >= 50:
            bonus = 5
        else:
            bonus = 0
        
        final_score = max(0, base_score - warning_penalty - error_penalty + bonus)
        return min(100, final_score)
    
    def validate_all_templates(self):
        """Validate all templates"""
        if not self.templates_data or 'templates' not in self.templates_data:
            return False
        
        templates = self.templates_data['templates']
        self.validation_results['total_templates'] = len(templates)
        
        for i, template in enumerate(templates):
            # Portainer format validation
            format_errors, format_warnings = self.validate_portainer_format(template, i)
            
            # Security validation
            security_warnings = self.validate_security_standards(template)
            
            # Community standards validation
            community_warnings = self.validate_community_standards(template)
            
            # Combine results
            all_errors = format_errors
            all_warnings = format_warnings + security_warnings + community_warnings
            
            if all_errors:
                self.validation_results['failed'] += 1
                self.validation_results['errors'].extend([
                    f"Template {i} ({template.get('title', 'Unknown')}): {error}"
                    for error in all_errors
                ])
            else:
                self.validation_results['passed'] += 1
            
            if all_warnings:
                self.validation_results['warnings'] += len(all_warnings)
                self.validation_results['warnings_list'].extend([
                    f"Template {i} ({template.get('title', 'Unknown')}): {warning}"
                    for warning in all_warnings
                ])
        
        # Calculate certification score
        self.validation_results['certification_score'] = self.calculate_certification_score()
        
        return True
    
    def generate_certification_report(self):
        """Generate detailed certification report"""
        print("🏆 PORTAINER TEMPLATE CERTIFICATION REPORT")
        print("=" * 80)
        print()
        
        # Overview
        results = self.validation_results
        print(f"📊 VALIDATION OVERVIEW:")
        print(f"   Total Templates: {results['total_templates']}")
        print(f"   ✅ Passed: {results['passed']}")
        print(f"   ❌ Failed: {results['failed']}")
        print(f"   ⚠️  Warnings: {results['warnings']}")
        print(f"   🎯 Certification Score: {results['certification_score']:.1f}/100")
        print()
        
        # Certification level
        score = results['certification_score']
        if score >= 95:
            level = "🏆 PLATINUM CERTIFICATION"
            color = "EXCELLENT"
        elif score >= 85:
            level = "🥇 GOLD CERTIFICATION"
            color = "VERY GOOD"
        elif score >= 75:
            level = "🥈 SILVER CERTIFICATION"
            color = "GOOD"
        elif score >= 65:
            level = "🥉 BRONZE CERTIFICATION"
            color = "ACCEPTABLE"
        else:
            level = "❌ CERTIFICATION FAILED"
            color = "NEEDS IMPROVEMENT"
        
        print(f"🎖️  CERTIFICATION LEVEL: {level}")
        print(f"📈 QUALITY RATING: {color}")
        print()
        
        # Detailed results
        if results['errors']:
            print("❌ CRITICAL ERRORS (Must be fixed for certification):")
            for error in results['errors'][:10]:  # Show first 10
                print(f"   • {error}")
            if len(results['errors']) > 10:
                print(f"   ... and {len(results['errors']) - 10} more errors")
            print()
        
        if results['warnings_list']:
            print("⚠️  WARNINGS (Recommendations for improvement):")
            for warning in results['warnings_list'][:10]:  # Show first 10
                print(f"   • {warning}")
            if len(results['warnings_list']) > 10:
                print(f"   ... and {len(results['warnings_list']) - 10} more warnings")
            print()
        
        # Recommendations
        print("💡 CERTIFICATION RECOMMENDATIONS:")
        if results['failed'] > 0:
            print("   🔧 Fix all critical errors before submitting for certification")
        if results['warnings'] > 50:
            print("   📝 Address warnings to improve certification score")
        if score < 85:
            print("   🎯 Aim for 85+ score for gold certification level")
        
        print("   ✅ Add comprehensive documentation")
        print("   ✅ Include security best practices")
        print("   ✅ Provide community support channels")
        print("   ✅ Implement automated testing")
        print()
        
        # Final assessment
        print("🎯 FINAL CERTIFICATION ASSESSMENT:")
        print("=" * 80)
        if score >= 85 and results['failed'] == 0:
            print("🎉 READY FOR PORTAINER CERTIFICATION!")
            print("   This template collection meets all requirements for official certification.")
            print("   Recommended actions:")
            print("   1. Submit to Portainer template repository")
            print("   2. Engage with Portainer community")
            print("   3. Request official review")
        elif results['failed'] == 0:
            print("✅ CERTIFICATION ELIGIBLE with minor improvements")
            print("   Address warnings to achieve higher certification level.")
        else:
            print("⚠️  CERTIFICATION BLOCKED - Critical errors must be resolved")
            print("   Fix all errors before resubmitting for certification.")
        
        return score >= 75 and results['failed'] == 0

def main():
    if len(sys.argv) > 1:
        template_file = sys.argv[1]
    else:
        template_file = 'web/portainer-template.json'
    
    validator = PortainerCertificationValidator(template_file)
    
    if not validator.load_templates():
        sys.exit(1)
    
    if not validator.validate_all_templates():
        print("❌ Validation failed")
        sys.exit(1)
    
    certification_ready = validator.generate_certification_report()
    
    sys.exit(0 if certification_ready else 1)

if __name__ == "__main__":
    main()