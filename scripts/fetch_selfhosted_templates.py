#!/usr/bin/env python3
"""
Comprehensive template collection from SelfhostedPro/selfhosted_templates repository
Fetches all major template files and merges them with existing collection
"""

import json
import requests
import os
from typing import Dict, List, Any, Set
import time

# Template sources from SelfhostedPro repository
TEMPLATE_SOURCES = {
    "template.json": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/template.json",
    "portainer-v1.json": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/portainer-v1.json", 
    "portainer-v2.json": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/portainer-v2.json",
    "omv-v1.json": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/omv-v1.json",
    "omv-v2.json": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/omv-v2.json",
    "yacht.json": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/yacht.json"
}

def normalize_env_variables(env_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize environment variables to v3 format"""
    if not env_list:
        return []
    
    normalized = []
    for env in env_list:
        if isinstance(env, dict):
            # Ensure required fields
            normalized_env = {
                "name": env.get("name", env.get("variable", "")),
                "label": env.get("label", env.get("name", env.get("variable", ""))),
            }
            
            # Add optional fields
            if "description" in env:
                normalized_env["description"] = env["description"]
            if "default" in env:
                normalized_env["default"] = env["default"]
            if "preset" in env:
                normalized_env["default"] = env["preset"]
            if "set" in env:
                normalized_env["default"] = env["set"]
                
            normalized.append(normalized_env)
    
    return normalized

def normalize_volumes(volumes: List) -> List[Dict[str, str]]:
    """Normalize volume definitions"""
    if not volumes:
        return []
    
    normalized = []
    for vol in volumes:
        if isinstance(vol, dict):
            normalized.append(vol)
        elif isinstance(vol, str):
            # Parse string format like "/host/path:/container/path"
            if ":" in vol:
                parts = vol.split(":")
                if len(parts) >= 2:
                    normalized.append({
                        "bind": parts[0],
                        "container": parts[1]
                    })
            else:
                normalized.append({"container": vol})
    
    return normalized

def convert_template_to_v3(template: Dict[str, Any], source_name: str) -> Dict[str, Any]:
    """Convert any template format to Portainer v3"""
    
    # Basic required fields
    v3_template = {
        "type": template.get("type", 1),
        "title": template.get("title", template.get("name", "Unknown")),
        "description": template.get("description", ""),
        "categories": template.get("categories", template.get("category", ["Other"])),
        "platform": template.get("platform", "linux")
    }
    
    # Ensure categories is a list
    if isinstance(v3_template["categories"], str):
        v3_template["categories"] = [v3_template["categories"]]
    
    # Add optional fields
    for field in ["logo", "note", "administrator_only"]:
        if field in template:
            v3_template[field] = template[field]
    
    # Handle template types
    template_type = template.get("type", 1)
    
    if template_type == 1:  # Container
        # Required for containers
        if "image" in template:
            v3_template["image"] = template["image"]
        
        # Optional container fields
        for field in ["command", "network", "hostname", "privileged", "interactive", "tty"]:
            if field in template:
                v3_template[field] = template[field]
        
        # Handle ports
        if "ports" in template:
            v3_template["ports"] = template["ports"]
        elif "port" in template:
            v3_template["ports"] = [template["port"]]
        
        # Handle volumes
        if "volumes" in template:
            v3_template["volumes"] = normalize_volumes(template["volumes"])
        
        # Handle environment variables
        if "env" in template:
            v3_template["env"] = normalize_env_variables(template["env"])
        elif "environment" in template:
            v3_template["env"] = normalize_env_variables(template["environment"])
        
        # Handle restart policy
        if "restart_policy" in template:
            v3_template["restart_policy"] = template["restart_policy"]
        elif "restart" in template:
            v3_template["restart_policy"] = template["restart"]
            
    elif template_type == 3:  # Stack
        if "repository" in template:
            v3_template["repository"] = template["repository"]
        
        # Handle environment variables for stacks
        if "env" in template:
            v3_template["env"] = normalize_env_variables(template["env"])
    
    # Add source info as note if not present
    if "note" not in v3_template:
        v3_template["note"] = f"Source: {source_name}"
    else:
        v3_template["note"] += f" (Source: {source_name})"
    
    return v3_template

def fetch_template_file(url: str, source_name: str) -> List[Dict[str, Any]]:
    """Fetch and parse a template file from URL"""
    try:
        print(f"   📥 Fetching {source_name}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Try to parse as JSON
        try:
            data = response.json()
        except json.JSONDecodeError:
            print(f"   ❌ Failed to parse JSON from {source_name}")
            return []
        
        # Extract templates
        templates = []
        if isinstance(data, dict):
            if "templates" in data:
                templates = data["templates"]
            elif "version" in data and isinstance(data.get("templates"), list):
                templates = data["templates"]
            else:
                # Maybe it's a single template
                templates = [data]
        elif isinstance(data, list):
            templates = data
        
        print(f"   ✅ Found {len(templates)} templates in {source_name}")
        return templates
        
    except requests.RequestException as e:
        print(f"   ❌ Failed to fetch {source_name}: {e}")
        return []
    except Exception as e:
        print(f"   ❌ Error processing {source_name}: {e}")
        return []

def deduplicate_templates(templates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate templates based on title"""
    seen_titles = set()
    unique_templates = []
    duplicates = []
    
    for template in templates:
        title = template.get("title", "").lower().strip()
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_templates.append(template)
        else:
            duplicates.append(template.get("title", "Unknown"))
    
    if duplicates:
        print(f"   🔄 Removed {len(duplicates)} duplicates")
    
    return unique_templates

def load_existing_templates(file_path: str) -> Dict[str, Any]:
    """Load existing template file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"version": "3", "templates": []}

def save_templates(templates_data: Dict[str, Any], file_path: str):
    """Save templates to file with proper formatting"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)

def main():
    """Main collection function"""
    print("🚀 Starting comprehensive template collection from SelfhostedPro repository...")
    
    # File paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    existing_file = os.path.join(base_dir, "web", "portainer-template.json")
    backup_file = os.path.join(base_dir, "web", "portainer-template.json.backup2")
    
    # Load existing templates
    existing_data = load_existing_templates(existing_file)
    existing_templates = existing_data.get("templates", [])
    existing_count = len(existing_templates)
    
    print(f"   📊 Current templates: {existing_count}")
    
    # Create backup
    if os.path.exists(existing_file):
        import shutil
        shutil.copy2(existing_file, backup_file)
        print(f"   💾 Backup created: {backup_file}")
    
    # Collect all new templates
    all_new_templates = []
    
    for source_name, url in TEMPLATE_SOURCES.items():
        templates = fetch_template_file(url, source_name)
        
        # Convert to v3 format
        for template in templates:
            try:
                converted = convert_template_to_v3(template, source_name)
                all_new_templates.append(converted)
            except Exception as e:
                print(f"   ⚠️  Failed to convert template from {source_name}: {e}")
        
        # Small delay to be respectful to GitHub
        time.sleep(0.5)
    
    print(f"\n📈 Collection Summary:")
    print(f"   • Templates collected: {len(all_new_templates)}")
    
    # Merge with existing templates and deduplicate
    all_templates = existing_templates + all_new_templates
    unique_templates = deduplicate_templates(all_templates)
    
    # Sort by category and title
    unique_templates.sort(key=lambda x: (x.get("categories", [""])[0], x.get("title", "")))
    
    # Create final template data
    final_data = {
        "version": "3",
        "templates": unique_templates
    }
    
    # Save merged templates
    save_templates(final_data, existing_file)
    
    print(f"\n🎉 Template collection completed!")
    print(f"   • Original templates: {existing_count}")
    print(f"   • New templates collected: {len(all_new_templates)}")
    print(f"   • Final unique templates: {len(unique_templates)}")
    print(f"   • New templates added: {len(unique_templates) - existing_count}")
    print(f"   • File saved: {existing_file}")
    
    # Validation
    try:
        with open(existing_file, 'r') as f:
            json.load(f)
        print(f"   ✅ JSON validation passed")
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON validation failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())