#!/usr/bin/env python3
"""
Portainer Template Manager - Main Orchestration Script

This script provides a unified interface to manage Portainer templates:
- Fetch templates from all configured sources
- Merge and deduplicate templates
- Validate template integrity
- Generate comprehensive reports
"""

import sys
import argparse
import asyncio
from pathlib import Path

# Add scripts directory to Python path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.append(str(scripts_dir))

try:
    from fetch_templates import TemplateFetcher
    from merge_templates import TemplateMerger
    from generate_report import TemplateReporter
    from validate_templates import TemplateValidator
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all script files are in the scripts directory.")
    sys.exit(1)

class PortainerTemplateManager:
    def __init__(self):
        self.fetcher = TemplateFetcher()
        self.merger = TemplateMerger()
        self.reporter = TemplateReporter()
        self.validator = TemplateValidator()
    
    async def full_update(self, validate: bool = True, sources: list = None):
        """Perform a complete template update cycle."""
        print("🚀 Starting full Portainer template update...")
        
        # Step 1: Fetch templates
        print("\n📥 Step 1: Fetching templates from sources...")
        await self.fetcher.run(sources)
        
        # Step 2: Validate templates (optional)
        if validate:
            print("\n🔍 Step 2: Validating templates...")
            validation_results = self.validator.validate_all_templates()
            self.validator.print_validation_summary(validation_results)
            
            # Check if there are critical errors
            if validation_results.get('summary', {}).get('files_with_errors', 0) > 0:
                print("⚠️  Warning: Some templates have validation errors. Continuing anyway...")
        
        # Step 3: Merge templates
        print("\n🔄 Step 3: Merging and deduplicating templates...")
        merged_data = self.merger.merge_templates()
        if merged_data:
            self.merger.save_merged_templates(merged_data)
        else:
            print("❌ No templates to merge!")
            return False
        
        # Step 4: Generate reports
        print("\n📊 Step 4: Generating reports...")
        self.reporter.save_reports()
        
        print("\n✅ Full update completed successfully!")
        return True
    
    async def fetch_only(self, sources: list = None):
        """Fetch templates only."""
        print("📥 Fetching templates from sources...")
        await self.fetcher.run(sources)
    
    def merge_only(self, categories: list = None):
        """Merge templates only."""
        print("🔄 Merging templates...")
        merged_data = self.merger.merge_templates(categories)
        if merged_data:
            self.merger.save_merged_templates(merged_data)
            return True
        return False
    
    def validate_only(self, verbose: bool = False):
        """Validate templates only."""
        print("🔍 Validating templates...")
        validation_results = self.validator.validate_all_templates()
        self.validator.print_validation_summary(validation_results)
        
        if verbose:
            # Show detailed issues
            print("\n🔍 Detailed Issues:")
            for result in validation_results.get('results', []):
                if result.get('issues'):
                    print(f"\n📄 {Path(result['file']).name}:")
                    for issue in result['issues']:
                        icon = "❌" if issue['type'] == 'error' else "⚠️"
                        print(f"  {icon} Template {issue['template_index']}: {issue['message']} (field: {issue['field']})")
        
        return validation_results
    
    def report_only(self):
        """Generate reports only."""
        print("📊 Generating reports...")
        self.reporter.save_reports()
    
    def list_sources(self):
        """List all configured template sources."""
        sources = self.fetcher.get_active_sources()
        
        print(f"📋 Configured template sources ({len(sources)}):\n")
        
        for source in sources:
            print(f"🔗 {source.name}")
            print(f"   URL: {source.url}")
            print(f"   Category: {source.category}")
            print(f"   Description: {source.description}")
            print()
    
    def get_status(self):
        """Get current status of templates."""
        # Check if files exist
        individual_dir = Path("templates/individual")
        merged_dir = Path("templates/merged")
        reports_dir = Path("reports")
        
        status = {
            'individual_templates': 0,
            'merged_template_exists': False,
            'reports_exist': False,
            'last_update': 'Unknown'
        }
        
        # Count individual templates
        if individual_dir.exists():
            status['individual_templates'] = len(list(individual_dir.glob("*.json")))
        
        # Check merged template
        master_file = merged_dir / "master_templates.json"
        if master_file.exists():
            status['merged_template_exists'] = True
            status['last_update'] = master_file.stat().st_mtime
        
        # Check reports
        if reports_dir.exists() and any(reports_dir.glob("*.json")):
            status['reports_exist'] = True
        
        print("📊 Current Status:")
        print(f"   Individual templates: {status['individual_templates']} files")
        print(f"   Merged template: {'✅' if status['merged_template_exists'] else '❌'}")
        print(f"   Reports: {'✅' if status['reports_exist'] else '❌'}")
        
        return status

async def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='Portainer Template Manager - Orchestrate your template collection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s update                    # Full update cycle
  %(prog)s fetch --sources lissy93   # Fetch from specific source
  %(prog)s merge --categories media  # Merge only media templates
  %(prog)s validate --verbose        # Validate with detailed output
  %(prog)s report                    # Generate reports only
  %(prog)s status                    # Show current status
  %(prog)s sources                   # List all configured sources
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Perform full update cycle')
    update_parser.add_argument('--no-validate', action='store_true', help='Skip validation step')
    update_parser.add_argument('--sources', help='Comma-separated list of sources to fetch')
    
    # Fetch command
    fetch_parser = subparsers.add_parser('fetch', help='Fetch templates from sources')
    fetch_parser.add_argument('--sources', help='Comma-separated list of sources to fetch')
    
    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge individual templates')
    merge_parser.add_argument('--categories', help='Comma-separated list of categories to include')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate template files')
    validate_parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed issues')
    
    # Report command
    subparsers.add_parser('report', help='Generate template reports')
    
    # Status command
    subparsers.add_parser('status', help='Show current status')
    
    # Sources command
    subparsers.add_parser('sources', help='List configured sources')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = PortainerTemplateManager()
    
    try:
        if args.command == 'update':
            source_list = args.sources.split(',') if args.sources else None
            await manager.full_update(validate=not args.no_validate, sources=source_list)
        
        elif args.command == 'fetch':
            source_list = args.sources.split(',') if args.sources else None
            await manager.fetch_only(sources=source_list)
        
        elif args.command == 'merge':
            category_list = args.categories.split(',') if args.categories else None
            success = manager.merge_only(categories=category_list)
            if not success:
                sys.exit(1)
        
        elif args.command == 'validate':
            manager.validate_only(verbose=args.verbose)
        
        elif args.command == 'report':
            manager.report_only()
        
        elif args.command == 'status':
            manager.get_status()
        
        elif args.command == 'sources':
            manager.list_sources()
    
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())