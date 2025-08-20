#!/bin/bash
# Test new API styling on haive-mcp package

set -e

echo "🎨 Testing New API Styling on haive-mcp"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Define paths
HAIVE_MCP="/home/will/Projects/haive/backend/haive/packages/haive-mcp"
PYDEVELOP_DOCS="/home/will/Projects/haive/backend/haive/tools/pydevelop-docs"

echo -e "${BLUE}📋 Building haive-mcp Documentation with Enhanced API Styling${NC}"
echo "Package: $HAIVE_MCP"
echo ""

# Clean existing docs
echo "🗑️  Cleaning existing haive-mcp docs..."
rm -rf "$HAIVE_MCP/docs"

# Run pydevelop-docs init with minimal style (includes new API styling)
echo "🔧 Initializing haive-mcp docs with enhanced API styling..."
(cd "$HAIVE_MCP" && poetry run pydevelop-docs init \
    --template-style minimal \
    --force)

# Check results
echo ""
echo "📊 Checking results..."

# Check if CSS file was copied
CSS_FILE="$HAIVE_MCP/docs/source/_static/api-function-styling.css"
if [ -f "$CSS_FILE" ]; then
    echo -e "${GREEN}✅ api-function-styling.css copied successfully${NC}"
else
    echo -e "${RED}❌ api-function-styling.css not found${NC}"
fi

# Check if AutoAPI templates were copied
TEMPLATE_DIR="$HAIVE_MCP/docs/source/_autoapi_templates"
if [ -d "$TEMPLATE_DIR" ]; then
    echo -e "${GREEN}✅ AutoAPI templates copied successfully${NC}"
    echo "   Templates found:"
    find "$TEMPLATE_DIR" -name "*.rst" -exec basename {} \; | sed 's/^/   - /'
else
    echo -e "${YELLOW}⚠️  AutoAPI templates not found (may use default)${NC}"
fi

# Build the documentation
echo ""
echo "🏗️  Building haive-mcp documentation..."
(cd "$HAIVE_MCP/docs" && poetry run sphinx-build -b html source build 2>&1 | tail -20)

# Check build results
if [ -f "$HAIVE_MCP/docs/build/index.html" ]; then
    echo -e "${GREEN}✅ Documentation built successfully${NC}"
    
    # Check CSS in built docs
    BUILT_CSS="$HAIVE_MCP/docs/build/_static/api-function-styling.css"
    if [ -f "$BUILT_CSS" ]; then
        echo -e "${GREEN}✅ API styling CSS included in build${NC}"
    else
        echo -e "${RED}❌ API styling CSS missing from build${NC}"
    fi
else
    echo -e "${RED}❌ Documentation build failed${NC}"
fi

echo ""
echo -e "${GREEN}✅ Test complete!${NC}"
echo ""
echo "To view the documentation:"
echo "cd $HAIVE_MCP/docs && python -m http.server 8006 --directory build"
echo "Then open: http://localhost:8006"
echo ""
echo "Check these pages for styling improvements:"
echo "  - http://localhost:8006/autoapi/mcp/haive_agent_mcp_integration/index.html"
echo "  - http://localhost:8006/autoapi/mcp/dynamic_activation_mcp/index.html"