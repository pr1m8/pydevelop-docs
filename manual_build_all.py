#!/usr/bin/env python3
"""Manual script to build all Haive packages using PyDevelop-Docs."""

import subprocess
import sys
import time
from pathlib import Path

# Set up the environment
haive_root = Path("/home/will/Projects/haive/backend/haive")
packages_dir = haive_root / "packages"

# Find packages with docs
packages_to_build = []
for pkg_dir in packages_dir.iterdir():
    if pkg_dir.is_dir() and (pkg_dir / "docs").exists():
        packages_to_build.append(pkg_dir)

print(f"🔍 Found {len(packages_to_build)} packages with docs directories")
for pkg in packages_to_build:
    print(f"   • {pkg.name}")

print(f"\n🚀 Starting documentation build at {time.strftime('%Y-%m-%d %H:%M:%S')}")

successful = 0
failed = 0

for i, pkg_dir in enumerate(packages_to_build, 1):
    print(f"\n📦 [{i}/{len(packages_to_build)}] Building {pkg_dir.name}...")

    # Change to package directory and run build
    try:
        cmd = [
            "poetry",
            "run",
            "--directory",
            str(Path(__file__).parent),
            "pydevelop-docs",
            "build",
            "--clean",
            "--ignore-warnings",
        ]

        result = subprocess.run(
            cmd,
            cwd=str(pkg_dir),
            capture_output=True,
            text=True,
            timeout=600,  # 10 minutes per package
        )

        if result.returncode == 0:
            print(f"   ✅ {pkg_dir.name} - Success")
            successful += 1
        else:
            print(f"   ❌ {pkg_dir.name} - Failed")
            print(f"      Error: {result.stderr[:200]}...")
            failed += 1

    except subprocess.TimeoutExpired:
        print(f"   ⏰ {pkg_dir.name} - Timeout (>10 minutes)")
        failed += 1
    except Exception as e:
        print(f"   💥 {pkg_dir.name} - Exception: {e}")
        failed += 1

    # Short pause between builds
    time.sleep(2)

print(f"\n📊 Build Summary:")
print(f"   ✅ Successful: {successful}")
print(f"   ❌ Failed: {failed}")
print(f"   📁 Total: {len(packages_to_build)}")
print(f"   ⏱️  Completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
