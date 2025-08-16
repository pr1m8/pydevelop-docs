#!/usr/bin/env python3
"""Run smart documentation builder with improved logging and monitoring."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from pydevelop_docs.smart_builder import SmartDocBuilder


def main():
    # Find Haive root
    haive_root = Path("/home/will/Projects/haive/backend/haive")

    # Create output directory
    output_dir = Path.cwd() / "smart_docs_build"
    output_dir.mkdir(exist_ok=True)

    print("🚀 Starting Smart Documentation Build")
    print(f"📁 Haive root: {haive_root}")
    print(f"📁 Output directory: {output_dir}")
    print()

    # Create builder and run full build
    builder = SmartDocBuilder(haive_root, output_dir)

    # Analyze and plan
    plan = builder.analyze_and_plan()

    # Build all packages
    builder.build_all()

    return 0


if __name__ == "__main__":
    sys.exit(main())
