#!/bin/bash
"""
🚀 EU-Compliant Deployment Controller
====================================

Automatische Deployment-Steuerung mit EU-DSGVO und Menschenrechts-Compliance.
Verwaltet alle Template-Deployments und stellt One-Click-Funktionalität sicher.
"""

# Farbdefinitionen
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Projektverzeichnis ermitteln
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"
TEMPLATE_FILE="$PROJECT_DIR/web/portainer-template.json"

# Log-Verzeichnis erstellen
mkdir -p "$LOG_DIR"

# Logging-Funktion
log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$LOG_DIR/deployment.log"
}

log_info() {
    log "INFO" "${BLUE}$*${NC}"
}

log_success() {
    log "SUCCESS" "${GREEN}$*${NC}"
}

log_warning() {
    log "WARNING" "${YELLOW}$*${NC}"
}

log_error() {
    log "ERROR" "${RED}$*${NC}"
}

# Banner anzeigen
show_banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                    🚀 EU-Compliant Deployment Controller             ║"
    echo "║                                                                      ║"
    echo "║  🇪🇺 EU-DSGVO Konform  │  🛡️ Menschenrechts-Compliant             ║"
    echo "║  🎯 One-Click Ready    │  ⚡ Automatisch Optimiert                 ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Template-Statistiken anzeigen
show_template_stats() {
    log_info "📊 Analysiere Template-Collection..."
    
    if [ ! -f "$TEMPLATE_FILE" ]; then
        log_error "Template-Datei nicht gefunden: $TEMPLATE_FILE"
        return 1
    fi
    
    # Template-Statistiken mit jq extrahieren
    local total_templates=$(jq '.templates | length' "$TEMPLATE_FILE")
    local container_templates=$(jq '.templates | map(select(.type == 1)) | length' "$TEMPLATE_FILE")
    local stack_templates=$(jq '.templates | map(select(.type == 2)) | length' "$TEMPLATE_FILE")
    local swarm_templates=$(jq '.templates | map(select(.type == 3)) | length' "$TEMPLATE_FILE")
    
    echo -e "${WHITE}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "                          📈 TEMPLATE COLLECTION STATUS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${NC}"
    
    echo -e "${CYAN}📦 Gesamt Templates:${NC}         ${WHITE}$total_templates${NC}"
    echo -e "${CYAN}🐳 Container Templates:${NC}      ${WHITE}$container_templates${NC}"
    echo -e "${CYAN}📚 Docker Compose Stacks:${NC}   ${WHITE}$stack_templates${NC}"
    echo -e "${CYAN}🐝 Docker Swarm Services:${NC}   ${WHITE}$swarm_templates${NC}"
    
    # One-Click Templates zählen
    local one_click_count=$(jq '.templates | map(select(.categories[]? == "One-Click Deployment")) | length' "$TEMPLATE_FILE" 2>/dev/null || echo "0")
    echo -e "${CYAN}🚀 One-Click Ready:${NC}          ${WHITE}$one_click_count${NC}"
    
    # EU-Compliance Status
    local eu_compliant=$(jq '.metadata.eu_compliance_enabled // false' "$TEMPLATE_FILE" 2>/dev/null)
    local gdpr_ready=$(jq '.metadata.gdpr_compliant // false' "$TEMPLATE_FILE" 2>/dev/null)
    
    echo -e "${CYAN}🇪🇺 EU-DSGVO Konform:${NC}       ${GREEN}$([ "$eu_compliant" = "true" ] && echo "✅ Aktiv" || echo "❌ Inaktiv")${NC}"
    echo -e "${CYAN}🛡️ DSGVO-Ready:${NC}              ${GREEN}$([ "$gdpr_ready" = "true" ] && echo "✅ Aktiv" || echo "❌ Inaktiv")${NC}"
    
    echo ""
}

# Beliebte Apps Status prüfen
check_popular_apps() {
    log_info "🔍 Prüfe Verfügbarkeit beliebter Selfhosted-Apps..."
    
    # Liste der wichtigsten Apps
    declare -A popular_apps
    popular_apps=(
        ["nextcloud"]="☁️ Nextcloud"
        ["jellyfin"]="🎬 Jellyfin"
        ["bitwarden"]="🔐 Bitwarden"
        ["vaultwarden"]="🔐 Vaultwarden"
        ["heimdall"]="🏠 Heimdall"
        ["plex"]="📺 Plex"
        ["portainer"]="🐳 Portainer"
        ["gitea"]="📚 Gitea"
        ["nginx"]="🌐 Nginx"
        ["mariadb"]="🗄️ MariaDB"
        ["photoprism"]="📸 PhotoPrism"
        ["pi-hole"]="🕳️ Pi-hole"
        ["bookstack"]="📖 BookStack"
        ["freshrss"]="📰 FreshRSS"
        ["homer"]="🏠 Homer"
        ["duplicati"]="💾 Duplicati"
        ["syncthing"]="🔄 Syncthing"
        ["wireguard"]="🔒 WireGuard"
    )
    
    echo -e "${WHITE}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "                      🌟 BELIEBTE SELFHOSTED APPS STATUS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${NC}"
    
    local found_count=0
    local total_count=${#popular_apps[@]}
    
    for app_key in "${!popular_apps[@]}"; do
        local app_name="${popular_apps[$app_key]}"
        
        # Prüfe ob App in Templates vorhanden ist (case insensitive)
        local found=$(jq -r --arg app "$app_key" '.templates[] | select(.name // "" | ascii_downcase | contains($app)) | .name' "$TEMPLATE_FILE" 2>/dev/null | head -1)
        
        if [ -n "$found" ]; then
            echo -e "${GREEN}✅${NC} $app_name ${CYAN}($found)${NC}"
            ((found_count++))
        else
            echo -e "${RED}❌${NC} $app_name ${YELLOW}(Nicht gefunden)${NC}"
        fi
    done
    
    echo ""
    echo -e "${CYAN}📊 App-Verfügbarkeit:${NC} ${WHITE}$found_count/$total_count${NC} ${GREEN}($(echo "scale=1; $found_count * 100 / $total_count" | bc)%)${NC}"
    echo ""
}

# EU-Compliance Validation
validate_eu_compliance() {
    log_info "🇪🇺 Führe EU-DSGVO Compliance-Validation durch..."
    
    # Python-Validationsskript verwenden
    if [ -f "$PROJECT_DIR/scripts/auto_template_integrator.py" ]; then
        cd "$PROJECT_DIR"
        if [ -f ".venv/bin/python" ]; then
            .venv/bin/python -c "
import json
import sys
from scripts.auto_template_integrator import check_eu_compliance

# Template-Datei laden
with open('web/portainer-template.json', 'r') as f:
    data = json.load(f)

templates = data.get('templates', [])
compliant_count = 0
violation_count = 0
violations = []

for template in templates:
    is_compliant, template_violations = check_eu_compliance(template)
    if is_compliant:
        compliant_count += 1
    else:
        violation_count += 1
        violations.extend(template_violations)

print(f'Compliant Templates: {compliant_count}')
print(f'Non-Compliant Templates: {violation_count}')
print(f'Total Violations: {len(violations)}')

if violations:
    print('\\nTop Violations:')
    for i, violation in enumerate(violations[:5]):
        print(f'  {i+1}. {violation}')
"
        else
            log_warning "Python virtual environment nicht gefunden"
        fi
    else
        log_warning "EU-Compliance Validator nicht gefunden"
    fi
    
    echo ""
}

# Automatische Integration durchführen
run_auto_integration() {
    log_info "🤖 Starte automatische Template-Integration..."
    
    cd "$PROJECT_DIR"
    
    if [ ! -f ".venv/bin/python" ]; then
        log_error "Python virtual environment nicht gefunden. Bitte setup.sh ausführen."
        return 1
    fi
    
    # Backup erstellen
    local backup_file="$PROJECT_DIR/web/portainer-template.backup.$(date +%s).json"
    cp "$TEMPLATE_FILE" "$backup_file"
    log_info "💾 Backup erstellt: $(basename "$backup_file")"
    
    # Automatische Integration starten
    .venv/bin/python scripts/auto_template_integrator.py
    
    if [ $? -eq 0 ]; then
        log_success "✅ Automatische Integration erfolgreich abgeschlossen!"
        
        # Neue Statistiken anzeigen
        show_template_stats
        
        # Git Commit (falls Git verfügbar)
        if [ -d ".git" ]; then
            log_info "📝 Erstelle Git-Commit..."
            git add .
            git commit -m "🤖 Automated EU-compliant template integration $(date)" || true
            log_info "🚀 Push to GitHub..."
            git push origin main || log_warning "Git push fehlgeschlagen"
        fi
        
    else
        log_error "❌ Automatische Integration fehlgeschlagen"
        
        # Backup wiederherstellen
        cp "$backup_file" "$TEMPLATE_FILE"
        log_info "🔄 Backup wiederhergestellt"
        return 1
    fi
}

# GitHub Status prüfen
check_github_status() {
    log_info "🐙 Prüfe GitHub-Integration Status..."
    
    if [ ! -d ".git" ]; then
        log_warning "Kein Git-Repository gefunden"
        return 1
    fi
    
    cd "$PROJECT_DIR"
    
    # Remote URL prüfen
    local remote_url=$(git remote get-url origin 2>/dev/null)
    if [ -n "$remote_url" ]; then
        echo -e "${CYAN}📡 Remote Repository:${NC} ${WHITE}$remote_url${NC}"
    else
        log_warning "Kein Git-Remote konfiguriert"
    fi
    
    # Status prüfen
    local status=$(git status --porcelain 2>/dev/null)
    if [ -z "$status" ]; then
        echo -e "${GREEN}✅ Working Directory Clean${NC}"
    else
        echo -e "${YELLOW}⚠️ Uncommitted Changes:${NC}"
        git status --short
    fi
    
    # GitHub Raw Access testen
    if [ -n "$remote_url" ]; then
        local github_raw_url="https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template.json"
        local http_status=$(curl -s -o /dev/null -w "%{http_code}" "$github_raw_url" 2>/dev/null)
        
        if [ "$http_status" = "200" ]; then
            echo -e "${GREEN}✅ GitHub Raw Access:${NC} ${WHITE}Funktioniert (HTTP $http_status)${NC}"
        else
            echo -e "${RED}❌ GitHub Raw Access:${NC} ${WHITE}Fehler (HTTP $http_status)${NC}"
        fi
    fi
    
    echo ""
}

# Docker Status prüfen
check_docker_status() {
    log_info "🐳 Prüfe Docker-Umgebung..."
    
    # Docker verfügbar?
    if command -v docker >/dev/null 2>&1; then
        local docker_version=$(docker --version 2>/dev/null)
        echo -e "${GREEN}✅ Docker:${NC} ${WHITE}$docker_version${NC}"
        
        # Docker Compose verfügbar?
        if command -v docker-compose >/dev/null 2>&1; then
            local compose_version=$(docker-compose --version 2>/dev/null)
            echo -e "${GREEN}✅ Docker Compose:${NC} ${WHITE}$compose_version${NC}"
        else
            echo -e "${YELLOW}⚠️ Docker Compose:${NC} ${WHITE}Nicht installiert${NC}"
        fi
        
        # Docker läuft?
        if docker info >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Docker Daemon:${NC} ${WHITE}Läuft${NC}"
        else
            echo -e "${RED}❌ Docker Daemon:${NC} ${WHITE}Nicht erreichbar${NC}"
        fi
        
    else
        echo -e "${RED}❌ Docker:${NC} ${WHITE}Nicht installiert${NC}"
    fi
    
    echo ""
}

# Hauptmenü
show_menu() {
    echo -e "${WHITE}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "                              🎯 AKTIONEN MENÜ"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${NC}"
    
    echo -e "${CYAN}1)${NC} 📊 Template-Statistiken anzeigen"
    echo -e "${CYAN}2)${NC} 🌟 Beliebte Apps Status prüfen"
    echo -e "${CYAN}3)${NC} 🇪🇺 EU-Compliance Validation"
    echo -e "${CYAN}4)${NC} 🤖 Automatische Template-Integration"
    echo -e "${CYAN}5)${NC} 🐙 GitHub-Integration Status"
    echo -e "${CYAN}6)${NC} 🐳 Docker-Umgebung prüfen"
    echo -e "${CYAN}7)${NC} 🚀 Vollständiger System-Check"
    echo -e "${CYAN}8)${NC} 🔄 Live Template-URL anzeigen"
    echo -e "${CYAN}0)${NC} 🚪 Beenden"
    echo ""
}

# Live Template URL anzeigen
show_live_url() {
    echo -e "${WHITE}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "                            🌐 LIVE TEMPLATE-URLS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${NC}"
    
    echo -e "${CYAN}🔗 GitHub Raw URL:${NC}"
    echo -e "${WHITE}   https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template.json${NC}"
    
    echo ""
    echo -e "${CYAN}📋 Für Portainer verwenden:${NC}"
    echo -e "${WHITE}   1. Portainer öffnen → Settings → App Templates${NC}"
    echo -e "${WHITE}   2. URL eingeben und speichern${NC}"
    echo -e "${WHITE}   3. App Templates neu laden${NC}"
    
    echo ""
    echo -e "${GREEN}🎯 One-Click Deployment:${NC} ${WHITE}Alle Templates sind vorkonfiguriert!${NC}"
    echo ""
}

# Vollständiger System-Check
full_system_check() {
    log_info "🚀 Führe vollständigen System-Check durch..."
    echo ""
    
    show_template_stats
    check_popular_apps
    validate_eu_compliance
    check_github_status
    check_docker_status
    
    log_success "✅ Vollständiger System-Check abgeschlossen!"
}

# Hauptfunktion
main() {
    show_banner
    
    # Arbeitsverzeichnis wechseln
    cd "$PROJECT_DIR"
    
    while true; do
        show_menu
        echo -n -e "${YELLOW}Wähle eine Aktion (0-8): ${NC}"
        read -r choice
        echo ""
        
        case $choice in
            1)
                show_template_stats
                ;;
            2)
                check_popular_apps
                ;;
            3)
                validate_eu_compliance
                ;;
            4)
                run_auto_integration
                ;;
            5)
                check_github_status
                ;;
            6)
                check_docker_status
                ;;
            7)
                full_system_check
                ;;
            8)
                show_live_url
                ;;
            0)
                log_info "👋 Auf Wiedersehen! EU-Compliant Deployment Controller beendet."
                exit 0
                ;;
            *)
                log_warning "Ungültige Auswahl. Bitte wähle 0-8."
                ;;
        esac
        
        echo ""
        echo -n -e "${YELLOW}Drücke Enter für das Hauptmenü...${NC}"
        read -r
        echo ""
    done
}

# Skript starten
main "$@"