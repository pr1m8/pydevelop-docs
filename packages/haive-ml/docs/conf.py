"""Sphinx configuration for Haive ML documentation."""

import sys
import os
from pathlib import Path

# Add the shared docs config to Python path
shared_config_path = Path(__file__).parent.parent.parent.parent / "shared-docs-config"
sys.path.insert(0, str(shared_config_path))

from shared_config_simple import get_base_config

# Package-specific information
PACKAGE_NAME = "haive-ml"
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
project = "Haive ML"
html_title = "Haive ML Documentation"
html_short_title = "ML"

# ML-specific theme options
html_theme_options.update({
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
})

# ML-specific intersphinx mappings
intersphinx_mapping.update({
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scikit-learn': ('https://scikit-learn.org/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'joblib': ('https://joblib.readthedocs.io/en/stable/', None),
    'haive-core': ('https://docs.haive.ai/core/', None),
})

# AutoAPI configuration for ML package
autoapi_dirs = ['../src']

# ML package examples and tutorials
examples_dirs = ['../examples']
gallery_dirs = 'examples'

# Additional ML-specific extensions
extensions.extend([
    'sphinx.ext.mathjax',  # For mathematical expressions
    'matplotlib.sphinxext.plot_directive',  # For plotting examples
])

# Math configuration
mathjax3_config = {
    'tex': {
        'inlineMath': [['$', '$'], ['\\(', '\\)']],
        'displayMath': [['$$', '$$'], ['\\[', '\\]']],
    }
}

# Plot directive configuration
plot_include_source = True
plot_html_show_source_link = False
plot_formats = ['png', 'pdf']

# Ensure source directory exists
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser.sphinx_',
}

# ML-specific content
html_context = {
    'display_github': True,
    'github_user': 'haive',
    'github_repo': 'haive-ml',
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