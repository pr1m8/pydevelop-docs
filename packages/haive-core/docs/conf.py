"""Sphinx configuration for Haive Core documentation."""

import sys
import os
from pathlib import Path

# Add the shared docs config to Python path
shared_config_path = Path(__file__).parent.parent.parent.parent / "shared-docs-config"
sys.path.insert(0, str(shared_config_path))

from shared_config_simple import get_base_config

# Package-specific information
PACKAGE_NAME = "haive-core"
PACKAGE_PATH = Path(__file__).parent.parent
PROJECT_ROOT = PACKAGE_PATH.parent.parent

# Get base configuration
config = get_base_config(
    package_name=PACKAGE_NAME,
    package_path=str(PACKAGE_PATH),
    is_root=False
)

# Apply all configuration settings
globals().update(config)

# Add autoapi extension for this package
extensions.append('autoapi.extension')

# Package-specific customizations
project = "Haive Core"
html_title = "Haive Core Documentation"
html_short_title = "Core"

# Package-specific theme options
html_theme_options.update({
    'navigation_depth': 3,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
})

# Core-specific intersphinx mappings
intersphinx_mapping.update({
    'pydantic': ('https://docs.pydantic.dev/latest/', None),
    'typing_extensions': ('https://typing-extensions.readthedocs.io/en/stable/', None),
})

# AutoAPI configuration for core package
autoapi_dirs = ['../src']

# Core package examples and tutorials
examples_dirs = ['../examples']
gallery_dirs = 'examples'

# Ensure source directory exists
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser.sphinx_',
}

# Core-specific content
html_context = {
    'display_github': True,
    'github_user': 'haive',
    'github_repo': 'haive-core',
    'github_version': 'main',
    'conf_py_path': '/docs/',
    'source_suffix': '.rst',
}

# Package-specific sidebar
html_sidebars = {
    '**': [
        'searchbox.html',
        'globaltoc.html',
        'relations.html',
        'sourcelink.html',
    ]
}