#!/usr/bin/env python3
"""
Portainer Template Merger

Merges individual template files into a single master template.
Handles deduplication, validation, and format normalization.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
import argparse
import hashlib
import click
from datetime import datetime

class TemplateMerger:
    def __init__(self, input_dir: str = "templates/individual", output_dir: str = "templates/merged"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load merger configuration."""
        config_path = Path("config/sources.json")
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"settings": {"deduplicate_by": ["name"], "merge_strategy": "latest_wins"}}
    
    def load_template_files(self) -> Dict[str, Dict]:
        """Load all template files from input directory."""
        templates = {}
        
        if not self.input_dir.exists():
            click.echo(f"❌ Input directory not found: {self.input_dir}")
            return templates
        
        for file_path in self.input_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    templates[file_path.stem] = data
                    click.echo(f"📄 Loaded {file_path.stem}")
            except Exception as e:
                click.echo(f"❌ Failed to load {file_path}: {e}")
        
        return templates
    
    def normalize_template_format(self, template_data: Dict) -> List[Dict]:
        """Normalize different template formats to a standard format."""
        templates = []
        
        # Extract templates from various formats
        if 'templates' in template_data:
            raw_templates = template_data['templates']
        elif isinstance(template_data, list):
            raw_templates = template_data
        else:
            raw_templates = [template_data]
        
        for template in raw_templates:
            if not isinstance(template, dict):
                continue
                
            # Skip if template is empty or invalid
            if not template.get('name') and not template.get('title'):
                continue
            
            # Normalize template structure
            normalized = {
                'type': template.get('type', 1),
                'title': template.get('title', template.get('name', 'Unknown')),
                'name': template.get('name', template.get('title', 'unknown')),
                'description': template.get('description', ''),
                'note': template.get('note', ''),
                'categories': template.get('categories', template.get('category', [])),
                'platform': template.get('platform', 'linux'),
                'logo': template.get('logo', ''),
                'image': template.get('image', ''),
                'restart_policy': template.get('restart_policy', 'unless-stopped'),
                'ports': template.get('ports', []),
                'volumes': template.get('volumes', []),
                'env': template.get('env', template.get('environment', [])),
                'command': template.get('command', ''),
                'network': template.get('network', ''),
                'hostname': template.get('hostname', ''),
                'privileged': template.get('privileged', False),
                'interactive': template.get('interactive', False),
                'stdin_open': template.get('stdin_open', False),
                'tty': template.get('tty', False)
            }
            
            # Normalize categories
            if isinstance(normalized['categories'], str):
                normalized['categories'] = [normalized['categories']]
            elif not isinstance(normalized['categories'], list):
                normalized['categories'] = []
            
            # Generate hash for deduplication
            hash_content = f"{normalized['name']}:{normalized['image']}"
            normalized['_hash'] = hashlib.md5(hash_content.encode()).hexdigest()
            
            templates.append(normalized)
        
        return templates
    
    def deduplicate_templates(self, all_templates: List[Dict]) -> List[Dict]:
        """Remove duplicate templates based on configuration."""
        dedupe_fields = self.config.get('settings', {}).get('deduplicate_by', ['name'])
        seen_combinations = set()
        unique_templates = []
        
        for template in all_templates:
            # Create deduplication key
            key_parts = []
            for field in dedupe_fields:
                value = template.get(field, '')
                if isinstance(value, list):
                    value = ','.join(sorted(str(v) for v in value))
                key_parts.append(str(value).lower().strip())
            
            dedupe_key = '|'.join(key_parts)
            
            if dedupe_key not in seen_combinations:
                seen_combinations.add(dedupe_key)
                unique_templates.append(template)
            else:
                click.echo(f"🔄 Duplicate found: {template.get('name', 'Unknown')}")
        
        return unique_templates
    
    def generate_statistics(self, templates: List[Dict], source_stats: Dict) -> Dict:
        """Generate statistics about the merged templates."""
        categories = defaultdict(int)
        platforms = defaultdict(int)
        
        for template in templates:
            # Count categories
            for category in template.get('categories', []):
                categories[category] += 1
            
            # Count platforms
            platform = template.get('platform', 'linux')
            platforms[platform] += 1
        
        return {
            'total_templates': len(templates),
            'total_sources': len(source_stats),
            'templates_by_category': dict(categories),
            'templates_by_platform': dict(platforms),
            'source_statistics': source_stats,
            'generated_at': datetime.now().isoformat(),
            'unique_categories': len(categories),
            'unique_platforms': len(platforms)
        }
    
    def merge_templates(self, filter_categories: Optional[List[str]] = None) -> Dict:
        """Merge all templates into a single collection."""
        click.echo("🔄 Loading template files...")
        template_files = self.load_template_files()
        
        if not template_files:
            click.echo("❌ No template files found!")
            return {}
        
        all_templates = []
        source_stats = {}
        
        # Process each source file
        for source_name, template_data in template_files.items():
            click.echo(f"🔄 Processing {source_name}...")
            
            normalized_templates = self.normalize_template_format(template_data)
            
            # Apply category filter if specified
            if filter_categories:
                filtered_templates = []
                for template in normalized_templates:
                    template_categories = template.get('categories', [])
                    if any(cat.lower() in [f.lower() for f in filter_categories] for cat in template_categories):
                        filtered_templates.append(template)
                normalized_templates = filtered_templates
            
            # Add source metadata to each template
            for template in normalized_templates:
                template['_source'] = source_name
            
            all_templates.extend(normalized_templates)
            source_stats[source_name] = {
                'template_count': len(normalized_templates),
                'metadata': template_data.get('_metadata', {}),
                'status': template_data.get('_metadata', {}).get('status', 'unknown')
            }
        
        click.echo(f"🔄 Deduplicating {len(all_templates)} templates...")
        unique_templates = self.deduplicate_templates(all_templates)
        
        click.echo(f"📊 Found {len(unique_templates)} unique templates")
        
        # Generate statistics
        stats = self.generate_statistics(unique_templates, source_stats)
        
        # Create final merged structure
        merged_data = {
            'version': '2',
            'templates': unique_templates,
            'statistics': stats
        }
        
        return merged_data
    
    def save_merged_templates(self, merged_data: Dict, filename: str = "master_templates.json") -> None:
        """Save merged templates to output file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / filename
        
        try:
            with open(output_path, 'w') as f:
                json.dump(merged_data, f, indent=2)
            
            template_count = len(merged_data.get('templates', []))
            click.echo(f"✅ Saved {template_count} templates to {output_path}")
            
            # Also save statistics separately
            stats_path = self.output_dir / "statistics.json"
            with open(stats_path, 'w') as f:
                json.dump(merged_data.get('statistics', {}), f, indent=2)
            
            click.echo(f"📊 Statistics saved to {stats_path}")
            
        except Exception as e:
            click.echo(f"❌ Failed to save merged templates: {e}")

@click.command()
@click.option('--categories', '-c', help='Comma-separated list of categories to include')
@click.option('--input', '-i', default='templates/individual', help='Input directory with template files')
@click.option('--output', '-o', default='templates/merged', help='Output directory for merged templates')
@click.option('--filename', '-f', default='master_templates.json', help='Output filename')
def main(categories: Optional[str], input: str, output: str, filename: str):
    """Merge individual template files into a master template collection."""
    
    # Parse category filter
    category_filter = categories.split(',') if categories else None
    
    # Create merger
    merger = TemplateMerger(input, output)
    
    # Merge templates
    merged_data = merger.merge_templates(category_filter)
    
    if merged_data:
        merger.save_merged_templates(merged_data, filename)
    else:
        click.echo("❌ No templates to merge!")

if __name__ == "__main__":
    main()