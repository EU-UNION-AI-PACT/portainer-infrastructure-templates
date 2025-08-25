#!/bin/bash

# 🚀 MASTER ALL-IN-ONE DEPLOYMENT SCRIPT
# Deployt die komplette Portainer Infrastructure Templates Suite

echo "🚀 PORTAINER INFRASTRUCTURE TEMPLATES - MASTER DEPLOYMENT"
echo "=========================================================="
echo ""

# Repository Information
REPO_URL="https://github.com/YOUR_USERNAME/portainer-infrastructure-templates"
TEMPLATE_URL="https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/portainer-template.json"

echo "📥 Downloading deployment configurations..."

# Create deployment directory
mkdir -p portainer-infrastructure
cd portainer-infrastructure

# Download all stack files
echo "🐳 Downloading Docker Compose stacks..."
curl -s -o docker-compose.yml "$REPO_URL/raw/main/docker-compose.yml"
curl -s -o free-alternatives.yml "$REPO_URL/raw/main/stacks/free-alternatives.yml"
curl -s -o extended-security-tools.yml "$REPO_URL/raw/main/stacks/extended-security-tools.yml"
curl -s -o security-only.yml "$REPO_URL/raw/main/stacks/security-only.yml"
curl -s -o monitoring-only.yml "$REPO_URL/raw/main/stacks/monitoring-only.yml"
curl -s -o vpn-only.yml "$REPO_URL/raw/main/stacks/vpn-only.yml"
curl -s -o development.yml "$REPO_URL/raw/main/stacks/development.yml"

# Download environment template
curl -s -o .env.example "$REPO_URL/raw/main/.env.example"
cp .env.example .env

echo "✅ All files downloaded successfully!"
echo ""

# Show deployment options
echo "🎯 DEPLOYMENT OPTIONS:"
echo "======================"
echo ""
echo "1. 🆓 FREE ALTERNATIVES (Keeper→Vaultwarden, Auth0→Keycloak, etc.):"
echo "   docker-compose -f free-alternatives.yml up -d"
echo ""
echo "2. 🔧 EXTENDED SECURITY TOOLS (SIEM, DevSecOps, Privacy):"
echo "   docker-compose -f extended-security-tools.yml up -d"
echo ""
echo "3. 🛡️ SECURITY ONLY (Wazuh, CrowdSec, Vault):"
echo "   docker-compose -f security-only.yml up -d"
echo ""
echo "4. 📊 MONITORING ONLY (Prometheus, Grafana, Loki):"
echo "   docker-compose -f monitoring-only.yml up -d"
echo ""
echo "5. 🔐 VPN ONLY (WireGuard, OpenVPN, Tailscale):"
echo "   docker-compose -f vpn-only.yml up -d"
echo ""
echo "6. 💻 DEVELOPMENT (GitLab, Jenkins, SonarQube):"
echo "   docker-compose -f development.yml up -d"
echo ""
echo "7. 🚀 COMPLETE INFRASTRUCTURE (All-in-One):"
echo "   docker-compose up -d"
echo ""

# Interactive deployment
read -p "🤔 Which stack would you like to deploy? (1-7, or 'skip' to configure manually): " choice

case $choice in
    1)
        echo "🆓 Deploying Free Alternatives Stack..."
        docker-compose -f free-alternatives.yml up -d
        echo ""
        echo "🌐 Access URLs:"
        echo "   Vaultwarden (Keeper):     http://localhost:8080"
        echo "   Keycloak (Auth0):         http://localhost:8081"
        echo "   Authentik (Authy):        http://localhost:8082"
        echo "   FusionAuth (Okta):        http://localhost:8084"
        ;;
    2)
        echo "🔧 Deploying Extended Security Tools..."
        docker-compose -f extended-security-tools.yml up -d
        echo ""
        echo "🌐 Access URLs:"
        echo "   Wazuh Manager:            http://localhost:55000"
        echo "   OWASP ZAP:                http://localhost:8080"
        echo "   Pi-hole:                  http://localhost:8082"
        echo "   TheHive:                  http://localhost:9000"
        ;;
    3)
        echo "🛡️ Deploying Security Only Stack..."
        docker-compose -f security-only.yml up -d
        ;;
    4)
        echo "📊 Deploying Monitoring Only Stack..."
        docker-compose -f monitoring-only.yml up -d
        echo ""
        echo "🌐 Access URLs:"
        echo "   Grafana:                  http://localhost:3000"
        echo "   Prometheus:               http://localhost:9090"
        echo "   Kibana:                   http://localhost:5601"
        ;;
    5)
        echo "🔐 Deploying VPN Only Stack..."
        docker-compose -f vpn-only.yml up -d
        ;;
    6)
        echo "💻 Deploying Development Stack..."
        docker-compose -f development.yml up -d
        ;;
    7)
        echo "🚀 Deploying Complete Infrastructure..."
        docker-compose up -d
        echo ""
        echo "🌐 All Services Available - Check individual stack access URLs"
        ;;
    skip)
        echo "⏭️ Skipping automatic deployment. You can deploy manually using the commands above."
        ;;
    *)
        echo "❌ Invalid choice. You can deploy manually using the commands above."
        ;;
esac

echo ""
echo "📋 PORTAINER INTEGRATION:"
echo "========================="
echo "Add this URL to Portainer App Templates for one-click deployment:"
echo "$TEMPLATE_URL"
echo ""
echo "🔧 MANUAL CONFIGURATION:"
echo "========================"
echo "1. Edit .env file for custom passwords and settings"
echo "2. Run: docker-compose -f [stack-name].yml up -d"
echo "3. Access services via the URLs shown above"
echo ""
echo "📚 DOCUMENTATION:"
echo "================="
echo "Repository: $REPO_URL"
echo "Setup Guide: $REPO_URL/blob/main/README.md"
echo "Deployment Guide: $REPO_URL/blob/main/DEPLOYMENT-README.md"
echo ""
echo "🎉 DEPLOYMENT COMPLETE! Happy securing! 🚀"