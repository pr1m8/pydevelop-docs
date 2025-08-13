"""Link existing built documentation into a central hub."""

import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

import click


class DocumentationLinker:
    """Links existing built documentation from multiple packages."""

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.packages_dir = root_path / "packages"
        self.root_docs = root_path / "docs"

    def discover_built_docs(self) -> Dict[str, Dict[str, Path]]:
        """Discover all packages with built documentation."""
        packages = {}

        if not self.packages_dir.exists():
            return packages

        for package_dir in self.packages_dir.iterdir():
            if not package_dir.is_dir() or package_dir.name.startswith("."):
                continue

            # Check for built docs
            html_dir = package_dir / "docs" / "build" / "html"
            objects_inv = html_dir / "objects.inv"

            if html_dir.exists() and objects_inv.exists():
                packages[package_dir.name] = {
                    "path": package_dir,
                    "html_dir": html_dir,
                    "objects_inv": objects_inv,
                    "index": html_dir / "index.html",
                }

        return packages

    def create_intersphinx_mapping(
        self, packages: Dict[str, Dict[str, Path]]
    ) -> Dict[str, tuple]:
        """Create intersphinx mapping for cross-referencing."""
        mapping = {
            "python": ("https://docs.python.org/3", None),
            "sphinx": ("https://www.sphinx-doc.org/en/master", None),
        }

        # Add each package
        for name, info in packages.items():
            # Use relative paths from root docs build
            relative_path = f"../../packages/{name}/docs/build/html"
            mapping[name] = (relative_path, None)

        return mapping

    def create_hub_index(self, packages: Dict[str, Dict[str, Path]]) -> str:
        """Create a hub index.rst that links to all packages."""
        content = """Haive Documentation Hub
=======================

Welcome to the Haive AI Agent Framework documentation!

This hub provides centralized access to all package documentation with cross-referencing capabilities.

Package Documentation
--------------------

.. grid:: 2 2 3 3
   :gutter: 3
   
"""

        # Add each package as a card
        for name, info in sorted(packages.items()):
            # Count HTML files for stats
            html_files = list(info["html_dir"].glob("**/*.html"))

            content += f"""   .. grid-item-card:: {name}
      :link: ../../packages/{name}/docs/build/html/index.html
      :shadow: md
      
      {self._get_package_description(name)}
      
      **{len(html_files)}** documentation pages
      
"""

        # Add search and indices
        content += """

Quick Links
-----------

.. toctree::
   :maxdepth: 1
   :caption: Navigation
   
   packages/index
   api_reference
   cross_references

Search and Indices
------------------

* :ref:`genindex` - General Index
* :ref:`modindex` - Module Index  
* :ref:`search` - Search Page

Cross-Package Search
-------------------

Use the search functionality to find items across all packages. The intersphinx 
mappings enable cross-referencing between packages.

Examples:

- :py:class:`haive.core.Agent` - Reference core Agent class
- :py:func:`haive.tools.create_tool` - Reference tools function
- :py:mod:`haive.agents` - Reference agents module
"""
        return content

    def _get_package_description(self, name: str) -> str:
        """Get package description based on name."""
        descriptions = {
            "haive-core": "Core framework with agent engine and infrastructure",
            "haive-agents": "Pre-built agent implementations and patterns",
            "haive-tools": "Tool integrations and utility functions",
            "haive-games": "Game environments and AI strategies",
            "haive-mcp": "Model Context Protocol integration",
            "haive-dataflow": "Streaming and data processing capabilities",
            "haive-prebuilt": "Ready-to-use agent configurations",
            "haive-models": "Model integrations and configurations",
        }
        return descriptions.get(name, f"Documentation for {name}")

    def create_hub_config(self, packages: Dict[str, Dict[str, Path]]) -> str:
        """Create hub conf.py with theming inherited from individual packages."""
        intersphinx = self.create_intersphinx_mapping(packages)

        content = f'''"""
Haive Documentation Hub Configuration.

This configuration inherits theming and styling from individual packages
while using only hub-safe extensions for reliability.
"""

import os
import sys
from pathlib import Path

# Import theming configuration from pydevelop-docs
from pydevelop_docs.config import get_haive_config

# Get base configuration for theming inheritance
base_config = get_haive_config("haive-hub", "", is_central_hub=True)

# Project information
project = "Haive AI Agent Framework" 
author = "Haive Team"
copyright = "2025, Haive Team"
release = "0.1.0"

# Hub-safe extensions (curated from full suite)
extensions = [
    # Core documentation
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon", 
    "sphinx.ext.viewcode", 
    "sphinx.ext.intersphinx",
    # Content & Design - Essential theming extensions
    "myst_parser",
    "sphinx_design",  # Grid cards, badges, buttons
    "sphinx_togglebutton",  # Collapsible sections
    "sphinx_copybutton",  # Code copy buttons
    "sphinx_tabs.tabs",  # Tabbed content
    # Social & SEO - Safe utilities
    "sphinxext.opengraph",  # Social media cards
    "sphinx_favicon",  # Consistent branding
    "sphinx_sitemap",  # SEO optimization
    "sphinx_last_updated_by_git",  # Git integration
    "notfound.extension",  # Custom 404 pages
]

# Intersphinx mapping to all packages
intersphinx_mapping = {repr(intersphinx)}

# INHERIT THEMING from individual packages
html_theme = base_config.get("html_theme", "furo")
html_title = "Haive Documentation Hub"

# Get theme options from base config and enhance for hub
html_theme_options = base_config.get("html_theme_options", {{}}).copy()
html_theme_options.update({{
    "announcement": "🚀 Central hub for all Haive AI Agent Framework documentation",
    "source_directory": "docs/",
    "navigation_with_keys": True,
    "top_of_page_buttons": ["view"],
}})

# INHERIT STYLING from individual packages  
html_static_path = base_config.get("html_static_path", ["_static"])
html_css_files = ["css/hub.css"]  # Hub-specific CSS

# Add package CSS files if they exist
if "html_css_files" in base_config:
    html_css_files.extend(base_config["html_css_files"])

templates_path = base_config.get("templates_path", ["_templates"])

# INHERIT MYST CONFIGURATION from individual packages
myst_enable_extensions = base_config.get("myst_enable_extensions", [
    "deflist", "tasklist", "html_image", "colon_fence",
    "smartquotes", "replacements", "linkify", "strikethrough",
    "attrs_inline", "attrs_block"
])
myst_heading_anchors = base_config.get("myst_heading_anchors", 3)
myst_fence_as_directive = base_config.get("myst_fence_as_directive", ["mermaid", "note", "warning"])

# INHERIT SPHINX DESIGN CONFIGURATION
sd_fontawesome_latex = base_config.get("sd_fontawesome_latex", True)

# INHERIT COPY BUTTON CONFIGURATION  
copybutton_prompt_text = base_config.get("copybutton_prompt_text", r">>> |\\.\\.\\. |\\$ |In \\[\\d*\\]: | {{2,5}}\\.\\.\\.: | {{5,8}}: ")
copybutton_prompt_is_regexp = base_config.get("copybutton_prompt_is_regexp", True)
copybutton_remove_prompts = base_config.get("copybutton_remove_prompts", True)

# INHERIT TOGGLE BUTTON CONFIGURATION
togglebutton_hint = base_config.get("togglebutton_hint", "Click to expand")
togglebutton_hint_hide = base_config.get("togglebutton_hint_hide", "Click to collapse")

# INHERIT OPENGRAPH CONFIGURATION
ogp_site_url = "https://docs.haive.ai/"
ogp_site_name = base_config.get("ogp_site_name", "Haive AI Agent Framework")
ogp_site_description = "Central hub for all Haive AI Agent Framework documentation"
ogp_type = base_config.get("ogp_type", "website")
ogp_locale = base_config.get("ogp_locale", "en_US")

# INHERIT GIT INTEGRATION
sphinx_git_show_branch = base_config.get("sphinx_git_show_branch", True)
sphinx_git_show_tags = base_config.get("sphinx_git_show_tags", True)

# INHERIT 404 PAGE CONFIGURATION with hub-specific content
notfound_context = {{
    "title": "Page Not Found",
    "body": """
<h1>🚀 Oops! Page Not Found</h1>
<p>The page you're looking for seems to have wandered off into the documentation cosmos.</p>

<div class="admonition tip">
<p class="admonition-title">Try these options:</p>
<ul>
<li><strong>Search:</strong> Use the search box above to find what you need</li>
<li><strong>Packages:</strong> Browse individual <a href="packages/index.html">package documentation</a></li>
<li><strong>Home:</strong> Return to the <a href="index.html">main documentation hub</a></li>
<li><strong>API Reference:</strong> Check the complete API documentation in each package</li>
</ul>
</div>

<p>Still can't find what you're looking for? <a href="https://github.com/haive-ai/haive/issues">Report an issue</a> and we'll help you out!</p>
""",
}}
notfound_template = base_config.get("notfound_template", "page.html")
notfound_no_urls_prefix = base_config.get("notfound_no_urls_prefix", True)

# INHERIT SITEMAP CONFIGURATION
sitemap_url_scheme = base_config.get("sitemap_url_scheme", "{{link}}")

# INHERIT GENERAL CONFIGURATION
exclude_patterns = base_config.get("exclude_patterns", [
    "_build", "Thumbs.db", ".DS_Store"
])
exclude_patterns.append("autoapi")  # Exclude autoapi for hub

add_module_names = base_config.get("add_module_names", False)
toc_object_entries_show_parents = base_config.get("toc_object_entries_show_parents", "hide")

# INHERIT TOC CONFIGURATION
navigation_with_keys = base_config.get("navigation_with_keys", True)
toctree_maxdepth = base_config.get("toctree_maxdepth", 4)
toctree_collapse = base_config.get("toctree_collapse", False)
toctree_titles_only = base_config.get("toctree_titles_only", False)
'''
        return content

    def create_hub_structure(self):
        """Create the complete hub structure."""
        # Create directories
        source_dir = self.root_docs / "source"
        source_dir.mkdir(parents=True, exist_ok=True)

        static_dir = source_dir / "_static"
        static_dir.mkdir(exist_ok=True)

        css_dir = static_dir / "css"
        css_dir.mkdir(exist_ok=True)

        # Discover packages
        packages = self.discover_built_docs()

        if not packages:
            click.echo("❌ No packages with built documentation found!")
            return False

        click.echo(f"📦 Found {len(packages)} packages with built docs:")
        for name in sorted(packages.keys()):
            click.echo(f"   ✅ {name}")

        # Create index
        index_content = self.create_hub_index(packages)
        index_path = source_dir / "index.rst"
        index_path.write_text(index_content)
        click.echo("✅ Created hub index.rst")

        # Create conf.py
        conf_content = self.create_hub_config(packages)
        conf_path = source_dir / "conf.py"
        conf_path.write_text(conf_content)
        click.echo("✅ Created hub conf.py with intersphinx mappings")

        # Create CSS
        css_content = """
/* Hub documentation styles */
.grid-item-card {
    height: 100%;
}

.grid-item-card .sd-card-body {
    display: flex;
    flex-direction: column;
}

.grid-item-card .sd-card-body > :last-child {
    margin-top: auto;
}
"""
        css_path = css_dir / "hub.css"
        css_path.write_text(css_content)

        # Create packages index
        packages_dir = source_dir / "packages"
        packages_dir.mkdir(exist_ok=True)

        packages_index = """Package Documentation
====================

Detailed documentation for each package:

.. toctree::
   :maxdepth: 1
   
"""
        for name in sorted(packages.keys()):
            packages_index += (
                f"   {name} <../../../packages/{name}/docs/build/html/index>\n"
            )

        (packages_dir / "index.rst").write_text(packages_index)

        return True

    def build_hub(self, open_browser: bool = False):
        """Build the hub documentation.

        Args:
            open_browser: Whether to open the documentation in browser after building
        """
        if not self.create_hub_structure():
            return False

        # Build command
        cmd = [
            "sphinx-build",
            "-b",
            "html",
            str(self.root_docs / "source"),
            str(self.root_docs / "build" / "html"),
        ]

        click.echo("\n🔨 Building documentation hub...")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                click.echo("✅ Hub documentation built successfully!")
                html_path = self.root_docs / "build" / "html" / "index.html"
                click.echo(f"📖 View at: {html_path}")

                # Generate summary report
                self._generate_summary_report()

                # Open in browser if requested
                if open_browser:
                    import webbrowser

                    webbrowser.open(f"file://{html_path}")
                    click.echo("🌐 Opened documentation in browser")

                return True
            else:
                click.echo("❌ Build failed:")
                click.echo(result.stderr)
                return False

        except Exception as e:
            click.echo(f"❌ Build error: {e}")
            return False

    def _generate_summary_report(self):
        """Generate a summary report of the documentation hub."""
        packages = self.discover_built_docs()

        click.echo("\n📊 Documentation Hub Summary:")
        click.echo("=" * 50)

        total_pages = 0
        for name, info in sorted(packages.items()):
            html_files = list(info["html_dir"].glob("**/*.html"))
            page_count = len(html_files)
            total_pages += page_count
            click.echo(f"  📦 {name:<20} {page_count:>5} pages")

        click.echo("=" * 50)
        click.echo(f"  📚 Total:              {total_pages:>5} pages")
        click.echo(f"  🔗 Intersphinx enabled: ✅")
        click.echo(f"  🌐 Cross-references:    ✅")

    def update_hub(self):
        """Update the hub without full rebuild (only regenerate index)."""
        packages = self.discover_built_docs()

        if not packages:
            click.echo("❌ No packages with built documentation found!")
            return False

        click.echo(f"📦 Updating hub for {len(packages)} packages...")

        # Update index.rst
        source_dir = self.root_docs / "source"
        if source_dir.exists():
            index_content = self.create_hub_index(packages)
            index_path = source_dir / "index.rst"
            index_path.write_text(index_content)
            click.echo("✅ Updated hub index.rst")

            # Quick rebuild (only HTML, not full rebuild)
            cmd = [
                "sphinx-build",
                "-b",
                "html",
                "-E",  # Don't use cached environment
                str(source_dir),
                str(self.root_docs / "build" / "html"),
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    click.echo("✅ Hub updated successfully!")
                    self._generate_summary_report()
                    return True
                else:
                    click.echo("❌ Update failed")
                    return False
            except Exception as e:
                click.echo(f"❌ Update error: {e}")
                return False
        else:
            click.echo("❌ Hub not initialized. Run 'link-docs' first.")
            return False
