# Comprehensive Sphinx Documentation Dependencies Guide for Haive

**Generated**: 2025-01-28  
**Purpose**: Complete guide to useful documentation dependencies for the Haive AI Agent Framework  
**Status**: Research and recommendations for optimal documentation setup

## 📋 Table of Contents

1. [Currently Active Dependencies](#currently-active-dependencies)
2. [Highly Recommended Additional Dependencies](#highly-recommended-additional-dependencies)
3. [Specialized Dependencies by Use Case](#specialized-dependencies-by-use-case)
4. [Configuration Best Practices](#configuration-best-practices)
5. [Dependencies to Avoid or Use with Caution](#dependencies-to-avoid-or-use-with-caution)
6. [Missing Dependencies Worth Adding](#missing-dependencies-worth-adding)

## 🚀 Currently Active Dependencies

Your `conf.py` currently uses these extensions effectively:

### 1. **autoapi.extension** ✅

- **Purpose**: Automatic API documentation generation
- **Status**: Well-configured with namespace package support
- **Best Practice**: Keep `autoapi_python_use_implicit_namespaces = True` for your structure

### 2. **sphinx.ext.napoleon** ✅

- **Purpose**: Support for Google/NumPy docstring styles
- **Status**: Properly configured for both styles
- **Best Practice**: Standardize on Google style for consistency

### 3. **sphinx_copybutton** ✅

- **Purpose**: Adds copy buttons to code blocks
- **Status**: Working well
- **Best Practice**: No additional configuration needed

### 4. **sphinx_design** ✅

- **Purpose**: Enhanced layouts with cards, grids, tabs
- **Status**: Active and useful for user guides
- **Best Practice**: Use for landing pages and tutorials

### 5. **myst_parser** ✅

- **Purpose**: Markdown support with extended syntax
- **Status**: Well-configured with useful extensions
- **Best Practice**: Enable more extensions like `colon_fence` for better code blocks

### 6. **sphinxcontrib.mermaid** ✅

- **Purpose**: Diagram support (flowcharts, sequence diagrams)
- **Status**: Active
- **Best Practice**: Use for architecture diagrams

### 7. **sphinx_gallery.gen_gallery** ✅

- **Purpose**: Create galleries from Python examples
- **Status**: Active
- **Best Practice**: Configure example directories properly

### 8. **sphinx_exec_directive** ✅

- **Purpose**: Execute code blocks during build
- **Status**: Active
- **Best Practice**: Use with caution; cache results for speed

## 🎯 Highly Recommended Additional Dependencies

Based on your pyproject.toml, these would significantly improve your documentation:

### 1. **sphinx-autodoc-typehints** (High Priority)

```python
extensions.append("sphinx_autodoc_typehints")

# Configuration
typehints_fully_qualified = False
always_document_param_types = True
typehints_document_rtype = True
```

- **Why**: Automatically documents type hints in function signatures
- **Benefit**: Critical for AI agent framework with complex types

### 2. **autodoc-pydantic** (High Priority)

```python
extensions.append("sphinxcontrib.autodoc_pydantic")

# Configuration
autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = False
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_model_show_field_summary = True
```

- **Why**: Enhanced documentation for Pydantic models
- **Benefit**: Perfect for StateSchema and configuration models

### 3. **sphinx-autosummary-accessors** (Medium Priority)

```python
extensions.append("sphinx_autosummary_accessors")
```

- **Why**: Better summaries for properties and accessors
- **Benefit**: Cleaner API documentation for agent properties

### 4. **sphinx-tabs** (Medium Priority)

```python
extensions.append("sphinx_tabs.tabs")
```

- **Why**: Create tabbed content (e.g., Python/CLI examples)
- **Benefit**: Show multiple implementation approaches

### 5. **sphinx-prompt** (Medium Priority)

```python
extensions.append("sphinx_prompt")
```

- **Why**: Better shell/prompt formatting
- **Benefit**: Cleaner installation and CLI documentation

### 6. **myst-nb** (High Priority for Examples)

```python
extensions.append("myst_nb")

# Configuration
nb_execution_mode = "cache"
nb_execution_timeout = 60
nb_execution_raise_on_error = True
```

- **Why**: Execute Jupyter notebooks as documentation
- **Benefit**: Interactive agent examples and tutorials

## 🔧 Specialized Dependencies by Use Case

### For API Documentation

1. **sphinxcontrib-openapi**

   ```python
   extensions.append("sphinxcontrib.openapi")
   ```

   - Use if you have REST APIs for agent services

2. **sphinx-jsonschema**

   ```python
   extensions.append("sphinx_jsonschema")
   ```

   - Document JSON schemas for agent configurations

### For Better Code Examples

1. **sphinx-codeautolink**

   ```python
   extensions.append("sphinx_codeautolink")

   # Configuration
   codeautolink_global_preface = """
   from haive.agents import *
   from haive.core import *
   """
   ```

   - Auto-link code references to API docs

2. **sphinx-plotly-directive**
   - For interactive performance charts and metrics

### For Internationalization

1. **sphinx-intl** + **babel**
   - If planning multi-language documentation

### For Quality Assurance

1. **doc8**

   ```bash
   doc8 docs/source --max-line-length 88
   ```

   - RST/MD linting

2. **sphinx-lint**
   - Additional documentation linting

3. **vale** or **proselint**
   - Advanced prose linting for better writing

## 📝 Configuration Best Practices

### 1. Enhanced MyST Configuration

```python
myst_enable_extensions = [
    "deflist",      # Definition lists
    "tasklist",     # Task lists
    "dollarmath",   # Math support
    "amsmath",      # Advanced math
    "colon_fence",  # ::: code blocks
    "linkify",      # Auto-link URLs
    "substitution", # Variable substitution
    "html_admonition", # HTML in admonitions
]

myst_heading_anchors = 3  # Auto-anchors for h1-h3
```

### 2. Better Intersphinx Mapping

```python
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "langchain": ("https://python.langchain.com/docs", None),
    "pydantic": ("https://docs.pydantic.dev", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
    "torch": ("https://pytorch.org/docs/stable", None),
}
```

### 3. Search Enhancement

```python
# For better search
extensions.append("readthedocs_sphinx_search")

# RTD search configuration
rtd_sphinx_search_auto_index = True
```

### 4. Version Support

```python
# For multi-version docs
extensions.append("sphinx_multiversion")

# Configuration
smv_branch_whitelist = r'^(main|stable|v\d+\.\d+)$'
smv_tag_whitelist = r'^v\d+\.\d+\.\d+$'
```

## ⚠️ Dependencies to Avoid or Use with Caution

### 1. **sphinx-autodoc2**

- Conflicts with autoapi; use one or the other

### 2. **Multiple themes**

- You have many themes installed; stick with Furo

### 3. **sphinx-pdf-generate** / **sphinx-simplepdf**

- Complex setup; only if PDF is critical

### 4. **sphinxcontrib-blockdiag** / **seqdiag**

- Prefer Mermaid for diagrams (already configured)

## 🆕 Missing Dependencies Worth Adding

### 1. **sphinx-notfound-page**

```bash
poetry add --group docs sphinx-notfound-page
```

```python
extensions.append("notfound.extension")
notfound_urls_prefix = "/docs/"
```

- Custom 404 pages for better UX

### 2. **sphinx-inline-code**

```bash
poetry add --group docs sphinx-inline-code
```

- Better inline code highlighting

### 3. **sphinx-sitemap**

```python
extensions.append("sphinx_sitemap")
html_baseurl = "https://haive.readthedocs.io/"
```

- Already in pyproject.toml; add to conf.py for SEO

### 4. **sphinx-last-updated-by-git**

```python
extensions.append("sphinx_last_updated_by_git")
```

- Show last update time from Git

### 5. **sphinxext-opengraph**

```python
extensions.append("sphinxext.opengraph")

ogp_site_url = "https://haive.readthedocs.io/"
ogp_image = "https://haive.readthedocs.io/_static/logo.png"
```

- Better social media previews

## 🚀 Recommended Extension Stack for Haive

```python
# Core extensions (keep current)
extensions = [
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx_gallery.gen_gallery",
    "sphinx_exec_directive",

    # Add these high-priority extensions
    "sphinx_autodoc_typehints",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_tabs.tabs",
    "sphinx_prompt",
    "myst_nb",
    "sphinx_codeautolink",

    # Add these for better UX
    "readthedocs_sphinx_search",
    "sphinx_sitemap",
    "sphinxext.opengraph",
    "sphinx_last_updated_by_git",
    "notfound.extension",
]
```

## 📊 Performance Considerations

1. **Cache notebook execution**: Use `nb_execution_mode = "cache"`
2. **Limit autoapi scope**: Your ignore patterns are good
3. **Use build parallelization**: `sphinx-build -j auto`
4. **Enable only needed MyST extensions**: Don't enable all

## 🎯 Next Steps

1. **Immediate additions**:
   - `sphinx-autodoc-typehints` for type documentation
   - `autodoc-pydantic` for model documentation
   - `myst-nb` for notebook examples

2. **Configuration improvements**:
   - Add more MyST extensions
   - Configure search enhancement
   - Add sitemap and OpenGraph

3. **Quality assurance**:
   - Set up `doc8` in CI/CD
   - Add `sphinx-lint` checks
   - Configure Vale for prose linting

## 📚 Resources

- [Sphinx Extensions Gallery](https://sphinx-extensions.readthedocs.io/)
- [MyST Parser Documentation](https://myst-parser.readthedocs.io/)
- [AutoAPI Documentation](https://sphinx-autoapi.readthedocs.io/)
- [Furo Theme Documentation](https://pradyunsg.me/furo/)

---

This guide provides a comprehensive overview of documentation dependencies tailored specifically for the Haive AI Agent Framework, focusing on practical recommendations that will enhance your documentation quality and developer experience.
