#!/bin/bash

# GitHub Repository Creation and Upload Script
# This script creates a new GitHub repository and uploads the Portainer Infrastructure Templates

echo "🚀 Portainer Infrastructure Templates - GitHub Deployment Script"
echo "=================================================================="

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed. Please install it first:"
    echo "   https://cli.github.com/manual/installation"
    exit 1
fi

# Check if user is logged in to GitHub CLI
if ! gh auth status &> /dev/null; then
    echo "🔑 Please authenticate with GitHub CLI:"
    gh auth login
fi

# Repository name
REPO_NAME="portainer-infrastructure-templates"
DESCRIPTION="🚀 Complete infrastructure stacks for instant deployment via Portainer. 77+ template sources with Docker Compose stacks for Security, Monitoring, VPN, and Development."

echo ""
echo "📂 Repository Details:"
echo "   Name: $REPO_NAME"
echo "   Description: $DESCRIPTION"
echo ""

# Create GitHub repository
echo "🏗️  Creating GitHub repository..."
gh repo create "$REPO_NAME" --public --description "$DESCRIPTION" --clone=false

if [ $? -eq 0 ]; then
    echo "✅ Repository created successfully!"
else
    echo "⚠️  Repository might already exist or creation failed. Continuing with push..."
fi

# Add remote origin
echo "🔗 Adding remote origin..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$(gh api user --jq .login)/$REPO_NAME.git"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main --force

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Repository uploaded to GitHub!"
    echo ""
    echo "📋 DEPLOYMENT URLs:"
    echo "=================================================================="
    
    # Get username
    USERNAME=$(gh api user --jq .login)
    
    echo "🔗 Repository URL:"
    echo "   https://github.com/$USERNAME/$REPO_NAME"
    echo ""
    echo "📦 Portainer Template URL (Add to Portainer App Templates):"
    echo "   https://raw.githubusercontent.com/$USERNAME/$REPO_NAME/main/portainer-template.json"
    echo ""
    echo "🐳 Direct Docker Compose URLs:"
    echo "   Complete Stack: https://raw.githubusercontent.com/$USERNAME/$REPO_NAME/main/docker-compose.yml"
    echo "   Security Only:  https://raw.githubusercontent.com/$USERNAME/$REPO_NAME/main/stacks/security-only.yml"
    echo "   Monitoring:     https://raw.githubusercontent.com/$USERNAME/$REPO_NAME/main/stacks/monitoring-only.yml"
    echo "   VPN Stack:      https://raw.githubusercontent.com/$USERNAME/$REPO_NAME/main/stacks/vpn-only.yml"
    echo "   Development:    https://raw.githubusercontent.com/$USERNAME/$REPO_NAME/main/stacks/development.yml"
    echo ""
    echo "🛠️  QUICK PORTAINER SETUP:"
    echo "=================================================================="
    echo "1. Open Portainer: http://localhost:9000"
    echo "2. Go to App Templates → Settings"
    echo "3. Add template URL (from above)"
    echo "4. Save and refresh"
    echo "5. Deploy any stack with one click!"
    echo ""
    echo "🚀 INSTANT DEPLOYMENT:"
    echo "=================================================================="
    echo "docker-compose -f <(curl -s https://raw.githubusercontent.com/$USERNAME/$REPO_NAME/main/docker-compose.yml) up -d"
    echo ""
else
    echo "❌ Failed to push to GitHub. Please check your authentication and try again."
    echo "Manual commands:"
    echo "  gh auth login"
    echo "  git push -u origin main"
fi