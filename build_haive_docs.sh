#!/bin/bash
# Quick wrapper to build all Haive documentation

echo "🚀 Building all Haive documentation..."
echo "This will:"
echo "  1. Initialize PyDevelop-Docs for each package"
echo "  2. Build Sphinx documentation"
echo "  3. Create a central hub"
echo "  4. Open the result in your browser"
echo ""

# Run the Python script
poetry run python scripts/build_all_haive_docs.py

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Documentation build complete!"
else
    echo ""
    echo "❌ Documentation build failed. Check the output above for errors."
fi