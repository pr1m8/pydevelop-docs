"""Clean Sphinx configuration for Haive Central Documentation Hub."""

import os
import sys

from sphinx.application import Sphinx

# Path setup
sys.path.insert(0, os.path.abspath("../../src"))

# Import shared Haive configuration
from haive_docs import get_central_hub_config

# Get central hub configuration
config = get_central_hub_config()

# Apply configuration to globals
globals().update(config)

# Central hub specific overrides
project = "Haive AI Agent Framework Documentation"
html_title = "Haive AI Agent Framework - Complete Documentation"

# Additional extensions for the central hub (beyond base config)
extensions.extend(
    [
        # Enhanced documentation features for central hub
        "sphinx_sitemap",
        "sphinx_copybutton",
        "sphinx_togglebutton",
        "sphinx_tabs.tabs",
        "sphinxcontrib.mermaid",
        "sphinx.ext.graphviz",
        "sphinx_design",
    ]
)

# Central hub specific theme options
html_theme_options.update(
    {
        "sidebar_hide_name": False,
        "navigation_with_keys": True,
        "announcement": "🎯 Central documentation hub for the Haive AI Agent Framework",
    }
)

# Additional static paths for central hub
html_static_path = ["_static"]
templates_path = ["_templates", "_autoapi_templates"]

# Sitemap configuration
html_baseurl = "https://docs.haive.ai/"
sitemap_url_scheme = "{link}"


def setup(app: Sphinx):
    """Sphinx setup function for central hub."""
    # Add custom CSS for central hub
    app.add_css_file("toc-enhancements.css")
    app.add_js_file("api-enhancements.js")
