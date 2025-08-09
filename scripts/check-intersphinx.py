#!/usr/bin/env python3
"""
Check and validate intersphinx mappings for the documentation.

This script:
1. Clears the seed-intersphinx-mapping cache
2. Builds documentation to populate mappings
3. Runs linkcheck to validate all cross-references
4. Reports any broken or missing intersphinx links
"""

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd: list[str], cwd: Path = None) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, and stderr."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def clear_intersphinx_cache():
    """Clear the seed-intersphinx-mapping cache."""
    print("🧹 Clearing intersphinx cache...")
    returncode, stdout, stderr = run_command(
        [sys.executable, "-m", "seed_intersphinx_mapping"]
    )
    if returncode == 0:
        print("✅ Cache cleared successfully")
    else:
        print(f"⚠️  Warning: Cache clear had issues: {stderr}")


def build_docs(docs_dir: Path) -> bool:
    """Build documentation to populate intersphinx mappings."""
    print("\n📚 Building documentation to populate intersphinx mappings...")
    build_dir = docs_dir / "build" / "intersphinx-test"

    # Clean build directory
    if build_dir.exists():
        shutil.rmtree(build_dir)

    returncode, stdout, stderr = run_command(
        ["poetry", "run", "sphinx-build", "-b", "html", "-q", "source", str(build_dir)],
        cwd=docs_dir,
    )

    if returncode == 0:
        print("✅ Documentation built successfully")
        return True
    else:
        print(f"❌ Documentation build failed:\n{stderr}")
        return False


def check_intersphinx_links(docs_dir: Path) -> dict:
    """Run linkcheck and analyze results."""
    print("\n🔗 Checking intersphinx links...")
    linkcheck_dir = docs_dir / "build" / "linkcheck"

    returncode, stdout, stderr = run_command(
        [
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "linkcheck",
            "-q",
            "source",
            str(linkcheck_dir),
        ],
        cwd=docs_dir,
    )

    # Parse linkcheck output
    output_file = linkcheck_dir / "output.txt"
    results = {"total": 0, "working": 0, "broken": 0, "redirected": 0, "errors": []}

    if output_file.exists():
        with open(output_file, "r") as f:
            for line in f:
                results["total"] += 1
                if "broken" in line:
                    results["broken"] += 1
                    results["errors"].append(line.strip())
                elif "redirected" in line:
                    results["redirected"] += 1
                else:
                    results["working"] += 1

    return results


def print_intersphinx_report(conf_file: Path):
    """Print a report of current intersphinx mappings."""
    print("\n📊 Intersphinx Mapping Report")
    print("=" * 50)

    # Extract intersphinx mappings from conf.py
    try:
        # Import conf.py module
        import importlib.util

        spec = importlib.util.spec_from_file_location("conf", conf_file)
        conf = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(conf)

        if hasattr(conf, "intersphinx_mapping"):
            print(f"Total mappings: {len(conf.intersphinx_mapping)}")
            print("\nConfigured mappings:")
            for name, (url, inv) in sorted(conf.intersphinx_mapping.items()):
                print(f"  - {name:20} → {url}")
        else:
            print("No intersphinx_mapping found in conf.py")

    except Exception as e:
        print(f"Error reading conf.py: {e}")


def main():
    """Main entry point."""
    print("🔍 PyAutoDoc Intersphinx Validation")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # Find project root and docs directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / "docs"
    conf_file = docs_dir / "source" / "conf.py"

    if not docs_dir.exists():
        print("❌ Error: docs directory not found!")
        sys.exit(1)

    # Clear cache
    clear_intersphinx_cache()

    # Build docs
    if not build_docs(docs_dir):
        sys.exit(1)

    # Check links
    results = check_intersphinx_links(docs_dir)

    # Print report
    print_intersphinx_report(conf_file)

    # Print results
    print("\n📈 Link Check Results")
    print("=" * 50)
    print(f"Total links checked: {results['total']}")
    print(f"✅ Working: {results['working']}")
    print(f"🔄 Redirected: {results['redirected']}")
    print(f"❌ Broken: {results['broken']}")

    if results["errors"]:
        print("\n⚠️  Broken links:")
        for error in results["errors"][:10]:  # Show first 10
            print(f"  - {error}")
        if len(results["errors"]) > 10:
            print(f"  ... and {len(results['errors']) - 10} more")

    # Exit with appropriate code
    if results["broken"] > 0:
        print(f"\n❌ Found {results['broken']} broken links!")
        sys.exit(1)
    else:
        print("\n✅ All intersphinx links are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
