"""Universal documentation initialization tool for Python projects.

This tool can initialize Sphinx documentation with the full PyAutoDoc configuration
for any Python project, whether it's a single package or monorepo.
"""

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
import tomlkit
import yaml

from .autofix import AutoFixer
from .builders import MonorepoBuilder, get_builder
from .config import get_central_hub_config, get_haive_config
from .display import EnhancedDisplay
from .interactive import interactive_cli as run_interactive
from .mock_operations import MockOperationPlan, create_documentation_plan


class ProjectAnalyzer:
    """Analyze Python project structure and configuration."""

    def __init__(self, path: Path):
        self.path = path

    def analyze(self) -> Dict[str, Any]:
        """Analyze project and return detailed configuration and package status."""
        info = {
            "type": "unknown",
            "name": self.path.name,
            "package_manager": None,
            "packages": [],
            "package_details": {},
            "has_docs": (self.path / "docs").exists(),
            "central_hub": self._analyze_central_hub(),
            "structure": None,
            "python_files": [],
            "dependencies": self._analyze_dependencies(),
        }

        # Detect package manager
        if (self.path / "pyproject.toml").exists():
            info["package_manager"] = self._detect_pyproject_manager()
            info["name"] = self._get_project_name()
        elif (self.path / "setup.py").exists():
            info["package_manager"] = "setuptools"
        elif (self.path / "requirements.txt").exists():
            info["package_manager"] = "pip"

        # Detect project type and structure
        if (self.path / "packages").exists():
            info["type"] = "monorepo"
            package_names = [
                p.name
                for p in (self.path / "packages").iterdir()
                if p.is_dir() and not p.name.startswith(".")
            ]
            info["packages"] = package_names
            info["package_details"] = {
                name: self._analyze_package(self.path / "packages" / name)
                for name in package_names
            }
        else:
            info["type"] = "single"
            info["package_details"] = {"single": self._analyze_package(self.path)}

        # Detect source structure
        if (self.path / "src").exists():
            info["structure"] = "src"
            info["python_files"] = list((self.path / "src").rglob("*.py"))
        elif list(self.path.glob("*.py")):
            info["structure"] = "flat"
            info["python_files"] = list(self.path.glob("**/*.py"))

        return info

    def _analyze_package(self, package_path: Path) -> Dict[str, Any]:
        """Analyze individual package structure and status."""
        return {
            "src_exists": (package_path / "src").exists(),
            "docs_exists": (package_path / "docs").exists(),
            "docs_source_exists": (package_path / "docs" / "source").exists(),
            "pyproject_exists": (package_path / "pyproject.toml").exists(),
            "conf_py_exists": (package_path / "docs" / "source" / "conf.py").exists(),
            "changelog_exists": (
                package_path / "docs" / "source" / "changelog.rst"
            ).exists(),
            "index_rst_exists": (
                package_path / "docs" / "source" / "index.rst"
            ).exists(),
            "uses_shared_config": self._uses_shared_config(package_path),
            "python_files_count": (
                len(list(package_path.rglob("*.py"))) if package_path.exists() else 0
            ),
        }

    def _analyze_central_hub(self) -> Dict[str, Any]:
        """Analyze central documentation hub status."""
        docs_path = self.path / "docs"
        return {
            "exists": docs_path.exists(),
            "source_exists": (docs_path / "source").exists(),
            "conf_py_exists": (docs_path / "source" / "conf.py").exists(),
            "index_rst_exists": (docs_path / "source" / "index.rst").exists(),
            "collections_configured": self._check_collections_config(docs_path),
            "build_exists": (docs_path / "build").exists(),
        }

    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Skip dependency analysis for existing projects - focus on documentation only."""
        pyproject_path = self.path / "pyproject.toml"

        if not pyproject_path.exists():
            return {"valid": False, "issues": ["No pyproject.toml found"]}

        try:
            # Just validate that the TOML file is readable
            with open(pyproject_path, "r") as f:
                content = f.read()

            # Ensure it's valid TOML
            tomlkit.parse(content)

            # For existing projects, assume dependencies are correctly managed
            # pydevelop-docs is a documentation tool, not a dependency manager
            return {"valid": True, "issues": []}

        except Exception as e:
            return {"valid": False, "issues": [f"TOML parse error: {e}"]}

    def _analyze_dependencies_old(self) -> Dict[str, Any]:
        """Original naive dependency analysis - now deprecated."""
        pyproject_path = self.path / "pyproject.toml"
        issues = []

        if not pyproject_path.exists():
            return {"valid": False, "issues": ["No pyproject.toml found"]}

        try:
            with open(pyproject_path, "r") as f:
                content = f.read()

            # Check for duplicate entries (DEPRECATED - too broad)
            lines = content.split("\n")
            seen_deps = {}
            for i, line in enumerate(lines, 1):
                if "=" in line and not line.strip().startswith("#"):
                    dep_name = line.split("=")[0].strip()
                    if dep_name in seen_deps and dep_name:
                        issues.append(
                            f"Duplicate dependency '{dep_name}' (lines {seen_deps[dep_name]}, {i})"
                        )
                    else:
                        seen_deps[dep_name] = i

            # Try to parse TOML
            import tomlkit

            tomlkit.parse(content)

        except Exception as e:
            issues.append(f"TOML parse error: {str(e)}")

        return {"valid": len(issues) == 0, "issues": issues}

    def _uses_shared_config(self, package_path: Path) -> bool:
        """Check if package uses shared pydevelop_docs config."""
        conf_py = package_path / "docs" / "source" / "conf.py"
        if not conf_py.exists():
            return False

        try:
            content = conf_py.read_text()
            return "pydevelop_docs.config" in content
        except:
            return False

    def _check_collections_config(self, docs_path: Path) -> bool:
        """Check if sphinx-collections is configured."""
        conf_py = docs_path / "source" / "conf.py"
        if not conf_py.exists():
            return False

        try:
            content = conf_py.read_text()
            return "sphinxcontrib.collections" in content
        except:
            return False

    def _detect_pyproject_manager(self) -> str:
        """Detect which tool manages the pyproject.toml."""
        try:
            with open(self.path / "pyproject.toml") as f:
                data = tomlkit.load(f)

            if "poetry" in data.get("tool", {}):
                return "poetry"
            elif "hatch" in data.get("tool", {}):
                return "hatch"
            elif "pdm" in data.get("tool", {}):
                return "pdm"
            elif "setuptools" in data.get("tool", {}):
                return "setuptools"
            else:
                return "pep621"  # Standard pyproject.toml
        except:
            return "unknown"

    def _get_project_name(self) -> str:
        """Extract project name from pyproject.toml."""
        try:
            with open(self.path / "pyproject.toml") as f:
                data = tomlkit.load(f)

            # Try different locations
            if "poetry" in data.get("tool", {}):
                return data["tool"]["poetry"].get("name", self.path.name)
            elif "project" in data:
                return data["project"].get("name", self.path.name)
            else:
                return self.path.name
        except:
            return self.path.name


class DocsInitializer:
    """Initialize documentation for Python projects."""

    def __init__(
        self,
        project_path: Path,
        project_info: Dict[str, Any],
        doc_config: Dict[str, bool] = None,
    ):
        self.project_path = project_path
        self.project_info = project_info
        self.template_path = Path(__file__).parent / "templates"
        self.doc_config = doc_config or {
            "with_guides": False,
            "with_examples": False,
            "with_cli": False,
            "with_tutorials": False,
        }

    def initialize(self, force: bool = False):
        """Initialize documentation structure."""
        docs_path = self.project_path / "docs"

        if docs_path.exists() and not force:
            raise click.ClickException(
                "Documentation already exists! Use --force to overwrite."
            )

        # Create directory structure
        self._create_directories()

        # Copy static files and templates
        self._copy_static_files()

        # Generate configuration files
        if self.doc_config.get("use_shared_config", True):
            # Use the new consolidated configuration method
            conf_content = self._generate_conf_py_from_config()
        else:
            # Use the legacy hardcoded configuration
            conf_content = self._generate_conf_py()

        # Write the configuration
        conf_path = self.project_path / "docs" / "source" / "conf.py"
        conf_path.write_text(conf_content)

        self._generate_index_rst()
        self._generate_makefile()
        self._generate_build_scripts()

        # Add dependencies if using Poetry
        if self.project_info["package_manager"] == "poetry":
            self._add_poetry_dependencies()

    def _create_directories(self):
        """Create documentation directory structure based on configuration."""
        # Essential directories that are always needed
        essential_dirs = [
            "docs",
            "docs/source",
            "docs/source/_static",
            "docs/source/_static/css",
            "docs/source/_static/js",
            "docs/source/_templates",
            "docs/source/_templates/includes",
            "docs/build",
            "scripts",
        ]

        for dir_path in essential_dirs:
            (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)

        # Create optional documentation sections using template manager
        from .template_manager import TemplateManager

        template_manager = TemplateManager(self.project_path, self.project_info)
        template_manager.create_all_sections(self.doc_config)

    def _copy_static_files(self):
        """Copy static assets from templates."""
        static_files = [
            ("static/css/custom.css", "docs/source/_static/css/custom.css"),
            (
                "static/js/api-enhancements.js",
                "docs/source/_static/js/api-enhancements.js",
            ),
        ]

        for src, dest in static_files:
            src_path = self.template_path / src
            dest_path = self.project_path / dest

            if src_path.exists():
                shutil.copy2(src_path, dest_path)

    def _generate_conf_py_from_config(self):
        """Generate Sphinx configuration using shared config module.

        This method uses the centralized configuration from config.py
        to ensure consistency and prevent duplication.
        """
        from .config import get_haive_config

        # Determine Python path based on project structure
        if self.project_info["structure"] == "src":
            sys_path = 'sys.path.insert(0, os.path.abspath("../../src"))'
        else:
            sys_path = 'sys.path.insert(0, os.path.abspath("../.."))'

        # Generate autoapi directories
        if self.project_info["structure"] == "src":
            autoapi_dirs = '["../../src"]'
        else:
            # Find package directories
            package_dirs = []
            for p in self.project_path.iterdir():
                if p.is_dir() and (p / "__init__.py").exists():
                    package_dirs.append(f'"../../{p.name}"')
            autoapi_dirs = (
                f'[{", ".join(package_dirs)}]' if package_dirs else '["../.."]'
            )

        # Get configuration from shared module
        config = get_haive_config(
            package_name=self.project_info["name"], package_path=str(self.project_path)
        )

        # Build the conf.py content
        conf_content = f'''"""
Sphinx configuration for {self.project_info["name"]}.

This configuration uses PyDevelop-Docs shared configuration.
Generated by pydevelop-docs init.
"""

import os
import sys
from datetime import date

# -- Path setup --------------------------------------------------------------
{sys_path}

# -- Project information -----------------------------------------------------
project = "{self.project_info["name"]}"
copyright = f"{{date.today().year}}, {self.project_info["name"]} Team"
author = "{self.project_info["name"]} Team"
release = "0.1.0"

# -- Import shared configuration from pydevelop_docs -------------------------
from pydevelop_docs.config import get_haive_config

# Get the standardized configuration
_config = get_haive_config(project, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Apply all configuration settings
for key, value in _config.items():
    if key not in ['project', 'copyright', 'author', 'release']:
        globals()[key] = value

# -- Project-specific overrides ----------------------------------------------
# Override autoapi_dirs for this specific project structure
autoapi_dirs = {autoapi_dirs}

# -- Additional setup --------------------------------------------------------

def setup(app):
    """Sphinx setup hook."""
    if os.path.exists("_static/css/custom.css"):
        app.add_css_file("css/custom.css")
    if os.path.exists("_static/js/api-enhancements.js"):
        app.add_js_file("js/api-enhancements.js")
'''

        return conf_content

    def _generate_conf_py(self):
        """Generate Sphinx configuration with full PyAutoDoc setup."""
        # Determine Python path based on project structure
        if self.project_info["structure"] == "src":
            sys_path = 'sys.path.insert(0, os.path.abspath("../../src"))'
        else:
            sys_path = 'sys.path.insert(0, os.path.abspath("../.."))'

        # Generate autoapi directories
        if self.project_info["structure"] == "src":
            autoapi_dirs = '["../../src"]'
        else:
            # Find package directories
            package_dirs = []
            for p in self.project_path.iterdir():
                if p.is_dir() and (p / "__init__.py").exists():
                    package_dirs.append(f'"../../{p.name}"')
            autoapi_dirs = (
                f'[{", ".join(package_dirs)}]' if package_dirs else '["../.."]'
            )

        conf_content = f'''"""
Sphinx configuration for {self.project_info["name"]}.

This configuration includes all extensions from PyAutoDoc (43+ extensions).
Generated by pydevelop-docs init.
"""

import os
import sys
from datetime import date

# -- Path setup --------------------------------------------------------------
{sys_path}

# -- Project information -----------------------------------------------------
project = "{self.project_info["name"]}"
copyright = f"{{date.today().year}}, {self.project_info["name"]} Team"
author = "{self.project_info["name"]} Team"

# The full version, including alpha/beta/rc tags
release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    # API Documentation - MUST BE FIRST
    "autoapi.extension",
    
    # Core Sphinx Extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.githubpages",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    
    # Special Features - MUST BE BEFORE sphinx_autodoc_typehints
    "enum_tools.autoenum",
    "sphinx_toolbox",
    "sphinx_toolbox.more_autodoc.overloads",
    "sphinx_toolbox.more_autodoc.typehints",
    "sphinx_toolbox.more_autodoc.sourcelink",
    
    # Typehints - MUST BE AFTER sphinx_toolbox
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosectionlabel",
    
    # Enhanced Documentation
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinx_design",
    "sphinx_tabs.tabs",
    "sphinx_inline_tabs",
    
    # Diagramming
    "sphinxcontrib.mermaid",
    "sphinxcontrib.plantuml",
    "sphinxcontrib.blockdiag",
    "sphinxcontrib.seqdiag",
    
    # Code and Examples
    "sphinx_codeautolink",
    "sphinx_exec_code",
    "sphinx_runpython",
    
    # UI Enhancements
    "sphinx_tippy",
    "sphinx_favicon",
    "sphinxemoji.sphinxemoji",
    
    # Utilities
    "sphinx_sitemap",
    "sphinx_last_updated_by_git",
    "sphinxext.opengraph",
    "sphinx_reredirects",
    
    # Search and Navigation
    "sphinx_treeview",
    
    # Pydantic Support
    "sphinxcontrib.autodoc_pydantic",
]

# -- Extension Configuration -------------------------------------------------

# AutoAPI configuration
autoapi_dirs = {autoapi_dirs}
autoapi_type = "python"
autoapi_template_dir = "_autoapi_templates"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_python_class_content = "both"
autoapi_member_order = "groupwise"
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_keep_files = True
# ✅ HIERARCHICAL ORGANIZATION FIX - The key setting!
autoapi_own_page_level = "module"  # Keep classes with their modules

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {{
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
}}
autodoc_typehints = "both"
autodoc_typehints_format = "short"
autodoc_mock_imports = []
autodoc_preserve_defaults = True

# MyST parser
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]
myst_heading_anchors = 3
myst_substitutions = {{
    "project": project,
}}

# Intersphinx mapping
intersphinx_mapping = {{
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}}

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
html_js_files = [
    "js/api-enhancements.js",
]

html_theme_options = {{
    "light_logo": "logo-light.png",
    "dark_logo": "logo-dark.png",
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["view", "edit"],
}}

html_favicon = "_static/favicon.ico"
html_title = f"{{project}} Documentation"
html_short_title = project
html_baseurl = ""

# -- Additional Configuration ------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"
pygments_dark_style = "monokai"

# -- Extension-specific settings ---------------------------------------------

# Sphinx-sitemap
html_baseurl = "https://docs.example.com/"
sitemap_locales = [None]
sitemap_url_scheme = "{{link}}"

# Tippy
tippy_props = {{
    "placement": "auto-start",
    "maxWidth": 500,
    "theme": "light-border",
    "interactive": True,
}}

# Mermaid
mermaid_version = "10.6.1"
mermaid_init_js = """
mermaid.initialize({{
    startOnLoad: true,
    theme: 'default',
    themeVariables: {{
        primaryColor: '#007bff',
        primaryBorderColor: '#0056b3',
        lineColor: '#333',
        secondaryColor: '#6c757d',
        tertiaryColor: '#f8f9fa'
    }}
}});
"""

# Todo extension
todo_include_todos = True

# Coverage extension
coverage_show_missing_items = True

def setup(app):
    """Sphinx setup hook."""
    app.add_css_file("css/custom.css")
    app.add_js_file("js/api-enhancements.js")
'''

        return conf_content

    def _generate_index_rst(self):
        """Generate index.rst file with configurable TOC sections."""
        # Build TOC entries based on configuration options
        toc_entries = []

        # Always include autoapi if it will be generated
        toc_entries.append("autoapi/index")

        # Add optional sections based on configuration (defaulting to false)
        if self.doc_config.get("with_guides", False):
            toc_entries.append("guides/index")

        if self.doc_config.get("with_examples", False):
            toc_entries.append("examples/index")

        if self.doc_config.get("with_cli", False):
            toc_entries.append("cli/index")

        if self.doc_config.get("with_tutorials", False):
            toc_entries.append("tutorials/index")

        # Always include changelog if it exists (this is typically generated)
        docs_source = self.project_path / "docs" / "source"
        if (docs_source / "changelog.rst").exists():
            toc_entries.append("changelog")

        # Generate TOC content
        toc_content = "\n   ".join(toc_entries)

        index_content = f"""
Welcome to {self.project_info["name"]} Documentation
{"=" * (len(self.project_info["name"]) + 25)}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   {toc_content}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

        index_path = self.project_path / "docs" / "source" / "index.rst"
        index_path.write_text(index_content)

    def _generate_makefile(self):
        """Generate Makefile for building docs."""
        makefile_content = """# Minimal makefile for Sphinx documentation

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
"""

        makefile_path = self.project_path / "docs" / "Makefile"
        makefile_path.write_text(makefile_content)

    def _generate_build_scripts(self):
        """Generate build scripts."""
        build_script = """#!/bin/bash
# Build documentation

set -e

echo "Building documentation..."

# Clean previous builds
rm -rf docs/build/*

# Build HTML documentation
cd docs && make html

echo "Documentation built successfully!"
echo "Open docs/build/html/index.html to view."
"""

        script_path = self.project_path / "scripts" / "build-docs.sh"
        script_path.write_text(build_script)
        script_path.chmod(0o755)

    def _add_poetry_dependencies(self):
        """Add documentation dependencies to pyproject.toml."""
        pyproject_path = self.project_path / "pyproject.toml"

        try:
            with open(pyproject_path) as f:
                doc = tomlkit.load(f)

            # Ensure structure exists
            if "tool" not in doc:
                doc["tool"] = {}
            if "poetry" not in doc["tool"]:
                doc["tool"]["poetry"] = {}
            if "group" not in doc["tool"]["poetry"]:
                doc["tool"]["poetry"]["group"] = {}
            if "docs" not in doc["tool"]["poetry"]["group"]:
                doc["tool"]["poetry"]["group"]["docs"] = {"dependencies": {}}

            # Add all documentation dependencies
            deps = doc["tool"]["poetry"]["group"]["docs"]["dependencies"]

            # Core dependencies
            deps.update(
                {
                    "sphinx": "^8.2.3",
                    "sphinx-autoapi": "^3.6.0",
                    "sphinx-autodoc-typehints": "^3.1.0",
                    "sphinxcontrib-autodoc-pydantic": "^2.2.0",
                    "furo": "^2024.8.6",
                    "myst-parser": "^4.0.1",
                    # UI enhancements
                    "sphinx-copybutton": "^0.5.2",
                    "sphinx-togglebutton": "^0.3.2",
                    "sphinx-design": "^0.6.1",
                    "sphinx-tabs": "^3.4.5",
                    "sphinx-inline-tabs": "^2023.4.21",
                    # Diagramming
                    "sphinxcontrib-mermaid": "^1.0.0",
                    "sphinxcontrib-plantuml": "^0.30",
                    "sphinxcontrib-blockdiag": "^3.0.0",
                    "sphinxcontrib-seqdiag": "^3.0.0",
                    # Code features
                    "sphinx-codeautolink": "^0.17.0",
                    "sphinx-exec-code": "^0.16",
                    "sphinx-runpython": "^0.4.0",
                    # Utilities
                    "sphinx-sitemap": "^2.6.0",
                    "sphinx-last-updated-by-git": "^0.3.8",
                    "sphinxext-opengraph": "^0.10.0",
                    "sphinx-reredirects": "^1.0.0",
                    "sphinx-favicon": "^1.0.1",
                    "sphinxemoji": "^0.3.1",
                    "sphinx-tippy": "^0.4.3",
                    # Special support
                    "enum-tools": "^0.13.0",
                    "sphinx-toolbox": "^3.8.1",
                    "seed-intersphinx-mapping": "^1.2.2",
                    # Development
                    "sphinx-autobuild": "^2024.10.3",
                }
            )

            # Write back
            with open(pyproject_path, "w") as f:
                tomlkit.dump(doc, f)

            click.echo("✅ Added documentation dependencies to pyproject.toml")

        except Exception as e:
            click.echo(f"⚠️  Could not add dependencies automatically: {e}")
            click.echo("   Please add the docs group manually to pyproject.toml")


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """PyDevelop documentation tools.

    Run without arguments for interactive mode.
    """
    if ctx.invoked_subcommand is None:
        # No subcommand, run interactive mode
        run_interactive()
    pass


@cli.command()
@click.option("--packages-dir", "-d", multiple=True, help="Package directories to scan")
@click.option(
    "--include-root", "-r", is_flag=True, help="Include root-level documentation"
)
@click.option("--packages", "-p", multiple=True, help="Specific packages to initialize")
@click.option(
    "--dry-run", "-n", is_flag=True, help="Show what would be done without doing it"
)
@click.option("--force", "-f", is_flag=True, help="Overwrite existing documentation")
@click.option("--quiet", "-q", is_flag=True, help="Minimal output")
@click.option("--debug", is_flag=True, help="Show debug information")
@click.option("--fix-dependencies", is_flag=True, help="Auto-fix dependency conflicts")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompts")
@click.option(
    "--with-guides", is_flag=True, help="Include guides section in TOC (default: false)"
)
@click.option(
    "--with-examples",
    is_flag=True,
    help="Include examples section in TOC (default: false)",
)
@click.option(
    "--with-cli",
    is_flag=True,
    help="Include CLI documentation section in TOC (default: false)",
)
@click.option(
    "--with-tutorials",
    is_flag=True,
    help="Include tutorials section in TOC (default: false)",
)
@click.option(
    "--use-shared-config/--use-inline-config",
    default=True,
    help="Use shared config module vs inline config (default: shared)",
)
def init(
    packages_dir,
    include_root,
    packages,
    dry_run,
    force,
    quiet,
    debug,
    fix_dependencies,
    yes,
    with_guides,
    with_examples,
    with_cli,
    with_tutorials,
    use_shared_config,
):
    """Initialize documentation for any Python project.

    This command creates a complete Sphinx documentation setup with all
    PyAutoDoc extensions (43+ extensions) configured and ready to use.
    """
    project_path = Path.cwd()

    # Initialize enhanced display with dry-run awareness
    display = EnhancedDisplay(quiet=quiet, debug=debug, dry_run=dry_run)

    # Log operation start
    display.log_operation(
        "init_start", f"Initializing documentation for {project_path}"
    )

    # Analyze project with enhanced detection
    analyzer = ProjectAnalyzer(project_path)
    start_time = datetime.now()
    analysis = analyzer.analyze()
    analysis_duration = (datetime.now() - start_time).total_seconds() * 1000
    display.log_timing("project_analysis", analysis_duration)

    analysis["path"] = str(project_path)

    # Show detailed analysis
    if debug:
        display.show_detailed_analysis(analysis)
    else:
        display.show_analysis(analysis)

    # Create operation plan
    operation_plan = create_documentation_plan(project_path, analysis, force)

    if dry_run:
        # Show what would be done
        display.show_mock_operations([op.to_dict() for op in operation_plan.operations])
        simulation_results = operation_plan.simulate_execution()

        if debug:
            click.echo("\n📊 Execution Simulation Results:")
            for key, value in simulation_results.items():
                click.echo(f"  {key}: {value}")

        display.log_operation(
            "dry_run_complete", f"Simulated {len(operation_plan.operations)} operations"
        )
        display.show_operations_summary()
        return

    # Check for dependency issues and auto-fix if requested
    autofix = AutoFixer(project_path, display)

    if not analysis["dependencies"]["valid"]:
        if dry_run:
            # In dry-run mode, only show what fixes would be applied
            available_fixes = autofix.analyze_and_fix(analysis, apply_fixes=False)
            if available_fixes and not quiet:
                click.echo(
                    f"ℹ️  Would apply {len(available_fixes)} fixes (dry-run mode)"
                )
        elif fix_dependencies or yes:
            display.debug("Auto-fixing dependency issues...")
            autofix.analyze_and_fix(analysis, apply_fixes=True)
        else:
            available_fixes = autofix.analyze_and_fix(analysis, apply_fixes=False)
            if available_fixes and not quiet:
                if display.show_fixes_prompt(
                    [f["description"] for f in available_fixes]
                ):
                    autofix.analyze_and_fix(analysis, apply_fixes=True)
                else:
                    display.warning("Dependency issues not fixed. Build may fail.")

    # Check if documentation exists
    has_existing_docs = (
        any(
            details.get("docs_exists", False)
            for details in analysis["package_details"].values()
        )
        or analysis["central_hub"]["exists"]
    )

    if has_existing_docs and not force:
        display.error("Documentation already exists! Use --force to overwrite.")
        return

    if dry_run:
        display.show_processing(analysis["packages"])
        click.echo("\n🔍 DRY RUN - No changes would be made")
        return

    # Process packages
    summary = {
        "packages_configured": 0,
        "packages_created": 0,
        "packages_updated": 0,
        "central_hub_status": "configured",
        "conflicts_resolved": len(autofix.get_applied_fixes()),
    }

    # Initialize each package
    for pkg_name in analysis["packages"]:
        pkg_path = project_path / "packages" / pkg_name
        pkg_details = analysis["package_details"][pkg_name]

        display.debug(f"Processing package: {pkg_name}")

        # Ensure docs structure exists
        if not pkg_details["docs_exists"]:
            display.debug(f"Creating docs structure for {pkg_name}")
            (pkg_path / "docs" / "source").mkdir(parents=True, exist_ok=True)
            summary["packages_created"] += 1
        else:
            summary["packages_updated"] += 1

        # Update to use shared config
        if autofix.ensure_shared_config(pkg_path, pkg_name):
            display.debug(f"Updated {pkg_name} to use shared config")

        # Create changelog
        if autofix.create_changelog(pkg_path, pkg_name):
            display.debug(f"Created changelog for {pkg_name}")

        # Update index.rst
        if autofix.update_index_rst(pkg_path, pkg_name):
            display.debug(f"Updated index.rst for {pkg_name}")

        summary["packages_configured"] += 1

    # Initialize documentation with configuration options
    doc_config = {
        "with_guides": with_guides,
        "with_examples": with_examples,
        "with_cli": with_cli,
        "with_tutorials": with_tutorials,
        "use_shared_config": use_shared_config,
    }
    initializer = DocsInitializer(project_path, analysis, doc_config)

    try:
        init_start = datetime.now()
        initializer.initialize(force=force)
        init_duration = (datetime.now() - init_start).total_seconds() * 1000
        display.log_timing("documentation_initialization", init_duration)

        display.log_operation(
            "init_success",
            "Documentation system initialized successfully",
            success=True,
        )
        display.success("All packages configured with enhanced documentation system!")

        # Show summary
        display.show_summary(summary)

        # Show comprehensive operations summary
        display.show_operations_summary()

    except Exception as e:
        display.log_operation(
            "init_failed", f"Initialization failed: {e}", success=False
        )
        display.error(f"Initialization failed: {e}")
        if debug:
            import traceback

            click.echo(traceback.format_exc(), err=True)

        # Still show operations summary for debugging
        if debug:
            display.show_operations_summary()
        raise click.Abort()


@cli.command()
@click.option("--fix", is_flag=True, help="Automatically fix detected issues")
@click.option("--quiet", "-q", is_flag=True, help="Minimal output")
def doctor(fix, quiet):
    """Check for common issues and suggest fixes."""
    project_path = Path.cwd()
    display = EnhancedDisplay(quiet=quiet)

    # Analyze project
    analyzer = ProjectAnalyzer(project_path)
    analysis = analyzer.analyze()
    analysis["path"] = str(project_path)

    # Show analysis
    display.show_analysis(analysis)

    # Check for issues and apply fixes if requested
    autofix = AutoFixer(project_path, display)

    issues_found = False

    if not analysis["dependencies"]["valid"]:
        issues_found = True
        if fix:
            autofix.analyze_and_fix(analysis, apply_fixes=True)
        else:
            available_fixes = autofix.analyze_and_fix(analysis, apply_fixes=False)
            if available_fixes:
                click.echo("\n🔧 Available fixes:")
                for fix_desc in [f["description"] for f in available_fixes]:
                    click.echo(f"   - {fix_desc}")
                click.echo("\nRun with --fix to apply these fixes automatically.")

    # Check package configurations
    for pkg_name, details in analysis["package_details"].items():
        if not details.get("uses_shared_config", False) and details.get(
            "conf_py_exists", False
        ):
            issues_found = True
            display.warning(
                f"{pkg_name} is using embedded config instead of shared config"
            )
            if fix:
                autofix.ensure_shared_config(
                    project_path / "packages" / pkg_name, pkg_name
                )

    if not issues_found:
        display.success("No issues detected! Project is healthy.")
    elif fix:
        applied_fixes = autofix.get_applied_fixes()
        if applied_fixes:
            display.success(f"Applied {len(applied_fixes)} fixes:")
            for fix in applied_fixes:
                click.echo(f"   ✅ {fix}")
        else:
            display.warning("No fixes could be applied automatically.")


@cli.command()
@click.option("--clean", "-c", is_flag=True, help="Clean build artifacts first")
@click.option("--builder", "-b", default="html", help="Sphinx builder to use")
@click.option("--no-parallel", is_flag=True, help="Disable parallel building")
@click.option("--package", "-p", help="Specific package to build (monorepo only)")
@click.option("--config", "-f", type=click.Path(exists=True), help="Custom config file")
def build(clean, builder, no_parallel, package, config):
    """Build documentation for current project.

    Supports single packages and monorepos. Auto-detects project type.
    """
    project_path = Path.cwd()

    # Get appropriate builder
    if config:
        doc_builder = get_builder(project_path, config_file=Path(config))
    else:
        doc_builder = get_builder(project_path)

    # Handle monorepo case
    if isinstance(doc_builder, MonorepoBuilder):
        if package:
            # Build specific package
            pkg_path = project_path / "packages" / package
            if not pkg_path.exists():
                click.echo(f"❌ Package '{package}' not found!")
                raise click.Abort()

            pkg_builder = get_builder(pkg_path, project_type="single")
            pkg_builder.prepare()
            success = pkg_builder.build(
                builder=builder, clean=clean, parallel=not no_parallel
            )
        else:
            # Build all packages
            success = doc_builder.build_all(clean=clean, parallel=not no_parallel)
    else:
        # Single package
        doc_builder.prepare()
        success = doc_builder.build(
            builder=builder, clean=clean, parallel=not no_parallel
        )

    if not success:
        raise click.Abort()


@cli.command()
@click.option("--clean", "-c", is_flag=True, help="Clean all build artifacts")
def build_all(clean):
    """Build documentation for all packages in monorepo."""
    project_path = Path.cwd()

    # Check if monorepo
    if not (project_path / "packages").exists():
        click.echo("❌ This command only works in monorepo projects!")
        click.echo("   Use 'pydevelop-docs build' for single packages.")
        raise click.Abort()

    builder = MonorepoBuilder(project_path, {"name": project_path.name})
    builder.prepare()

    # Build all packages
    success = builder.build_all(clean=clean)

    # Build aggregate docs
    if success:
        click.echo("\n📚 Building aggregate documentation...")
        builder.build_aggregate()
    else:
        click.echo("\n❌ Some packages failed to build!")
        raise click.Abort()


@cli.command()
def clean():
    """Clean all documentation build artifacts."""
    project_path = Path.cwd()

    # Clean patterns
    patterns = [
        "docs/build",
        "docs/source/autoapi",
        "packages/*/docs/build",
        "packages/*/docs/source/autoapi",
    ]

    cleaned = 0
    for pattern in patterns:
        for path in project_path.glob(pattern):
            if path.exists():
                shutil.rmtree(path)
                click.echo(f"✅ Cleaned {path}")
                cleaned += 1

    if cleaned == 0:
        click.echo("✅ No build artifacts found to clean")
    else:
        click.echo(f"\n✅ Cleaned {cleaned} directories")


@cli.command()
@click.argument("source", type=click.Path(exists=True))
@click.argument("target", type=click.Path())
def sync(source, target):
    """Sync documentation configuration from source to target.

    Useful for copying configuration between packages.
    """
    source_path = Path(source)
    target_path = Path(target)

    # Files to sync
    sync_files = [
        "docs/source/conf.py",
        "docs/source/_static/css/custom.css",
        "docs/source/_static/js/api-enhancements.js",
        "docs/Makefile",
        "scripts/build-docs.sh",
    ]

    synced = 0
    for file_path in sync_files:
        src_file = source_path / file_path
        if src_file.exists():
            tgt_file = target_path / file_path
            tgt_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, tgt_file)
            click.echo(f"✅ Synced {file_path}")
            synced += 1

    click.echo(f"\n✅ Synced {synced} files from {source} to {target}")


@cli.command()
@click.option("--clean", "-c", is_flag=True, help="Clean build directory first")
@click.option(
    "--open", "-o", is_flag=True, help="Open documentation in browser after building"
)
@click.option(
    "--update-only", "-u", is_flag=True, help="Update hub index only (faster)"
)
def link_docs(clean, open, update_only):
    """Link existing built documentation into a central hub.

    This command creates a documentation hub that links to all existing
    built documentation in the packages/ directory with intersphinx mappings
    for cross-referencing. Uses the complete pydevelop-docs configuration
    with 40+ extensions to match individual package styling.
    """
    from .link_builder import DocumentationLinker

    project_path = Path.cwd()
    linker = DocumentationLinker(project_path)

    if clean and (project_path / "docs" / "build").exists():
        shutil.rmtree(project_path / "docs" / "build")
        click.echo("✅ Cleaned docs/build directory")

    if update_only:
        success = linker.update_hub()
    else:
        success = linker.build_hub(open_browser=open)

    if not success:
        raise click.Abort()


@cli.command()
@click.option(
    "--open", "-o", is_flag=True, help="Open documentation in browser after updating"
)
def update_hub(open):
    """Update the documentation hub index (faster than full rebuild).

    This command updates the hub index with any new packages that have
    built documentation without doing a full rebuild.
    """
    from .link_builder import DocumentationLinker

    project_path = Path.cwd()
    linker = DocumentationLinker(project_path)

    success = linker.update_hub()

    if success and open:
        import webbrowser

        html_path = project_path / "docs" / "build" / "html" / "index.html"
        if html_path.exists():
            webbrowser.open(f"file://{html_path}")
            click.echo("🌐 Opened documentation in browser")

    if not success:
        raise click.Abort()


@cli.command()
def list_extensions():
    """List all available Sphinx extensions."""
    extensions = [
        "sphinx.ext.autodoc",
        "sphinx.ext.autosummary",
        "sphinx.ext.napoleon",
        "sphinx.ext.viewcode",
        "sphinx.ext.intersphinx",
        "sphinx.ext.todo",
        "sphinx.ext.coverage",
        "sphinx.ext.mathjax",
        "sphinx.ext.ifconfig",
        "sphinx.ext.githubpages",
        "sphinx.ext.inheritance_diagram",
        "sphinx.ext.graphviz",
        "autoapi.extension",
        "sphinx_autodoc_typehints",
        "sphinx.ext.autosectionlabel",
        "myst_parser",
        "sphinx_copybutton",
        "sphinx_togglebutton",
        "sphinx_design",
        "sphinx_tabs.tabs",
        "sphinx_inline_tabs",
        "sphinxcontrib.mermaid",
        "sphinxcontrib.plantuml",
        "sphinxcontrib.blockdiag",
        "sphinxcontrib.seqdiag",
        "sphinx_codeautolink",
        "sphinx_exec_code",
        "sphinx_runpython",
        "sphinx_tippy",
        "sphinx_favicon",
        "sphinxemoji.sphinxemoji",
        "sphinx_sitemap",
        "sphinx_last_updated_by_git",
        "sphinxext.opengraph",
        "sphinx_reredirects",
        "sphinx_treeview",
        "enum_tools.autoenum",
        "sphinx_toolbox",
        "sphinx_toolbox.more_autodoc.overloads",
        "sphinx_toolbox.more_autodoc.typehints",
        "sphinx_toolbox.more_autodoc.sourcelink",
        "sphinxcontrib.autodoc_pydantic",
    ]

    click.echo("📚 Available Sphinx Extensions (43 total):\n")
    for ext in extensions:
        click.echo(f"   • {ext}")


if __name__ == "__main__":
    cli()
