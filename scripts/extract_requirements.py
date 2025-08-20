#!/usr/bin/env python3
"""Extract requirements from pyproject.toml for Read the Docs."""

import tomlkit
from pathlib import Path

def extract_requirements():
    """Extract requirements from pyproject.toml and generate requirements.txt"""
    
    # Load pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "r") as f:
        data = tomlkit.load(f)
    
    requirements = []
    
    # Extract main dependencies (excluding Python version constraint)
    main_deps = data["tool"]["poetry"]["dependencies"]
    for name, version in main_deps.items():
        if name != "python":
            # Convert poetry version constraints to pip format
            if isinstance(version, str):
                if version.startswith("^"):
                    version = ">=" + version[1:]
                elif version.startswith("~"):
                    version = "~=" + version[1:]
                requirements.append(f"{name}{version}")
            elif isinstance(version, dict):
                # Handle complex version specifications
                if "version" in version:
                    req_version = version["version"]
                    if req_version.startswith("^"):
                        req_version = ">=" + req_version[1:]
                    requirements.append(f"{name}{req_version}")
    
    # Extract docs dependencies
    if "docs" in data["tool"]["poetry"]["group"]:
        docs_deps = data["tool"]["poetry"]["group"]["docs"]["dependencies"]
        for name, version in docs_deps.items():
            if isinstance(version, str):
                if version.startswith("^"):
                    version = ">=" + version[1:]
                elif version.startswith("~"):
                    version = "~=" + version[1:]
                requirements.append(f"{name}{version}")
    
    # Write requirements.txt
    output_path = Path(__file__).parent.parent / "docs" / "requirements.txt"
    with open(output_path, "w") as f:
        f.write("# Auto-generated from pyproject.toml\n")
        f.write("# Run: python scripts/extract_requirements.py to update\n\n")
        for req in sorted(requirements):
            f.write(f"{req}\n")
    
    print(f"Generated {output_path} with {len(requirements)} dependencies")

if __name__ == "__main__":
    extract_requirements()