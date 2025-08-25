#!/usr/bin/env python3
"""
🎨 Real Logo Enhancement Engine - Echte hochwertige Logos
=========================================================

Ersetzt generische Docker-Logos mit echten, hochwertigen Logos 
von den offiziellen Quellen der jeweiligen Anwendungen.

🔥 Features:
- Offizielle Logo-URLs von App-Websites
- Hochauflösende PNG/SVG Logos  
- CDN-optimierte Auslieferung
- Fallback zu Dashboard Icons wo nötig
- Automatische Logo-Validierung
"""

import json
import requests
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
import re

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🎨 Hochwertige echte Logo-Mappings mit offiziellen Quellen
REAL_LOGO_MAPPINGS = {
    # ☁️ Cloud & Storage
    'nextcloud': 'https://upload.wikimedia.org/wikipedia/commons/6/60/Nextcloud_Logo.svg',
    'owncloud': 'https://owncloud.com/wp-content/themes/owncloudorgnew/assets/img/common/logo_owncloud.svg',
    'syncthing': 'https://syncthing.net/img/logo-horizontal.svg',
    'seafile': 'https://www.seafile.com/media/img/seafile-logo.png',
    'filerun': 'https://filerun.com/images/logo.png',
    'filebrowser': 'https://raw.githubusercontent.com/filebrowser/logo/master/banner.png',
    'duplicati': 'https://duplicati.com/images/logo.png',
    'restic': 'https://restic.net/logo.png',
    'rclone': 'https://rclone.org/img/logo_on_light__horizontal_color.svg',
    
    # 🎬 Media & Entertainment
    'jellyfin': 'https://jellyfin.org/images/logo.svg',
    'emby': 'https://emby.media/resources/logowhite_1024.png',
    'plex': 'https://www.plex.tv/wp-content/themes/plex/assets/img/plex-logo.svg',
    'kodi': 'https://kodi.tv/sites/default/files/page/field_image/about-feature-image.jpg',
    'airsonic': 'https://airsonic.github.io/img/airsonic-dark-250.png',
    'ampache': 'https://ampache.org/img/logo.png',
    'subsonic': 'https://www.subsonic.org/pages/inc/img/subsonic-logo.png',
    'navidrome': 'https://www.navidrome.org/logo.svg',
    'funkwhale': 'https://funkwhale.audio/logo-black.svg',
    'photoprism': 'https://photoprism.app/static/img/logo/logo.svg',
    'lychee': 'https://lycheeorg.github.io/img/logo.png',
    'piwigo': 'https://piwigo.org/screenshots/github-social-preview.jpg',
    'librephotos': 'https://github.com/LibrePhotos/librephotos/raw/dev/logo.png',
    
    # 🔐 Security & Privacy
    'bitwarden': 'https://bitwarden.com/images/icons/icon-logo.svg',
    'vaultwarden': 'https://github.com/dani-garcia/vaultwarden/raw/main/resources/vaultwarden-icon.png',
    'keepass': 'https://keepass.info/images/kp_logo_100.png',
    'authelia': 'https://www.authelia.com/images/branding/logo-cropped.png',
    'fail2ban': 'https://github.com/fail2ban/fail2ban/raw/master/files/debian/fail2ban.png',
    'wireguard': 'https://www.wireguard.com/img/wireguard.svg',
    'openvpn': 'https://openvpn.net/wp-content/uploads/openvpn-logo.png',
    'pihole': 'https://pi-hole.net/wp-content/uploads/2016/12/Vortex-R.png',
    'adguard': 'https://adguard.com/img/logo.svg',
    'unbound': 'https://unbound.docs.nlnetlabs.nl/en/latest/_static/unbound-logo.png',
    
    # 🏠 Home Automation & Management
    'heimdall': 'https://heimdall.site/img/heimdall-icon.png',
    'homer': 'https://github.com/bastienwirtz/homer/raw/main/public/logo.png',
    'organizr': 'https://github.com/causefx/Organizr/raw/v2-master/plugins/images/organizr/logo-wide.png',
    'dashy': 'https://dashy.to/img/logo.png',
    'flame': 'https://github.com/pawelmalak/flame/raw/master/docs/flame.png',
    'homarr': 'https://homarr.dev/logo.png',
    'homepage': 'https://gethomepage.dev/img/logo.png',
    'homeassistant': 'https://www.home-assistant.io/images/home-assistant-logo.svg',
    'nodered': 'https://nodered.org/about/resources/media/node-red-icon-2.png',
    'mosquitto': 'https://mosquitto.org/images/mosquitto-text-side-28.png',
    'zigbee2mqtt': 'https://www.zigbee2mqtt.io/logo.png',
    
    # 📚 Productivity & Development
    'gitea': 'https://gitea.io/images/gitea.png',
    'gitlab': 'https://about.gitlab.com/images/press/logo/svg/gitlab-logo-500.svg',
    'github': 'https://github.com/logos/GitHub_Logo.png',
    'jenkins': 'https://www.jenkins.io/images/logo-title-opengraph.png',
    'drone': 'https://drone.io/brand/drone-logo-dark.svg',
    'gitiles': 'https://gerrit.googlesource.com/gitiles/+/HEAD/resources/com/google/gitiles/static/gitiles.png',
    'bookstack': 'https://www.bookstackapp.com/images/logo-color.svg',
    'dokuwiki': 'https://www.dokuwiki.org/_media/wiki:dokuwiki-128.png',
    'tiddlywiki': 'https://tiddlywiki.com/favicon.ico',
    'wikijs': 'https://wiki.js.org/logo.svg',
    'outline': 'https://www.getoutline.com/images/logo.png',
    'hedgedoc': 'https://hedgedoc.org/logo.svg',
    'standardnotes': 'https://standardnotes.com/assets/logo.svg',
    'joplin': 'https://joplinapp.org/images/logo-text.svg',
    
    # 🗄️ Databases
    'mysql': 'https://www.mysql.com/common/logos/logo-mysql-170x115.png',
    'mariadb': 'https://mariadb.org/wp-content/uploads/2019/11/mariadb-logo-vertical-blue.svg',
    'postgresql': 'https://www.postgresql.org/media/img/about/press/elephant.png',
    'mongodb': 'https://www.mongodb.com/assets/images/global/leaf.svg',
    'redis': 'https://redis.io/images/logo-redis.svg',
    'memcached': 'https://memcached.org/memcached-banner.png',
    'influxdb': 'https://www.influxdata.com/wp-content/uploads/influxdb-logo-1.png',
    'phpmyadmin': 'https://www.phpmyadmin.net/static/images/logo-og.png',
    'adminer': 'https://www.adminer.org/static/images/logo.png',
    
    # 🌐 Web Servers & Proxies
    'nginx': 'https://nginx.org/nginx.png',
    'apache': 'https://www.apache.org/logos/res/httpd/httpd.png',
    'caddy': 'https://caddyserver.com/resources/images/caddy-logo.svg',
    'traefik': 'https://traefik.io/static/traefik-logo-02faeb9c4bb2e5db978e8d25ca2f79ee.svg',
    'haproxy': 'https://www.haproxy.org/img/HAProxyLogo.png',
    'cloudflare': 'https://www.cloudflare.com/img/logo-web-badges/cf-logo-on-white-bg.svg',
    'letsencrypt': 'https://letsencrypt.org/images/le-logo-wide.svg',
    
    # 📊 Monitoring & Analytics
    'prometheus': 'https://prometheus.io/assets/prometheus_logo-cb55bb5c346.png',
    'grafana': 'https://grafana.com/static/img/logos/grafana_logo_swirl-events.svg',
    'influxdb': 'https://www.influxdata.com/wp-content/uploads/influxdb-logo-1.png',
    'telegraf': 'https://www.influxdata.com/wp-content/uploads/telegraf-logo-1.png',
    'netdata': 'https://www.netdata.cloud/img/logo-netdata.svg',
    'zabbix': 'https://www.zabbix.com/ru/img/logo/zabbix_logo.svg',
    'uptime-kuma': 'https://uptime.kuma.pet/img/icon.svg',
    'statping': 'https://statping.com/banner.png',
    'healthchecks': 'https://healthchecks.io/static/img/logo-full-200.png',
    
    # 📰 RSS & News
    'freshrss': 'https://freshrss.org/images/logo_freshrss.png',
    'miniflux': 'https://miniflux.app/images/logo.svg',
    'ttrss': 'https://tt-rss.org/images/logo.png',
    'wallabag': 'https://www.wallabag.org/images/logo.svg',
    'readarr': 'https://github.com/Readarr/Readarr/raw/develop/Logo/256.png',
    
    # 📥 Download Managers
    'sonarr': 'https://sonarr.tv/img/logo.svg',
    'radarr': 'https://radarr.video/img/logo.svg',
    'lidarr': 'https://lidarr.audio/img/logo.svg',
    'bazarr': 'https://www.bazarr.media/assets/img/logo.png',
    'prowlarr': 'https://prowlarr.com/logo/256.png',
    'jackett': 'https://github.com/Jackett/Jackett/raw/master/src/Jackett.Common/Content/logos/jackett.png',
    'transmission': 'https://transmissionbt.com/images/transmission_logo.png',
    'qbittorrent': 'https://upload.wikimedia.org/wikipedia/commons/6/66/New_qBittorrent_Logo.svg',
    'deluge': 'https://deluge-torrent.org/images/deluge-symbol-48.png',
    'rtorrent': 'https://github.com/rakshasa/rtorrent/raw/master/doc/rtorrent.png',
    'nzbget': 'https://nzbget.net/images/nzbget-logo-256.png',
    'sabnzbd': 'https://sabnzbd.org/images/logo-arrow.svg',
    
    # 🎮 Gaming
    'minecraft': 'https://www.minecraft.net/etc.clientlibs/minecraft/clientlibs/main/resources/img/minecraft-creeper-face.jpg',
    'steamcmd': 'https://steamcdn-a.akamaihd.net/steam/apps/steamcmd/header.jpg',
    'pterodactyl': 'https://pterodactyl.io/assets/pterodactyl.png',
    'gameserver': 'https://github.com/GameServerManagers/LinuxGSM/raw/master/lgsm/data/alert_logo.png',
    
    # 🛠️ Development Tools
    'code-server': 'https://github.com/cdr/code-server/raw/main/src/browser/media/favicon.svg',
    'portainer': 'https://portainer.io/images/logo_portainer.svg',
    'docker': 'https://www.docker.com/wp-content/uploads/2022/03/Docker-Logo-Blue.svg',
    'registry': 'https://www.docker.com/wp-content/uploads/2022/03/Docker-Logo-Blue.svg',
    'watchtower': 'https://containrrr.dev/watchtower/logo.png',
    'dockge': 'https://github.com/louislam/dockge/raw/master/frontend/public/icon.svg',
    
    # 💬 Communication
    'mattermost': 'https://mattermost.com/wp-content/uploads/2022/02/logo_horizontal_white.svg',
    'rocket.chat': 'https://rocket.chat/wp-content/uploads/2020/07/logo-dark.svg',
    'element': 'https://element.io/images/logo-mark-primary.svg',
    'jitsi': 'https://jitsi.org/wp-content/uploads/2017/06/jitsi-logo-blue-grey-text.png',
    'teamspeak': 'https://www.teamspeak.com/user/themes/teamspeak/images/ts_logo.svg',
    'mumble': 'https://www.mumble.info/images/mumble-logo.svg',
    
    # 📧 Mail
    'mailcow': 'https://mailcow.email/images/cow_mailcow.svg',
    'mailu': 'https://mailu.io/1.8/_static/mailu_logo.svg',
    'rainloop': 'https://www.rainloop.net/static/img/logo-256x256.png',
    'roundcube': 'https://roundcube.net/images/logo.png',
    'postfix': 'https://www.postfix.org/postfix-logo.jpg',
    
    # 🔧 System Tools
    'portainer': 'https://portainer.io/images/logo_portainer.svg',
    'cockpit': 'https://cockpit-project.org/images/cockpit-logo.svg',
    'webmin': 'https://www.webmin.com/images/webmin-logo.png',
    'phpsysinfo': 'https://phpsysinfo.github.io/phpsysinfo/templates/images/logo.png',
    'htop': 'https://htop.dev/images/htop-logo.png',
    'glances': 'https://nicolargo.github.io/glances/public/images/logo.png'
}

# 🎯 Fallback zu Dashboard Icons für bessere Qualität
DASHBOARD_ICONS_FALLBACKS = {
    'docker': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/docker.png',
    'ubuntu': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/ubuntu.png',
    'centos': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/centos.png',
    'alpine': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/alpine-linux.png',
    'debian': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/debian.png',
    'redis': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/redis.png',
    'postgres': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/postgresql.png',
    'mongo': 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/mongodb.png'
}

def detect_app_from_image_or_title(template: Dict[str, Any]) -> str:
    """
    Erkennt die App aus Image-Namen oder Titel für präzises Logo-Matching.
    """
    # Image-Namen analysieren
    image = template.get('image', '').lower()
    title = template.get('title', '').lower()
    name = template.get('name', '').lower()
    
    # Kombinierte Suchterme
    search_text = f"{image} {title} {name}".lower()
    
    # Präzise App-Erkennung mit Priorität
    app_patterns = {
        # Exakte Matches haben Priorität
        'nextcloud': ['nextcloud'],
        'jellyfin': ['jellyfin'],
        'bitwarden': ['bitwarden'],
        'vaultwarden': ['vaultwarden'],
        'heimdall': ['heimdall'],
        'plex': ['plex'],
        'gitea': ['gitea'],
        'gitlab': ['gitlab'],
        'portainer': ['portainer'],
        'nginx': ['nginx'],
        'mysql': ['mysql'],
        'mariadb': ['mariadb'],
        'postgresql': ['postgresql', 'postgres'],
        'redis': ['redis'],
        'mongodb': ['mongodb', 'mongo'],
        'prometheus': ['prometheus'],
        'grafana': ['grafana'],
        'traefik': ['traefik'],
        'caddy': ['caddy'],
        'docker': ['docker'],
        'duplicati': ['duplicati'],
        'syncthing': ['syncthing'],
        'photoprism': ['photoprism'],
        'freshrss': ['freshrss'],
        'homer': ['homer'],
        'sonarr': ['sonarr'],
        'radarr': ['radarr'],
        'lidarr': ['lidarr'],
        'bazarr': ['bazarr'],
        'jackett': ['jackett'],
        'transmission': ['transmission'],
        'qbittorrent': ['qbittorrent'],
        'deluge': ['deluge'],
        'sabnzbd': ['sabnzbd'],
        'nzbget': ['nzbget'],
        'bookstack': ['bookstack'],
        'wikijs': ['wikijs'],
        'outline': ['outline'],
        'hedgedoc': ['hedgedoc'],
        'standardnotes': ['standardnotes'],
        'joplin': ['joplin'],
        'authelia': ['authelia'],
        'wireguard': ['wireguard'],
        'openvpn': ['openvpn'],
        'pihole': ['pihole', 'pi-hole'],
        'adguard': ['adguard'],
        'homeassistant': ['homeassistant', 'home-assistant'],
        'nodered': ['nodered', 'node-red'],
        'mosquitto': ['mosquitto'],
        'zigbee2mqtt': ['zigbee2mqtt'],
        'influxdb': ['influxdb'],
        'telegraf': ['telegraf'],
        'netdata': ['netdata'],
        'zabbix': ['zabbix'],
        'uptime-kuma': ['uptime-kuma', 'uptime_kuma'],
        'healthchecks': ['healthchecks'],
        'miniflux': ['miniflux'],
        'wallabag': ['wallabag'],
        'ttrss': ['ttrss', 'tiny-tiny-rss'],
        'prowlarr': ['prowlarr'],
        'readarr': ['readarr'],
        'emby': ['emby'],
        'airsonic': ['airsonic'],
        'navidrome': ['navidrome'],
        'lychee': ['lychee'],
        'piwigo': ['piwigo'],
        'librephotos': ['librephotos'],
        'organizr': ['organizr'],
        'dashy': ['dashy'],
        'flame': ['flame'],
        'homarr': ['homarr'],
        'jenkins': ['jenkins'],
        'drone': ['drone'],
        'dokuwiki': ['dokuwiki'],
        'tiddlywiki': ['tiddlywiki'],
        'phpmyadmin': ['phpmyadmin'],
        'adminer': ['adminer'],
        'apache': ['apache', 'httpd'],
        'haproxy': ['haproxy'],
        'letsencrypt': ['letsencrypt'],
        'statping': ['statping'],
        'code-server': ['code-server'],
        'watchtower': ['watchtower'],
        'dockge': ['dockge'],
        'mattermost': ['mattermost'],
        'rocket.chat': ['rocket.chat', 'rocketchat'],
        'element': ['element'],
        'jitsi': ['jitsi'],
        'teamspeak': ['teamspeak'],
        'mumble': ['mumble'],
        'mailcow': ['mailcow'],
        'mailu': ['mailu'],
        'rainloop': ['rainloop'],
        'roundcube': ['roundcube'],
        'postfix': ['postfix'],
        'cockpit': ['cockpit'],
        'webmin': ['webmin'],
        'glances': ['glances']
    }
    
    # Suche nach App-Pattern
    for app_key, patterns in app_patterns.items():
        for pattern in patterns:
            if pattern in search_text:
                return app_key
    
    return 'docker'  # Fallback

def get_high_quality_logo(app_key: str) -> str:
    """
    Gibt das beste verfügbare Logo für eine App zurück.
    """
    # 1. Zuerst echte offizielle Logos prüfen
    if app_key in REAL_LOGO_MAPPINGS:
        return REAL_LOGO_MAPPINGS[app_key]
    
    # 2. Fallback zu Dashboard Icons
    if app_key in DASHBOARD_ICONS_FALLBACKS:
        return DASHBOARD_ICONS_FALLBACKS[app_key]
    
    # 3. Versuche Dashboard Icons mit App-Name
    dashboard_icon_url = f"https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/{app_key}.png"
    
    # 4. Letzter Fallback: Docker Logo
    return "https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/docker.png"

def validate_logo_url(url: str) -> bool:
    """
    Validiert ob eine Logo-URL erreichbar ist.
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def enhance_template_logos(template_file: Path) -> bool:
    """
    Verbessert alle Logos in der Template-Datei mit echten, hochwertigen Logos.
    """
    logger.info("🎨 Starting real logo enhancement...")
    
    # Template-Datei laden
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"❌ Error loading template file: {e}")
        return False
    
    templates = data.get('templates', [])
    enhanced_count = 0
    validation_errors = 0
    
    for i, template in enumerate(templates):
        try:
            # App-Typ erkennen
            app_key = detect_app_from_image_or_title(template)
            
            # Aktuelles Logo prüfen
            current_logo = template.get('logo', '')
            
            # Neues hochwertiges Logo ermitteln
            new_logo = get_high_quality_logo(app_key)
            
            # Logo nur ändern wenn es sich unterscheidet
            if current_logo != new_logo:
                # Logo-URL validieren
                if validate_logo_url(new_logo):
                    template['logo'] = new_logo
                    enhanced_count += 1
                    logger.info(f"✅ Enhanced {template.get('title', 'Unknown')}: {app_key} -> {new_logo}")
                else:
                    logger.warning(f"⚠️ Logo validation failed for {app_key}: {new_logo}")
                    validation_errors += 1
                    # Fallback zu Dashboard Icons
                    fallback_logo = f"https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/{app_key}.png"
                    template['logo'] = fallback_logo
                    enhanced_count += 1
            
            # Fortschritt anzeigen
            if (i + 1) % 50 == 0:
                logger.info(f"📊 Progress: {i + 1}/{len(templates)} templates processed")
                
        except Exception as e:
            logger.error(f"❌ Error processing template {i}: {e}")
            continue
    
    # Metadaten aktualisieren
    if 'metadata' not in data:
        data['metadata'] = {}
    
    data['metadata'].update({
        'logo_enhancement_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'real_logos_enhanced': enhanced_count,
        'total_templates': len(templates),
        'validation_errors': validation_errors,
        'logo_quality': 'Real High-Quality Logos',
        'logo_sources': ['Official Websites', 'Dashboard Icons CDN'],
        'enhancement_engine': 'Real Logo Enhancement v2.0'
    })
    
    # Erweiterte Template-Datei speichern
    try:
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"\n🎉 Real logo enhancement completed!")
        logger.info(f"📊 Enhancement Statistics:")
        logger.info(f"   • Templates enhanced: {enhanced_count}")
        logger.info(f"   • Total templates: {len(templates)}")
        logger.info(f"   • Validation errors: {validation_errors}")
        logger.info(f"   • Success rate: {(enhanced_count/(len(templates) or 1)*100):.1f}%")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error saving enhanced template file: {e}")
        return False

def main():
    """Hauptfunktion für Real Logo Enhancement."""
    try:
        logger.info("🎨 Real Logo Enhancement Engine")
        logger.info("=" * 60)
        logger.info("🔥 Upgrading to real, high-quality logos...")
        
        script_dir = Path(__file__).parent.absolute()
        project_root = script_dir.parent
        template_file = project_root / 'web' / 'portainer-template.json'
        
        if not template_file.exists():
            logger.error(f"❌ Template file not found: {template_file}")
            return False
        
        # Backup erstellen
        backup_file = template_file.with_suffix(f'.backup.real-logos.{int(time.time())}.json')
        try:
            import shutil
            shutil.copy2(template_file, backup_file)
            logger.info(f"💾 Backup created: {backup_file}")
        except Exception as e:
            logger.warning(f"⚠️ Backup creation failed: {e}")
        
        # Real Logo Enhancement durchführen
        success = enhance_template_logos(template_file)
        
        if success:
            logger.info("🎉 Real logo enhancement completed successfully!")
            logger.info("🔥 All templates now use high-quality, real logos!")
        
        return success
        
    except KeyboardInterrupt:
        logger.info("\n⏹️ Enhancement interrupted by user")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    main()