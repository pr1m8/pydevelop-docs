"""Shared Sphinx configuration for Haive packages.

This module provides the complete 43+ extension configuration system
migrated from PyAutoDoc's proven 635-line configuration.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional


def get_haive_config(
    package_name: str,
    package_path: str,
    is_central_hub: bool = False,
    extra_extensions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Get complete Haive Sphinx configuration for a package.

    Provides the full 43+ extension configuration system with all
    advanced theming, validation, and documentation features.

    Args:
        package_name: Name of the package (e.g., "haive-core")
        package_path: Path to the package source code
        is_central_hub: Whether this is the central documentation hub
        extra_extensions: Additional extensions to include

    Returns:
        Dictionary of complete Sphinx configuration settings
    """

    # Base project info
    display_name = package_name.replace("haive-", "").replace("-", " ").title()
    if package_name == "haive-docs":
        display_name = "Haive AI Agent Framework"

    config = {
        # Project information
        "project": (
            f"Haive {display_name}" if package_name != "haive-docs" else display_name
        ),
        "author": "Haive Team",
        "copyright": "2025, Haive Team",
        "release": "0.1.0",
        # Extensions - COMPLETE 43+ extension system from PyAutoDoc
        "extensions": _get_complete_extensions(is_central_hub, extra_extensions),
        # General configuration
        "templates_path": ["_templates", "_autoapi_templates"],
        "html_static_path": ["_static"],
        "exclude_patterns": [
            "_build",
            "Thumbs.db",
            ".DS_Store",
            "**/CVS",
            "**/.git",
            "_collections/*/_collections",  # Prevent nested collection directories
            "**/symlink_loops",  # Prevent symlink loop directories
        ],
        "add_module_names": False,
        "toc_object_entries_show_parents": "hide",
        # TOC Configuration - Enhanced nesting and presentation
        "html_sidebars": {
            "**": [
                "sidebar/brand.html",
                "sidebar/search.html",
                "sidebar/scroll-start.html",
                "sidebar/navigation.html",
                "sidebar/ethical-ads.html",
                "sidebar/scroll-end.html",
            ]
        },
        # Furo-specific TOC options
        "navigation_with_keys": True,
        "top_of_page_button": "edit",
        # Sphinx TOC settings
        "toctree_maxdepth": 4,  # Maximum depth for nested TOC
        "toctree_collapse": False,  # Don't collapse by default
        "toctree_titles_only": False,  # Show full titles
        "toctree_includehidden": True,  # Include hidden TOC entries
        # Jinja2 options
        "jinja_env_options": {"extensions": ["jinja2.ext.do"]},
        # AutoAPI configuration (if not central hub)
        **(_get_complete_autoapi_config(package_path) if not is_central_hub else {}),
        # Napoleon configuration
        "napoleon_google_docstring": True,
        "napoleon_numpy_docstring": True,
        "napoleon_include_init_with_doc": False,
        "napoleon_include_private_with_doc": False,
        # Intersphinx configuration
        "pkg_requirements_source": "pyproject",  # Read dependencies from pyproject.toml
        "repository_root": "../..",  # Path to repo root from docs/source
        "intersphinx_mapping": _get_complete_intersphinx_mapping(),
        # Pydantic configuration - COMPLETE
        "autodoc_pydantic_model_show_json": True,
        "autodoc_pydantic_model_show_config_summary": True,
        "autodoc_pydantic_model_show_validator_summary": True,
        "autodoc_pydantic_model_show_field_summary": True,
        "autodoc_pydantic_model_show_validator_members": True,
        "autodoc_pydantic_field_list_validators": True,
        "autodoc_pydantic_field_show_constraints": True,
        "autodoc_pydantic_model_erdantic_figure": False,
        "autodoc_pydantic_model_erdantic_figure_collapsed": False,
        # Type hints configuration
        "typehints_fully_qualified": False,
        "typehints_use_signature": True,
        # MyST Parser configuration - COMPLETE
        "myst_enable_extensions": [
            "deflist",
            "tasklist",
            "html_image",
            "colon_fence",
            "smartquotes",
            "replacements",
            "linkify",
            "strikethrough",
            "attrs_inline",
            "attrs_block",
        ],
        "myst_heading_anchors": 3,
        "myst_fence_as_directive": ["mermaid", "note", "warning"],
        # Sphinx Design configuration - INTENSE THEMING
        "sd_fontawesome_latex": True,
        # Toggle button configuration
        "togglebutton_hint": "Click to expand",
        "togglebutton_hint_hide": "Click to collapse",
        # Copy button configuration
        "copybutton_prompt_text": r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: ",
        "copybutton_prompt_is_regexp": True,
        "copybutton_remove_prompts": True,
        # Tabs configuration
        "sphinx_tabs_disable_tab_closing": True,
        # Execution extensions configuration
        "programoutput_use_ansi": True,
        # Mermaid configuration - CUSTOM THEMING
        "mermaid_params": [
            "--theme",
            "neutral",
            "--width",
            "800",
            "--backgroundColor",
            "transparent",
        ],
        "mermaid_verbose": True,
        # PlantUML configuration
        "plantuml_output_format": "svg",
        "plantuml": "plantuml",
        # Sitemap configuration
        "html_baseurl": (
            f"https://docs.haive.ai/packages/{package_name}/"
            if not is_central_hub
            else "https://docs.haive.ai/"
        ),
        # Code autolink configuration
        "codeautolink_autodoc_inject": True,
        "codeautolink_concat_default": True,
        # Treeview configuration
        "treeview_expand_all": False,
        "treeview_collapse_inactive": True,
        "treeview_max_depth": 4,
        # Toggle prompt configuration
        "toggleprompt_offset_right": 30,
        "toggleprompt_default_hidden": "true",
        # Git last updated configuration
        "git_last_updated_show_commit_hash": True,
        "git_last_updated_format": "%Y-%m-%d %H:%M",
        # Inline code configuration
        "inlinecode_highlight_language": "python",
        # Library configuration
        "library_show_summary": True,
        "library_group_by_type": True,
        # iContract configuration
        "icontract_include_repr": True,
        "icontract_include_snapshot": False,
        # Comments configuration
        "comments_config": {
            "hypothesis": True,
            "utterances": False,
        },
        # Contributors configuration
        "contributors_show_contribution_counts": True,
        "contributors_sort_by_contribution": True,
        # Issues configuration
        "issues_github_path": "haive-ai/haive",
        "issues_uri": "https://github.com/haive-ai/haive/issues/{issue}",
        # Sphinx Tippy configuration - Rich hover tooltips
        "tippy_props": {
            "placement": "auto",
            "maxWidth": 600,
            "theme": "light-border",
            "delay": [200, 100],
            "duration": [200, 100],
            "interactive": True,
        },
        "tippy_enable_mathjax": True,
        "tippy_enable_doitips": True,
        "tippy_rtd_urls": ["https://docs.haive.ai"],
        "tippy_anchor_parent_selector": "article.bd-article",
        # Sphinx-prompt configuration
        "prompt_modifiers": "auto",
        "prompt_default_prompts": ["$", ">>>", "..."],
        # Sphinx-needs configuration - Requirements tracking
        "needs_types": [
            {
                "directive": "req",
                "title": "Requirement",
                "prefix": "R_",
                "color": "#BFD8D2",
                "style": "node",
            },
            {
                "directive": "spec",
                "title": "Specification",
                "prefix": "S_",
                "color": "#FEDCD2",
                "style": "node",
            },
            {
                "directive": "test",
                "title": "Test Case",
                "prefix": "T_",
                "color": "#DF744A",
                "style": "node",
            },
        ],
        "needs_statuses": [
            {"name": "open", "description": "New requirement"},
            {"name": "in_progress", "description": "Being implemented"},
            {"name": "implemented", "description": "Completed"},
            {"name": "closed", "description": "Done and verified"},
        ],
        "needs_tags": [
            {"name": "security", "description": "Security related"},
            {"name": "performance", "description": "Performance critical"},
            {"name": "ui", "description": "User interface"},
        ],
        # Sphinx-notfound-page configuration
        "notfound_context": {
            "title": "Page Not Found",
            "body": f"""
<h1>🚀 Oops! Page Not Found</h1>
<p>The page you're looking for seems to have wandered off into the documentation cosmos.</p>

<div class="admonition tip">
<p class="admonition-title">Try these options:</p>
<ul>
<li><strong>Search:</strong> Use the search box above to find what you need</li>
<li><strong>API Reference:</strong> Check our <a href="/autoapi/">complete API documentation</a></li> 
<li><strong>Home:</strong> Return to the <a href="/">main documentation</a></li>
</ul>
</div>

<p>Still can't find what you're looking for? <a href="https://github.com/haive-ai/haive/issues">Report an issue</a> and we'll help you out!</p>
            """,
        },
        "notfound_template": "page.html",
        "notfound_no_urls_prefix": True,
        # Sphinx-reredirects configuration
        "redirects": {},
        # Rediraffe configuration
        "rediraffe_redirects": {},
        "rediraffe_branch": "main",
        "rediraffe_auto_redirect_perc": 50,
        # Sphinx-git configuration
        "sphinx_git_changelog": True,
        "sphinx_git_changelog_title": "📝 Documentation Changes",
        "sphinx_git_show_tags": True,
        "sphinx_git_show_branch": True,
        "sphinx_git_tracked_files": ["docs/source/"],
        "sphinx_git_untracked": False,
        # Debug info configuration
        "debuginfo_enable": True,
        "debuginfo_show_performance": True,
        "debuginfo_show_warnings": True,
        "debuginfo_show_extensions": True,
        # OpenGraph configuration
        "ogp_site_url": (
            "https://docs.haive.ai/"
            if is_central_hub
            else f"https://docs.haive.ai/packages/{package_name}/"
        ),
        "ogp_site_name": display_name,
        "ogp_site_description": f"{display_name} - Part of the Haive AI Agent Framework",
        "ogp_image": "_static/social-preview.png",
        "ogp_image_alt": f"{display_name} Documentation",
        "ogp_type": "website",
        "ogp_locale": "en_US",
        "ogp_social_cards": {
            "enable": True,
            "image": "_static/social-card-template.png",
            "line_color": "#2563eb",
            "text_color": "#ffffff",
        },
        # Sphinx-tags configuration
        "tags_create_tags": True,
        "tags_create_index": True,
        "tags_create_badges": True,
        "tags_page_title": "Documentation Tags",
        "tags_intro_text": "Browse documentation content by tags",
        "tags_extension": [".rst", ".md"],
        "tags_badge_colors": {
            "security": "#dc3545",
            "performance": "#28a745",
            "ui": "#007bff",
            "api": "#6f42c1",
            "config": "#fd7e14",
            "tutorial": "#20c997",
            "reference": "#6c757d",
        },
        # Sphinx-favicon configuration
        "favicons": [
            {
                "rel": "icon",
                "sizes": "32x32",
                "href": "favicon-32x32.png",
                "type": "image/png",
            },
            {
                "rel": "icon",
                "sizes": "16x16",
                "href": "favicon-16x16.png",
                "type": "image/png",
            },
            {
                "rel": "apple-touch-icon",
                "sizes": "180x180",
                "href": "apple-touch-icon.png",
                "type": "image/png",
            },
            {
                "rel": "shortcut icon",
                "href": "favicon.ico",
                "type": "image/x-icon",
            },
        ],
        # Collections configuration (only for central hub)
        **(_get_collections_config() if is_central_hub else {}),
        # Theme configuration - INTENSE FURO THEMING
        "html_theme": "furo",
        "html_theme_options": _get_complete_theme_options(package_name, is_central_hub),
        # Custom CSS and JS files
        "html_css_files": [
            "furo-intense.css",
            "api-docs.css",
            "mermaid-custom.css",
            "toc-enhancements.css",
            "tippy-enhancements.css",
        ],
        "html_js_files": [
            "furo-enhancements.js",
            "mermaid-config.js",
            "toc-navigator.js",
            "js/api-enhancements.js",
        ],
    }

    return config


def get_central_hub_config() -> Dict[str, Any]:
    """Get configuration specific to the central documentation hub.

    This includes sphinx-collections configuration for aggregating
    all package documentation.

    Returns:
        Dictionary with complete central hub configuration
    """
    return get_haive_config(
        package_name="haive-docs", package_path="", is_central_hub=True
    )


def _get_complete_extensions(
    is_central_hub: bool, extra_extensions: Optional[List[str]] = None
) -> List[str]:
    """Get complete 43+ extension system from PyAutoDoc."""
    extensions = [
        # Core (Priority 1-10) - AutoAPI FIRST as requested
        "sphinx.ext.autodoc",
        "sphinx.ext.napoleon",
        "sphinx.ext.viewcode",
        "sphinx.ext.intersphinx",
        # "seed_intersphinx_mapping",  # Disabled - requires requirements.txt
        # Enhanced API (Priority 11-20)
        "sphinxcontrib.autodoc_pydantic",
        "sphinx_autodoc_typehints",
        # Content & Design (Priority 21-30) - INTENSE FURO FOCUS
        "myst_parser",
        "sphinx_design",  # KEY for intense theming
        "sphinx_togglebutton",
        "sphinx_copybutton",
        "sphinx_tabs.tabs",
        # Execution (Priority 31-40) - TESTING FOCUS
        "sphinxcontrib.programoutput",
        # Diagrams (Priority 41-50) - MERMAID FOCUS
        "sphinx.ext.graphviz",
        "sphinxcontrib.mermaid",
        "sphinxcontrib.plantuml",
        # Utilities (Priority 51-60)
        "sphinx_sitemap",
        "sphinx_codeautolink",
        # TOC Enhancements (Priority 61-70)
        "sphinx_treeview",
        # Enhanced Features (Priority 71-80)
        "sphinx_toggleprompt",
        "sphinx_prompt",
        "sphinx_last_updated_by_git",
        "sphinx_inlinecode",
        "sphinx_library",
        "sphinx_icontract",
        "sphinx_tippy",
        # Documentation Tools (Priority 81-90)
        "sphinx_comments",
        "sphinx_contributors",
        "sphinx_issues",
        "sphinx_needs",
        "sphinxarg.ext",
        "notfound.extension",
        "sphinx_reredirects",
        "sphinxext.rediraffe",
        "sphinx_git",
        "sphinx_debuginfo",
        "sphinxext.opengraph",
        "sphinx_tags",
        "sphinx_favicon",
        "sphinx_combine",
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


def _get_complete_autoapi_config(package_path: str) -> Dict[str, Any]:
    """Get complete AutoAPI configuration."""
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
            "private-members",
            "special-members",
            "imported-members",
        ],
        "autoapi_python_class_content": "both",
        "autoapi_add_class_diagram": True,
        "autoapi_class_diagram_depth": 2,
        "autoapi_member_order": "groupwise",
        "autoapi_root": "autoapi",
        "autoapi_toctree_depth": 3,
    }


def _get_collections_config() -> Dict[str, Any]:
    """Get sphinx-collections configuration for central hub."""
    return {
        "collections": {
            "haive_packages": {
                "driver": "copy_folder",
                "source_folder": "../../../packages/*/docs/build/html/",
                "target_folder": "_collections/",
                "active": True,
                "clean": True,
            },
        },
        "collections_clean": True,
        "collections_final_clean": False,
    }


def _get_complete_theme_options(
    package_name: str, is_central_hub: bool
) -> Dict[str, Any]:
    """Get complete Furo theme options with intense theming."""
    return {
        "sidebar_hide_name": False,
        # Enhanced TOC configuration
        "navigation_depth": 4,
        "collapse_navigation": False,
        "sticky_navigation": True,
        "includehidden": True,
        "titles_only": False,
        # Intense branding colors
        "light_css_variables": {
            "color-brand-primary": "#2563eb",  # Blue-600
            "color-brand-content": "#1d4ed8",  # Blue-700
            "color-background-primary": "#ffffff",
            "color-background-secondary": "#f8fafc",  # Slate-50
            "color-background-hover": "#e2e8f0",  # Slate-200
            "color-background-border": "#cbd5e1",  # Slate-300
            "color-code-background": "#1e293b",  # Slate-800
            "color-code-foreground": "#e2e8f0",  # Slate-200
            "color-sidebar-background": "#0f172a",  # Slate-900
            "color-sidebar-foreground": "#cbd5e1",  # Slate-300
            "color-api-background": "#f1f5f9",  # Slate-100
            "color-api-background-hover": "#e2e8f0",  # Slate-200
            "color-admonition-background": "#dbeafe",  # Blue-100
        },
        "dark_css_variables": {
            "color-brand-primary": "#60a5fa",  # Blue-400
            "color-brand-content": "#3b82f6",  # Blue-500
            "color-background-primary": "#0f172a",  # Slate-900
            "color-background-secondary": "#1e293b",  # Slate-800
            "color-background-hover": "#334155",  # Slate-700
            "color-background-border": "#475569",  # Slate-600
            "color-code-background": "#0f172a",  # Slate-900
            "color-code-foreground": "#cbd5e1",  # Slate-300
            "color-sidebar-background": "#020617",  # Slate-950
            "color-sidebar-foreground": "#94a3b8",  # Slate-400
        },
        # Repository integration
        "source_repository": "https://github.com/haive-ai/haive/",
        "source_branch": "main",
        "source_directory": (
            f"packages/{package_name}/docs/"
            if not is_central_hub
            else "tools/haive-docs/docs/"
        ),
        # Announcements
        "announcement": (
            "🚀 <strong>Haive AI Agent Framework</strong> - Complete monorepo documentation system!"
            if is_central_hub
            else f"🎯 {package_name} - Part of the Haive AI Agent Framework"
        ),
        # Footer icons
        "footer_icons": [
            {
                "name": "GitHub",
                "url": "https://github.com/haive-ai/haive/",
                "html": """<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                </svg>""",
            },
        ],
    }


def _get_complete_intersphinx_mapping() -> Dict[str, tuple]:
    """Get complete intersphinx mapping for cross-references."""
    return {
        "python": ("https://docs.python.org/3", None),
        "sphinx": ("https://www.sphinx-doc.org/en/master", None),
        "pydantic": ("https://docs.pydantic.dev/latest", None),
        "langchain": ("https://python.langchain.com/", None),
        "fastapi": ("https://fastapi.tiangolo.com/", None),
        # Add other Haive packages as they become available
        # "haive-core": ("https://docs.haive.ai/packages/haive-core/", None),
        # "haive-agents": ("https://docs.haive.ai/packages/haive-agents/", None),
    }
