#!/usr/bin/env python3
"""Clean up old CSS files from Haive packages after CSS simplification."""

import sys
from pathlib import Path

# Base path to Haive packages
HAIVE_BASE = Path("/home/will/Projects/haive/backend/haive")
PACKAGES_DIR = HAIVE_BASE / "packages"

# Packages to clean
PACKAGES = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-mcp",
    "haive-prebuilt",
]

# CSS files to remove (these are now excluded from PyDevelop-Docs)
CSS_FILES_TO_REMOVE = [
    "enhanced-design.css",  # Marketing-style design (900+ lines)
    "api-docs.css",  # Aggressive API styling with badges
    "enhanced-index.css",  # More marketing styling
    "furo-enhancements.js",  # JS counterpart to CSS
    "toc-enhancements.css",  # TOC overrides (if causing issues)
    "furo-intense.css",  # Aggressive dark mode overrides
]

# CSS files to keep (minimal set)
CSS_FILES_TO_KEEP = [
    "breadcrumb-navigation.css",
    "mermaid-custom.css",
    "tippy-enhancements.css",
    # "css/custom.css" is in a subdirectory
]


def cleanup_package_css(package_name: str) -> tuple[bool, list[str]]:
    """Clean up old CSS files from a package."""
    package_path = PACKAGES_DIR / package_name
    static_path = package_path / "docs" / "source" / "_static"

    if not static_path.exists():
        return True, []  # No static directory, nothing to clean

    removed_files = []

    for css_file in CSS_FILES_TO_REMOVE:
        file_path = static_path / css_file
        if file_path.exists():
            print(f"   🗑️  Removing {css_file}")
            file_path.unlink()
            removed_files.append(css_file)

    return True, removed_files


def main():
    """Clean up old CSS files from all packages."""
    print("🧹 Cleaning up old CSS files from Haive packages")
    print("=" * 50)

    total_removed = 0

    for package in PACKAGES:
        print(f"\n📦 Cleaning {package}...")
        success, removed_files = cleanup_package_css(package)

        if removed_files:
            total_removed += len(removed_files)
            print(f"   ✅ Removed {len(removed_files)} files")
        else:
            print(f"   ✓ Already clean")

    print("\n" + "=" * 50)
    print(f"🎯 Total files removed: {total_removed}")
    print("\n✅ Cleanup complete!")
    print("\n📋 Next steps:")
    print("   1. Rebuild documentation to see clean styling")
    print("   2. Run: poetry run python scripts/build_haive_docs_v2.py haive-mcp")

    return 0


if __name__ == "__main__":
    sys.exit(main())
