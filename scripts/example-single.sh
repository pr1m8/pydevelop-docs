#!/bin/bash
# Example: Initialize and build documentation for a single package

echo "📦 PyDevelop-docs Single Package Example"
echo "===================================="
echo ""
echo "This example shows how to use pydevelop-docs with a single Python package."
echo ""

# Initialize documentation
echo "1. Initialize documentation in current directory:"
echo "   $ pydevelop-docs init --include-root"
echo ""

# Dry run first
echo "2. Preview what will be created:"
echo "   $ pydevelop-docs init --include-root --dry-run"
echo ""

# Build documentation
echo "3. Build the documentation:"
echo "   $ pydevelop-docs build"
echo ""

# Build with auto-open
echo "4. Build and open in browser:"
echo "   $ pydevelop-docs build --open"
echo ""

# Add dependencies
echo "5. Add documentation dependencies:"
echo "   $ pydevelop-docs deps add"
echo ""

echo "Run these commands in your package directory!"