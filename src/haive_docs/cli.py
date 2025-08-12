"""Universal documentation initialization tool for Python projects.

This tool can initialize Sphinx documentation with the full PyAutoDoc configuration
for any Python project, whether it's a single package or monorepo.
"""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
import tomlkit
import yaml

from .config import get_haive_config


class ProjectAnalyzer:
    """Analyze Python project structure and configuration."""

    def __init__(self, path: Path):
        self.path = path

    def analyze(self) -> Dict[str, Any]:
        """Analyze project and return configuration details."""
        info = {
            "type": "unknown",
            "name": self.path.name,
            "package_manager": None,
            "packages": [],
            "has_docs": (self.path / "docs").exists(),
            "structure": None,
            "python_files": [],
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
            info["packages"] = [
                p.name
                for p in (self.path / "packages").iterdir()
                if p.is_dir() and not p.name.startswith(".")
            ]
        else:
            info["type"] = "single"

        # Detect source structure
        if (self.path / "src").exists():
            info["structure"] = "src"
            info["python_files"] = list((self.path / "src").rglob("*.py"))
        elif list(self.path.glob("*.py")):
            info["structure"] = "flat"
            info["python_files"] = list(self.path.glob("**/*.py"))

        return info

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

    def __init__(self, project_path: Path, project_info: Dict[str, Any]):
        self.project_path = project_path
        self.project_info = project_info
        self.template_path = Path(__file__).parent.parent.parent / "docs" / "source"

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
        self._generate_conf_py()
        self._generate_index_rst()
        self._generate_makefile()
        self._generate_build_scripts()

        # Add dependencies if using Poetry
        if self.project_info["package_manager"] == "poetry":
            self._add_poetry_dependencies()

    def _create_directories(self):
        """Create standard documentation directory structure."""
        dirs = [
            "docs",
            "docs/source",
            "docs/source/_static",
            "docs/source/_static/css",
            "docs/source/_static/js",
            "docs/source/_templates",
            "docs/source/_templates/includes",
            "docs/source/api",
            "docs/source/guides",
            "docs/source/examples",
            "docs/build",
            "scripts",
        ]

        for dir_path in dirs:
            (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)

    def _copy_static_files(self):
        """Copy static assets from templates."""
        static_files = [
            ("_static/css/custom.css", "docs/source/_static/css/custom.css"),
            (
                "_static/js/api-enhancements.js",
                "docs/source/_static/js/api-enhancements.js",
            ),
            ("_static/logo-light.png", "docs/source/_static/logo-light.png"),
            ("_static/logo-dark.png", "docs/source/_static/logo-dark.png"),
        ]

        for src, dest in static_files:
            src_path = self.template_path / src
            dest_path = self.project_path / dest

            if src_path.exists():
                shutil.copy2(src_path, dest_path)

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
Generated by haive-docs init.
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
    
    # API Documentation
    "autoapi.extension",
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
    
    # Special Features
    "enum_tools.autoenum",
    "sphinx_toolbox",
    "sphinx_toolbox.more_autodoc.overloads",
    "sphinx_toolbox.more_autodoc.typehints",
    "sphinx_toolbox.more_autodoc.sourcelink",
    
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

        conf_path = self.project_path / "docs" / "source" / "conf.py"
        conf_path.write_text(conf_content)

    def _generate_index_rst(self):
        """Generate index.rst file."""
        index_content = f"""
Welcome to {self.project_info["name"]} Documentation
{"=" * (len(self.project_info["name"]) + 25)}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   autoapi/index
   guides/index
   examples/index
   changelog

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


@click.group()
def cli():
    """Haive documentation tools."""
    pass


@cli.command()
@click.option("--force", "-f", is_flag=True, help="Overwrite existing documentation")
def init(force):
    """Initialize documentation for any Python project.

    This command creates a complete Sphinx documentation setup with all
    PyAutoDoc extensions (43+ extensions) configured and ready to use.
    """
    project_path = Path.cwd()

    # Analyze project
    click.echo(f"🔍 Analyzing project at {project_path}...")
    analyzer = ProjectAnalyzer(project_path)
    project_info = analyzer.analyze()

    click.echo(f"📦 Project: {project_info['name']}")
    click.echo(f"📁 Type: {project_info['type']}")
    click.echo(f"🔧 Package Manager: {project_info['package_manager']}")

    if project_info["has_docs"] and not force:
        click.echo("⚠️  Documentation already exists! Use --force to overwrite.")
        return

    # Initialize documentation
    initializer = DocsInitializer(project_path, project_info)

    try:
        initializer.initialize(force=force)

        click.echo("\n✅ Documentation initialized successfully!")
        click.echo("\n📚 Next steps:")

        if project_info["package_manager"] == "poetry":
            click.echo("   1. Run: poetry install --with docs")
            click.echo("   2. Run: cd docs && poetry run make html")
        else:
            click.echo("   1. Install dependencies from requirements.txt")
            click.echo("   2. Run: cd docs && make html")

        click.echo("   3. Open: docs/build/html/index.html")

    except Exception as e:
        click.echo(f"\n❌ Error: {e}")
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
