#!/usr/bin/env python3
"""Test seed-intersphinx-mapping functionality."""

import sys
from pathlib import Path

# Add docs/source to path so we can import conf
docs_source = Path(__file__).parent.parent / "docs" / "source"
sys.path.insert(0, str(docs_source))

# Import the conf module
import conf

print("Current intersphinx_mapping:")
print("=" * 50)
for key, value in conf.intersphinx_mapping.items():
    print(f"{key:20} -> {value[0]}")

print("\n\nChecking seed-intersphinx-mapping configuration:")
print("=" * 50)
print(f"pkg_requirements_source: {getattr(conf, 'pkg_requirements_source', 'NOT SET')}")
print(f"repository_root: {getattr(conf, 'repository_root', 'NOT SET')}")

# Try to manually trigger seed-intersphinx-mapping
print("\n\nAttempting to read pyproject.toml dependencies:")
print("=" * 50)

import toml

pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
if pyproject_path.exists():
    data = toml.load(pyproject_path)

    # Check standard dependencies
    if "project" in data and "dependencies" in data["project"]:
        print("Standard dependencies:")
        for dep in data["project"]["dependencies"][:10]:
            print(f"  - {dep}")

    # Check Poetry dependencies
    if (
        "tool" in data
        and "poetry" in data["tool"]
        and "dependencies" in data["tool"]["poetry"]
    ):
        print("\nPoetry dependencies:")
        deps = data["tool"]["poetry"]["dependencies"]
        for name, version in list(deps.items())[:10]:
            if name != "python":
                print(f"  - {name}: {version}")

    # Check docs group
    if (
        "tool" in data
        and "poetry" in data["tool"]
        and "group" in data["tool"]["poetry"]
    ):
        if (
            "docs" in data["tool"]["poetry"]["group"]
            and "dependencies" in data["tool"]["poetry"]["group"]["docs"]
        ):
            print("\nDocs group dependencies:")
            deps = data["tool"]["poetry"]["group"]["docs"]["dependencies"]
            for name, version in list(deps.items())[:10]:
                print(f"  - {name}: {version}")
