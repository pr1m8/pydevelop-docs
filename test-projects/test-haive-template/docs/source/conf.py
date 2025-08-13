"""
Simplified Sphinx configuration for test-haive-template.
Focus on AutoAPI hierarchical testing.
"""

import os
import sys
from datetime import date

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
project = "test-haive-template"
copyright = f"{date.today().year}, test-haive-template Team"
author = "test-haive-template Team"
release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    # Core Sphinx Extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    # API Documentation
    "autoapi.extension",
    # Theme
    "myst_parser",
]

# -- AutoAPI Configuration ---------------------------------------------------

# AutoAPI configuration
autoapi_dirs = ["../.."]
autoapi_type = "python"
autoapi_template_dir = "_autoapi_templates"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",  # Critical for hierarchical organization
]
autoapi_python_class_content = "both"
autoapi_member_order = "groupwise"
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_keep_files = True

# ✅ HIERARCHICAL ORGANIZATION FIX - The key setting!
autoapi_own_page_level = "module"  # Keep classes with their modules

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]

html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "navigation_depth": 4,  # Allow deep nesting
    "collapse_navigation": False,  # Keep expanded by default
}

# -- Additional Configuration ------------------------------------------------

templates_path = ["_templates"]
exclude_patterns = []
pygments_style = "sphinx"
pygments_dark_style = "monokai"


def setup(app):
    """Sphinx setup hook."""
    pass
