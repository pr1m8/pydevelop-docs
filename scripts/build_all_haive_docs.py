#!/usr/bin/env python3
"""
Build all Haive package documentation using PyDevelop-Docs.

This script:
1. Initializes documentation for each Haive package
2. Builds all documentation
3. Creates a central hub index
4. Opens the result in the browser
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

# Colors for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_status(message: str, color: str = BLUE):
    """Print colored status message."""
    print(f"{color}{'='*80}{RESET}")
    print(f"{color}{message}{RESET}")
    print(f"{color}{'='*80}{RESET}")


def run_command(cmd: List[str], cwd: str = None) -> Tuple[bool, str]:
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}\n{e.stdout}"


def build_package_docs(package_path: Path, package_name: str) -> bool:
    """Build documentation for a single package."""
    print(f"\n{BLUE}📦 Building documentation for {package_name}...{RESET}")

    # Check if package has pyproject.toml
    if not (package_path / "pyproject.toml").exists():
        print(f"{YELLOW}⚠️  Skipping {package_name} - no pyproject.toml found{RESET}")
        return False

    # Initialize PyDevelop-Docs
    print(f"  Initializing PyDevelop-Docs...")
    success, output = run_command(
        ["poetry", "run", "pydevelop-docs", "init", "--force", "--yes"],
        cwd=str(package_path),
    )

    if not success:
        print(f"{RED}  ❌ Failed to initialize: {output}{RESET}")
        return False

    print(f"{GREEN}  ✅ Initialized successfully{RESET}")

    # Build documentation
    print(f"  Building Sphinx documentation...")
    docs_source = package_path / "docs" / "source"
    docs_build = package_path / "docs" / "build"

    if not docs_source.exists():
        print(f"{RED}  ❌ No docs/source directory found{RESET}")
        return False

    # Clean build directory
    if docs_build.exists():
        shutil.rmtree(docs_build)

    success, output = run_command(
        ["poetry", "run", "sphinx-build", "-b", "html", "source", "build", "-E"],
        cwd=str(package_path / "docs"),
    )

    if not success:
        # Check if it's a union type error
        if "unsupported operand type" in output and "NoneType" in output:
            print(
                f"{YELLOW}  ⚠️  Union type syntax detected - using fallback mode{RESET}"
            )
        else:
            print(f"{RED}  ❌ Build failed: {output}{RESET}")
            return False

    # Check if build succeeded despite warnings
    if (docs_build / "index.html").exists():
        print(f"{GREEN}  ✅ Documentation built successfully{RESET}")
        return True
    else:
        print(f"{RED}  ❌ Build failed - no output generated{RESET}")
        return False


def create_central_hub(haive_root: Path, built_packages: List[str]):
    """Create a central documentation hub."""
    print(f"\n{BLUE}🏠 Creating central documentation hub...{RESET}")

    hub_dir = haive_root / "docs" / "hub"
    hub_dir.mkdir(parents=True, exist_ok=True)

    # Create index.html
    index_content = """<!DOCTYPE html>
<html>
<head>
    <title>Haive Documentation Hub</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 2rem;
        }
        .packages {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }
        .package {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .package:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .package h2 {
            margin: 0 0 0.5rem 0;
            color: #2563eb;
        }
        .package a {
            color: #2563eb;
            text-decoration: none;
        }
        .package a:hover {
            text-decoration: underline;
        }
        .status {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.875rem;
            margin-left: 0.5rem;
        }
        .status.success {
            background: #10b981;
            color: white;
        }
        .status.failed {
            background: #ef4444;
            color: white;
        }
        .timestamp {
            text-align: center;
            color: #666;
            margin-top: 2rem;
            font-size: 0.875rem;
        }
    </style>
</head>
<body>
    <h1>🚀 Haive Documentation Hub</h1>
    <div class="packages">
"""

    # Add each package
    for package in [
        "haive-core",
        "haive-agents",
        "haive-tools",
        "haive-games",
        "haive-dataflow",
        "haive-mcp",
        "haive-prebuilt",
    ]:
        status = "success" if package in built_packages else "failed"
        status_text = "✅ Built" if status == "success" else "❌ Not Built"

        package_path = f"../../packages/{package}/docs/build/index.html"

        index_content += f"""
        <div class="package">
            <h2>{package}</h2>
            <span class="status {status}">{status_text}</span>
            <p>Documentation for the {package} package.</p>
            <a href="{package_path}" target="_blank">View Documentation →</a>
        </div>
"""

    index_content += f"""
    </div>
    <div class="timestamp">
        Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>
"""

    (hub_dir / "index.html").write_text(index_content)
    print(f"{GREEN}✅ Documentation hub created{RESET}")
    return hub_dir / "index.html"


def main():
    """Main function to build all Haive documentation."""
    print_status("🚀 Haive Documentation Builder", GREEN)

    # Get Haive root directory
    haive_root = Path(__file__).parent.parent.parent.parent
    packages_dir = haive_root / "packages"

    if not packages_dir.exists():
        print(f"{RED}❌ Packages directory not found at {packages_dir}{RESET}")
        sys.exit(1)

    # List of packages to build (skip problematic ones if needed)
    packages_to_build = [
        "haive-core",
        "haive-agents",
        "haive-tools",
        "haive-games",
        "haive-dataflow",
        "haive-mcp",
        "haive-prebuilt",
    ]

    # Skip packages without proper structure
    skip_packages = ["haive-models", "haive-agp", "haive-ui"]

    built_packages = []
    failed_packages = []

    # Build each package
    for package_name in packages_to_build:
        package_path = packages_dir / package_name

        if not package_path.exists():
            print(f"{YELLOW}⚠️  Package {package_name} not found{RESET}")
            continue

        if package_name in skip_packages:
            print(f"{YELLOW}⚠️  Skipping {package_name} (marked to skip){RESET}")
            continue

        if build_package_docs(package_path, package_name):
            built_packages.append(package_name)
        else:
            failed_packages.append(package_name)

    # Summary
    print_status("📊 Build Summary", BLUE)
    print(f"{GREEN}✅ Successfully built: {len(built_packages)} packages{RESET}")
    for pkg in built_packages:
        print(f"   - {pkg}")

    if failed_packages:
        print(f"\n{RED}❌ Failed to build: {len(failed_packages)} packages{RESET}")
        for pkg in failed_packages:
            print(f"   - {pkg}")

    # Create central hub
    hub_index = create_central_hub(haive_root, built_packages)

    # Open documentation
    print_status("🌐 Opening Documentation", GREEN)

    # Try to open the hub
    try:
        subprocess.run(["xdg-open", str(hub_index)])
        print(f"{GREEN}✅ Documentation hub opened in browser{RESET}")
    except Exception as e:
        print(f"{YELLOW}⚠️  Could not open browser automatically: {e}{RESET}")
        print(f"Open manually: file://{hub_index}")

    # Also print individual package URLs
    print(f"\n{BLUE}📚 Individual Package Documentation:{RESET}")
    for package in built_packages:
        doc_path = packages_dir / package / "docs" / "build" / "index.html"
        print(f"   {package}: file://{doc_path}")


if __name__ == "__main__":
    main()
