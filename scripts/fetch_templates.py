#!/usr/bin/env python3
"""
Portainer Template Fetcher

Downloads templates from configured sources and saves them individually.
Supports concurrent downloads, retry logic, and progress tracking.
"""

import json
import os
import sys
import asyncio
import aiohttp
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from urllib.parse import urlparse
import click
from tqdm import tqdm
import time

@dataclass
class TemplateSource:
    name: str
    url: str
    description: str
    active: bool
    category: str

class TemplateFetcher:
    def __init__(self, config_path: str = "config/sources.json"):
        self.config_path = Path(config_path)
        self.output_dir = Path("templates/individual")
        self.config = self._load_config()
        self.session: Optional[aiohttp.ClientSession] = None
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            click.echo(f"❌ Config file not found: {self.config_path}", err=True)
            sys.exit(1)
        except json.JSONDecodeError as e:
            click.echo(f"❌ Invalid JSON in config file: {e}", err=True)
            sys.exit(1)
    
    def get_active_sources(self, filter_sources: Optional[List[str]] = None) -> List[TemplateSource]:
        """Get list of active template sources."""
        sources = []
        for source_data in self.config['sources']:
            if not source_data.get('active', True):
                continue
                
            if filter_sources and source_data['name'] not in filter_sources:
                continue
                
            sources.append(TemplateSource(**source_data))
        
        return sources
    
    async def fetch_template(self, source: TemplateSource) -> Dict:
        """Fetch a single template from source."""
        timeout = aiohttp.ClientTimeout(total=self.config['settings']['timeout_seconds'])
        
        for attempt in range(self.config['settings']['retry_attempts']):
            try:
                async with self.session.get(source.url, timeout=timeout) as response:
                    if response.status == 200:
                        content = await response.text()
                        template_data = json.loads(content)
                        
                        # Add metadata
                        metadata = {
                            'source_name': source.name,
                            'source_url': source.url,
                            'description': source.description,
                            'category': source.category,
                            'fetched_at': time.time(),
                            'status': 'success'
                        }
                        
                        # Handle different template formats
                        if isinstance(template_data, dict):
                            if 'templates' in template_data:
                                template_data['_metadata'] = metadata
                                return template_data
                            elif 'version' in template_data or 'templates' in str(template_data):
                                return {'templates': [template_data], '_metadata': metadata}
                            else:
                                return {'templates': [template_data], '_metadata': metadata}
                        elif isinstance(template_data, list):
                            return {'templates': template_data, '_metadata': metadata}
                        else:
                            return {'templates': [], '_metadata': metadata}
                            
                    else:
                        if attempt == self.config['settings']['retry_attempts'] - 1:
                            return {
                                'templates': [],
                                '_metadata': {
                                    'source_name': source.name,
                                    'source_url': source.url,
                                    'status': 'failed',
                                    'error': f"HTTP {response.status}",
                                    'fetched_at': time.time()
                                }
                            }
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                        
            except asyncio.TimeoutError:
                if attempt == self.config['settings']['retry_attempts'] - 1:
                    return {
                        'templates': [],
                        '_metadata': {
                            'source_name': source.name,
                            'source_url': source.url,
                            'status': 'failed',
                            'error': 'Timeout',
                            'fetched_at': time.time()
                        }
                    }
                await asyncio.sleep(2 ** attempt)
                
            except Exception as e:
                if attempt == self.config['settings']['retry_attempts'] - 1:
                    return {
                        'templates': [],
                        '_metadata': {
                            'source_name': source.name,
                            'source_url': source.url,
                            'status': 'failed',
                            'error': str(e),
                            'fetched_at': time.time()
                        }
                    }
                await asyncio.sleep(2 ** attempt)
    
    async def fetch_all_templates(self, sources: List[TemplateSource]) -> Dict[str, Dict]:
        """Fetch templates from all sources concurrently."""
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create aiohttp session
        connector = aiohttp.TCPConnector(limit=self.config['settings']['concurrent_downloads'])
        self.session = aiohttp.ClientSession(connector=connector)
        
        try:
            # Create progress bar
            with tqdm(total=len(sources), desc="Fetching templates") as pbar:
                # Create semaphore to limit concurrent downloads
                semaphore = asyncio.Semaphore(self.config['settings']['concurrent_downloads'])
                
                async def fetch_with_semaphore(source):
                    async with semaphore:
                        result = await self.fetch_template(source)
                        pbar.update(1)
                        return source.name, result
                
                # Execute all downloads
                tasks = [fetch_with_semaphore(source) for source in sources]
                results = await asyncio.gather(*tasks)
                
                # Convert to dictionary
                return dict(results)
                
        finally:
            await self.session.close()
    
    def save_templates(self, templates: Dict[str, Dict]) -> None:
        """Save fetched templates to individual files."""
        success_count = 0
        failed_count = 0
        
        for source_name, template_data in templates.items():
            try:
                output_file = self.output_dir / f"{source_name}.json"
                with open(output_file, 'w') as f:
                    json.dump(template_data, f, indent=2)
                
                if template_data.get('_metadata', {}).get('status') == 'success':
                    template_count = len(template_data.get('templates', []))
                    click.echo(f"✅ {source_name}: {template_count} templates saved")
                    success_count += 1
                else:
                    error = template_data.get('_metadata', {}).get('error', 'Unknown error')
                    click.echo(f"❌ {source_name}: Failed - {error}")
                    failed_count += 1
                    
            except Exception as e:
                click.echo(f"❌ {source_name}: Save failed - {e}")
                failed_count += 1
        
        click.echo(f"\n📊 Summary: {success_count} successful, {failed_count} failed")
    
    async def run(self, filter_sources: Optional[List[str]] = None) -> None:
        """Main execution method."""
        sources = self.get_active_sources(filter_sources)
        
        if not sources:
            click.echo("❌ No active sources found!")
            return
        
        click.echo(f"🚀 Fetching templates from {len(sources)} sources...")
        
        templates = await self.fetch_all_templates(sources)
        self.save_templates(templates)

@click.command()
@click.option('--sources', '-s', help='Comma-separated list of source names to fetch')
@click.option('--config', '-c', default='config/sources.json', help='Path to config file')
@click.option('--output', '-o', default='templates/individual', help='Output directory')
def main(sources: Optional[str], config: str, output: str):
    """Fetch Portainer templates from configured sources."""
    
    # Parse source filter
    source_filter = sources.split(',') if sources else None
    
    # Create fetcher
    fetcher = TemplateFetcher(config)
    fetcher.output_dir = Path(output)
    
    # Run async fetch
    asyncio.run(fetcher.run(source_filter))

if __name__ == "__main__":
    main()