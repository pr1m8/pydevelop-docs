"""Sphinx configuration for Haive API documentation."""

import sys
import os
from pathlib import Path

# Add the shared docs config to Python path
shared_config_path = Path(__file__).parent.parent.parent.parent / "shared-docs-config"
sys.path.insert(0, str(shared_config_path))

from shared_config_simple import get_base_config

# Package-specific information
PACKAGE_NAME = "haive-api"
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
project = "Haive API"
html_title = "Haive API Documentation"
html_short_title = "API"

# API-specific theme options
html_theme_options.update({
    'navigation_depth': 3,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
})

# API-specific intersphinx mappings
intersphinx_mapping.update({
    'fastapi': ('https://fastapi.tiangolo.com/', None),
    'uvicorn': ('https://www.uvicorn.org/', None),
    'pydantic': ('https://docs.pydantic.dev/latest/', None),
    'httpx': ('https://www.python-httpx.org/', None),
    'haive-core': ('https://docs.haive.ai/core/', None),
    'haive-ml': ('https://docs.haive.ai/ml/', None),
})

# AutoAPI configuration for API package
autoapi_dirs = ['../src']

# API package examples and tutorials
examples_dirs = ['../examples']
gallery_dirs = 'examples'

# Additional API-specific extensions
extensions.extend([
    'sphinxcontrib.openapi',  # For OpenAPI/Swagger documentation
    'sphinxcontrib.httpdomain',  # For HTTP API documentation
])

# OpenAPI configuration (if using)
openapi_spec_url = 'https://api.haive.ai/openapi.json'

# HTTP domain configuration
http_index_shortname = 'api'
http_index_localname = 'Haive API'

# Ensure source directory exists
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser.sphinx_',
}

# API-specific content
html_context = {
    'display_github': True,
    'github_user': 'haive',
    'github_repo': 'haive-api',
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