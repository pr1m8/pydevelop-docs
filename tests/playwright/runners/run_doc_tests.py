#!/usr/bin/env python3
"""Simple runner for documentation tests."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def main():
    """Run documentation tests with proper setup."""

    print("🧪 Haive Documentation Testing Suite")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check if playwright is installed
    try:
        import playwright

        print("✅ Playwright is installed")
    except ImportError:
        print("❌ Playwright not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"])
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Playwright installed")

    # Set up test directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_dir = Path(f"doc_test_results_{timestamp}")
    test_dir.mkdir(exist_ok=True)

    print(f"📁 Test results will be saved to: {test_dir}")
    print()

    # Run the test suite
    test_script = Path(__file__).parent.parent / "core" / "test_documentation.py"
    cmd = [
        sys.executable,
        str(test_script),
        "--base-dir",
        "/home/will/Projects/haive/backend/haive",
        "--output-dir",
        str(test_dir),
    ]

    print("🚀 Starting tests...")
    print("-" * 50)

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print()
        print("✅ Tests completed successfully!")
        print(f"📊 View results in: {test_dir}/test_results_{timestamp}.json")
        print(f"📸 Screenshots saved in: {test_dir}/*/")
    else:
        print()
        print("❌ Tests failed!")

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
