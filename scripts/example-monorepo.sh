#!/bin/bash
# Example: Initialize and build documentation for a monorepo

echo "🚀 PyDevelop-docs Monorepo Example"
echo "=============================="
echo ""
echo "This example shows how to use pydevelop-docs with a monorepo structure."
echo ""

# Initialize documentation for all packages
echo "1. Initialize documentation for packages/ and tools/ directories:"
echo "   $ pydevelop-docs init --packages-dir packages --packages-dir tools --include-root"
echo ""

# Build all documentation
echo "2. Build documentation for all packages:"
echo "   $ pydevelop-docs build"
echo ""

# Build specific package
echo "3. Build specific package only:"
echo "   $ pydevelop-docs build --package haive-core"
echo ""

# Clean and rebuild
echo "4. Clean and rebuild everything:"
echo "   $ pydevelop-docs clean"
echo "   $ pydevelop-docs build --clean"
echo ""

# Interactive mode
echo "5. Use interactive mode for guided setup:"
echo "   $ pydevelop-docs"
echo ""

echo "Try these commands in your monorepo!"