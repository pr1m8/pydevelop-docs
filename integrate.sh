#!/bin/bash
# PyAutoDoc Integration Script
# This script helps you integrate PyAutoDoc into any project

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where pyautodoc files are located
PYAUTODOC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}🚀 PyAutoDoc Integration Helper${NC}\n"

# Check if target directory is provided
if [ -z "$1" ]; then
    echo "Usage: ./integrate.sh /path/to/your/project"
    echo ""
    echo "This will copy PyAutoDoc to your project and set up documentation."
    exit 1
fi

TARGET_DIR="$1"

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}❌ Directory not found: $TARGET_DIR${NC}"
    exit 1
fi

echo -e "${GREEN}📁 Integrating into: $TARGET_DIR${NC}"

# Copy the simple version
echo -e "${BLUE}📄 Copying pyautodoc_simple.py...${NC}"
cp "$PYAUTODOC_DIR/pyautodoc_simple.py" "$TARGET_DIR/pyautodoc.py"

# Make it executable
chmod +x "$TARGET_DIR/pyautodoc.py"

echo -e "${GREEN}✅ PyAutoDoc installed!${NC}"
echo ""
echo -e "${BLUE}📖 Next steps:${NC}"
echo "   cd $TARGET_DIR"
echo "   python pyautodoc.py        # Setup and build docs"
echo "   python pyautodoc.py serve  # View docs at localhost:8000"
echo ""
echo -e "${GREEN}🎉 Done!${NC}"