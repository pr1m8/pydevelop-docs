"""General project setup for any Python project.

This module provides functionality to automatically detect and set up
documentation for any Python project structure.
"""

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import click
import tomlkit
import yaml


class ProjectDetector:
    """Detect and analyze Python project structure."""

    def __init__(self, project_path: Path):
        self.project_path = project_path.resolve()

    def detect_project_type(self) -> Dict[str, Any]:
        """Detect the type and structure of the Python project."""
        info = {
            "type": "unknown",
            "name": self.project_path.name,
            "package_manager": self._detect_package_manager(),
            "structure": self._detect_structure(),
            "packages": self._find_packages(),
            "source_dirs": self._find_source_dirs(),
            "has_tests": self._has_tests(),
            "has_docs": self._has_docs(),
            "python_files": self._count_python_files(),
            "dependencies": self._analyze_dependencies(),
            "metadata": self._extract_metadata(),
        }

        # Determine project type based on structure
        if len(info["packages"]) > 1:
            info["type"] = "monorepo"
        elif len(info["packages"]) == 1:
            info["type"] = "single_package"
        elif info["source_dirs"]:
            info["type"] = "simple_project"
        else:
            info["type"] = "unknown"

        return info

    def _detect_package_manager(self) -> Optional[str]:
        """Detect which package manager is being used."""
        if (self.project_path / "pyproject.toml").exists():
            try:
                pyproject = tomlkit.parse((self.project_path / "pyproject.toml").read_text())
                if "poetry" in str(pyproject):
                    return "poetry"
                elif "setuptools" in str(pyproject):
                    return "setuptools"
                elif "flit" in str(pyproject):
                    return "flit"
                elif "hatchling" in str(pyproject):
                    return "hatch"
                return "pyproject"
            except Exception:
                return "pyproject"

        if (self.project_path / "poetry.lock").exists():
            return "poetry"
        if (self.project_path / "setup.py").exists():
            return "setuptools"
        if (self.project_path / "requirements.txt").exists():
            return "pip"
        if (self.project_path / "Pipfile").exists():
            return "pipenv"
        if (self.project_path / "environment.yml").exists():
            return "conda"

        return None

    def _detect_structure(self) -> Dict[str, Any]:
        """Detect the project structure pattern."""
        structure = {
            "pattern": "unknown",
            "src_layout": False,
            "flat_layout": False,
            "namespace_packages": False,
            "monorepo": False,
        }

        # Check for src layout
        src_dir = self.project_path / "src"
        if src_dir.exists() and any(src_dir.iterdir()):
            structure["src_layout"] = True
            structure["pattern"] = "src_layout"

        # Check for packages directory (monorepo pattern)
        packages_dir = self.project_path / "packages"
        if packages_dir.exists() and any(packages_dir.iterdir()):
            structure["monorepo"] = True
            structure["pattern"] = "monorepo"

        # Check for flat layout
        python_dirs = [d for d in self.project_path.iterdir() 
                      if d.is_dir() and (d / "__init__.py").exists()]
        if python_dirs and not structure["src_layout"] and not structure["monorepo"]:
            structure["flat_layout"] = True
            if structure["pattern"] == "unknown":
                structure["pattern"] = "flat_layout"

        return structure

    def _find_packages(self) -> List[Dict[str, Any]]:
        """Find all Python packages in the project."""
        packages = []

        # Check different locations
        search_dirs = [
            self.project_path / "src",
            self.project_path / "packages",
            self.project_path,
        ]

        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            # Find packages in this directory
            for item in search_dir.iterdir():
                if not item.is_dir():
                    continue

                # Skip common non-package directories
                if item.name.startswith(".") or item.name in {
                    "__pycache__", "tests", "test", "docs", "build", "dist",
                    "venv", ".venv", "node_modules", ".git", ".tox", ".pytest_cache"
                }:
                    continue

                # Check if it's a Python package
                package_info = self._analyze_package(item, search_dir)
                if package_info:
                    packages.append(package_info)

        return packages

    def _analyze_package(self, package_path: Path, root_dir: Path) -> Optional[Dict[str, Any]]:
        """Analyze a potential package directory."""
        # Check if it has __init__.py
        init_file = package_path / "__init__.py"
        if not init_file.exists():
            # Check if it contains subdirectories with __init__.py
            has_python_packages = any(
                (subdir / "__init__.py").exists()
                for subdir in package_path.iterdir()
                if subdir.is_dir()
            )
            if not has_python_packages:
                return None

        # Count Python files
        python_files = list(package_path.rglob("*.py"))
        if not python_files:
            return None

        # Determine relative path
        try:
            relative_path = package_path.relative_to(self.project_path)
        except ValueError:
            relative_path = package_path

        return {
            "name": package_path.name,
            "path": str(package_path),
            "relative_path": str(relative_path),
            "root_dir": str(root_dir),
            "python_files": len(python_files),
            "has_init": init_file.exists(),
            "has_docs": (package_path / "docs").exists(),
            "subpackages": self._find_subpackages(package_path),
        }

    def _find_subpackages(self, package_path: Path) -> List[str]:
        """Find subpackages within a package."""
        subpackages = []
        for item in package_path.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                subpackages.append(item.name)
        return subpackages

    def _find_source_dirs(self) -> List[str]:
        """Find directories containing Python source code."""
        source_dirs = []
        
        # Common source directory names
        common_dirs = ["src", "lib", "code", "source"]
        
        for dirname in common_dirs:
            dir_path = self.project_path / dirname
            if dir_path.exists() and any(dir_path.rglob("*.py")):
                source_dirs.append(dirname)

        return source_dirs

    def _has_tests(self) -> bool:
        """Check if the project has tests."""
        test_indicators = [
            "tests", "test", "testing", "pytest", "unittest"
        ]
        
        for indicator in test_indicators:
            if (self.project_path / indicator).exists():
                return True
            
        # Check for test files
        test_files = list(self.project_path.rglob("test_*.py")) + \
                    list(self.project_path.rglob("*_test.py"))
        return len(test_files) > 0

    def _has_docs(self) -> bool:
        """Check if the project already has documentation."""
        return (self.project_path / "docs").exists()

    def _count_python_files(self) -> int:
        """Count total Python files in the project."""
        return len(list(self.project_path.rglob("*.py")))

    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies."""
        deps = {
            "has_requirements_txt": (self.project_path / "requirements.txt").exists(),
            "has_pyproject_toml": (self.project_path / "pyproject.toml").exists(),
            "has_setup_py": (self.project_path / "setup.py").exists(),
            "sphinx_deps": [],
            "doc_deps": [],
        }

        # Check for existing Sphinx dependencies
        if deps["has_pyproject_toml"]:
            try:
                pyproject = tomlkit.parse((self.project_path / "pyproject.toml").read_text())
                
                # Check dependencies
                for section in ["dependencies", "dev-dependencies", "docs"]:
                    if section in pyproject.get("tool", {}).get("poetry", {}):
                        deps_list = pyproject["tool"]["poetry"][section]
                        for dep in deps_list:
                            if "sphinx" in dep.lower():
                                deps["sphinx_deps"].append(dep)
                            elif any(doc_term in dep.lower() for doc_term in 
                                   ["doc", "documentation", "readme", "markdown"]):
                                deps["doc_deps"].append(dep)

            except Exception:
                pass

        return deps

    def _extract_metadata(self) -> Dict[str, Any]:
        """Extract project metadata."""
        metadata = {
            "title": self.project_path.name,
            "description": "",
            "author": "",
            "version": "",
            "license": "",
            "url": "",
        }

        # Try to extract from pyproject.toml
        if (self.project_path / "pyproject.toml").exists():
            try:
                pyproject = tomlkit.parse((self.project_path / "pyproject.toml").read_text())
                
                # Poetry metadata
                if "poetry" in pyproject.get("tool", {}):
                    poetry = pyproject["tool"]["poetry"]
                    metadata.update({
                        "title": poetry.get("name", metadata["title"]),
                        "description": poetry.get("description", ""),
                        "author": poetry.get("author", ""),
                        "version": poetry.get("version", ""),
                        "license": poetry.get("license", ""),
                        "url": poetry.get("homepage", poetry.get("repository", "")),
                    })
                
                # Standard project metadata
                elif "project" in pyproject:
                    project = pyproject["project"]
                    metadata.update({
                        "title": project.get("name", metadata["title"]),
                        "description": project.get("description", ""),
                        "version": project.get("version", ""),
                        "license": project.get("license", {}).get("text", ""),
                    })
                    
                    if "authors" in project and project["authors"]:
                        metadata["author"] = project["authors"][0].get("name", "")

            except Exception:
                pass

        # Try to extract from setup.py (basic)
        if (self.project_path / "setup.py").exists():
            try:
                setup_content = (self.project_path / "setup.py").read_text()
                # Basic regex extraction would go here
                # For now, just use the directory name
                pass
            except Exception:
                pass

        return metadata


class GeneralDocumentationSetup:
    """Set up documentation for any Python project."""

    def __init__(self, project_path: Path, target_dir: Optional[Path] = None):
        self.project_path = project_path.resolve()
        self.target_dir = target_dir or (project_path / "docs")
        self.detector = ProjectDetector(project_path)

    def setup_documentation(self, 
                           force: bool = False,
                           interactive: bool = True,
                           dry_run: bool = False) -> Dict[str, Any]:
        """Set up documentation for the detected project."""
        
        # Detect project structure
        project_info = self.detector.detect_project_type()
        
        if interactive:
            self._display_project_info(project_info)
            if not click.confirm("Proceed with documentation setup?"):
                return {"status": "cancelled"}

        if dry_run:
            return self._create_dry_run_plan(project_info)

        # Create documentation structure
        result = self._create_documentation_structure(project_info, force)
        
        # Copy templates and configuration
        self._setup_configuration(project_info)
        
        # Generate initial content
        self._generate_initial_content(project_info)
        
        return result

    def _display_project_info(self, project_info: Dict[str, Any]):
        """Display detected project information."""
        click.echo("\n🔍 Project Analysis Results:")
        click.echo(f"  📁 Project: {project_info['name']}")
        click.echo(f"  🏗️  Type: {project_info['type']}")
        click.echo(f"  📦 Package Manager: {project_info['package_manager'] or 'None detected'}")
        click.echo(f"  📊 Structure: {project_info['structure']['pattern']}")
        click.echo(f"  🐍 Python Files: {project_info['python_files']}")
        click.echo(f"  📚 Has Docs: {'Yes' if project_info['has_docs'] else 'No'}")
        click.echo(f"  🧪 Has Tests: {'Yes' if project_info['has_tests'] else 'No'}")
        
        if project_info['packages']:
            click.echo(f"\n📦 Found {len(project_info['packages'])} package(s):")
            for pkg in project_info['packages']:
                click.echo(f"  • {pkg['name']} ({pkg['python_files']} files)")

    def _create_dry_run_plan(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create a plan of what would be done without executing."""
        plan = {
            "status": "dry_run",
            "project_info": project_info,
            "actions": [],
        }
        
        # Documentation directory
        if not self.target_dir.exists():
            plan["actions"].append(f"📁 Create directory: {self.target_dir}")
        
        # Configuration files
        plan["actions"].extend([
            f"📄 Create: {self.target_dir}/source/conf.py",
            f"📄 Create: {self.target_dir}/source/index.rst",
            f"📄 Create: {self.target_dir}/Makefile",
            f"📁 Create: {self.target_dir}/source/_static",
            f"📁 Create: {self.target_dir}/source/_templates",
        ])
        
        # Package-specific setup
        for pkg in project_info['packages']:
            plan["actions"].append(f"📦 Configure package: {pkg['name']}")
        
        return plan

    def _create_documentation_structure(self, project_info: Dict[str, Any], force: bool) -> Dict[str, Any]:
        """Create the documentation directory structure."""
        if self.target_dir.exists() and not force:
            if not click.confirm(f"Documentation directory {self.target_dir} exists. Continue?"):
                return {"status": "cancelled"}

        # Create directories
        directories = [
            self.target_dir / "source",
            self.target_dir / "source" / "_static",
            self.target_dir / "source" / "_static" / "css",
            self.target_dir / "source" / "_templates",
            self.target_dir / "build",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        return {"status": "created", "directories": [str(d) for d in directories]}

    def _setup_configuration(self, project_info: Dict[str, Any]):
        """Set up Sphinx configuration based on project type."""
        # Import configuration from our existing system
        from .config import get_haive_config
        
        # Get base configuration
        config = get_haive_config(
            package_name=project_info['name'],
            package_dir=str(self.project_path),
            base_dir=str(self.project_path)
        )
        
        # Customize based on project info
        metadata = project_info['metadata']
        config.update({
            'project': metadata['title'],
            'author': metadata['author'] or 'Documentation Team',
            'version': metadata['version'] or '0.1.0',
            'release': metadata['version'] or '0.1.0',
        })
        
        # Adjust AutoAPI settings based on structure
        if project_info['structure']['src_layout']:
            config['autoapi_dirs'] = ['../src']
        elif project_info['structure']['monorepo']:
            config['autoapi_dirs'] = ['../packages']
        else:
            # Find the main package directory
            if project_info['packages']:
                main_pkg = project_info['packages'][0]
                config['autoapi_dirs'] = [f"../{main_pkg['relative_path']}"]

        # Write configuration file
        conf_py_path = self.target_dir / "source" / "conf.py"
        self._write_conf_py(conf_py_path, config)

    def _write_conf_py(self, conf_py_path: Path, config: Dict[str, Any]):
        """Write the conf.py file with the configuration."""
        conf_content = f'''"""
Configuration file for the Sphinx documentation builder.

Generated by PyDevelop-Docs for {config.get('project', 'Unknown Project')}.
"""

# -- Project information -----------------------------------------------------

project = "{config.get('project', 'Documentation')}"
author = "{config.get('author', 'Documentation Team')}"
version = "{config.get('version', '0.1.0')}"
release = "{config.get('release', '0.1.0')}"

# -- General configuration ---------------------------------------------------

extensions = {config.get('extensions', [])}

# -- AutoAPI configuration ---------------------------------------------------

autoapi_dirs = {config.get('autoapi_dirs', ['../src'])}
autoapi_type = "python"
autoapi_template_dir = "_autoapi_templates"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]
autoapi_own_page_level = "module"  # Hierarchical organization
autoapi_keep_files = True

# -- HTML output options -----------------------------------------------------

html_theme = "{config.get('html_theme', 'furo')}"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]

html_theme_options = {{
    "navigation_with_keys": True,
    "sidebar_hide_name": True,
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
}}

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Intersphinx settings
intersphinx_mapping = {{
    "python": ("https://docs.python.org/3", None),
}}

# Copy button settings
copybutton_prompt_text = r">>> |\\.\\.\\. |\\$ |In \\[\\d*\\]: | {2,5}\\.\\.\\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# -- Custom configuration ---------------------------------------------------

# Add any custom configuration here
'''

        conf_py_path.write_text(conf_content)

    def _generate_initial_content(self, project_info: Dict[str, Any]):
        """Generate initial documentation content."""
        # Create index.rst
        self._create_index_rst(project_info)
        
        # Create Makefile
        self._create_makefile()
        
        # Copy static files
        self._copy_static_files()
        
        # Create custom CSS
        self._create_custom_css()

    def _create_index_rst(self, project_info: Dict[str, Any]):
        """Create the main index.rst file."""
        metadata = project_info['metadata']
        
        index_content = f'''{metadata['title']}
{'=' * len(metadata['title'])}

{metadata['description'] or f"Documentation for {metadata['title']}"}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   autoapi/index

Installation
============

To install {metadata['title']}:

.. code-block:: bash

   pip install {metadata['title'].lower().replace(' ', '-')}

Quick Start
===========

Here's how to get started with {metadata['title']}:

.. code-block:: python

   # Add your quick start example here
   import {project_info['packages'][0]['name'] if project_info['packages'] else 'your_package'}
   
   # Example usage
   print("Hello from {metadata['title']}!")

API Reference
=============

.. toctree::
   :maxdepth: 1
   
   autoapi/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
'''

        index_path = self.target_dir / "source" / "index.rst"
        index_path.write_text(index_content)

    def _create_makefile(self):
        """Create Makefile for building documentation."""
        makefile_content = '''# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    = -W --keep-going
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
\t@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
\t@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets
clean:
\trm -rf $(BUILDDIR)/* $(SOURCEDIR)/autoapi

livehtml:
\tsphinx-autobuild -b html $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/html

linkcheck:
\t$(SPHINXBUILD) -b linkcheck $(SOURCEDIR) $(BUILDDIR)/linkcheck
'''

        makefile_path = self.target_dir / "Makefile"
        makefile_path.write_text(makefile_content)

    def _copy_static_files(self):
        """Copy static files from templates."""
        # Copy CSS and other static files from our templates
        template_static = Path(__file__).parent / "templates" / "static"
        target_static = self.target_dir / "source" / "_static"
        
        if template_static.exists():
            for item in template_static.rglob("*"):
                if item.is_file():
                    relative_path = item.relative_to(template_static)
                    target_file = target_static / relative_path
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target_file)

    def _create_custom_css(self):
        """Create custom CSS file."""
        css_content = '''/* Custom styles for documentation */

/* Improve readability */
.bd-main .bd-content .bd-article-container {
    max-width: 100rem;
}

/* Better code block styling */
.highlight {
    border-radius: 0.375rem;
    margin: 1rem 0;
}

/* Responsive improvements */
@media (max-width: 768px) {
    .bd-sidebar {
        transform: translateX(-100%);
    }
}

/* Dark mode improvements */
[data-theme="dark"] {
    --color-background-primary: #1a1a1a;
    --color-background-secondary: #262626;
}
'''

        css_path = self.target_dir / "source" / "_static" / "css" / "custom.css"
        css_path.parent.mkdir(parents=True, exist_ok=True)
        css_path.write_text(css_content)


def setup_project_docs(project_path: str,
                      target_dir: Optional[str] = None,
                      force: bool = False,
                      interactive: bool = True,
                      dry_run: bool = False) -> Dict[str, Any]:
    """Main function to set up documentation for any Python project."""
    
    project_path = Path(project_path).resolve()
    target_dir = Path(target_dir) if target_dir else project_path / "docs"
    
    if not project_path.exists():
        raise ValueError(f"Project path does not exist: {project_path}")
    
    if not project_path.is_dir():
        raise ValueError(f"Project path is not a directory: {project_path}")
    
    setup = GeneralDocumentationSetup(project_path, target_dir)
    return setup.setup_documentation(force=force, interactive=interactive, dry_run=dry_run)