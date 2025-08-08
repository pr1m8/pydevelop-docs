#!/usr/bin/env python3
"""
Enhanced Sphinx documentation builder with detailed error reporting.

This script provides better error reporting and debugging for Sphinx builds,
showing detailed warnings and errors with context.
"""

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class BuildError:
    """Represents a build error or warning."""

    level: str  # WARNING, ERROR, CRITICAL
    file_path: str
    line_number: int
    message: str
    context: str = ""


class SphinxBuilder:
    """Enhanced Sphinx builder with error reporting."""

    def __init__(self, source_dir: str = "docs/source", build_dir: str = "docs/build"):
        self.source_dir = Path(source_dir)
        self.build_dir = Path(build_dir)
        self.errors: List[BuildError] = []

    def parse_build_output(self, output: str) -> None:
        """Parse sphinx-build output for errors and warnings."""
        lines = output.split("\n")

        for line in lines:
            # Match Sphinx warning/error pattern
            match = re.match(r"(.+):(\d+): (WARNING|ERROR|CRITICAL): (.+)", line)
            if match:
                file_path, line_num, level, message = match.groups()

                error = BuildError(
                    level=level,
                    file_path=file_path,
                    line_number=int(line_num),
                    message=message,
                )
                self.errors.append(error)

    def build(self, builder: str = "html", verbose: bool = True) -> bool:
        """Build documentation with enhanced error reporting."""
        cmd = [
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            builder,
            "-W",  # Treat warnings as errors for strict mode
            "-v",  # Verbose output
            str(self.source_dir),
            str(self.build_dir),
        ]

        if verbose:
            print(f"🏗️  Building Sphinx documentation...")
            print(f"📁 Source: {self.source_dir}")
            print(f"📁 Build:  {self.build_dir}")
            print(f"🔧 Command: {' '.join(cmd)}")
            print("-" * 60)

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

            # Parse output for errors
            self.parse_build_output(result.stderr)
            self.parse_build_output(result.stdout)

            if result.returncode == 0:
                if verbose:
                    print("✅ Build successful!")
                    if self.errors:
                        self._print_warnings()
                return True
            else:
                if verbose:
                    print("❌ Build failed!")
                    self._print_errors()
                    print(f"\nFull output:\n{result.stdout}")
                    print(f"\nErrors:\n{result.stderr}")
                return False

        except Exception as e:
            print(f"💥 Build command failed: {e}")
            return False

    def _print_errors(self) -> None:
        """Print formatted error report."""
        if not self.errors:
            return

        print("\n📋 Error Report:")
        print("=" * 60)

        # Group by level
        by_level: Dict[str, List[BuildError]] = {}
        for error in self.errors:
            by_level.setdefault(error.level, []).append(error)

        for level, errors in by_level.items():
            print(f"\n{level} ({len(errors)} issues):")
            print("-" * 30)

            for error in errors:
                print(f"  📄 {error.file_path}:{error.line_number}")
                print(f"     {error.message}")
                if error.context:
                    print(f"     Context: {error.context}")
                print()

    def _print_warnings(self) -> None:
        """Print formatted warning report."""
        warnings = [e for e in self.errors if e.level == "WARNING"]
        if not warnings:
            return

        print(f"\n⚠️  {len(warnings)} warnings found:")
        print("-" * 30)

        for warning in warnings[:10]:  # Show first 10
            print(f"  📄 {warning.file_path}:{warning.line_number}")
            print(f"     {warning.message}")

        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more warnings")


def get_argument_parser():
    """Get the argument parser for documentation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Enhanced Sphinx documentation builder"
    )
    parser.add_argument(
        "--builder", "-b", default="html", help="Builder to use (default: html)"
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet mode")
    parser.add_argument(
        "--source", "-s", default="docs/source", help="Source directory"
    )
    parser.add_argument("--build", "-d", default="docs/build", help="Build directory")
    return parser


def main():
    """Main entry point."""
    builder = SphinxBuilder()

    # Parse command line arguments
    parser = get_argument_parser()

    args = parser.parse_args()

    builder.source_dir = Path(args.source)
    builder.build_dir = Path(args.build)

    success = builder.build(args.builder, verbose=not args.quiet)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
