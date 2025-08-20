# Haive Documentation Build Guide

**Created**: 2025-08-13
**Purpose**: Complete guide for building Haive documentation using PyDevelop-Docs

## Overview

Haive is a monorepo with 7 packages. PyDevelop-Docs can build documentation for:

1. **Individual packages** - Each package's own documentation
2. **Central hub** - Unified documentation portal
3. **Aggregate docs** - Combined documentation with cross-references

## Prerequisites

```bash
# Navigate to Haive project root
cd /home/will/Projects/haive/backend/haive

# Ensure PyDevelop-Docs is installed
cd tools/pydvlp-docs
poetry install
cd ../..
```

## Building Documentation

### Option 1: Build Everything (Recommended)

```bash
# From Haive root directory
cd /home/will/Projects/haive/backend/haive

# Initialize documentation structure for monorepo
poetry run pydvlp-docs init --project-type monorepo

# Build all package documentation + central hub
poetry run pydvlp-docs build --all

# The command will:
# 1. Build docs for each package in packages/
# 2. Create a central hub in docs/
# 3. Set up cross-package navigation
```

### Option 2: Build Individual Package Documentation

```bash
# Build specific package documentation
cd packages/haive-core
poetry run pydvlp-docs init --force
poetry run pydvlp-docs build

# Or build from root with package specification
poetry run pydvlp-docs build --package haive-core
poetry run pydvlp-docs build --package haive-agents
poetry run pydvlp-docs build --package haive-tools
```

### Option 3: Build Central Hub Only

```bash
# From Haive root
poetry run pydvlp-docs init --project-type central-hub
poetry run pydvlp-docs build --hub-only
```

## Documentation Structure

After building, you'll have:

```
haive/
├── docs/                           # Central documentation hub
│   ├── source/
│   │   ├── index.rst              # Main landing page
│   │   ├── packages/              # Package overview
│   │   └── _collections/          # Aggregated docs
│   └── build/
│       └── html/                  # Built documentation
├── packages/
│   ├── haive-core/
│   │   └── docs/
│   │       ├── source/            # Package-specific docs
│   │       └── build/html/        # Built package docs
│   ├── haive-agents/
│   │   └── docs/build/html/
│   └── ... (other packages)
```

## Viewing Documentation

### 1. View Central Hub

```bash
# Start server for central hub
cd docs/build/html
python -m http.server 8000
# Open http://localhost:8000
```

### 2. View Individual Package Docs

```bash
# For specific package
cd packages/haive-core/docs/build/html
python -m http.server 8001
# Open http://localhost:8001
```

### 3. View All Documentation with Navigation

The central hub provides navigation to all package documentation with:

- Package overview cards
- Direct links to each package's documentation
- Cross-package search functionality
- Unified API index

## Advanced Build Options

### Clean Build

```bash
# Remove all previous build artifacts
poetry run pydvlp-docs clean --all
poetry run pydvlp-docs build --all --clean
```

### Parallel Building

```bash
# Build all packages in parallel (faster)
poetry run pydvlp-docs build --all --parallel
```

### Watch Mode (Development)

```bash
# Auto-rebuild on file changes
poetry run pydvlp-docs build --watch
```

### Custom Configuration

```bash
# Use custom Sphinx configuration
poetry run pydvlp-docs build --config path/to/custom_conf.py
```

## Build Process Details

### For Each Package

1. **AutoAPI** scans source code and generates API documentation
2. **Intersphinx** creates cross-references between packages
3. **Extensions** enhance documentation (mermaid diagrams, copy buttons, etc.)
4. **Templates** apply intelligent formatting based on object types

### For Central Hub

1. **sphinx-collections** aggregates all package documentation
2. **Navigation** creates unified menu structure
3. **Search** builds combined search index
4. **Landing page** provides overview and quick access

## Troubleshooting

### Common Issues

1. **Import Errors**

   ```bash
   # Ensure all packages are installed
   poetry install --all-extras
   ```

2. **AutoAPI Not Finding Code**

   ```bash
   # Check autoapi_dirs in each package's conf.py
   # Should point to source code location
   ```

3. **Missing Dependencies**
   ```bash
   # Install documentation dependencies
   poetry install --with docs
   ```

### Build Verification

```bash
# Check build was successful
find . -name "index.html" -path "*/docs/build/*" | head -10

# Should show:
# ./docs/build/html/index.html
# ./packages/haive-core/docs/build/html/index.html
# ./packages/haive-agents/docs/build/html/index.html
# etc.
```

## Configuration Customization

### Package-Specific Configuration

Each package can have custom documentation settings:

```python
# packages/haive-core/docs/source/conf.py
from pydevelop_docs.config import get_haive_config

# Get base configuration
config = get_haive_config("haive-core", project_root="../..")

# Customize for this package
config.update({
    "html_theme_options": {
        "announcement": "Core API Documentation"
    }
})

globals().update(config)
```

### Central Hub Configuration

```python
# docs/source/conf.py
from pydevelop_docs.config import get_central_hub_config

config = get_central_hub_config(
    project_name="Haive AI Framework",
    packages=[
        "haive-core",
        "haive-agents",
        "haive-tools",
        "haive-games",
        "haive-mcp",
        "haive-dataflow",
        "haive-prebuilt"
    ]
)

globals().update(config)
```

## Best Practices

1. **Always build from root** for monorepo projects
2. **Use --clean** for production builds
3. **Test locally** before deploying
4. **Keep package docs independent** but linked
5. **Use central hub** as main entry point

## CI/CD Integration

```yaml
# .github/workflows/docs.yml
name: Build Documentation
on:
  push:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Poetry
        uses: snok/install-poetry@v1
      - name: Install dependencies
        run: poetry install --with docs
      - name: Build all documentation
        run: poetry run pydvlp-docs build --all --clean
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/build/html
```

## Summary

PyDevelop-Docs handles the complexity of monorepo documentation:

- **Automatic package discovery**
- **Hierarchical API documentation**
- **Cross-package linking**
- **Unified search and navigation**
- **Beautiful, consistent styling**

Just run `poetry run pydvlp-docs build --all` and get professional documentation for your entire project!
