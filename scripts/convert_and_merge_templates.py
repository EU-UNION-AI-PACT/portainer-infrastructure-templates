#!/usr/bin/env python3
"""
Convert Portainer v2 templates to v3 format and merge with existing templates
"""

import json
import os
from typing import Dict, List, Any

def convert_v2_to_v3_template(v2_template: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a Portainer v2 template to v3 format
    """
    v3_template = {
        "type": v2_template.get("type", 1),  # Default to container if not specified
        "title": v2_template.get("title", v2_template.get("name", "Unknown")),
        "description": v2_template.get("description", ""),
        "categories": v2_template.get("categories", ["Other"]),
        "platform": v2_template.get("platform", "linux")
    }
    
    # Add logo if present
    if "logo" in v2_template:
        v3_template["logo"] = v2_template["logo"]
    
    # Add note if present
    if "note" in v2_template:
        v3_template["note"] = v2_template["note"]
    
    # Handle different template types
    if v2_template.get("type") == 1:  # Container
        v3_template.update({
            "image": v2_template.get("image", ""),
            "ports": v2_template.get("ports", []),
            "volumes": v2_template.get("volumes", []),
            "env": v2_template.get("env", [])
        })
        
        # Add restart policy if present
        if "restart_policy" in v2_template:
            v3_template["restart_policy"] = v2_template["restart_policy"]
            
    elif v2_template.get("type") == 3:  # Stack
        if "repository" in v2_template:
            v3_template["repository"] = v2_template["repository"]
        v3_template["env"] = v2_template.get("env", [])
    
    return v3_template

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

def merge_templates(existing_file: str, new_v2_templates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge new v2 templates with existing v3 templates
    """
    # Load existing templates
    existing_data = load_existing_templates(existing_file)
    existing_templates = existing_data.get("templates", [])
    
    # Convert v2 templates to v3
    converted_templates = []
    for template in new_v2_templates:
        try:
            converted = convert_v2_to_v3_template(template)
            converted_templates.append(converted)
            print(f"✅ Converted: {converted['title']}")
        except Exception as e:
            print(f"❌ Failed to convert template {template.get('name', 'Unknown')}: {e}")
    
    # Check for duplicates (by title)
    existing_titles = {t.get("title", "").lower() for t in existing_templates}
    new_templates = []
    duplicates = []
    
    for template in converted_templates:
        title = template.get("title", "").lower()
        if title in existing_titles:
            duplicates.append(template["title"])
        else:
            new_templates.append(template)
            existing_titles.add(title)
    
    # Merge templates
    all_templates = existing_templates + new_templates
    
    result = {
        "version": "3",
        "templates": all_templates
    }
    
    print(f"\n📊 Merge Summary:")
    print(f"   • Existing templates: {len(existing_templates)}")
    print(f"   • New templates added: {len(new_templates)}")
    print(f"   • Duplicates skipped: {len(duplicates)}")
    print(f"   • Total templates: {len(all_templates)}")
    
    if duplicates:
        print(f"\n⚠️  Skipped duplicates: {', '.join(duplicates)}")
    
    return result

def main():
    """Main function"""
    # Define the new v2 templates
    v2_templates_data = {
        "version": "2",
        "templates": [
            {
                "categories": ["Other", "Tools"],
                "description": "This is a Bitwarden server API implementation written in Rust compatible with upstream Bitwarden clients*, perfect for self-hosted deployment where running the official resource-heavy service might not be ideal..",
                "image": "bitwardenrs/server:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/bitwarden.png",
                "name": "bitwardenrs",
                "note": "This project is not associated with the Bitwarden project nor 8bit Solutions LLC.",
                "platform": "linux",
                "ports": ["80/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Bitwarden RS",
                "type": 1,
                "volumes": [{"bind": "/srv/dev-disk-by-label-Files/Config/Bitwarden-rs", "container": "/config"}]
            },
            {
                "categories": ["Other", "Tools"],
                "description": "Embystat is a personal web server that can calculate all kinds of statistics from your (local) Emby server. Just install this on your server and let him calculate all kinds of fun stuff.",
                "image": "linuxserver/embystat:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/embystat.png",
                "name": "embystat",
                "note": "Access the ui at your-ip:6555. Follow the setup wizard on initial install. Then configure the required services.",
                "platform": "linux",
                "ports": ["6555:6555/tcp"],
                "restart_policy": "unless-stopped",
                "title": "EmbyStat",
                "type": 1,
                "volumes": [{"bind": "/srv/dev-disk-by-label-Files/Config/EmbyStat", "container": "/config"}]
            },
            {
                "categories": ["Downloaders", "Tools"],
                "description": "Jackett works as a proxy server it translates queries from apps like Sonarr etc into tracker-site-specific http queries and parses the html response sending results back to the requesting software.[",
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"}
                ],
                "image": "linuxserver/jackett:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/jacket-icon.png",
                "name": "jackett",
                "platform": "linux",
                "ports": ["9117:9117/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Jackett",
                "type": 1,
                "volumes": [
                    {"bind": "/srv/dev-disk-by-label-Files/Config/Jackett", "container": "/config"},
                    {"bind": "/portainer/Downloads", "container": "/downloads"}
                ]
            },
            {
                "categories": ["Cloud", "Web", "Management", "Photos"],
                "description": "Lychee is a free photo-management tool, which runs on your server or web-space. Installing is a matter of seconds. Upload, manage and share photos like from a native application. Lychee comes with everything you need and all your photos are stored securely.",
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"}
                ],
                "image": "linuxserver/lychee:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/lychee-icon.png",
                "name": "lychee",
                "platform": "linux",
                "ports": ["80/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Lychee",
                "type": 1,
                "volumes": [
                    {"bind": "/srv/dev-disk-by-label-Files/Config/Lychee", "container": "/config"},
                    {"bind": "/portainer/Pictures", "container": "/pictures"}
                ]
            },
            {
                "categories": ["Cloud", "Productivity", "Tools", "Other", "Web"],
                "description": "Where are your photos and documents? With Nextcloud you pick a server of your choice, at home, in a data center or at a provider. And that is where your files will be. Nextcloud runs on that server, protecting your data and giving you access from your desktop or mobile devices.",
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"},
                    {"label": "TZ", "name": "TZ"},
                    {"label": "DATABASE_PASSWORD", "name": "DATABASE_PASSWORD"},
                    {"label": "MYSQL_ROOT_PASSWORD", "name": "MYSQL_ROOT_PASSWORD"},
                    {"label": "PORT", "name": "PORT"}
                ],
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/nextcloud-icon.png",
                "name": "nextcloud",
                "note": "The database user is nextcloud and the database is nextcloud_db. The host of the database will be located at the bottom of the DB conotainer in portainer.",
                "platform": "linux",
                "repository": {
                    "stackfile": "Template/Stack/nextcloud.yml",
                    "url": "https://github.com/SelfhostedPro/selfhosted_templates"
                },
                "title": "Nextcloud",
                "type": 3
            },
            {
                "categories": ["Proxy", "Tools"],
                "description": "Nginx Proxy Manager enables you to easily forward to your websites running at home or otherwise, including free SSL, without having to know too much about Nginx or Letsencrypt.",
                "image": "jlesage/nginx-proxy-manager",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/proxy_mgr.png",
                "name": "nginx-proxy-manager",
                "platform": "linux",
                "ports": ["80:8080/tcp", "81:8181/tcp", "443:4443/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Nginx Proxy Manager",
                "type": 1,
                "volumes": [{"bind": "/srv/dev-disk-by-label-Files/Config/Nginx-Proxy", "container": "/config"}]
            },
            {
                "categories": ["Other"],
                "description": "OpenVPN Access Server is a full featured secure network tunneling VPN software solution that integrates OpenVPN server capabilities, enterprise management capabilities, simplified OpenVPN Connect UI, and OpenVPN Client software packages that accommodate Windows, MAC, Linux, Android, and iOS environments.",
                "env": [
                    {"label": "INTERFACE", "name": "INTERFACE", "set": "eth0"},
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"}
                ],
                "image": "linuxserver/openvpn-as:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/openvpn-as-icon.png",
                "name": "openvpn-as",
                "platform": "linux",
                "ports": ["943:943/tcp", "9443:9443/tcp", "1194:1194/udp"],
                "restart_policy": "unless-stopped",
                "title": "OpenVPN Access Server",
                "type": 1,
                "volumes": [{"bind": "/srv/dev-disk-by-label-Files/Config/OpenVPN-AS", "container": "/config"}]
            },
            {
                "categories": ["Wiki"],
                "description": "Bookstack is a free and open source Wiki designed for creating beautiful documentation. Feautring a simple, but powerful WYSIWYG editor it allows for teams to create detailed and useful documentation with ease.",
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"},
                    {"label": "TZ", "name": "TZ"},
                    {"label": "DATABASE_PASSWORD", "name": "DATABASE_PASSWORD"},
                    {"label": "MYSQL_ROOT_PASSWORD", "name": "MYSQL_ROOT_PASSWORD"},
                    {"label": "PORT", "name": "PORT"}
                ],
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/bookstack2.png",
                "note": "Default login is admin@admin.com with a password of password. The database created is called bookstackapp and the database user is called bookstack",
                "platform": "linux",
                "repository": {
                    "stackfile": "Template/Stack/bookstack.yml",
                    "url": "https://github.com/SelfhostedPro/selfhosted_templates"
                },
                "title": "Bookstack",
                "type": 3
            },
            {
                "categories": ["Other", "Tools", "Photo"],
                "description": "Chevereto is a powerful and fast image hosting script that allows you to create your very own full featured image hosting website in just minutes. Please note that this offers only the free Chevereto version..",
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"},
                    {"label": "CHEVERETO_DB_HOST", "name": "CHEVERETO_DB_HOST", "set": ""},
                    {"label": "CHEVERETO_DB_USERNAME", "name": "CHEVERETO_DB_USERNAME", "set": ""},
                    {"label": "CHEVERETO_DB_PASSWORD", "name": "CHEVERETO_DB_PASSWORD", "set": ""},
                    {"label": "CHEVERETO_DB_NAME", "name": "CHEVERETO_DB_NAME", "set": ""},
                    {"label": "CHEVERETO_DB_PREFIX", "name": "CHEVERETO_DB_PREFIX", "set": ""}
                ],
                "image": "nmtan/chevereto:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/Chevereto.png",
                "name": "Chevereto",
                "platform": "linux",
                "ports": ["80/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Chevereto",
                "type": 1,
                "volumes": [{"container": "/var/www/html/images"}]
            },
            {
                "categories": ["Other", "Tools"],
                "description": "Another application bookmark dashboard, with fun features.",
                "image": "rmountjoy/dashmachine:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/dashmachine_logo.png",
                "name": "dashmachine",
                "platform": "linux",
                "ports": ["5000:5000/tcp"],
                "restart_policy": "unless-stopped",
                "title": "DashMachine",
                "type": 1,
                "volumes": [{"bind": "/srv/dev-disk-by-label-Files/Config/Dashmachine", "container": "/dashmachine/dashmachine/user_data"}]
            },
            {
                "categories": ["Backup", "Cloud", "Other", "Productivity", "Tools"],
                "description": "Free backup software to store encrypted backups online, Duplicati works with standard protocols like FTP, SSH, WebDAV as well as popular services like Microsoft OneDrive, Amazon Cloud Drive and S3, Google Drive, box.com, Mega, hubiC and many others.",
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"}
                ],
                "image": "linuxserver/duplicati:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/duplicati-icon.png",
                "name": "duplicati",
                "platform": "linux",
                "ports": ["8200:8200/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Duplicati",
                "type": 1,
                "volumes": [
                    {"bind": "/srv/dev-disk-by-label-Files/Config/Duplicati", "container": "/config"},
                    {"container": "/tmp"},
                    {"container": "/backups"},
                    {"container": "/source"}
                ]
            },
            {
                "categories": ["Video", "Music", "Photos"],
                "description": "Emby organizes video, music, live TV, and photos from personal media libraries and streams them to smart TVs, streaming boxes and mobile devices. This container is packaged as a standalone emby Media Server.",
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"},
                    {"label": "TZ", "name": "TZ"}
                ],
                "image": "linuxserver/emby:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/emby.png",
                "name": "emby",
                "platform": "linux",
                "ports": ["8096:8096/tcp", "8920:8920/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Emby",
                "type": 1,
                "volumes": [
                    {"bind": "/srv/dev-disk-by-label-Files/Config/Emby", "container": "/config"},
                    {"bind": "/portainer/TV", "container": "/data/tvshows"},
                    {"bind": "/portainer/Movies", "container": "/data/movies"}
                ]
            },
            {
                "categories": ["Other", "Tools"],
                "description": "A Linux network-level advertisement and Internet tracker blocking application which acts as a DNS sinkhole.",
                "image": "pihole/pihole:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/pihole.png",
                "name": "pihole",
                "note": "When the installation is complete, navigate to your.ip.goes.here:1010/admin. Follow the article <a href='https://medium.com/@niktrix/getting-rid-of-systemd-resolved-consuming-port-53-605f0234f32f'>here</a> if you run into issues binding to port 53.",
                "platform": "linux",
                "ports": ["53:53/tcp", "53:53/udp", "67:67/udp", "1010:80/tcp", "4443:443/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Pi-Hole",
                "type": 1,
                "volumes": [
                    {"bind": "/srv/dev-disk-by-label-Files/Config/PiHole", "container": "/etc/pihole"},
                    {"bind": "/srv/dev-disk-by-label-Files/Config/PiHole/DNS", "container": "/etc/dnsmasq.d"}
                ]
            },
            {
                "categories": ["Downloaders"],
                "description": "The qBittorrent project aims to provide an open-source software alternative to µTorrent. qBittorrent is based on the Qt toolkit and libtorrent-rasterbar library.",
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"},
                    {"default": "username", "label": "VPN_USERNAME", "name": "VPN_USERNAME"},
                    {"default": "password", "label": "VPN_PASSWORD", "name": "VPN_PASSWORD"},
                    {"default": "8080", "label": "WEBUI_PORT_ENV", "name": "WEBUI_PORT_ENV"},
                    {"default": "8999", "label": "INCOMING_PORT_ENV", "name": "INCOMING_PORT_ENV"},
                    {"default": "yes", "label": "VPN_ENABLED", "name": "VPN_ENABLED"},
                    {"default": "192.168.68.0/24", "label": "LAN_NETWORK", "name": "LAN_NETWORK"}
                ],
                "image": "markusmcnugen/qbittorrentvpn",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/qbittorrent-icon.png",
                "name": "qbittorrentvpn",
                "platform": "linux",
                "ports": ["8080:8080/tcp", "8999:8999/udp", "8999:8999/tcp"],
                "restart_policy": "unless-stopped",
                "title": "qBittorrentVPN",
                "type": 1,
                "volumes": [
                    {"bind": "/srv/dev-disk-by-label-Files/Config/qBittorrent", "container": "/config"},
                    {"bind": "/portainer/Downloads", "container": "/downloads"},
                    {"bind": "/etc/timezone", "container": "/etc/timezone"}
                ]
            },
            {
                "categories": ["Downloaders", "Video"],
                "description": "Radarr - A fork of Sonarr to work with movies à la Couchpotato.",
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"}
                ],
                "image": "linuxserver/radarr:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/radarr.png",
                "name": "radarr",
                "platform": "linux",
                "ports": ["7878:7878/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Radarr",
                "type": 1,
                "volumes": [
                    {"bind": "/srv/dev-disk-by-label-Files/Config/Radarr", "container": "/config"},
                    {"bind": "/portainer/Downloads", "container": "/downloads"},
                    {"bind": "/portainer/Movies", "container": "/movies"}
                ]
            },
            {
                "categories": ["Management"],
                "description": None,
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"}
                ],
                "image": "linuxserver/smokeping:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/smokeping-icon.png",
                "name": "smokeping",
                "platform": "linux",
                "ports": ["80/tcp"],
                "restart_policy": "unless-stopped",
                "title": "SmokePing",
                "type": 1,
                "volumes": [
                    {"bind": "/srv/dev-disk-by-label-Files/Config/Smokeping", "container": "/config"},
                    {"bind": "/portainer/Files/AppData/Smokeping", "container": "/data"}
                ]
            },
            {
                "categories": ["Downloaders", "Video"],
                "description": "Sonarr (formerly NZBdrone) is a PVR for usenet and bittorrent users. It can monitor multiple RSS feeds for new episodes of your favorite shows and will grab, sort and rename them. It can also be configured to automatically upgrade the quality of files already downloaded when a better quality format becomes available.",
                "env": [
                    {"default": "998", "label": "PUID", "name": "PUID"},
                    {"default": "100", "label": "PGID", "name": "PGID"}
                ],
                "image": "linuxserver/sonarr:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/sonarr-icon.png",
                "name": "sonarr",
                "platform": "linux",
                "ports": ["8989:8989/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Sonarr",
                "type": 1,
                "volumes": [
                    {"bind": "/srv/dev-disk-by-label-Files/Config/Sonarr", "container": "/config"},
                    {"bind": "/dev/rtc", "container": "/dev/rtc"},
                    {"bind": "/portainer/TV", "container": "/tv"},
                    {"bind": "/portainer/Downloads", "container": "/downloads"}
                ]
            },
            {
                "categories": ["Other", "Tools", "Maintenance"],
                "description": "With watchtower you can update the running version of your containerized app simply by pushing a new image to the Docker Hub or your own image registry. Watchtower will pull down your new image, gracefully shut down your existing container and restart it with the same options that were used when it was deployed initially.",
                "image": "containrrr/watchtower:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/watchtower.png",
                "name": "watchtower",
                "note": "It is recommended to manually update your containers but we're including this for those of you that don't care",
                "platform": "linux",
                "restart_policy": "unless-stopped",
                "title": "Watchtower",
                "type": 1,
                "volumes": [{"bind": "/var/run/docker.sock", "container": "/var/run/docker.sock"}]
            },
            {
                "categories": ["Other", "Tools"],
                "description": "Self-hosted, ad-free, privacy-respecting Google metasearch engine.",
                "image": "benbusby/whoogle-search:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/whoogle.png",
                "name": "whoogle",
                "platform": "linux",
                "ports": ["5001:5000/tcp"],
                "restart_policy": "unless-stopped",
                "title": "Whoogle",
                "type": 1,
                "volumes": [{"bind": "/srv/dev-disk-by-label-Files/Config/Whoogle", "container": "/config"}]
            },
            {
                "categories": ["Other", "Downloaders"],
                "description": "YoutubeDL-Material is a Material Design frontend for youtube-dl. It's coded using Angular 9 for the frontend, and Node.js on the backend.",
                "image": "tzahi12345/youtubedl-material:latest",
                "logo": "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Images/ytdlm.png",
                "name": "youtubedl-material",
                "platform": "linux",
                "ports": ["17442:17442/tcp"],
                "restart_policy": "unless-stopped",
                "title": "YouTubeDL-Material",
                "type": 1,
                "volumes": [
                    {"bind": "/srv/dev-disk-by-label-Files/Config/YTDLM", "container": "/app/appdata"},
                    {"bind": "/srv/dev-disk-by-label-Files/YouTube/Video", "container": "/app/video"},
                    {"bind": "/srv/dev-disk-by-label-Files/YouTube/Subscriptions", "container": "/app/subscriptions"},
                    {"bind": "/srv/dev-disk-by-label-Files/YouTube/Users", "container": "/app/users"},
                    {"bind": "/srv/dev-disk-by-label-Files/YouTube/Audio", "container": "/app/audio"}
                ]
            }
        ]
    }
    
    # File paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    existing_file = os.path.join(base_dir, "web", "portainer-template.json")
    backup_file = os.path.join(base_dir, "web", "portainer-template.json.backup")
    
    print("🔄 Converting and merging Portainer templates...")
    print(f"   📁 Base directory: {base_dir}")
    print(f"   📄 Existing templates: {existing_file}")
    
    # Create backup
    if os.path.exists(existing_file):
        import shutil
        shutil.copy2(existing_file, backup_file)
        print(f"   💾 Backup created: {backup_file}")
    
    # Merge templates
    merged_data = merge_templates(existing_file, v2_templates_data["templates"])
    
    # Save merged templates
    save_templates(merged_data, existing_file)
    print(f"   ✅ Merged templates saved to: {existing_file}")
    
    # Validation
    try:
        with open(existing_file, 'r') as f:
            json.load(f)
        print("   ✅ JSON validation passed")
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON validation failed: {e}")
        return 1
    
    print("\n🎉 Template conversion and merge completed successfully!")
    return 0

if __name__ == "__main__":
    exit(main())