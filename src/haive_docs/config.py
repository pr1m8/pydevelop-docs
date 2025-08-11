"""Shared Sphinx configuration for Haive packages."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional


def get_haive_config(
    package_name: str,
    package_path: str,
    is_central_hub: bool = False,
    extra_extensions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Get base Haive Sphinx configuration for a package.

    Args:
        package_name: Name of the package (e.g., "haive-core")
        package_path: Path to the package source code
        is_central_hub: Whether this is the central documentation hub
        extra_extensions: Additional extensions to include

    Returns:
        Dictionary of Sphinx configuration settings
    """
    config = {
        # Project information
        "project": f"Haive {package_name.replace('haive-', '').replace('-', ' ').title()}",
        "author": "Haive Team",
        "copyright": "2025, Haive Team",
        "release": "0.1.0",
        # Extensions - Core Haive documentation stack
        "extensions": _get_base_extensions(is_central_hub, extra_extensions),
        # Theme configuration
        "html_theme": "furo",
        "html_theme_options": _get_theme_options(package_name),
        # Path configuration
        "templates_path": ["_templates"],
        "html_static_path": ["_static"],
        # AutoAPI configuration (if not central hub)
        **(_get_autoapi_config(package_path) if not is_central_hub else {}),
        # Intersphinx mapping
        "intersphinx_mapping": _get_intersphinx_mapping(),
        # MyST configuration
        "myst_enable_extensions": [
            "colon_fence",
            "deflist",
            "html_image",
            "linkify",
            "replacements",
            "smartquotes",
            "tasklist",
        ],
    }

    return config


def get_central_hub_config() -> Dict[str, Any]:
    """Get configuration specific to the central documentation hub.

    Returns:
        Dictionary with sphinx-collections configuration
    """
    base_config = get_haive_config(
        package_name="haive-docs", package_path="", is_central_hub=True
    )

    # Add collections configuration
    base_config.update(
        {
            "collections": {
                "haive_packages": {
                    "driver": "copy_folder",
                    "source_folder": "../../../packages/*/docs/build/html/",
                    "target_folder": "_collections/",
                    "active": True,
                }
            }
        }
    )

    return base_config


def _get_base_extensions(
    is_central_hub: bool, extra_extensions: Optional[List[str]] = None
) -> List[str]:
    """Get base extensions for Haive documentation."""
    extensions = [
        # Core Sphinx
        "sphinx.ext.autodoc",
        "sphinx.ext.napoleon",
        "sphinx.ext.viewcode",
        "sphinx.ext.intersphinx",
        # Haive essentials
        # "seed_intersphinx_mapping",  # Disabled for now - requires requirements.txt
        "myst_parser",
        "sphinx_copybutton",
        "sphinx_design",
        # Theme and styling
        "sphinx_togglebutton",
        "sphinx_tabs.tabs",
    ]

    # Add AutoAPI for individual packages
    if not is_central_hub:
        extensions.insert(1, "autoapi.extension")

    # Add collections for central hub
    if is_central_hub:
        extensions.append("sphinxcontrib.collections")

    # Add extra extensions
    if extra_extensions:
        extensions.extend(extra_extensions)

    return extensions


def _get_autoapi_config(package_path: str) -> Dict[str, Any]:
    """Get AutoAPI configuration for individual packages."""
    return {
        "autoapi_type": "python",
        "autoapi_dirs": [package_path],
        "autoapi_template_dir": "_autoapi_templates",
        "autoapi_add_toctree_entry": True,
        "autoapi_generate_api_docs": True,
        "autoapi_keep_files": True,
        "autoapi_options": [
            "members",
            "undoc-members",
            "show-inheritance",
            "show-module-summary",
            "imported-members",
        ],
    }


def _get_theme_options(package_name: str) -> Dict[str, Any]:
    """Get Furo theme options with Haive branding."""
    return {
        "sidebar_hide_name": False,
        "navigation_with_keys": True,
        "top_of_page_buttons": ["view", "edit"],
        "source_repository": "https://github.com/haive-ai/haive",
        "source_branch": "main",
        "source_directory": f"packages/{package_name}/",
        "light_css_variables": {
            "color-brand-primary": "#2563eb",  # Haive blue
            "color-brand-content": "#2563eb",
        },
        "dark_css_variables": {
            "color-brand-primary": "#3b82f6",  # Lighter blue for dark mode
            "color-brand-content": "#3b82f6",
        },
    }


def _get_intersphinx_mapping() -> Dict[str, tuple]:
    """Get intersphinx mapping for cross-references."""
    return {
        "python": ("https://docs.python.org/3", None),
        "sphinx": ("https://www.sphinx-doc.org/en/master", None),
        "pydantic": ("https://docs.pydantic.dev/latest", None),
        # Add other Haive packages as they become available
        # "haive-core": ("https://docs.haive.ai/core/", None),
        # "haive-agents": ("https://docs.haive.ai/agents/", None),
    }
