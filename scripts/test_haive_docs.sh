#!/bin/bash
# Test documentation for all Haive packages

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCREENSHOT_SCRIPT="$SCRIPT_DIR/serve_and_screenshot.py"

# Haive packages to test
PACKAGES=(
    "haive-core"
    "haive-agents"
    "haive-tools"
    "haive-games"
    "haive-mcp"
    "haive-prebuilt"
    "haive-dataflow"
)

echo "📸 Haive Documentation Screenshot Testing"
echo "========================================"
echo ""

# Check if screenshot script exists
if [ ! -f "$SCREENSHOT_SCRIPT" ]; then
    echo "Error: Screenshot script not found at $SCREENSHOT_SCRIPT"
    exit 1
fi

# Test each package
for package in "${PACKAGES[@]}"; do
    echo "Testing $package documentation..."
    echo "---------------------------------"
    
    # Use different ports for each package to avoid conflicts
    case $package in
        "haive-core") PORT=8005 ;;
        "haive-agents") PORT=8006 ;;
        "haive-tools") PORT=8007 ;;
        "haive-games") PORT=8008 ;;
        "haive-mcp") PORT=8009 ;;
        "haive-prebuilt") PORT=8010 ;;
        "haive-dataflow") PORT=8011 ;;
        *) PORT=8012 ;;
    esac
    
    # Run screenshot test
    poetry run python "$SCREENSHOT_SCRIPT" --package "$package" --port "$PORT"
    
    echo ""
done

echo "✅ All package documentation tests complete!"
echo ""
echo "Screenshot results are in:"
echo "  $SCRIPT_DIR/../debug/screenshots/"