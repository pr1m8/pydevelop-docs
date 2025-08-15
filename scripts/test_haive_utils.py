#!/usr/bin/env python3
"""Test script for Haive documentation utilities.

This script validates the HaiveDocumentationManager can detect and work with
the Haive monorepo structure without actually running builds.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pydevelop_docs.haive_utils import HaiveDocumentationManager


def test_haive_detection():
    """Test auto-detection of Haive monorepo structure."""
    print("🔍 Testing Haive monorepo detection...")

    # Try to find Haive root from current directory
    current_path = Path.cwd()
    haive_root = None

    # Look for Haive markers in current path and parents
    for path in [current_path] + list(current_path.parents):
        if (path / "packages").exists() and (path / "CLAUDE.md").exists():
            haive_root = path
            break

    if not haive_root:
        print("❌ Could not detect Haive monorepo structure")
        print(f"   Current dir: {current_path}")
        print("   Looking for: packages/ directory + CLAUDE.md file")
        return False

    print(f"✅ Found Haive root: {haive_root}")

    # Test HaiveDocumentationManager initialization
    try:
        manager = HaiveDocumentationManager(haive_root, quiet=True, debug=False)
        print(f"✅ Manager initialized successfully")
        print(f"   Packages dir: {manager.packages_dir}")
        print(f"   Master docs: {manager.master_docs}")
        print(f"   Expected packages: {len(manager.packages)}")

        # Check which packages actually exist
        existing_packages = []
        for package in manager.packages:
            package_path = manager.packages_dir / package
            if package_path.exists():
                existing_packages.append(package)

        print(f"   Existing packages: {len(existing_packages)}")
        for pkg in existing_packages:
            print(f"     ✅ {pkg}")

        missing_packages = set(manager.packages) - set(existing_packages)
        if missing_packages:
            print(f"   Missing packages: {len(missing_packages)}")
            for pkg in missing_packages:
                print(f"     ❌ {pkg}")

        return True

    except Exception as e:
        print(f"❌ Manager initialization failed: {e}")
        return False


def test_package_structure():
    """Test analysis of package documentation structure."""
    print("\n📦 Testing package structure analysis...")

    # Find Haive root
    current_path = Path.cwd()
    haive_root = None

    for path in [current_path] + list(current_path.parents):
        if (path / "packages").exists() and (path / "CLAUDE.md").exists():
            haive_root = path
            break

    if not haive_root:
        print("❌ Haive root not found")
        return False

    manager = HaiveDocumentationManager(haive_root, quiet=True)

    # Analyze each package
    for package in manager.packages:
        package_path = manager.packages_dir / package
        if not package_path.exists():
            continue

        print(f"\n📋 Analyzing {package}:")
        print(f"   Path: {package_path}")

        # Check documentation structure
        docs_dir = package_path / "docs"
        docs_source = docs_dir / "source"
        conf_py = docs_source / "conf.py"

        print(f"   docs/: {'✅' if docs_dir.exists() else '❌'}")
        print(f"   docs/source/: {'✅' if docs_source.exists() else '❌'}")
        print(f"   conf.py: {'✅' if conf_py.exists() else '❌'}")

        # Check if using shared config
        if conf_py.exists():
            try:
                content = conf_py.read_text()
                uses_shared = "pydevelop_docs.config" in content
                print(f"   Shared config: {'✅' if uses_shared else '❌'}")
            except:
                print(f"   Shared config: ❌ (read error)")

    return True


def main():
    """Run all tests."""
    print("🧪 Haive Documentation Utils Test")
    print("=" * 50)

    success = True

    # Test 1: Haive detection
    if not test_haive_detection():
        success = False

    # Test 2: Package structure
    if not test_package_structure():
        success = False

    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed!")
        print("\n✨ Ready to run: poetry run pydevelop-docs rebuild-haive")
    else:
        print("❌ Some tests failed!")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
