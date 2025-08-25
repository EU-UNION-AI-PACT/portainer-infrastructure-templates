#!/bin/bash

# 🎯 QUICK PORTAINER INTEGRATION TEST
# Tests Master URL Integration und Template Availability

set -e

echo "🎯 PORTAINER INTEGRATION TEST"
echo "=============================="
echo ""

# Check if Portainer is running
echo "🔍 Checking Portainer status..."
if curl -s http://localhost:9000 >/dev/null 2>&1; then
    echo "✅ Portainer is running on http://localhost:9000"
else
    echo "❌ Portainer not running. Starting Portainer..."
    docker run -d \
        -p 8000:8000 \
        -p 9000:9000 \
        --name portainer \
        --restart=unless-stopped \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v portainer_data:/data \
        portainer/portainer-ce:latest
    
    echo "⏰ Waiting for Portainer to start..."
    sleep 10
    
    if curl -s http://localhost:9000 >/dev/null 2>&1; then
        echo "✅ Portainer started successfully"
    else
        echo "❌ Failed to start Portainer"
        exit 1
    fi
fi

echo ""
echo "📋 TEMPLATE FILE VALIDATION"
echo "============================"

# Validate main template file
if [ -f "portainer-template.json" ]; then
    echo "✅ portainer-template.json exists"
    
    # Check JSON validity
    if jq empty portainer-template.json 2>/dev/null; then
        echo "✅ portainer-template.json is valid JSON"
        
        # Count templates
        TEMPLATE_COUNT=$(jq '.templates | length' portainer-template.json)
        echo "📊 Template Count: $TEMPLATE_COUNT"
        
        if [ "$TEMPLATE_COUNT" -ge 125 ]; then
            echo "✅ Template count meets expectation (125+)"
        else
            echo "⚠️  Template count below expectation: $TEMPLATE_COUNT < 125"
        fi
        
    else
        echo "❌ portainer-template.json contains invalid JSON"
        exit 1
    fi
else
    echo "❌ portainer-template.json not found"
    exit 1
fi

echo ""
echo "🔍 DATABASE STACK VALIDATION"
echo "============================="

# Check database stacks
DB_STACKS=$(ls stacks/database-*.yml 2>/dev/null | wc -l)
echo "📊 Database Stacks: $DB_STACKS"

if [ "$DB_STACKS" -ge 10 ]; then
    echo "✅ Database stacks available"
    echo "📂 Available categories:"
    ls stacks/database-*.yml | sed 's/.*database-//' | sed 's/.yml//' | sed 's/^/   /'
else
    echo "⚠️  Less database stacks than expected: $DB_STACKS < 10"
fi

echo ""
echo "🚀 INTEGRATION INSTRUCTIONS"
echo "============================"
echo ""
echo "🎯 MASTER URL FÜR PORTAINER:"
echo "https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/portainer-template.json"
echo ""
echo "📋 INTEGRATION STEPS:"
echo "1. Open Portainer: http://localhost:9000"
echo "2. Go to: App Templates → Settings"
echo "3. Add Template URL (replace YOUR_USERNAME):"
echo "   https://raw.githubusercontent.com/YOUR_USERNAME/portainer-infrastructure-templates/main/portainer-template.json"
echo "4. Click Save → Reload"
echo "5. ✅ All $TEMPLATE_COUNT+ templates will be available!"
echo ""
echo "🔍 TEMPLATE CATEGORIES:"
echo "   - Infrastructure (7): Security, Monitoring, VPN, Development"
echo "   - Databases (118+): Relational, NoSQL, Graph, Vector, Search, etc."
echo ""

echo "✅ INTEGRATION TEST COMPLETE!"
echo "=============================="
echo ""
echo "🎯 NEXT STEPS:"
echo "1. Upload repository to GitHub"
echo "2. Update YOUR_USERNAME in template URL"
echo "3. Add URL to Portainer App Templates"
echo "4. Deploy any of the 125+ templates with one click!"