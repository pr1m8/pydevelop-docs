# PyDevelop-Docs Complete System Guide

**Created**: 2025-08-18
**Purpose**: Complete documentation of PyDevelop-Docs system - what it is, what it does, and how to use everything
**Status**: Current System Analysis

## 🎯 What PyDevelop-Docs Is

PyDevelop-Docs is a **complete documentation system** for Python projects that provides:

1. **Universal Documentation Generator** - Transforms any Python project into beautiful docs
2. **40+ Pre-configured Sphinx Extensions** - Zero-configuration professional documentation
3. **Monorepo Support** - Handles complex multi-package projects like Haive
4. **Advanced Build Systems** - Multiple build approaches with monitoring and testing
5. **Visual Testing Suite** - Playwright-based screenshot testing for documentation quality
6. **AutoAPI Hierarchical Organization** - Fixes flat API documentation into organized structures

## 🏗️ System Architecture

### Core Components

1. **CLI System** (`src/pydevelop_docs/cli.py`)
   - Main command-line interface
   - Project initialization and building
   - Basic build commands

2. **Enhanced Build System** (`rebuild-haive` command)
   - Phase-based building (packages → master hub)
   - Real-time monitoring and error classification
   - Performance tracking and statistics
   - Advanced logging with JSON output

3. **Smart Builder** (`src/pydevelop_docs/smart_builder.py`)
   - Intelligent package ordering and dependency analysis
   - Build estimation and resource prediction
   - Package auditing and pre-build analysis

4. **Configuration System** (`src/pydevelop_docs/config.py`)
   - Centralized 830-line configuration
   - AutoAPI hierarchical fix (`autoapi_own_page_level = "module"`)
   - All 40+ Sphinx extensions pre-configured

5. **Visual Testing Suite** (`scripts/debug/`)
   - Playwright-based screenshot testing
   - Comprehensive documentation quality checks
   - Light/dark theme testing
   - Navigation and usability validation

## 🚀 How to Use the System

### 1. For Haive Documentation (Primary Use Case)

#### Full Haive Documentation Rebuild (Recommended)

```bash
# Navigate to PyDevelop-Docs
cd /home/will/Projects/haive/backend/haive/tools/pydevelop-docs

# Install all dependencies
poetry install --with dev,docs,web

# Run the enhanced build system (BEST for Haive)
poetry run pydevelop-docs rebuild-haive --debug --save-log

# Monitor progress (from another terminal)
tail -f /tmp/haive_rebuild_enhanced.log

# Check results
find /home/will/Projects/haive/backend/haive/packages/*/docs/build/html -name "index.html" | wc -l
```

**What this does:**

- **Phase 1**: Builds all 9 Haive packages individually with error classification
- **Phase 2**: Creates master documentation hub with cross-package linking
- **Features**: Real-time monitoring, build statistics, comprehensive logging
- **Output**: Complete documentation for all Haive packages + centralized hub

#### Background Build (For Long Operations)

```bash
# Start enhanced build in background
nohup poetry run pydevelop-docs rebuild-haive --debug > /tmp/haive_build.log 2>&1 &

# Monitor with
tail -f /tmp/haive_build.log

# Check process status
ps aux | grep rebuild-haive

# Check build completion
grep "Build Summary" /tmp/haive_build.log
```

### 2. Smart Builder (For Advanced Analysis)

```bash
# Interactive smart build with analysis
python src/pydevelop_docs/smart_builder.py

# What this provides:
# - Pre-build package analysis
# - Dependency-aware build ordering
# - Time and resource estimation
# - Detailed auditing reports
```

### 3. Individual Package Development

```bash
# From within a specific package (e.g., haive-core)
cd /home/will/Projects/haive/backend/haive/packages/haive-core

# Build just this package
poetry run --directory=../../tools/pydevelop-docs pydevelop-docs build --clean

# Watch for changes during development
poetry run --directory=../../tools/pydevelop-docs pydevelop-docs watch
```

### 4. Basic CLI Commands

```bash
# Initialize documentation for any project
cd your-project/
poetry run pydevelop-docs init

# Build with basic system
poetry run pydevelop-docs build

# Build all packages (monorepo)
poetry run pydevelop-docs build-all --clean
```

## 📸 Visual Testing System

### Complete Screenshot Testing Workflow

#### 1. Build Documentation First

```bash
# Use any of the build methods above, or build a specific package:
cd /home/will/Projects/haive/backend/haive/packages/haive-dataflow
poetry run sphinx-build -b html docs/source docs/build/html
```

#### 2. Serve Documentation

```bash
# Serve the built documentation
cd docs/build/html
python -m http.server 8003 --directory . &

# Or use nohup for background
nohup python -m http.server 8003 --directory . > /dev/null 2>&1 &
```

#### 3. Run Comprehensive Screenshot Tests

```bash
# From PyDevelop-Docs directory
cd /home/will/Projects/haive/backend/haive/tools/pydevelop-docs

# Install Playwright if needed
poetry run playwright install chromium

# Run comprehensive screenshot testing
poetry run python scripts/debug/comprehensive_screenshot.py 8003
```

#### 4. Run Specific Page Screenshots

```bash
# Screenshot a specific documentation page
poetry run python scripts/debug/screenshot_specific.py \
  "http://localhost:8003/autoapi/index.html" \
  "api_reference"

# Screenshot with custom output name
poetry run python scripts/debug/screenshot_specific.py \
  "http://localhost:8003/index.html" \
  "homepage"
```

### Screenshot Testing Features

**Comprehensive Testing (`comprehensive_screenshot.py`):**

- Tests 20+ documentation pages automatically
- Both light and dark theme screenshots
- Detects navigation issues, missing content, CSS problems
- Creates timestamped session directories
- Generates summary reports with issue analysis

**Specific Page Testing (`screenshot_specific.py`):**

- Test individual pages
- Quick visual validation
- Custom output naming
- Light/dark theme versions

**Output Structure:**

```
debug/screenshots/
├── comprehensive_20250818_HHMMSS/
│   ├── 01_index_light_full.png
│   ├── 01_index_light_viewport.png
│   ├── 01_index_light_issues.txt
│   ├── 01_index_dark_full.png
│   ├── 01_index_dark_viewport.png
│   ├── 01_index_dark_issues.txt
│   └── SUMMARY.md
└── specific_page_20250818_HHMMSS_light_full.png
```

## 🎯 Build System Comparison

### Enhanced Build (`rebuild-haive`) ⭐ **BEST FOR HAIVE**

**Command**: `poetry run pydevelop-docs rebuild-haive --debug --save-log`

- **Best For**: Complete Haive monorepo rebuilds, production builds
- **Features**: Phase-based building, error classification, statistics, monitoring
- **Performance**: ~10 minutes for all 9 packages with comprehensive logging
- **Output**: Rich monitoring data, build statistics, JSON logs

### Smart Builder (`smart_builder.py`) 🎯 **ADVANCED ANALYSIS**

**Command**: `python src/pydevelop_docs/smart_builder.py`

- **Best For**: Large monorepos, when you need build planning and analysis
- **Features**: Dependency-aware ordering, build estimation, package auditing
- **Performance**: Pre-analysis + optimized build ordering
- **Output**: Pre-build analysis, estimated times, detailed auditing

### Standard CLI (`build-all`) 📦 **BASIC**

**Command**: `poetry run pydevelop-docs build-all --clean`

- **Best For**: Simple builds, individual packages, debugging
- **Features**: Basic sequential building with minimal monitoring
- **Performance**: Sequential package building
- **Output**: Basic success/failure reporting

## 🔧 System Configuration

### Key Configuration Files

1. **Master Config**: `src/pydevelop_docs/config.py`
   - 830-line comprehensive Sphinx configuration
   - AutoAPI hierarchical fix on line 547: `"autoapi_own_page_level": "module"`
   - All 40+ extensions pre-configured

2. **CLI Implementation**: `src/pydevelop_docs/cli.py`
   - Command-line interface implementation
   - Now imports from config.py (consolidated)

3. **Templates**: `src/pydevelop_docs/templates/`
   - AutoAPI templates for hierarchical organization
   - Static assets (CSS, JS)
   - Jinja2 templates for customization

### Extension Categories (40+ Total)

- **Core Documentation (7)**: autodoc, napoleon, viewcode, intersphinx, todo, coverage, mathjax
- **API Documentation (3)**: autoapi, sphinx_autodoc_typehints, autodoc_pydantic
- **Enhanced Documentation (6)**: myst_parser, copybutton, togglebutton, design, tabs, inline_tabs
- **Diagramming (5)**: mermaid, plantuml, blockdiag, seqdiag, graphviz
- **Code & Examples (3)**: codeautolink, exec_code, runpython
- **UI Enhancements (3)**: tippy, favicon, sphinxemoji
- **Utilities (8)**: sitemap, last_updated_by_git, opengraph, reredirects, treeview, enum_tools, sphinx_toolbox
- **Pydantic Support (1)**: sphinxcontrib.autodoc_pydantic

## 🎨 Visual Features

### CSS Architecture (6 Files)

1. `api-docs.css` - API documentation styling
2. `css/custom.css` - General customizations
3. `furo-intense.css` - Dark mode fixes
4. `mermaid-custom.css` - Diagram styling
5. `tippy-enhancements.css` - Tooltip improvements
6. `toc-enhancements.css` - Table of contents

### AutoAPI Hierarchical Organization

**The Key Fix**: `autoapi_own_page_level = "module"`

- **Before**: 200+ classes in flat alphabetical list (unusable)
- **After**: Organized hierarchical structure with package/module grouping
- **Result**: Same content, dramatically better navigation

## 🚀 Quick Commands Reference

### Installation & Setup

```bash
cd /home/will/Projects/haive/backend/haive/tools/pydevelop-docs
poetry install --with dev,docs,web
```

### Build Commands

```bash
# Enhanced build (recommended)
poetry run pydevelop-docs rebuild-haive --debug --save-log

# Smart build with analysis
python src/pydevelop_docs/smart_builder.py

# Basic build
poetry run pydevelop-docs build-all --clean

# Single package
poetry run pydevelop-docs build --clean
```

### Testing Commands

```bash
# Serve documentation
python -m http.server 8003 --directory docs/build/html

# Screenshot testing
poetry run python scripts/debug/comprehensive_screenshot.py 8003
poetry run python scripts/debug/screenshot_specific.py "http://localhost:8003/index.html"
```

### Monitoring Commands

```bash
# Monitor enhanced build
tail -f /tmp/haive_rebuild_enhanced.log

# Check build status
grep "Build Summary" /tmp/haive_rebuild_enhanced.log

# Check running processes
ps aux | grep pydevelop-docs
```

## 🎯 What Each Command Actually Does

### `rebuild-haive --debug --save-log`

1. Clears all existing Haive documentation
2. Analyzes all 9 packages for dependencies and structure
3. Builds packages in dependency order with real-time monitoring
4. Creates comprehensive build statistics and error classification
5. Builds master documentation hub with cross-package linking
6. Saves detailed logs to `/tmp/haive_rebuild_enhanced.log`

### Screenshot Testing System

1. Launches Playwright browser (Chromium)
2. Takes full-page and viewport screenshots of documentation
3. Tests both light and dark themes
4. Checks for navigation issues, missing content, CSS problems
5. Creates comprehensive reports with issue analysis
6. Saves timestamped screenshots and summary reports

### Smart Builder Analysis

1. Scans all packages for size, dependencies, complexity
2. Creates build plan with estimated times and resource usage
3. Orders packages by dependency requirements
4. Provides pre-build audit and recommendations
5. Executes optimized build sequence with monitoring

## 🔍 Troubleshooting

### Common Issues

1. **Build Fails**: Check `/tmp/haive_rebuild_enhanced.log` for detailed errors
2. **Screenshots Fail**: Ensure HTTP server is running on specified port
3. **Import Errors**: Run `poetry install --with dev,docs,web`
4. **Memory Issues**: Use smart builder for large monorepos

### Debug Commands

```bash
# Check if server is running
curl -I http://localhost:8003

# Verify dependencies
poetry show | grep sphinx

# Test basic functionality
poetry run pydevelop-docs --help
```

## 📊 Current Status (2025-08-18)

### ✅ What's Working

- All 9 Haive packages build successfully with enhanced system
- AutoAPI hierarchical organization implemented and working
- Comprehensive screenshot testing system operational
- All 40+ Sphinx extensions integrated and functional
- Real-time build monitoring and error classification

### 🔄 What You Can Do Right Now

1. **Build all Haive documentation**: `poetry run pydevelop-docs rebuild-haive --debug`
2. **Test any package visually**: Build + serve + screenshot
3. **Analyze build performance**: Use smart builder for detailed analysis
4. **Customize documentation**: Modify templates and CSS files
5. **Monitor builds in real-time**: Use debug mode with tail -f

### 📅 Future Enhancements

- Performance optimization for faster builds
- Additional theme support beyond Furo
- Enhanced error reporting and auto-fixing
- Integration with CI/CD pipelines
- Publication to PyPI for public use

---

**Remember**: This is a complete, working documentation system. Every feature described above is operational and ready to use right now.
