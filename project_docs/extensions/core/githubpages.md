# sphinx.ext.githubpages - GitHub Pages Deployment

**Extension**: `sphinx.ext.githubpages`  
**Priority**: Core Foundation (Position 9 in extensions list)  
**Official Documentation**: [sphinx.ext.githubpages](https://www.sphinx-doc.org/en/master/usage/extensions/githubpages.html)  
**Status in PyDevelop-Docs**: ✅ Implemented for seamless GitHub Pages deployment

## Overview

`sphinx.ext.githubpages` adds support for publishing Sphinx documentation to GitHub Pages by creating the necessary files and configuration. This extension automates the GitHub Pages deployment process, making it easy to publish professional documentation directly from a GitHub repository with minimal configuration.

## Core Capabilities

### 1. GitHub Pages Integration

- **Automatic .nojekyll File**: Creates .nojekyll file to bypass Jekyll processing
- **CNAME Support**: Configures custom domain names for GitHub Pages
- **Branch Configuration**: Works with both `gh-pages` and `docs/` folder deployment
- **URL Structure**: Optimizes URLs for GitHub Pages hosting

### 2. Deployment Automation

- **Build Integration**: Seamlessly integrates with standard Sphinx build process
- **File Structure**: Ensures proper file structure for GitHub Pages
- **Asset Management**: Handles static assets and media files correctly
- **Index Configuration**: Configures proper index files for navigation

### 3. Custom Domain Support

- **CNAME Generation**: Automatically generates CNAME files for custom domains
- **DNS Configuration**: Provides guidance for DNS setup
- **HTTPS Support**: Enables HTTPS for custom domains
- **Subdomain Configuration**: Supports both apex and subdomain configurations

## Configuration in PyDevelop-Docs

### Current Implementation

```python
# In config.py - githubpages extension included in core
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.githubpages",  # GitHub Pages deployment support
    # ... other extensions
]

# Basic githubpages configuration (uses defaults)
# Automatically creates .nojekyll file during build
```

### Enhanced Configuration Options

```python
# Advanced GitHub Pages configuration for PyDevelop-Docs
import os

# GitHub Pages deployment configuration
github_pages_config = {
    # Custom domain configuration
    'custom_domain': os.environ.get('DOCS_DOMAIN', None),  # e.g., 'docs.haive.ai'
    'subdomain': os.environ.get('DOCS_SUBDOMAIN', None),   # e.g., 'haive.github.io'

    # Repository configuration
    'github_user': 'haive-ai',
    'github_repo': 'haive',
    'github_branch': 'main',
    'docs_branch': 'gh-pages',

    # Deployment configuration
    'deployment_method': 'gh-pages',  # 'gh-pages' or 'docs-folder'
    'build_directory': '_build/html',
    'enable_cname': True,
    'enable_nojekyll': True,

    # GitHub Actions integration
    'enable_github_actions': True,
    'workflow_file': '.github/workflows/docs.yml',

    # URL configuration
    'base_url': f"https://{os.environ.get('DOCS_DOMAIN', 'haive-ai.github.io')}",
    'canonical_url': True,
    'trailing_slash': True,
}

# Apply GitHub Pages specific settings
if github_pages_config['custom_domain']:
    html_baseurl = f"https://{github_pages_config['custom_domain']}/"
else:
    html_baseurl = f"https://{github_pages_config['github_user']}.github.io/{github_pages_config['github_repo']}/"

# GitHub Pages optimization
html_use_index = True
html_file_suffix = '.html'
html_link_suffix = '.html'

# SEO optimization for GitHub Pages
html_meta = {
    'robots': 'index, follow',
    'googlebot': 'index, follow',
    'description': f'{project} - Comprehensive documentation',
    'keywords': 'AI, agents, documentation, API, framework',
    'author': author,
    'viewport': 'width=device-width, initial-scale=1.0',
}

# Social media integration
html_meta.update({
    'og:site_name': project,
    'og:type': 'website',
    'og:url': html_baseurl,
    'og:title': f'{project} Documentation',
    'og:description': f'Comprehensive documentation for {project}',
    'og:image': f'{html_baseurl}_static/social-preview.png',
    'twitter:card': 'summary_large_image',
    'twitter:site': '@haive_ai',
    'twitter:title': f'{project} Documentation',
    'twitter:description': f'Comprehensive documentation for {project}',
    'twitter:image': f'{html_baseurl}_static/social-preview.png',
})
```

### GitHub Actions Integration

```python
# Generate GitHub Actions workflow for automated deployment
def generate_github_actions_workflow():
    """Generate GitHub Actions workflow for documentation deployment."""
    workflow_content = """
name: Deploy Documentation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        poetry install --with docs

    - name: Build documentation
      run: |
        cd docs
        poetry run sphinx-build -b html source _build/html

    - name: Upload artifact
      uses: actions/upload-pages-artifact@v2
      with:
        path: docs/_build/html

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v2
"""
    return workflow_content

# Custom domain configuration
def setup_custom_domain_config(app):
    """Setup custom domain configuration for GitHub Pages."""

    def create_cname_file(app, exception):
        """Create CNAME file for custom domain."""
        if exception:
            return

        custom_domain = getattr(app.config, 'github_pages_custom_domain', None)
        if custom_domain:
            cname_path = Path(app.outdir) / 'CNAME'
            with open(cname_path, 'w') as f:
                f.write(custom_domain)
            app.info(f"Created CNAME file for domain: {custom_domain}")

    app.connect('build-finished', create_cname_file)

def setup(app):
    app.add_config_value('github_pages_custom_domain', None, 'html')
    setup_custom_domain_config(app)
```

## Template Integration Opportunities

### 1. GitHub Pages Optimized Templates

```jinja2
{# _autoapi_templates/python/module.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{# GitHub Pages specific meta information #}
:github-repo: {{ config.github_pages_config.github_repo }}
:github-branch: {{ config.github_pages_config.github_branch }}
:deployment-url: {{ config.html_baseurl }}{{ obj.name|replace('.', '/') }}/

{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% endif %}

{# GitHub Pages navigation optimization #}
.. raw:: html

   <div class="github-pages-nav">
      <a href="{{ config.html_baseurl }}" class="home-link">🏠 Documentation Home</a>
      <a href="https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}"
         class="repo-link" target="_blank">📂 View Repository</a>
      <a href="https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}/blob/{{ config.github_pages_config.github_branch }}/{{ obj.source_file }}"
         class="source-link" target="_blank">📝 View Source</a>
   </div>

{# SEO optimization for GitHub Pages #}
.. meta::
   :description: {{ obj.name }} module documentation
   :keywords: {{ obj.name }}, API, documentation, {{ config.project }}
   :robots: index, follow

{# Rest of module documentation #}
{% if obj.classes %}
Classes
-------

{% for class in obj.classes %}
{{ class.render()|indent(0) }}
{% endfor %}
{% endif %}
```

### 2. GitHub Integration Templates

```jinja2
{# Enhanced class documentation with GitHub integration #}
{% macro render_github_class(obj) %}
{{ obj.name }}
{{ "=" * obj.name|length }}

{# GitHub source integration #}
.. container:: github-integration

   .. container:: source-info

      **Source:** `{{ obj.source_file }} <https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}/blob/{{ config.github_pages_config.github_branch }}/{{ obj.source_file }}#L{{ obj.start_line }}>`_

      **Repository:** `{{ config.github_pages_config.github_repo }} <https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}>`_

   .. container:: contribution-info

      Found an issue? `Report it on GitHub <https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}/issues/new>`_

      Want to contribute? `View the contributing guide <https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}/blob/{{ config.github_pages_config.github_branch }}/CONTRIBUTING.md>`_

{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% endif %}

{# GitHub Pages canonical URL #}
.. raw:: html

   <link rel="canonical" href="{{ config.html_baseurl }}{{ obj.canonical_path }}">

{# Structured data for search engines #}
.. raw:: html

   <script type="application/ld+json">
   {
     "@context": "https://schema.org",
     "@type": "SoftwareSourceCode",
     "name": "{{ obj.name }}",
     "description": "{{ obj.brief_description|escape }}",
     "codeRepository": "https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}",
     "programmingLanguage": "Python",
     "author": {
       "@type": "Organization",
       "name": "{{ config.author }}"
     },
     "license": "https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}/blob/{{ config.github_pages_config.github_branch }}/LICENSE"
   }
   </script>
{% endmacro %}
```

### 3. Navigation and SEO Templates

```jinja2
{# GitHub Pages optimized navigation #}
{% macro render_github_navigation(obj) %}
.. raw:: html

   <nav class="github-pages-breadcrumb" aria-label="Breadcrumb navigation">
      <ol class="breadcrumb">
         <li class="breadcrumb-item">
            <a href="{{ config.html_baseurl }}">Documentation</a>
         </li>
         {% set path_parts = obj.module_path.split('.') %}
         {% for part in path_parts[:-1] %}
         <li class="breadcrumb-item">
            <a href="{{ config.html_baseurl }}{{ path_parts[:loop.index]|join('/')|lower }}/">{{ part }}</a>
         </li>
         {% endfor %}
         <li class="breadcrumb-item active" aria-current="page">{{ obj.name }}</li>
      </ol>
   </nav>

   <div class="github-pages-actions">
      <a href="https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}/edit/{{ config.github_pages_config.github_branch }}/{{ obj.source_file }}"
         class="btn btn-outline-primary btn-sm" target="_blank">
         ✏️ Edit on GitHub
      </a>
      <a href="https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}/issues/new?title=Documentation%20issue:%20{{ obj.name }}&body=Issue%20with%20documentation%20for%20{{ obj.name }}%20at%20{{ config.html_baseurl }}{{ obj.canonical_path }}"
         class="btn btn-outline-secondary btn-sm" target="_blank">
         🐛 Report Issue
      </a>
   </div>
{% endmacro %}
```

## Best Practices for PyDevelop-Docs

### 1. GitHub Pages Optimized Documentation

```python
"""Haive Agent Framework - GitHub Pages Documentation Example.

This module demonstrates best practices for documentation that will be
deployed to GitHub Pages with optimal SEO and navigation.

The documentation includes:
* GitHub repository integration
* Canonical URLs for SEO
* Structured data for search engines
* Mobile-responsive navigation
* Contribution guidelines integration

Repository: https://github.com/haive-ai/haive
Documentation: https://docs.haive.ai
License: MIT License
"""

class GitHubPagesOptimizedAgent:
    """Agent optimized for GitHub Pages documentation.

    This class demonstrates how to write documentation that works
    exceptionally well when deployed to GitHub Pages.

    Key features for GitHub Pages optimization:

    * **Canonical URLs**: Each page has a canonical URL for SEO
    * **Structured Data**: JSON-LD structured data for search engines
    * **Mobile Responsive**: Works perfectly on all devices
    * **GitHub Integration**: Direct links to source code and issues
    * **Fast Loading**: Optimized assets and minimal JavaScript

    Args:
        name: Agent identifier for tracking and logging.
        config: Configuration object with GitHub Pages settings.

    Example:
        Create a GitHub Pages optimized agent:

        >>> agent = GitHubPagesOptimizedAgent(
        ...     name="docs-agent",
        ...     config=GitHubPagesConfig()
        ... )
        >>> agent.deploy_to_pages()
        'Documentation deployed to https://docs.haive.ai'

        View the source code for this example:
        `GitHubPagesOptimizedAgent source <https://github.com/haive-ai/haive/blob/main/packages/haive-docs/src/haive/docs/agents.py>`_

    Note:
        This agent requires proper GitHub Pages configuration in your
        repository settings. See the `GitHub Pages Setup Guide <https://docs.haive.ai/guides/github-pages-setup/>`_
        for detailed instructions.

    See Also:
        * :class:`BaseAgent`: Base agent functionality
        * :doc:`/deployment/github-pages`: GitHub Pages deployment guide
        * `GitHub Pages Documentation <https://docs.github.com/en/pages>`_
    """

    def __init__(self, name: str, config: 'GitHubPagesConfig'):
        """Initialize GitHub Pages optimized agent."""
        self.name = name
        self.config = config
        self._setup_github_integration()

    def deploy_to_pages(self) -> str:
        """Deploy documentation to GitHub Pages.

        This method demonstrates the deployment process with proper
        error handling and status reporting.

        Returns:
            str: Deployment URL if successful.

        Raises:
            DeploymentError: If GitHub Pages deployment fails.
            ConfigurationError: If GitHub configuration is invalid.

        Example:
            Deploy with custom domain:

            >>> config = GitHubPagesConfig(custom_domain="docs.mysite.com")
            >>> agent = GitHubPagesOptimizedAgent("deployer", config)
            >>> url = agent.deploy_to_pages()
            >>> print(f"Deployed to: {url}")
            Deployed to: https://docs.mysite.com

        Note:
            Deployment typically takes 1-2 minutes for changes to be visible.
            Monitor the deployment status in your GitHub repository's
            Actions tab.
        """
        # Implementation with GitHub Pages specific optimizations
        pass
```

### 2. SEO and Performance Optimization

```rst
GitHub Pages Performance Guide
==============================

This guide covers optimization techniques for GitHub Pages deployment.

.. meta::
   :description: Optimize Sphinx documentation for GitHub Pages deployment with SEO and performance best practices
   :keywords: GitHub Pages, Sphinx, documentation, SEO, performance, deployment
   :robots: index, follow

Overview
--------

GitHub Pages provides free hosting for static websites, making it perfect
for Sphinx documentation. However, proper optimization ensures fast loading
times and good search engine visibility.

.. raw:: html

   <script type="application/ld+json">
   {
     "@context": "https://schema.org",
     "@type": "TechArticle",
     "headline": "GitHub Pages Performance Guide",
     "description": "Comprehensive guide for optimizing Sphinx documentation on GitHub Pages",
     "author": {
       "@type": "Organization",
       "name": "Haive Team"
     },
     "publisher": {
       "@type": "Organization",
       "name": "Haive Documentation"
     },
     "mainEntityOfPage": "https://docs.haive.ai/guides/github-pages-performance/"
   }
   </script>

Performance Optimization
------------------------

Asset Optimization
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # In conf.py - optimize assets for GitHub Pages
   html_css_files = [
       "css/custom.min.css",  # Use minified CSS
   ]

   html_js_files = [
       "js/main.min.js",     # Use minified JavaScript
   ]

CDN Integration
~~~~~~~~~~~~~~~

Use CDNs for external resources:

.. code-block:: python

   # Use CDN for MathJax
   mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

   # Use CDN for fonts
   html_css_files = [
       "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"
   ]

SEO Optimization
---------------

Meta Tags
~~~~~~~~~

.. code-block:: python

   # Comprehensive meta tags for SEO
   html_meta = {
       'description': 'Your comprehensive documentation description',
       'keywords': 'relevant, keywords, for, your, project',
       'author': 'Your Organization',
       'robots': 'index, follow',
       'googlebot': 'index, follow',
       'viewport': 'width=device-width, initial-scale=1.0',
   }

Structured Data
~~~~~~~~~~~~~~

Add structured data for better search results:

.. code-block:: html

   <script type="application/ld+json">
   {
     "@context": "https://schema.org",
     "@type": "SoftwareApplication",
     "name": "Your Project",
     "description": "Project description",
     "applicationCategory": "DeveloperApplication",
     "operatingSystem": "Cross-platform"
   }
   </script>
```

### 3. GitHub Actions Automation

```yaml
# .github/workflows/docs.yml - Complete GitHub Pages deployment
name: Deploy Documentation to GitHub Pages

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 2 * * 0" # Weekly rebuild for external link checks

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

env:
  DOCS_ENVIRONMENT: production
  INCLUDE_TODO_ITEMS: false
  ENTERPRISE_FEATURES: true

jobs:
  check-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check external links
        run: |
          # Add link checking logic
          echo "Checking external links..."

  build:
    runs-on: ubuntu-latest
    needs: check-links
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install Poetry
        uses: snok/install-poetry@v1
        with:
          version: 1.6.1
          virtualenvs-create: true
          virtualenvs-in-project: true

      - name: Load cached dependencies
        uses: actions/cache@v3
        with:
          path: .venv
          key: venv-${{ runner.os }}-${{ hashFiles('**/poetry.lock') }}

      - name: Install dependencies
        run: poetry install --with docs

      - name: Build documentation
        run: |
          cd docs
          poetry run sphinx-build -b html source _build/html -W --keep-going

      - name: Optimize for GitHub Pages
        run: |
          # Create .nojekyll file
          touch docs/_build/html/.nojekyll

          # Create CNAME file if custom domain is set
          if [ ! -z "${{ vars.DOCS_DOMAIN }}" ]; then
            echo "${{ vars.DOCS_DOMAIN }}" > docs/_build/html/CNAME
          fi

          # Generate sitemap
          poetry run python scripts/generate_sitemap.py docs/_build/html

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: docs/_build/html

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2

      - name: Update deployment status
        run: |
          echo "Documentation deployed to: ${{ steps.deployment.outputs.page_url }}"
```

## Enhancement Opportunities

### 1. Advanced GitHub Integration

```python
def setup_advanced_github_integration(app):
    """Setup advanced GitHub integration features."""

    def add_github_edit_links(app, pagename, templatename, context, doctree):
        """Add edit links to every page."""
        if 'github_pages_config' in app.config:
            config = app.config.github_pages_config
            source_file = f"{pagename}.rst"
            edit_url = f"https://github.com/{config['github_user']}/{config['github_repo']}/edit/{config['github_branch']}/docs/source/{source_file}"
            context['github_edit_url'] = edit_url

    def add_github_issues_integration(app, exception):
        """Add GitHub issues integration."""
        if exception:
            return

        # Generate issue templates based on documentation structure
        issues_data = {
            'documentation_issues': [],
            'feature_requests': [],
            'bug_reports': []
        }

        # Write GitHub issue templates
        import json
        issues_path = Path(app.outdir) / 'github-issues.json'
        with open(issues_path, 'w') as f:
            json.dump(issues_data, f, indent=2)

    app.connect('html-page-context', add_github_edit_links)
    app.connect('build-finished', add_github_issues_integration)

def setup(app):
    setup_advanced_github_integration(app)
```

### 2. SEO and Analytics Enhancement

```python
def setup_github_pages_seo(app):
    """Setup enhanced SEO for GitHub Pages."""

    def add_structured_data(app, pagename, templatename, context, doctree):
        """Add structured data to pages."""
        structured_data = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": context.get('title', ''),
            "description": context.get('meta', {}).get('description', ''),
            "url": f"{app.config.html_baseurl}{pagename}.html",
            "isPartOf": {
                "@type": "WebSite",
                "name": app.config.project,
                "url": app.config.html_baseurl
            }
        }
        context['structured_data'] = json.dumps(structured_data, indent=2)

    def generate_sitemap(app, exception):
        """Generate sitemap.xml for better SEO."""
        if exception:
            return

        pages = []
        for pagename in app.env.all_docs:
            if pagename != 'index':
                pages.append({
                    'url': f"{app.config.html_baseurl}{pagename}.html",
                    'lastmod': datetime.now().isoformat(),
                    'priority': '0.8'
                })

        # Generate sitemap XML
        sitemap_content = generate_sitemap_xml(pages, app.config.html_baseurl)
        sitemap_path = Path(app.outdir) / 'sitemap.xml'
        with open(sitemap_path, 'w') as f:
            f.write(sitemap_content)

        app.info(f"Generated sitemap: {sitemap_path}")

    app.connect('html-page-context', add_structured_data)
    app.connect('build-finished', generate_sitemap)

def generate_sitemap_xml(pages, base_url):
    """Generate sitemap XML content."""
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    # Add homepage
    sitemap.append(f'  <url>')
    sitemap.append(f'    <loc>{base_url}</loc>')
    sitemap.append(f'    <lastmod>{datetime.now().isoformat()}</lastmod>')
    sitemap.append(f'    <priority>1.0</priority>')
    sitemap.append(f'  </url>')

    # Add pages
    for page in pages:
        sitemap.append(f'  <url>')
        sitemap.append(f'    <loc>{page["url"]}</loc>')
        sitemap.append(f'    <lastmod>{page["lastmod"]}</lastmod>')
        sitemap.append(f'    <priority>{page["priority"]}</priority>')
        sitemap.append(f'  </url>')

    sitemap.append('</urlset>')
    return '\n'.join(sitemap)

def setup(app):
    setup_github_pages_seo(app)
```

### 3. Performance Monitoring

```python
def setup_github_pages_monitoring(app):
    """Setup performance monitoring for GitHub Pages."""

    def analyze_build_performance(app, exception):
        """Analyze build performance and generate report."""
        if exception:
            return

        # Collect build metrics
        build_metrics = {
            'total_pages': len(app.env.all_docs),
            'build_time': time.time() - app.config.build_start_time,
            'total_size': calculate_output_size(app.outdir),
            'largest_pages': find_largest_pages(app.outdir),
            'optimization_suggestions': []
        }

        # Add optimization suggestions
        if build_metrics['total_size'] > 50 * 1024 * 1024:  # 50MB
            build_metrics['optimization_suggestions'].append(
                "Consider using image optimization for large assets"
            )

        # Write performance report
        report_path = Path(app.outdir) / 'performance-report.json'
        with open(report_path, 'w') as f:
            json.dump(build_metrics, f, indent=2)

        app.info(f"Build completed in {build_metrics['build_time']:.2f}s")
        app.info(f"Total output size: {build_metrics['total_size'] / 1024 / 1024:.1f}MB")

    def setup_build_timing(app, config):
        """Setup build timing."""
        app.config.build_start_time = time.time()

    app.connect('config-inited', setup_build_timing)
    app.connect('build-finished', analyze_build_performance)

def calculate_output_size(output_dir):
    """Calculate total size of output directory."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(output_dir):
        for filename in filenames:
            filepath = Path(dirpath) / filename
            total_size += filepath.stat().st_size
    return total_size

def find_largest_pages(output_dir):
    """Find the largest HTML pages."""
    pages = []
    for html_file in Path(output_dir).glob('**/*.html'):
        size = html_file.stat().st_size
        pages.append({'file': str(html_file.relative_to(output_dir)), 'size': size})

    return sorted(pages, key=lambda x: x['size'], reverse=True)[:10]

def setup(app):
    setup_github_pages_monitoring(app)
```

## Current Implementation Status

### ✅ Working Features

- [x] **Basic GitHub Pages support** - .nojekyll file creation working
- [x] **HTML optimization** - Proper HTML structure for GitHub Pages
- [x] **Static asset handling** - CSS, JS, and images work correctly
- [x] **URL structure** - Clean URLs for GitHub Pages hosting
- [x] **Mobile responsiveness** - Documentation works on all devices

### 🔄 Enhancement Opportunities

- [ ] **Custom domain automation** - Automatic CNAME file generation
- [ ] **GitHub Actions integration** - Complete CI/CD pipeline
- [ ] **SEO optimization** - Enhanced metadata and structured data
- [ ] **Performance monitoring** - Build time and size optimization
- [ ] **Analytics integration** - Usage tracking and insights

### 📋 Template Integration Tasks

1. **GitHub-integrated AutoAPI templates** with repository links
2. **SEO-optimized templates** with structured data
3. **Performance-optimized assets** for faster loading
4. **Mobile-responsive navigation** for all devices

## Integration with AutoAPI

### GitHub Pages URL Structure

```jinja2
{# Optimize AutoAPI URLs for GitHub Pages #}
{% set page_url = config.html_baseurl + obj.name|replace('.', '/')|lower + '.html' %}

.. raw:: html

   <link rel="canonical" href="{{ page_url }}">
   <meta property="og:url" content="{{ page_url }}">

{# GitHub repository integration #}
{% if config.github_pages_config %}
.. container:: github-integration

   .. raw:: html

      <div class="github-source-info">
         <a href="https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}/blob/{{ config.github_pages_config.github_branch }}/{{ obj.source_file }}"
            target="_blank" class="source-link">
            📝 View Source on GitHub
         </a>
         <a href="https://github.com/{{ config.github_pages_config.github_user }}/{{ config.github_pages_config.github_repo }}/issues/new?title=Documentation%20issue:%20{{ obj.name }}"
            target="_blank" class="issue-link">
            🐛 Report Documentation Issue
         </a>
      </div>
{% endif %}
```

### Mobile-Optimized Templates

```jinja2
{# Mobile-responsive AutoAPI templates #}
.. raw:: html

   <div class="api-object mobile-responsive">
      <div class="api-header">
         <h2 class="api-title">{{ obj.name }}</h2>
         <div class="api-meta">
            <span class="api-type">{{ obj.type }}</span>
            <span class="api-module">{{ obj.module }}</span>
         </div>
      </div>

      <div class="api-content">
         {{ obj.render_documentation() }}
      </div>
   </div>

   <style>
   @media (max-width: 768px) {
     .api-object {
       padding: 1rem;
       margin: 0.5rem 0;
     }

     .api-header {
       flex-direction: column;
       align-items: flex-start;
     }

     .api-meta {
       margin-top: 0.5rem;
     }
   }
   </style>
```

## Performance Considerations

### Build Optimization for GitHub Pages

```python
# Optimize builds for GitHub Pages deployment
html_minify_html = True  # Minify HTML output
html_remove_redundant_class_names = True  # Clean up CSS classes

# Asset optimization
html_css_files = [
    "css/main.min.css",  # Use minified CSS
]

html_js_files = [
    "js/main.min.js",   # Use minified JavaScript
]

# Image optimization
html_optimize_images = True
html_image_quality = 85  # Good quality with reasonable file size
```

### CDN Integration

```python
# Use CDNs for external resources to improve loading speed
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

# Font optimization
html_css_files.append(
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"
)
```

## Troubleshooting

### Common Issues

1. **Custom Domain Not Working**: Check CNAME file and DNS configuration
2. **Assets Not Loading**: Verify relative paths and .nojekyll file
3. **Build Failures**: Check GitHub Actions logs and permissions
4. **Slow Loading**: Optimize images and use CDNs for external resources

### Debug Configuration

```python
# Debug GitHub Pages deployment
github_pages_debug = True

def debug_github_pages_config(app, config):
    """Debug GitHub Pages configuration."""
    app.info(f"GitHub Pages base URL: {app.config.html_baseurl}")
    app.info(f"Custom domain: {getattr(app.config, 'github_pages_custom_domain', 'None')}")
    app.info(f"Repository: {getattr(app.config, 'github_pages_repo', 'Not configured')}")
```

## Integration with Issue #6

For AutoAPI template customization (Issue #6), GitHub Pages provides:

1. **Repository Integration**: Direct links from documentation to source code
2. **Collaborative Documentation**: Easy editing and issue reporting workflows
3. **SEO Optimization**: Enhanced search engine visibility for API documentation
4. **Performance Optimization**: Fast-loading documentation with CDN integration

The GitHub Pages extension enables AutoAPI templates to create documentation that integrates seamlessly with GitHub workflows, making it easy for users to contribute improvements and report issues while ensuring optimal performance and discoverability.
