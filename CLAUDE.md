# PyDevelop-Docs - Development Memory Hub

**Project**: PyDevelop Documentation Tools
**Purpose**: Universal Python documentation generator with 40+ Sphinx extensions pre-configured
**Location**: `/home/will/Projects/haive/backend/haive/tools/pydevelop-docs`
**Created**: 2025-01-08
**Last Updated**: 2025-08-13

## 🎯 Project Overview

PyDevelop-Docs is a comprehensive documentation generation tool that transforms any Python project into beautiful documentation with zero configuration. It provides a pre-configured setup with 40+ Sphinx extensions and supports single packages, monorepos, and complex project structures.

## 🏗️ Project Structure

```
pydevelop-docs/
├── src/pydevelop_docs/          # Core source code
│   ├── __init__.py              # Main exports and version info
│   ├── cli.py                   # Command-line interface (main entry point)
│   ├── config.py                # Sphinx configuration generator
│   ├── interactive.py           # Interactive CLI with rich UI
│   ├── builders.py              # Documentation builders
│   ├── autofix.py               # Automatic documentation fixes
│   ├── commands.py              # CLI command implementations
│   ├── mock_operations.py       # Dry-run and operation preview
│   ├── package_handlers.py      # Package detection and handling
│   ├── display.py               # Rich terminal display utilities
│   ├── link_builder.py          # Documentation linking utilities
│   ├── sphinx_debug.py          # Sphinx debugging utilities
│   └── templates/               # Configuration templates
│       ├── central_hub_conf.py  # Central hub configuration
│       ├── changelog.rst        # Changelog template
│       └── static/              # Static asset templates
├── docs/                        # PyDevelop-Docs own documentation
│   ├── source/                  # Sphinx source files
│   │   ├── conf.py             # Main Sphinx configuration
│   │   ├── conf_modules/       # Modular configuration system
│   │   ├── _static/            # CSS/JS assets (6 CSS files)
│   │   └── _templates/         # Custom Jinja2 templates
│   └── project-notes/          # Development documentation
├── project_docs/               # Project documentation and analysis
│   ├── AUTOAPI_HIERARCHICAL_FIX_STATUS_20250813.md
│   ├── CSS_FILES_COMPARISON_20250813.md
│   └── archive_haive_migration_20250813_142242/
├── test-projects/              # Test environments
│   └── test-haive-template/    # Test monorepo structure
└── scripts/                    # Utility scripts
    ├── example-monorepo.sh     # Monorepo example
    └── example-single.sh       # Single package example
```

## 🎯 Current Goals & Status

### ✅ Completed

1. **CLI Configuration Consolidation** - CLI now uses shared config module
2. **AutoAPI Hierarchical Fix** - Recursive nested structure working perfectly
3. **CSS White-on-White Fix** - Dark mode visibility fixes implemented
4. **Extension Order Fix** - sphinx_toolbox must load before sphinx_autodoc_typehints
5. **Test Environment** - test-haive-template validates all fixes

### 🔄 In Progress

1. **Issue #6**: Custom Jinja2 templates for AutoAPI - Assigned to other agent
2. **Template Infrastructure** - Setting up \_autoapi_templates/ directory

### 📅 Pending

1. **Issue #1**: Fix broken TOC references - Create missing index.rst files
2. **Issue #3**: Add minimal getting started content
3. **Issue #5**: Fix annoying UI elements (back-to-top button)
4. **Issue #7**: Consolidate CSS conflicts (17+ → 6 files)
5. **Issue #8**: Fix Pydantic information overload
6. **Issue #9-#12**: Various UI/UX improvements

## 🚨 CRITICAL DIRECTIVES FOR AGENTS

### 1. Configuration is Centralized

- **ALWAYS** make changes in `/src/pydevelop_docs/config.py`
- **NEVER** modify the hardcoded config in cli.py (lines 375-683)
- The CLI now imports from config.py - maintaining single source of truth

### 2. Testing Must Use Shared Config

```bash
# Always test with shared config (default)
poetry run pydevelop-docs init --use-shared-config

# Never use inline config unless specifically debugging
poetry run pydevelop-docs init --use-inline-config  # AVOID
```

### 3. Documentation Organization

- **Issues**: `/project_docs/issues/` - All issue tracking
- **Architecture**: `/project_docs/architecture/` - Design decisions
- **Testing**: `/project_docs/testing/` - Test results
- **See**: `/project_docs/README.md` for navigation

### 4. Template Locations

- **AutoAPI Templates**: `/src/pydevelop_docs/templates/_autoapi_templates/` (TODO)
- **Static Assets**: `/docs/source/_static/`
- **Sphinx Templates**: `/docs/source/_templates/`

## 🔑 Key Components

### 1. CLI System (`cli.py`)

- Main entry point for the tool
- Generates conf.py from hardcoded template
- **ISSUE**: Missing `autoapi_own_page_level = "module"` in template
- Commands: init, build, clean, sync

### 2. Configuration System (`config.py`)

- Provides `get_haive_config()` and `get_central_hub_config()`
- Contains complete AutoAPI configuration with hierarchical fix
- Used when projects import from pydevelop_docs.config

### 3. Builders (`builders.py`)

- SinglePackageBuilder - For individual packages
- MonorepoBuilder - For multi-package projects
- CustomConfigBuilder - For advanced setups

### 4. Mock Operations (`mock_operations.py`)

- Dry-run capability
- Operation preview before execution
- Risk assessment for file operations

### 5. Interactive Mode (`interactive.py`)

- Rich terminal UI
- Guided setup process
- Project type detection

## 📋 Configuration Approaches

### 1. Direct Template Generation (CLI)

```python
# cli.py generates conf.py with hardcoded template
# ❌ Missing: autoapi_own_page_level = "module"
```

### 2. Config Module Import

```python
# Projects can import shared configuration
from pydevelop_docs.config import get_haive_config
config = get_haive_config(package_name="my-package")
globals().update(config)
# ✅ Includes: autoapi_own_page_level = "module"
```

## 🐛 Known Issues

### 1. AutoAPI Hierarchical Fix Not in CLI Template

- **Location**: cli.py lines 441-460
- **Fix**: Add `autoapi_own_page_level = "module"`
- **Impact**: New projects get flat API documentation

### 2. Extension Loading Order

- **Fixed**: autoapi.extension must be first
- **Fixed**: sphinx_toolbox before sphinx_autodoc_typehints

### 3. CSS Files Structure

- **Current**: 6 consolidated CSS files (vs 17+ in Haive)
- **Benefit**: Cleaner, more maintainable

## 🛠️ Common Commands

```bash
# Development
poetry install --with dev
poetry run pydevelop-docs --help

# Testing with Shared Config (ALWAYS USE THIS)
cd test-projects/test-haive-template
poetry run pydevelop-docs init --force
poetry run sphinx-build -b html docs/source docs/build

# Quick Test Commands
poetry run pytest
poetry run pydevelop-docs init --dry-run

# Build PyDevelop-Docs own docs
cd docs && make html

# Full test cycle
cd test-projects/test-haive-template
poetry run pydevelop-docs init --force
poetry run pydevelop-docs build
python -m http.server 8003 --directory docs/build
# Open http://localhost:8003
```

## 🚀 Quick Reference

### Key Settings That Make It Work

```python
# In config.py - The magic setting for hierarchical docs
"autoapi_own_page_level": "module",  # Keep classes with modules

# Extension order (CRITICAL)
extensions = [
    "autoapi.extension",  # MUST be first
    # ... other extensions ...
    "sphinx_toolbox",  # MUST be before sphinx_autodoc_typehints
    "sphinx_autodoc_typehints",  # MUST be after sphinx_toolbox
]
```

### File Locations

- **Master Config**: `/src/pydevelop_docs/config.py`
- **Issue List**: `/project_docs/issues/COMPREHENSIVE_DOCUMENTATION_ISSUES_20250813.md`
- **Test Project**: `/test-projects/test-haive-template/`
- **CSS Files**: `/docs/source/_static/css/`

## 📝 Important Files

### Configuration

- `/src/pydevelop_docs/config.py` - Main configuration generator (SINGLE SOURCE OF TRUTH)
- `/src/pydevelop_docs/cli.py` - CLI interface (now uses config.py via consolidation)
- `/docs/source/conf.py` - PyDevelop-Docs own Sphinx config

### Documentation Hub

- `/project_docs/README.md` - Central documentation index
- `/project_docs/issues/` - Issue tracking and analysis
- `/project_docs/architecture/` - Architecture decisions
- `/project_docs/testing/` - Test results and progress
- `/EXTENSIONS.md` - List of all 40+ extensions

### Templates

- `/src/pydevelop_docs/templates/` - Configuration templates
- `/src/pydevelop_docs/templates/_autoapi_templates/` - Custom AutoAPI Jinja2 templates (TODO)
- `/docs/source/_templates/` - Sphinx Jinja2 templates
- `/docs/source/_static/` - CSS/JS assets

## 🎨 CSS Organization

### Current Structure (6 files)

1. `api-docs.css` - API documentation styling
2. `css/custom.css` - General customizations
3. `furo-intense.css` - Dark mode fixes
4. `mermaid-custom.css` - Diagram styling
5. `tippy-enhancements.css` - Tooltip improvements
6. `toc-enhancements.css` - Table of contents

### Key CSS Fixes

- White-on-white text in dark mode (furo-intense.css)
- Code block visibility
- Navigation contrast

## 🚀 Quick Fixes Needed

### 1. Update CLI Template

```python
# In cli.py after line 458:
autoapi_own_page_level = "module"  # Keep classes with their modules
```

### 2. Complete Visual Testing

```bash
cd test-projects/test-haive-template
poetry run sphinx-build -b html docs/source docs/build
# Open docs/build/index.html in browser
# Test dark mode toggle
```

## 📚 Extension Categories

### Core Documentation (7)

- autodoc, napoleon, viewcode, intersphinx, todo, coverage, mathjax

### API Documentation (3)

- autoapi, sphinx_autodoc_typehints, autodoc_pydantic

### Enhanced Documentation (6)

- myst_parser, copybutton, togglebutton, design, tabs, inline_tabs

### Diagramming (5)

- mermaid, plantuml, blockdiag, seqdiag, graphviz

### Code & Examples (3)

- codeautolink, exec_code, runpython

### UI Enhancements (3)

- tippy, favicon, sphinxemoji

### Utilities (8)

- sitemap, last_updated_by_git, opengraph, reredirects, treeview, enum_tools, sphinx_toolbox

### Pydantic Support (1)

- sphinxcontrib.autodoc_pydantic

## 🔗 Integration Points

### With Haive

- Originally developed for Haive documentation
- Migrated from haive_docs to pydevelop_docs
- Supports Haive's 7-package monorepo structure

### With Sphinx

- Extends standard Sphinx functionality
- Compatible with all Sphinx themes
- Preserves Sphinx command compatibility

## 💡 Design Philosophy

1. **Zero Configuration** - Works out of the box
2. **Universal Support** - Any Python project structure
3. **Beautiful Defaults** - Professional appearance immediately
4. **Extensible** - Easy to customize when needed
5. **Smart Detection** - Understands project structure

## 🎯 Next Steps

1. **Immediate**: Fix CLI template to include hierarchical AutoAPI setting
2. **Short-term**: Complete visual testing of CSS fixes
3. **Medium-term**: Add remaining documentation sections
4. **Long-term**: Publish to PyPI for public use

---

**Remember**: This tool aims to make Python documentation effortless. Every decision should reduce friction for users while maintaining flexibility for advanced use cases.
