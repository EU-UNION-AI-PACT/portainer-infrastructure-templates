#!/bin/bash

# 🔧 Portainer Template Validation Script
# Validates the fixed JSON format and tests Portainer compatibility

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

echo -e "${PURPLE}🔧 Portainer Template Validation${NC}"
echo -e "${CYAN}================================${NC}"

# URLs to test
MAIN_URL="https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template.json"
TEST_URL="https://raw.githubusercontent.com/EU-UNION-AI-PACT/portainer-infrastructure-templates/main/web/portainer-template-test.json"

function test_json_validity() {
    local url=$1
    local name=$2
    
    echo -e "\n${WHITE}Testing $name...${NC}"
    
    # Test JSON validity
    if curl -s "$url" | jq . >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Valid JSON format${NC}"
    else
        echo -e "${RED}❌ Invalid JSON format${NC}"
        return 1
    fi
    
    # Test labels format
    local labels_test=$(curl -s "$url" | jq '.templates[0].labels | type' 2>/dev/null)
    if [[ "$labels_test" == '"array"' ]]; then
        echo -e "${GREEN}✅ Labels format correct (array)${NC}"
    else
        echo -e "${RED}❌ Labels format incorrect (should be array)${NC}"
        return 1
    fi
    
    # Test required fields
    local required_fields=("version" "templates")
    for field in "${required_fields[@]}"; do
        if curl -s "$url" | jq "has(\"$field\")" | grep -q "true"; then
            echo -e "${GREEN}✅ Has required field: $field${NC}"
        else
            echo -e "${RED}❌ Missing required field: $field${NC}"
            return 1
        fi
    done
    
    # Count templates
    local template_count=$(curl -s "$url" | jq '.templates | length' 2>/dev/null)
    echo -e "${CYAN}📊 Template count: $template_count${NC}"
    
    return 0
}

function test_portainer_compatibility() {
    echo -e "\n${WHITE}🐳 Testing Portainer Compatibility...${NC}"
    
    # Test template structure
    local first_template=$(curl -s "$MAIN_URL" | jq '.templates[0]' 2>/dev/null)
    
    # Required template fields
    local template_fields=("type" "title" "description" "categories" "platform" "image")
    
    for field in "${template_fields[@]}"; do
        if echo "$first_template" | jq "has(\"$field\")" | grep -q "true"; then
            echo -e "${GREEN}✅ Template has required field: $field${NC}"
        else
            echo -e "${RED}❌ Template missing required field: $field${NC}"
            return 1
        fi
    done
    
    # Test labels structure specifically
    local labels_structure=$(curl -s "$MAIN_URL" | jq '.templates[0].labels[0] | has("name") and has("value")' 2>/dev/null)
    if [[ "$labels_structure" == "true" ]]; then
        echo -e "${GREEN}✅ Labels have correct {name, value} structure${NC}"
    else
        echo -e "${RED}❌ Labels structure incorrect${NC}"
        return 1
    fi
    
    return 0
}

function show_integration_info() {
    echo -e "\n${WHITE}🚀 Integration Information${NC}"
    echo -e "${CYAN}=========================${NC}"
    
    echo -e "\n${WHITE}📋 Portainer URLs:${NC}"
    echo -e "${GREEN}Main Collection (248 templates):${NC}"
    echo -e "  $MAIN_URL"
    echo -e "\n${YELLOW}Test Template (1 template):${NC}"
    echo -e "  $TEST_URL"
    
    echo -e "\n${WHITE}🔧 Integration Steps:${NC}"
    echo -e "1. Open Portainer Admin Panel"
    echo -e "2. Go to ${CYAN}Settings${NC} → ${CYAN}App Templates${NC}"
    echo -e "3. Add the main URL above"
    echo -e "4. Save and refresh the App Templates page"
    
    echo -e "\n${WHITE}💡 Troubleshooting:${NC}"
    echo -e "• If main URL fails, try the test URL first"
    echo -e "• Check Portainer logs for specific errors"
    echo -e "• Ensure Portainer has internet access to GitHub"
    echo -e "• Verify Portainer version supports v3 templates"
}

function main() {
    echo -e "${YELLOW}Testing JSON format fixes...${NC}"
    
    # Test main template
    if test_json_validity "$MAIN_URL" "Main Template Collection"; then
        echo -e "${GREEN}✅ Main template validation passed${NC}"
    else
        echo -e "${RED}❌ Main template validation failed${NC}"
        exit 1
    fi
    
    # Test simplified template
    if test_json_validity "$TEST_URL" "Test Template"; then
        echo -e "${GREEN}✅ Test template validation passed${NC}"
    else
        echo -e "${RED}❌ Test template validation failed${NC}"
        exit 1
    fi
    
    # Test Portainer compatibility
    if test_portainer_compatibility; then
        echo -e "${GREEN}✅ Portainer compatibility test passed${NC}"
    else
        echo -e "${RED}❌ Portainer compatibility test failed${NC}"
        exit 1
    fi
    
    # Show integration info
    show_integration_info
    
    echo -e "\n${PURPLE}🎉 All validations passed! Template is ready for Portainer! ${PURPLE}${NC}"
}

main "$@"