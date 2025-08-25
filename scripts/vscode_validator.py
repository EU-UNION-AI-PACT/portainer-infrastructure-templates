#!/usr/bin/env python3
"""
🔍 VS Code Optimized Portainer Template Validator
Complete validation suite for Portainer template collections with VS Code integration.
"""

import json
import os
import sys
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class VSCodePortainerValidator:
    def __init__(self, template_file: str = "web/portainer-template.json"):
        self.template_file = template_file
        self.stacks_dir = "stacks"
        self.errors = []
        self.warnings = []
        self.info = []
        
    def log_error(self, message: str):
        self.errors.append(f"❌ {message}")
        
    def log_warning(self, message: str):
        self.warnings.append(f"⚠️  {message}")
        
    def log_info(self, message: str):
        self.info.append(f"ℹ️  {message}")

    def validate_json_structure(self) -> bool:
        """Validate JSON syntax and basic structure"""
        print("🔍 Validating JSON structure...")
        
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check required top-level fields
            if 'version' not in data:
                self.log_error("Missing 'version' field in template")
                
            if 'templates' not in data:
                self.log_error("Missing 'templates' field")
                return False
                
            if not isinstance(data['templates'], list):
                self.log_error("'templates' must be an array")
                return False
                
            self.log_info(f"JSON structure valid - {len(data['templates'])} templates found")
            return True
            
        except FileNotFoundError:
            self.log_error(f"Template file not found: {self.template_file}")
            return False
        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON syntax: {e}")
            return False

    def validate_docker_compose_stacks(self) -> bool:
        """Validate Docker Compose stack files"""
        print("🔍 Validating Docker Compose stacks...")
        
        if not os.path.exists(self.stacks_dir):
            self.log_warning(f"Stacks directory '{self.stacks_dir}' not found")
            return True
            
        stack_files = list(Path(self.stacks_dir).glob("*.yml")) + list(Path(self.stacks_dir).glob("*.yaml"))
        
        if not stack_files:
            self.log_warning("No stack files found in stacks directory")
            return True
            
        valid_stacks = 0
        for stack_file in stack_files:
            try:
                # Use docker-compose config to validate syntax
                result = subprocess.run(
                    ['docker', 'compose', '-f', str(stack_file), 'config'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    self.log_info(f"Stack '{stack_file.name}': Valid")
                    valid_stacks += 1
                else:
                    self.log_error(f"Stack '{stack_file.name}': Invalid - {result.stderr.strip()}")
                    
            except subprocess.TimeoutExpired:
                self.log_error(f"Stack '{stack_file.name}': Validation timeout")
            except FileNotFoundError:
                self.log_warning("Docker not found - skipping stack validation")
                break
            except Exception as e:
                self.log_error(f"Stack '{stack_file.name}': Validation error - {e}")
                
        if stack_files:
            self.log_info(f"Stack validation completed: {valid_stacks}/{len(stack_files)} valid")
            
        return True

    def test_github_access(self) -> bool:
        """Test access to GitHub raw template file"""
        print("🔍 Testing GitHub raw access...")
        
        github_url = "https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template.json"
        
        try:
            result = subprocess.run(
                ['curl', '-fsSL', '-w', 'HTTP %{http_code} - %{size_download} bytes - %{time_total}s', github_url],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines:
                    self.log_info(f"GitHub access: {lines[-1]}")
                else:
                    self.log_info("GitHub access: Successful")
            else:
                self.log_error(f"GitHub access failed: {result.stderr.strip()}")
                
        except subprocess.TimeoutExpired:
            self.log_error("GitHub access: Timeout")
        except FileNotFoundError:
            self.log_warning("curl not found - skipping GitHub access test")
        except Exception as e:
            self.log_error(f"GitHub access error: {e}")
            
        return True

    def generate_report(self) -> Dict:
        """Generate comprehensive validation report"""
        print("📊 Generating template report...")
        
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            templates = data.get('templates', [])
            
            # Count by type
            type_counts = {1: 0, 2: 0}  # Container, Stack
            for template in templates:
                template_type = template.get('type', 1)
                type_counts[template_type] = type_counts.get(template_type, 0) + 1
                
            # Count One-Click templates
            one_click_count = sum(1 for t in templates if 
                                'One-Click' in t.get('title', '') or 
                                'Pre-configured' in t.get('categories', []))
                                
            report = {
                'timestamp': datetime.now().isoformat(),
                'total_templates': len(templates),
                'container_templates': type_counts.get(1, 0),
                'stack_templates': type_counts.get(2, 0),
                'one_click_templates': one_click_count,
                'validation_errors': len(self.errors),
                'validation_warnings': len(self.warnings),
                'validation_info': len(self.info)
            }
            
            return report
            
        except Exception as e:
            self.log_error(f"Error generating report: {e}")
            return {}

    def run_full_validation(self) -> bool:
        """Run complete validation suite"""
        print("🚀 VS Code Portainer Template Validation Suite")
        print("=" * 70)
        
        # Run all validations
        json_valid = self.validate_json_structure()
        self.validate_docker_compose_stacks()
        self.test_github_access()
        
        # Generate report
        report = self.generate_report()
        
        # Print results
        print("\n📊 VALIDATION REPORT")
        print("=" * 50)
        
        if report:
            print(f"Total Templates: {report['total_templates']}")
            print(f"Container Templates: {report['container_templates']}")
            print(f"Stack Templates: {report['stack_templates']}")
            print(f"One-Click Ready: {report['one_click_templates']}")
                    
        print(f"\n🔍 Validation Results:")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Info: {len(self.info)}")
        
        # Print detailed results
        if self.errors:
            print(f"\n❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")
                
        if self.warnings:
            print(f"\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
                
        if self.info:
            print(f"\n ℹ️ INFO:")
            for info in self.info:
                print(f"  {info}")
                
        # Final status
        print("\n" + "=" * 70)
        if len(self.errors) == 0:
            print("🎉 VALIDATION SUCCESSFUL - Template collection ready!")
            print("💎 Pink Star Diamond Certification: VERIFIED")
            return True
        else:
            print("❌ VALIDATION FAILED - Please fix errors")
            return False

def main():
    """Main entry point"""
    validator = VSCodePortainerValidator()
    success = validator.run_full_validation()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()