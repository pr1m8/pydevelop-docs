#!/usr/bin/env python3
"""
Demonstration of the AutoAPI flattening issue.

This script simulates what AutoAPI discovers in our complex nested structure
and shows how it creates a flat alphabetical list instead of hierarchical organization.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Set


def discover_classes_in_file(file_path: Path) -> Dict[str, List[str]]:
    """Discover classes in a Python file (simulates AutoAPI discovery)."""
    try:
        with open(file_path, "r") as f:
            content = f.read()

        tree = ast.parse(content)

        classes = []
        enums = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it's an enum
                if any(
                    isinstance(base, ast.Attribute) and base.attr == "Enum"
                    for base in node.bases
                ):
                    enums.append(node.name)
                elif any(
                    isinstance(base, ast.Name) and base.id == "Enum"
                    for base in node.bases
                ):
                    enums.append(node.name)
                else:
                    classes.append(node.name)

        return {"classes": classes, "enums": enums}

    except Exception as e:
        return {"classes": [], "enums": []}


def scan_packages() -> Dict[str, Dict[str, List[str]]]:
    """Scan all packages and discover their structure."""
    packages = {}

    for package_dir in Path("packages").iterdir():
        if not package_dir.is_dir():
            continue

        package_name = package_dir.name
        src_dir = package_dir / "src"

        if not src_dir.exists():
            continue

        modules = {}

        # Walk through all Python files
        for py_file in src_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            # Convert path to module name
            rel_path = py_file.relative_to(src_dir)
            module_name = str(rel_path.with_suffix(""))
            module_name = module_name.replace(os.sep, ".")

            discovered = discover_classes_in_file(py_file)
            if discovered["classes"] or discovered["enums"]:
                modules[module_name] = discovered

        if modules:
            packages[package_name] = modules

    return packages


def show_flat_structure(packages: Dict[str, Dict[str, List[str]]]):
    """Show the current flat AutoAPI structure (the problem)."""
    print("🔴 CURRENT AUTOAPI STRUCTURE (BAD - Flat Alphabetical)")
    print("=" * 60)

    all_items = []

    for package_name, modules in packages.items():
        for module_name, items in modules.items():
            for class_name in items["classes"] + items["enums"]:
                all_items.append(class_name)

    # Sort alphabetically (what AutoAPI does by default)
    all_items.sort()

    print("API Reference")
    for item in all_items:
        print(f"├── {item}")

    print(f"\n📊 STATS: {len(all_items)} items in one flat list - UNUSABLE!")


def show_hierarchical_structure(packages: Dict[str, Dict[str, List[str]]]):
    """Show the desired hierarchical structure (the solution)."""
    print("\n✅ DESIRED HIERARCHICAL STRUCTURE (GOOD - Organized)")
    print("=" * 60)

    print("API Reference")

    for package_name, modules in packages.items():
        # Clean package name for display
        display_name = package_name.replace("testhaive-", "testhaive.")
        print(f"├── {display_name}")

        module_list = list(modules.items())
        for i, (module_name, items) in enumerate(module_list):
            is_last_module = i == len(module_list) - 1
            module_prefix = "└──" if is_last_module else "├──"

            # Clean module name
            clean_module = module_name.replace("testhaive.", "").replace(".", "/")
            print(f"│   {module_prefix} {clean_module}")

            all_items = items["classes"] + items["enums"]
            for j, item in enumerate(all_items):
                is_last_item = j == len(all_items) - 1
                item_prefix = "└──" if is_last_item else "├──"

                if is_last_module:
                    print(f"    {item_prefix} {item}")
                else:
                    print(f"│       {item_prefix} {item}")

    total_items = sum(
        len(items["classes"]) + len(items["enums"])
        for modules in packages.values()
        for items in modules.values()
    )
    print(f"\n📊 STATS: {total_items} items organized logically - USABLE!")


def main():
    """Demonstrate the AutoAPI flattening issue."""
    print("🧪 AUTOAPI FLATTENING ISSUE DEMONSTRATION")
    print("This shows how our complex nested structure gets flattened")
    print("=" * 70)

    # Scan the packages
    packages = scan_packages()

    if not packages:
        print(
            "❌ No packages found. Make sure you're in the test-haive-template directory."
        )
        return

    # Show the problem (flat structure)
    show_flat_structure(packages)

    # Show the solution (hierarchical structure)
    show_hierarchical_structure(packages)

    print("\n🎯 THE PROBLEM:")
    print("- AutoAPI creates a flat alphabetical list of all classes")
    print("- No logical grouping by package or module")
    print("- Impossible to navigate in large projects")
    print("- Loses the architectural organization")

    print("\n💡 THE SOLUTION:")
    print("- Configure autoapi_own_page_level = 'module'")
    print("- Create custom AutoAPI templates for package grouping")
    print("- Use Furo theme navigation settings")
    print("- Maintain logical hierarchical organization")

    print("\n📝 NEXT STEPS:")
    print("1. Test autoapi_own_page_level configuration")
    print("2. Create custom AutoAPI templates")
    print("3. Apply to real Haive documentation")


if __name__ == "__main__":
    main()
