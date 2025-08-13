"""Test Sphinx configuration for PyDevelop-Docs CSS testing."""

import os
import sys

# Path setup
sys.path.insert(0, os.path.abspath("../../src"))

# Basic project information
project = "PyDevelop-Docs CSS Test"
copyright = "2025, Haive Team"
author = "Haive Team"
version = "0.1.0"
release = "0.1.0"

# Basic Sphinx configuration with hierarchical AutoAPI fix
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_autoapi.extension",
    "myst_parser",
]

# AutoAPI configuration with hierarchical fix
autoapi_type = "python"
autoapi_dirs = ["../../src"]
autoapi_root = "autoapi"
autoapi_add_toctree_entry = False
autoapi_member_order = "groupwise"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]
# ✅ HIERARCHICAL ORGANIZATION FIX - The key setting!
autoapi_own_page_level = "module"  # Keep classes with their modules

# Theme configuration
html_theme = "furo"
html_title = "PyDevelop-Docs CSS Test"
html_static_path = ["_static"]

# Custom CSS files to test white-on-white issues
html_css_files = [
    "css/custom.css",
    "furo-intense.css",
]

# Basic HTML options
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

# Source file patterns
source_suffix = {
    ".rst": None,
    ".md": "myst_parser",
}

# Master document
master_doc = "index"
