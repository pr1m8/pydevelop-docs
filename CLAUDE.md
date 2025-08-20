# PyDevelop-Docs - Development Memory Hub

**Project**: PyDevelop Documentation Tools
**Purpose**: Universal Python documentation generator with 40+ Sphinx extensions pre-configured
**Status**: Standalone Package Ready for Isolation
**Created**: 2025-01-08
**Last Updated**: 2025-08-20 (Prepared for Isolation)

## 🎯 Project Overview

PyDevelop-Docs is a comprehensive documentation generation tool that transforms any Python project into beautiful documentation with zero configuration. It provides a pre-configured setup with 40+ Sphinx extensions and supports single packages, monorepos, and complex project structures.

## 🚀 **QUICK START - HOW TO USE EVERYTHING**

### **📖 COMPLETE GUIDE**: [COMPLETE_DOCUMENTATION_SYSTEM_GUIDE.md](./COMPLETE_DOCUMENTATION_SYSTEM_GUIDE.md)

### **Most Used Commands:**

```bash
# Build documentation for any Python project
poetry run pydvlp-docs build --clean

# Build all packages in a monorepo
poetry run pydvlp-docs build-all --clean

# Interactive initialization
poetry run pydvlp-docs init

# Visual testing (after building and serving docs)  
poetry run python scripts/debug/comprehensive_screenshot.py 8003

# Smart analysis and building
python src/pydevelop_docs/smart_builder.py
```

### **What Each System Does:**

- **Enhanced Build** ⭐ = Phase-based building with monitoring (best for large projects)
- **Smart Builder** 🎯 = Intelligent analysis and dependency-aware building
- **Visual Testing** 📸 = Playwright screenshots and quality validation
- **Standard CLI** 📦 = Basic building for simple projects

## 🏗️ Project Structure

```
pydvlp-docs/
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

## ✅ **COMPLETE SYSTEM STATUS (2025-08-18)**

### 🚀 **FULLY OPERATIONAL DOCUMENTATION SYSTEM**

**All Core Features Working:**

1. ✅ **Enhanced Build System** - Phase-based building with real-time monitoring
2. ✅ **AutoAPI Hierarchical Organization** - `autoapi_own_page_level = "module"` implemented
3. ✅ **Visual Testing Suite** - Playwright screenshot testing operational
4. ✅ **40+ Sphinx Extensions** - All pre-configured and working
5. ✅ **Smart Builder** - Intelligent package analysis and dependency-aware building
6. ✅ **CSS Architecture** - 6 modern CSS files with dark mode support
7. ✅ **Template System** - Custom Jinja2 templates with enhanced layouts
8. ✅ **Monorepo Support** - Complete Haive 9-package documentation system

### 📋 **COMPLETE SYSTEM GUIDE AVAILABLE**

**📖 See: [COMPLETE_DOCUMENTATION_SYSTEM_GUIDE.md](./COMPLETE_DOCUMENTATION_SYSTEM_GUIDE.md)**

- **What it is**: Complete architecture and feature explanation
- **How to use everything**: Step-by-step instructions for all features
- **Build system comparison**: Enhanced vs Smart vs Standard CLI
- **Visual testing workflow**: Complete screenshot testing guide
- **Command reference**: All commands with explanations

### 🎯 **READY TO USE RIGHT NOW**

**Primary Command for Haive:**

```bash
poetry run pydvlp-docs rebuild-haive --debug --save-log
```

**Visual Testing:**

```bash
poetry run python scripts/debug/comprehensive_screenshot.py 8003
```

**All features documented and operational - no pending development needed.**

## 🚀 Current Build Status (2025-08-17)

### ✅ **SUCCESS: All Haive Documentation Built**

**Enhanced Build Results:**

- **Method**: `rebuild-haive` command with advanced monitoring
- **Status**: ✅ **ALL 9 PACKAGES SUCCESSFUL** (Phase-based building completed)
- **Time**: ~10 minutes with comprehensive error classification
- **Features Used**: Real-time monitoring, error classification, performance tracking

**Packages Built with Enhanced System:**

1. ✅ haive-agp - Enhanced monitoring with docstring analysis
2. ✅ haive-dataflow - 23KB, 1161 warnings, 43.57s build time
3. ✅ haive-prebuilt - With grid structure analysis (712 occurrences)
4. ✅ haive-models - Docstring markup analysis (117 occurrences)
5. ✅ haive-games - Enhanced error classification
6. ✅ haive-mcp - Build monitoring and statistics
7. ✅ haive-agents - Comprehensive logging
8. ✅ haive-core - Advanced error handling
9. ✅ haive-tools - Performance tracking

**Master Documentation Hub**: ✅ Built with cross-package linking

## 📊 Build System Comparison

### Enhanced `rebuild-haive` ⭐ **BEST**

- **Performance**: Phase-based building with monitoring
- **Features**: Error classification, statistics, comprehensive logging
- **Use For**: Full Haive monorepo rebuilds, production builds
- **Output**: Rich monitoring data, build statistics, JSON logs

### Smart Builder `smart_builder.py` 🎯 **ADVANCED**

- **Performance**: Intelligent package ordering, dependency-aware
- **Features**: Build estimation, package auditing, resource prediction
- **Use For**: Large monorepos, when you need build planning
- **Output**: Pre-build analysis, estimated times, detailed auditing

### Standard CLI `build-all` 📦 **BASIC**

- **Performance**: Sequential package building
- **Features**: Basic build with minimal monitoring
- **Use For**: Simple builds, individual packages, debugging
- **Output**: Basic success/failure reporting

## 📋 Quick Start Project Guide

### For Haive Documentation (Recommended Workflow)

```bash
# 1. Navigate to pydvlp-docs
cd /home/will/Projects/haive/backend/haive/tools/pydvlp-docs

# 2. Install dependencies
poetry install --with dev,docs,web

# 3. Run enhanced build (BEST for Haive)
poetry run pydvlp-docs rebuild-haive --debug --save-log

# 4. Monitor progress (from another terminal)
tail -f /tmp/haive_rebuild_enhanced.log

# 5. Check results
find /home/will/Projects/haive/backend/haive/packages/*/docs/build/html -name "index.html" | wc -l
```

### For Individual Package Development

```bash
# From within a specific package directory (e.g., haive-core)
cd /home/will/Projects/haive/backend/haive/packages/haive-core

# Build just this package
poetry run --directory=../../tools/pydvlp-docs pydvlp-docs build --clean

# Watch for changes during development
poetry run --directory=../../tools/pydvlp-docs pydvlp-docs watch
```

### For New Projects

```bash
# Initialize documentation for any Python project
cd your-project/
poetry run pydvlp-docs init

# Build documentation
poetry run pydvlp-docs build

# Serve locally for development
cd docs && python -m http.server 8000
```

### Background Builds (Long-Running)

```bash
# For large monorepos - run in background with nohup
nohup poetry run pydvlp-docs rebuild-haive --debug > /tmp/build.log 2>&1 &

# Monitor with
tail -f /tmp/build.log

# Check process status
ps aux | grep rebuild-haive
```

## 🚨 CRITICAL DIRECTIVES FOR AGENTS

### 1. Configuration is Centralized

- **ALWAYS** make changes in `/src/pydevelop_docs/config.py`
- **NEVER** modify the hardcoded config in cli.py (lines 375-683)
- The CLI now imports from config.py - maintaining single source of truth

### 2. Testing Must Use Shared Config

```bash
# Always test with shared config (default)
poetry run pydvlp-docs init --use-shared-config

# Never use inline config unless specifically debugging
poetry run pydvlp-docs init --use-inline-config  # AVOID
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

## 🔑 Key Components & Build Systems

### 1. Enhanced Build System ⭐ **RECOMMENDED**

**Use the `rebuild-haive` command for comprehensive builds:**

```bash
# Full enhanced rebuild with monitoring and error classification
poetry run pydvlp-docs rebuild-haive --debug --save-log

# Rebuild specific packages only
poetry run pydvlp-docs rebuild-haive -p haive-core -p haive-agents

# Quick rebuild without master hub
poetry run pydvlp-docs rebuild-haive --no-master
```

**Features:**

- **Phase-based building**: Individual packages → Master documentation hub
- **Advanced monitoring**: Real-time error classification and statistics
- **Smart error handling**: Build monitoring with detailed logs
- **Performance tracking**: Build times, file counts, warning analysis
- **Comprehensive logging**: Debug mode with JSON operation logs

### 2. Smart Builder System (`smart_builder.py`)

**For large monorepos with intelligent package ordering:**

```bash
# Interactive smart build with confirmation
python -m pydevelop_docs.smart_builder /path/to/haive

# Non-interactive with custom output
python src/pydevelop_docs/smart_builder.py
```

**Features:**

- **Dependency-aware ordering**: Core packages first (haive-core → haive-tools → haive-agents)
- **Build estimation**: Time and resource prediction
- **Package auditing**: Comprehensive analysis before building
- **Real-time monitoring**: Progress tracking and error classification
- **Performance optimization**: Parallel builds and intelligent scheduling

### 3. Standard CLI System (`cli.py`)

**For basic builds and individual packages:**

```bash
# Build single package (from package directory)
poetry run pydvlp-docs build --clean --ignore-warnings

# Build all packages (basic, from monorepo root)
poetry run pydvlp-docs build-all --clean --ignore-warnings
```

### 4. Configuration System (`config.py`)

- **Centralized config**: 830-line comprehensive configuration
- **AutoAPI hierarchical fix**: `autoapi_own_page_level = "module"` on line 547
- **40+ Extensions**: Complete Sphinx extension ecosystem
- **Functions**: `get_haive_config()` and `get_central_hub_config()`

### 5. Builder Classes (`builders.py`)

- **BaseDocumentationBuilder**: Core builder with hooks and templates
- **SinglePackageBuilder**: Individual package documentation
- **MonorepoBuilder**: Multi-package projects with ignore support
- **CustomConfigBuilder**: YAML/TOML configuration support

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
poetry run pydvlp-docs --help

# Testing with Shared Config (ALWAYS USE THIS)
cd test-projects/test-haive-template
poetry run pydvlp-docs init --force
poetry run sphinx-build -b html docs/source docs/build

# Quick Test Commands
poetry run pytest
poetry run pydvlp-docs init --dry-run

# Build PyDevelop-Docs own docs
cd docs && make html

# Full test cycle
cd test-projects/test-haive-template
poetry run pydvlp-docs init --force
poetry run pydvlp-docs build
python -m http.server 8003 --directory docs/build
# Open http://localhost:8003
```

## 📸 Documentation Screenshot Tools

### Overview

PyDevelop-Docs includes powerful screenshot utilities for visual documentation testing and debugging. These tools help identify rendering issues, theme problems, and navigation failures.

### Available Scripts

Located in `/scripts/debug/`:

#### 1. `comprehensive_screenshot.py` - Full Documentation Screenshots

Takes screenshots of all major documentation pages in both light and dark themes.

```bash
# First, serve the docs
python -m http.server 8003 --directory docs/build

# Then run the screenshot tool
poetry run python scripts/debug/comprehensive_screenshot.py [port]
```

**Features:**

- Captures 20+ documentation pages automatically
- Tests both light and dark themes
- Checks for common issues (missing navigation, white-on-white text)
- Creates timestamped session directories
- Generates comprehensive summary reports

**Output:**

- Full page screenshots (entire scrollable content)
- Viewport screenshots (above the fold)
- Issue reports for each page
- Summary markdown report with analysis

#### 2. `screenshot_specific.py` - Single Page Screenshots

Captures screenshots of a specific documentation page.

```bash
# Screenshot a specific page
poetry run python scripts/debug/screenshot_specific.py <url> [output_prefix]

# Example: Screenshot the downloader config page
poetry run python scripts/debug/screenshot_specific.py \
  "http://localhost:8003/autoapi/mcp/downloader/config/index.html" \
  "downloader_config"
```

**Features:**

- Captures any specific URL
- Light and dark theme versions
- Quick issue detection
- Custom output naming

### Using the Screenshot Tools

1. **Build the documentation:**

   ```bash
   poetry run sphinx-build -b html docs/source docs/build
   ```

2. **Start the documentation server:**

   ```bash
   python -m http.server 8003 --directory docs/build
   ```

3. **Run screenshots:**

   ```bash
   # Comprehensive session
   poetry run python scripts/debug/comprehensive_screenshot.py

   # Specific page
   poetry run python scripts/debug/screenshot_specific.py "http://localhost:8003/autoapi/index.html"
   ```

4. **Review results:**

   ```bash
   # View screenshots
   ls -la debug/screenshots/

   # Check issue reports
   cat debug/screenshots/*/SUMMARY.md

   # Open specific screenshot (Linux)
   xdg-open debug/screenshots/*_light_full.png
   ```

### Common Issues Detected

The screenshot tools automatically check for:

- **Missing navigation sidebar** - Critical for usability
- **Missing TOC tree** - Table of contents issues
- **White-on-white text** - Dark mode visibility problems
- **CSS loading failures** - Styling not applied
- **Missing AutoAPI content** - API documentation generation issues
- **Broken source links** - GitHub integration problems

### Output Directory Structure

```
debug/screenshots/
├── comprehensive_20250815_135311/
│   ├── 01_index_light_full.png
│   ├── 01_index_light_viewport.png
│   ├── 01_index_light_issues.txt
│   ├── 01_index_dark_full.png
│   ├── 01_index_dark_viewport.png
│   ├── 01_index_dark_issues.txt
│   └── SUMMARY.md
└── downloader_config_20250815_135704_light_full.png
```

### Why Use These Tools?

1. **Visual Regression Testing** - Catch rendering issues before release
2. **Theme Testing** - Ensure both light and dark modes work
3. **Navigation Verification** - Confirm TOC and sidebar render correctly
4. **Cross-browser Testing** - Screenshots use Chromium engine
5. **Documentation QA** - Part of documentation quality assurance

### Testing on Real Projects

The screenshot tools are tested against real documentation, particularly the **haive-mcp** package documentation. This provides real-world validation of:

- Complex module hierarchies
- Multiple submodules (agents, cli, config, downloader, etc.)
- AutoAPI generation with nested structures
- Source code linking to GitHub repositories

Example testing workflow with haive-mcp:

```bash
# In haive-mcp directory
cd /home/will/Projects/haive/backend/haive/packages/haive-mcp

# Build docs
poetry run sphinx-build -b html docs/source docs/build

# Serve
python -m http.server 8003 --directory docs/build

# Run screenshots (from pydvlp-docs)
cd /home/will/Projects/haive/backend/haive/tools/pydvlp-docs
poetry run python scripts/debug/comprehensive_screenshot.py
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
