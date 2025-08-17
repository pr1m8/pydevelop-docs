#!/bin/bash
#
# Quick script to build just haive-mcp documentation
# This is useful for testing PyDevelop-Docs with a single package
#

echo "🚀 Building haive-mcp documentation with PyDevelop-Docs..."
echo ""

# Make sure we have rich installed for the progress bars
poetry add rich --group dev 2>/dev/null || true

# Run the enhanced builder for just haive-mcp
poetry run python scripts/build_haive_docs_v2.py haive-mcp

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ haive-mcp documentation built successfully!"
    echo ""
    echo "The documentation should have opened in your browser."
    echo "If not, you can manually open:"
    echo "  file://$(pwd)/../../../packages/haive-mcp/docs/build/index.html"
else
    echo ""
    echo "❌ Build failed. Check the output above for errors."
fi