#!/usr/bin/env python3
"""
Simple test to build haive-mcp docs and check union type handling.
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    # Get path to haive-mcp
    haive_mcp = Path(__file__).parent.parent.parent / "packages" / "haive-mcp"

    if not haive_mcp.exists():
        print(f"❌ haive-mcp not found at {haive_mcp}")
        sys.exit(1)

    print(f"📁 Found haive-mcp at: {haive_mcp}")

    # Check if already initialized
    if (haive_mcp / "docs" / "source" / "conf.py").exists():
        print("✅ PyDevelop-Docs already initialized")
    else:
        print("📝 Initializing PyDevelop-Docs...")
        result = subprocess.run(
            ["poetry", "run", "pydevelop-docs", "init", "--force", "--yes"],
            cwd=str(haive_mcp),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"❌ Init failed: {result.stderr}")
            sys.exit(1)

        print("✅ Initialized successfully")

    # Build documentation
    print("\n🔨 Building documentation...")
    print("   This may take a few minutes for a large package like haive-mcp...")

    docs_dir = haive_mcp / "docs"
    result = subprocess.run(
        ["poetry", "run", "sphinx-build", "-b", "html", "source", "build", "-E"],
        cwd=str(docs_dir),
        capture_output=True,
        text=True,
    )

    # Check for union type errors
    if "unsupported operand type" in result.stderr:
        print("\n⚠️  Union type syntax detected!")
        print("   sphinx-codeautolink wrapper should handle this gracefully")

    # Check if build succeeded
    index_html = docs_dir / "build" / "index.html"
    if index_html.exists():
        print("\n✅ Build succeeded!")
        print(f"   Documentation at: file://{index_html}")

        # Count warnings
        warning_count = result.stderr.count("WARNING:")
        if warning_count > 0:
            print(f"   ⚠️  {warning_count} warnings during build")

        # Open in browser
        print("\n🌐 Opening documentation...")
        try:
            subprocess.run(["xdg-open", str(index_html)])
        except Exception as e:
            print(f"   Could not open browser: {e}")
    else:
        print("\n❌ Build failed!")
        print("STDOUT:", result.stdout[:500])
        print("STDERR:", result.stderr[:500])
        sys.exit(1)


if __name__ == "__main__":
    main()
