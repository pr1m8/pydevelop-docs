# Configuration file for the Unified Haive Documentation Hub
# This uses sphinx-collections to gather documentation from all Haive packages

import os
import sys
from pathlib import Path

# Configuration metadata
project = "Haive AI Agent Framework"
copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0.0"
release = "1.0.0"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here
extensions = [
    # Core Sphinx extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    # AutoAPI for hierarchical API documentation
    "autoapi.extension",
    # Sphinx-collections for multi-project aggregation
    "sphinxcontrib.collections",
    # Enhanced documentation
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_tabs",
    "myst_parser",
    # Utilities
    "sphinx_last_updated_by_git",
    "sphinx_sitemap",
]

# Templates path
templates_path = ["_templates"]

# List of patterns to ignore when building the documentation
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Sphinx-Collections Configuration ---------------------------------------

# This is the key configuration that will collect documentation from all Haive packages
collections = {
    # Core framework
    "haive-core": {
        "driver": "symlink",
        "source": "../../../../../../packages/haive-core/docs/source",
        "target": "packages/core",
        "tags": ["core", "api"],
        "active": True,
    },
    # Agent implementations
    "haive-agents": {
        "driver": "symlink",
        "source": "../../../../../../packages/haive-agents/docs/source",
        "target": "packages/agents",
        "tags": ["agents", "api"],
        "active": True,
    },
    # Tool integrations
    "haive-tools": {
        "driver": "symlink",
        "source": "../../../../../../packages/haive-tools/docs/source",
        "target": "packages/tools",
        "tags": ["tools", "api"],
        "active": True,
    },
    # Game environments
    "haive-games": {
        "driver": "symlink",
        "source": "../../../../../../packages/haive-games/docs/source",
        "target": "packages/games",
        "tags": ["games", "api"],
        "active": True,
    },
    # Model Context Protocol integration
    "haive-mcp": {
        "driver": "symlink",
        "source": "../../../../../../packages/haive-mcp/docs/source",
        "target": "packages/mcp",
        "tags": ["mcp", "api"],
        "active": True,
    },
    # Data processing
    "haive-dataflow": {
        "driver": "symlink",
        "source": "../../../../../../packages/haive-dataflow/docs/source",
        "target": "packages/dataflow",
        "tags": ["dataflow", "api"],
        "active": True,
    },
    # Pre-built configurations
    "haive-prebuilt": {
        "driver": "symlink",
        "source": "../../../../../../packages/haive-prebuilt/docs/source",
        "target": "packages/prebuilt",
        "tags": ["prebuilt", "api"],
        "active": True,
    },
}

# -- AutoAPI Configuration ---------------------------------------------------

# Configure AutoAPI for the unified documentation
autoapi_type = "python"
autoapi_dirs = [
    "_collections/haive-core",
    "_collections/haive-agents",
    "_collections/haive-tools",
    "_collections/haive-games",
    "_collections/haive-mcp",
    "_collections/haive-dataflow",
    "_collections/haive-prebuilt",
]

# Use hierarchical organization (this was our major fix!)
autoapi_own_page_level = "module"

# AutoAPI options for better organization
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",  # Critical for hierarchical organization
    "special-members",
]

# Generate AutoAPI documentation
autoapi_generate_api_docs = True
autoapi_add_toctree_entry = True

# -- Intersphinx Configuration ----------------------------------------------

# Cross-reference configuration for linking between packages
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "langchain": ("https://python.langchain.com/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# -- HTML output options ----------------------------------------------------

# The theme to use for HTML and HTML Help pages
html_theme = "furo"

# Theme options for Furo
html_theme_options = {
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    "source_repository": "https://github.com/haive-ai/haive",
    "source_branch": "main",
    "source_directory": "docs/",
    # Enhanced navigation for multi-package documentation
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "titles_only": False,
    # Custom styling
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#1d4ed8",
    },
    "dark_css_variables": {
        "color-brand-primary": "#60a5fa",
        "color-brand-content": "#3b82f6",
    },
}

# Add any paths that contain custom static files (such as style sheets)
html_static_path = ["_static"]

# Custom CSS files for unified styling
html_css_files = [
    "css/haive-unified.css",  # We'll create this
    "css/cross-package-navigation.css",  # We'll create this
]

# Custom JavaScript for enhanced navigation
html_js_files = [
    "js/package-switcher.js",  # We'll create this
    "js/unified-navigation.js",  # We'll create this
]

# HTML context for templates
html_context = {
    "package_navigation": {
        "hub_url": "/",
        "packages": {
            "haive-core": {
                "title": "Core Framework",
                "url": "/packages/core/",
                "description": "Foundation classes and utilities",
                "depends_on": [],
                "used_by": [
                    "haive-agents",
                    "haive-tools",
                    "haive-games",
                    "haive-mcp",
                    "haive-dataflow",
                ],
            },
            "haive-agents": {
                "title": "Agent Implementations",
                "url": "/packages/agents/",
                "description": "Pre-built AI agents and patterns",
                "depends_on": ["haive-core"],
                "used_by": ["haive-games", "haive-prebuilt"],
            },
            "haive-tools": {
                "title": "Tool Integrations",
                "url": "/packages/tools/",
                "description": "External tool and API integrations",
                "depends_on": ["haive-core"],
                "used_by": ["haive-agents", "haive-games"],
            },
            "haive-games": {
                "title": "Game Environments",
                "url": "/packages/games/",
                "description": "Gaming and simulation environments",
                "depends_on": ["haive-core", "haive-agents", "haive-tools"],
                "used_by": [],
            },
            "haive-mcp": {
                "title": "MCP Integration",
                "url": "/packages/mcp/",
                "description": "Model Context Protocol support",
                "depends_on": ["haive-core"],
                "used_by": ["haive-agents"],
            },
            "haive-dataflow": {
                "title": "Data Processing",
                "url": "/packages/dataflow/",
                "description": "Streaming and batch data processing",
                "depends_on": ["haive-core"],
                "used_by": ["haive-agents"],
            },
            "haive-prebuilt": {
                "title": "Pre-built Solutions",
                "url": "/packages/prebuilt/",
                "description": "Ready-to-use agent configurations",
                "depends_on": ["haive-core", "haive-agents"],
                "used_by": [],
            },
        },
    }
}

# Sitemap configuration
sitemap_url_scheme = "{link}"

# -- MyST Configuration -----------------------------------------------------

# MyST parser configuration for Markdown support
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "colon_fence",
    "linkify",
]

# -- Custom configuration for unified docs ----------------------------------


# Add custom roles and directives for cross-package documentation
def setup(app):
    """Custom Sphinx setup for unified Haive documentation."""
    app.add_css_file("css/haive-unified.css")
    app.add_js_file("js/package-switcher.js")

    # Add custom directives for package information
    from docutils import nodes
    from docutils.parsers.rst import directives
    from sphinx.util.docutils import SphinxDirective

    class PackageInfo(SphinxDirective):
        """Directive to display package dependency information."""

        has_content = True
        required_arguments = 1
        option_spec = {
            "depends_on": directives.unchanged,
            "used_by": directives.unchanged,
        }

        def run(self):
            package_name = self.arguments[0]
            container = nodes.container(classes=["package-info"])

            # Add package info content
            title = nodes.title(text=f"{package_name} Dependencies")
            container += title

            return [container]

    app.add_directive("package-info", PackageInfo)

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
