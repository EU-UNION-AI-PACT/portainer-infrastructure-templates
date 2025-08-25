#!/usr/bin/env python3
"""
🎨 Enhanced Logo Integration for Portainer Templates
Adds high-quality, consistent logos for all templates
"""

import json
import re

def get_enhanced_logo_url(template):
    """Generate enhanced logo URL based on template information"""
    
    title = template.get('title', '').lower()
    image = template.get('image', '').lower()
    
    # High-quality logo mappings
    logo_mappings = {
        # Database Systems
        'postgres': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/postgresql.png',
        'mysql': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/mysql.png',
        'mariadb': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/mariadb.png',
        'mongodb': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/mongodb.png',
        'redis': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/redis.png',
        'influxdb': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/influxdb.png',
        'elasticsearch': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/elasticsearch.png',
        'cassandra': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/cassandra.png',
        'couchdb': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/couchdb.png',
        'neo4j': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/neo4j.png',
        
        # Web Servers & Proxies
        'nginx': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/nginx.png',
        'apache': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/apache.png',
        'traefik': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/traefik.png',
        'caddy': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/caddy.png',
        'haproxy': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/haproxy.png',
        
        # Monitoring & Analytics
        'prometheus': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/prometheus.png',
        'grafana': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/grafana.png',
        'portainer': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/portainer.png',
        'uptimekuma': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/uptime-kuma.png',
        'netdata': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/netdata.png',
        'zabbix': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/zabbix.png',
        
        # Development Tools
        'gitlab': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/gitlab.png',
        'jenkins': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/jenkins.png',
        'sonarqube': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/sonarqube.png',
        'nexus': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/nexus.png',
        'registry': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/docker.png',
        
        # Media & Entertainment
        'plex': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/plex.png',
        'jellyfin': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/jellyfin.png',
        'emby': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/emby.png',
        'sonarr': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/sonarr.png',
        'radarr': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/radarr.png',
        'lidarr': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/lidarr.png',
        'prowlarr': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/prowlarr.png',
        'transmission': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/transmission.png',
        
        # File Storage & Sync
        'nextcloud': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/nextcloud.png',
        'owncloud': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/owncloud.png',
        'seafile': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/seafile.png',
        'syncthing': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/syncthing.png',
        'filebrowser': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/filebrowser.png',
        'minio': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/minio.png',
        
        # Communication
        'rocket.chat': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/rocket-chat.png',
        'mattermost': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/mattermost.png',
        'discord': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/discord.png',
        
        # CMS & Websites
        'wordpress': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/wordpress.png',
        'drupal': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/drupal.png',
        'joomla': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/joomla.png',
        'ghost': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/ghost.png',
        
        # Security & VPN
        'wireguard': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/wireguard.png',
        'openvpn': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/openvpn.png',
        'bitwarden': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/bitwarden.png',
        'vaultwarden': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/vaultwarden.png',
        
        # Development Frameworks
        'node': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/nodejs.png',
        'python': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/python.png',
        'golang': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/go.png',
        'react': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/react.png',
        'vue': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/vue.png',
        'angular': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/angular.png',
        
        # Utilities
        'duplicati': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/duplicati.png',
        'watchtower': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/watchtower.png',
        'dozzle': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/dozzle.png',
        'adminer': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/adminer.png',
        'phpmyadmin': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/phpmyadmin.png',
    }
    
    # Try to match by image name first
    for key, logo_url in logo_mappings.items():
        if key in image:
            return logo_url
    
    # Try to match by title
    for key, logo_url in logo_mappings.items():
        if key in title:
            return logo_url
    
    # Fallback: extract main service name from image
    service_name = image.split('/')[0] if '/' in image else image.split(':')[0]
    if service_name in logo_mappings:
        return logo_mappings[service_name]
    
    # Ultimate fallback: Docker logo
    return 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/docker.png'

def enhance_template_logos():
    """Enhance all template logos with high-quality versions"""
    
    print("🎨 Enhancing Template Logos...")
    print("=" * 50)
    
    # Load current templates
    with open('web/portainer-template.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    enhanced_count = 0
    total_templates = len(data['templates'])
    
    for i, template in enumerate(data['templates']):
        title = template.get('title', f'Template {i+1}')
        current_logo = template.get('logo', '')
        
        # Get enhanced logo
        enhanced_logo = get_enhanced_logo_url(template)
        
        # Update logo if it's different or missing
        if current_logo != enhanced_logo:
            template['logo'] = enhanced_logo
            enhanced_count += 1
            print(f"✅ Enhanced: {title[:40]}...")
    
    # Save enhanced templates
    with open('web/portainer-template.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Logo Enhancement Complete!")
    print(f"📊 Templates Enhanced: {enhanced_count}/{total_templates}")
    print(f"📈 Logo Quality: High-Resolution CDN URLs")
    print(f"🎯 Logo Source: Dashboard Icons (walkxcode)")
    print(f"💎 Status: Pink Star Diamond Logo Quality Achieved!")
    
    return enhanced_count

if __name__ == '__main__':
    enhance_template_logos()