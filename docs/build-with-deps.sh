#!/bin/bash
# Build documentation with all dependencies installed
# This script ensures all system and Python dependencies are available

set -e  # Exit on error

echo "🔧 Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install -y $(grep -v '^#' apt-requirements.txt | grep -v '^$')
elif command -v yum &> /dev/null; then
    # RHEL/CentOS
    echo "⚠️  Please manually install: graphviz graphviz-devel java plantuml imagemagick pandoc"
elif command -v brew &> /dev/null; then
    # macOS
    brew install graphviz plantuml imagemagick pandoc
fi

echo "📦 Installing Python dependencies..."
# Install the package itself
pip install -e ..

# Install documentation requirements
pip install -r requirements.txt

echo "🔨 Building documentation..."
make clean
make html

echo "✅ Documentation built successfully!"
echo "📂 Output: build/html/index.html"
echo ""
echo "To view locally:"
echo "  python -m http.server 8000 --directory build/html"