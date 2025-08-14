#!/bin/bash
# Build documentation for Haive monorepo
# Usage: ./build-haive-docs.sh [options]

set -e  # Exit on error

# Configuration
HAIVE_ROOT="/home/will/Projects/haive/backend/haive"
PYDEVELOP_DOCS_PATH="${HAIVE_ROOT}/tools/pydevelop-docs"
BUILD_TYPE="${1:-all}"  # all, hub, packages, or specific package name

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Haive Documentation Builder${NC}"
echo -e "================================"

# Ensure we're in the right directory
cd "$HAIVE_ROOT"

# Check if PyDevelop-Docs is installed
if ! command -v pydevelop-docs &> /dev/null; then
    echo -e "${YELLOW}Installing PyDevelop-Docs...${NC}"
    cd "$PYDEVELOP_DOCS_PATH"
    poetry install
    cd "$HAIVE_ROOT"
fi

case "$BUILD_TYPE" in
    "all")
        echo -e "${GREEN}📚 Building all documentation (packages + hub)${NC}"
        poetry run pydevelop-docs init --project-type monorepo --force
        poetry run pydevelop-docs build --all --clean
        
        echo -e "\n${GREEN}✅ Documentation built successfully!${NC}"
        echo -e "📍 Central Hub: ${HAIVE_ROOT}/docs/build/html/index.html"
        echo -e "📦 Package Docs:"
        find packages/*/docs/build/html/index.html 2>/dev/null | while read -r file; do
            echo -e "   - $file"
        done
        ;;
        
    "hub")
        echo -e "${GREEN}🏠 Building central hub only${NC}"
        poetry run pydevelop-docs init --project-type central-hub --force
        poetry run pydevelop-docs build --hub-only
        
        echo -e "\n${GREEN}✅ Hub built successfully!${NC}"
        echo -e "📍 Location: ${HAIVE_ROOT}/docs/build/html/index.html"
        ;;
        
    "packages")
        echo -e "${GREEN}📦 Building all package documentation${NC}"
        
        for package_dir in packages/*/; do
            if [ -d "$package_dir" ]; then
                package_name=$(basename "$package_dir")
                echo -e "\n${BLUE}Building ${package_name}...${NC}"
                
                cd "$package_dir"
                poetry run pydevelop-docs init --force
                poetry run pydevelop-docs build --clean
                cd "$HAIVE_ROOT"
            fi
        done
        
        echo -e "\n${GREEN}✅ All packages built successfully!${NC}"
        ;;
        
    haive-*)
        # Build specific package
        package_name="$BUILD_TYPE"
        package_dir="packages/${package_name}"
        
        if [ -d "$package_dir" ]; then
            echo -e "${GREEN}📦 Building ${package_name} documentation${NC}"
            cd "$package_dir"
            poetry run pydevelop-docs init --force
            poetry run pydevelop-docs build --clean
            
            echo -e "\n${GREEN}✅ ${package_name} built successfully!${NC}"
            echo -e "📍 Location: ${package_dir}/docs/build/html/index.html"
        else
            echo -e "${YELLOW}⚠️  Package ${package_name} not found${NC}"
            exit 1
        fi
        ;;
        
    *)
        echo -e "${YELLOW}Usage: $0 [all|hub|packages|haive-core|haive-agents|...]${NC}"
        echo -e "\nOptions:"
        echo -e "  all         - Build everything (packages + central hub)"
        echo -e "  hub         - Build central hub only"
        echo -e "  packages    - Build all individual packages"
        echo -e "  haive-*     - Build specific package (e.g., haive-core)"
        exit 1
        ;;
esac

# Offer to start web server
echo -e "\n${BLUE}View documentation?${NC}"
echo -e "1) Central Hub (http://localhost:8000)"
echo -e "2) Package docs (select package)"
echo -e "3) No, exit"
read -p "Choice [1-3]: " choice

case "$choice" in
    1)
        echo -e "${GREEN}Starting server for central hub...${NC}"
        cd "${HAIVE_ROOT}/docs/build/html"
        python -m http.server 8000
        ;;
    2)
        echo -e "\nAvailable packages:"
        i=1
        packages=()
        for package_dir in packages/*/docs/build/html; do
            if [ -d "$package_dir" ]; then
                package_name=$(basename $(dirname $(dirname "$package_dir")))
                echo "$i) $package_name"
                packages+=("$package_dir")
                ((i++))
            fi
        done
        
        read -p "Select package [1-$((i-1))]: " pkg_choice
        if [ "$pkg_choice" -ge 1 ] && [ "$pkg_choice" -lt "$i" ]; then
            selected_dir="${packages[$((pkg_choice-1))]}"
            echo -e "${GREEN}Starting server for package documentation...${NC}"
            cd "$selected_dir"
            python -m http.server 8001
        fi
        ;;
    3)
        echo -e "${GREEN}Done!${NC}"
        ;;
esac