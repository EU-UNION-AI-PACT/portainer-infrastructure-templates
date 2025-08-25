#!/usr/bin/env python3
"""
Portainer Template Report Generator

Generates detailed reports about available templates, sources, and statistics.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict, Counter
from datetime import datetime
import argparse

class TemplateReporter:
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.individual_dir = self.templates_dir / "individual"
        self.merged_dir = self.templates_dir / "merged"
        self.reports_dir = Path("reports")
        
    def load_merged_templates(self) -> Dict:
        """Load the master merged template file."""
        master_file = self.merged_dir / "master_templates.json"
        
        if not master_file.exists():
            print(f"❌ Master template file not found: {master_file}")
            return {}
        
        try:
            with open(master_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load master templates: {e}")
            return {}
    
    def load_individual_templates(self) -> Dict[str, Dict]:
        """Load all individual template files."""
        templates = {}
        
        if not self.individual_dir.exists():
            return templates
        
        for file_path in self.individual_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    templates[file_path.stem] = json.load(f)
            except Exception as e:
                print(f"❌ Failed to load {file_path}: {e}")
        
        return templates
    
    def generate_summary_report(self) -> Dict:
        """Generate a comprehensive summary report."""
        merged_data = self.load_merged_templates()
        individual_data = self.load_individual_templates()
        
        if not merged_data:
            return {"error": "No merged template data available"}
        
        templates = merged_data.get('templates', [])
        statistics = merged_data.get('statistics', {})
        
        # Analyze templates
        categories = Counter()
        platforms = Counter()
        sources = Counter()
        images = Counter()
        
        for template in templates:
            # Categories
            for category in template.get('categories', []):
                categories[category] += 1
            
            # Platforms
            platform = template.get('platform', 'linux')
            platforms[platform] += 1
            
            # Sources
            source = template.get('_source', 'unknown')
            sources[source] += 1
            
            # Images (Docker images)
            image = template.get('image', '')
            if image:
                # Extract base image name (before ':' tag)
                base_image = image.split(':')[0]
                images[base_image] += 1
        
        # Source health analysis
        source_health = {}
        for source_name, source_data in individual_data.items():
            metadata = source_data.get('_metadata', {})
            source_health[source_name] = {
                'status': metadata.get('status', 'unknown'),
                'template_count': len(source_data.get('templates', [])),
                'last_fetched': metadata.get('fetched_at'),
                'error': metadata.get('error'),
                'url': metadata.get('source_url')
            }
        
        return {
            'summary': {
                'total_templates': len(templates),
                'total_sources': len(individual_data),
                'active_sources': len([s for s in source_health.values() if s['status'] == 'success']),
                'failed_sources': len([s for s in source_health.values() if s['status'] == 'failed']),
                'unique_categories': len(categories),
                'unique_images': len(images),
                'report_generated': datetime.now().isoformat()
            },
            'categories': {
                'top_categories': dict(categories.most_common(10)),
                'all_categories': dict(categories)
            },
            'platforms': dict(platforms),
            'sources': {
                'template_count_by_source': dict(sources),
                'source_health': source_health
            },
            'popular_images': dict(images.most_common(20)),
            'statistics': statistics
        }
    
    def generate_detailed_template_list(self) -> List[Dict]:
        """Generate detailed list of all templates."""
        merged_data = self.load_merged_templates()
        templates = merged_data.get('templates', [])
        
        detailed_list = []
        for template in templates:
            detailed_info = {
                'name': template.get('name', 'Unknown'),
                'title': template.get('title', ''),
                'description': template.get('description', ''),
                'image': template.get('image', ''),
                'categories': template.get('categories', []),
                'platform': template.get('platform', 'linux'),
                'source': template.get('_source', 'unknown'),
                'ports': len(template.get('ports', [])),
                'volumes': len(template.get('volumes', [])),
                'environment_vars': len(template.get('env', [])),
                'has_logo': bool(template.get('logo', '')),
                'restart_policy': template.get('restart_policy', ''),
                'privileged': template.get('privileged', False)
            }
            detailed_list.append(detailed_info)
        
        # Sort by name
        return sorted(detailed_list, key=lambda x: x['name'].lower())
    
    def generate_category_breakdown(self) -> Dict[str, List[Dict]]:
        """Generate templates grouped by category."""
        merged_data = self.load_merged_templates()
        templates = merged_data.get('templates', [])
        
        category_groups = defaultdict(list)
        
        for template in templates:
            categories = template.get('categories', ['uncategorized'])
            
            for category in categories:
                category_groups[category].append({
                    'name': template.get('name', 'Unknown'),
                    'title': template.get('title', ''),
                    'description': template.get('description', ''),
                    'image': template.get('image', ''),
                    'source': template.get('_source', 'unknown')
                })
        
        # Sort templates within each category
        for category in category_groups:
            category_groups[category].sort(key=lambda x: x['name'].lower())
        
        return dict(category_groups)
    
    def generate_source_analysis(self) -> Dict:
        """Generate detailed analysis of template sources."""
        individual_data = self.load_individual_templates()
        
        source_analysis = {}
        
        for source_name, source_data in individual_data.items():
            metadata = source_data.get('_metadata', {})
            templates = source_data.get('templates', [])
            
            # Analyze this source's templates
            categories = Counter()
            images = set()
            
            for template in templates:
                for category in template.get('categories', []):
                    categories[category] += 1
                
                image = template.get('image', '')
                if image:
                    images.add(image.split(':')[0])
            
            source_analysis[source_name] = {
                'metadata': {
                    'url': metadata.get('source_url', ''),
                    'description': metadata.get('description', ''),
                    'status': metadata.get('status', 'unknown'),
                    'last_fetched': metadata.get('fetched_at'),
                    'error': metadata.get('error')
                },
                'template_stats': {
                    'total_templates': len(templates),
                    'categories': dict(categories),
                    'unique_images': len(images),
                    'top_categories': dict(categories.most_common(5))
                }
            }
        
        return source_analysis
    
    def save_reports(self) -> None:
        """Generate and save all reports."""
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        print("📊 Generating comprehensive template reports...")
        
        # Summary report
        print("🔄 Generating summary report...")
        summary = self.generate_summary_report()
        with open(self.reports_dir / "summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Detailed template list
        print("🔄 Generating detailed template list...")
        detailed_list = self.generate_detailed_template_list()
        with open(self.reports_dir / "detailed_templates.json", 'w') as f:
            json.dump(detailed_list, f, indent=2)
        
        # Category breakdown
        print("🔄 Generating category breakdown...")
        categories = self.generate_category_breakdown()
        with open(self.reports_dir / "templates_by_category.json", 'w') as f:
            json.dump(categories, f, indent=2)
        
        # Source analysis
        print("🔄 Generating source analysis...")
        source_analysis = self.generate_source_analysis()
        with open(self.reports_dir / "source_analysis.json", 'w') as f:
            json.dump(source_analysis, f, indent=2)
        
        # Generate markdown summary
        self.generate_markdown_report(summary)
        
        print("✅ All reports generated successfully!")
    
    def generate_markdown_report(self, summary_data: Dict) -> None:
        """Generate a human-readable markdown report."""
        summary = summary_data.get('summary', {})
        categories = summary_data.get('categories', {})
        sources = summary_data.get('sources', {})
        
        markdown_content = f"""# Portainer Template Collection Report

Generated on: {summary.get('report_generated', 'Unknown')}

## 📊 Overview

- **Total Templates**: {summary.get('total_templates', 0)}
- **Active Sources**: {summary.get('active_sources', 0)}
- **Failed Sources**: {summary.get('failed_sources', 0)}
- **Unique Categories**: {summary.get('unique_categories', 0)}
- **Unique Images**: {summary.get('unique_images', 0)}

## 🏷️ Top Categories

"""
        
        top_categories = categories.get('top_categories', {})
        for category, count in top_categories.items():
            markdown_content += f"- **{category}**: {count} templates\n"
        
        markdown_content += "\n## 📦 Source Status\n\n"
        
        source_health = sources.get('source_health', {})
        successful_sources = [name for name, health in source_health.items() if health['status'] == 'success']
        failed_sources = [name for name, health in source_health.items() if health['status'] == 'failed']
        
        markdown_content += f"### ✅ Successful Sources ({len(successful_sources)})\n\n"
        for source in successful_sources:
            health = source_health[source]
            markdown_content += f"- **{source}**: {health['template_count']} templates\n"
        
        if failed_sources:
            markdown_content += f"\n### ❌ Failed Sources ({len(failed_sources)})\n\n"
            for source in failed_sources:
                health = source_health[source]
                error = health.get('error', 'Unknown error')
                markdown_content += f"- **{source}**: {error}\n"
        
        markdown_content += """
## 🔗 Popular Images

"""
        
        popular_images = summary_data.get('popular_images', {})
        for image, count in list(popular_images.items())[:10]:
            markdown_content += f"- **{image}**: {count} templates\n"
        
        # Save markdown report
        with open(self.reports_dir / "README.md", 'w') as f:
            f.write(markdown_content)

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description='Generate Portainer template reports')
    parser.add_argument('--templates-dir', '-t', default='templates', 
                       help='Directory containing template files')
    parser.add_argument('--output-dir', '-o', default='reports',
                       help='Directory for generated reports')
    
    args = parser.parse_args()
    
    reporter = TemplateReporter(args.templates_dir)
    reporter.reports_dir = Path(args.output_dir)
    
    reporter.save_reports()

if __name__ == "__main__":
    main()