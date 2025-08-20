#!/usr/bin/env python3
"""Update CSS configuration for all Haive packages after PyDevelop-Docs CSS fix."""

import subprocess
import sys
from pathlib import Path

# Base path to Haive packages
HAIVE_BASE = Path("/home/will/Projects/haive/backend/haive")
PACKAGES_DIR = HAIVE_BASE / "packages"

# Packages to update
PACKAGES = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-mcp",
    "haive-prebuilt",
]


def update_package(package_name: str) -> bool:
    """Update a single package's documentation configuration."""
    package_path = PACKAGES_DIR / package_name

    if not package_path.exists():
        print(f"❌ Package not found: {package_path}")
        return False

    print(f"\n📦 Updating {package_name}...")

    # Change to package directory and run pydevelop-docs init
    try:
        # Run pydevelop-docs init in the package directory
        result = subprocess.run(
            ["poetry", "run", "pydevelop-docs", "init", "--force"],
            cwd=str(package_path),
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"❌ Failed to update {package_name}")
            print(f"   Error: {result.stderr}")
            return False

        print(f"✅ Successfully updated {package_name}")
        return True

    except Exception as e:
        print(f"❌ Error updating {package_name}: {e}")
        return False


def main():
    """Update all packages with new CSS configuration."""
    print("🔧 Updating CSS configuration for all Haive packages")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path.cwd().name == "pydevelop-docs":
        print("⚠️  Please run this script from the pydevelop-docs directory")
        return 1

    success_count = 0
    failed_packages = []

    for package in PACKAGES:
        if update_package(package):
            success_count += 1
        else:
            failed_packages.append(package)

    # Summary
    print("\n" + "=" * 50)
    print("📊 Update Summary:")
    print(f"   ✅ Successful: {success_count}/{len(PACKAGES)}")
    print(f"   ❌ Failed: {len(failed_packages)}")

    if failed_packages:
        print(f"\n❌ Failed packages:")
        for pkg in failed_packages:
            print(f"   - {pkg}")

    if success_count == len(PACKAGES):
        print("\n✅ All packages updated successfully!")
        print("\n🎯 Next steps:")
        print(
            "   1. Build docs: poetry run python scripts/build_haive_docs_v2.py haive-mcp"
        )
        print("   2. Open in browser to verify clean styling")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
