# PyDevelop Documentation Tools

**🚀 Universal Python documentation generator with 40+ Sphinx extensions pre-configured**

Turn any Python project into beautiful documentation with one command. No configuration needed.

## ✨ Features

- **🎯 Zero Configuration**: Works out-of-the-box with any Python project
- **📦 Universal Support**: Single packages, monorepos, any structure
- **🎨 Beautiful Themes**: Pre-configured Furo theme with dark mode
- **🔧 40+ Extensions**: Full PyAutoDoc configuration included
- **⚡ Smart Detection**: Automatically detects project structure
- **🚀 Interactive CLI**: Guided setup with rich terminal UI

## 🚀 Quick Start

### 1. Install

```bash
# With pip
pip install pydevelop-docs

# With Poetry (recommended)
poetry add --group docs pydevelop-docs
```

### 2. Initialize Documentation

```bash
# Interactive mode (recommended)
pydevelop-docs

# Or command line
pydevelop-docs init
```

### 3. Build Documentation

```bash
pydevelop-docs build
```

Your documentation is now available at `docs/build/html/index.html`!

## 📋 What You Get

- **Complete Sphinx Setup**: Ready-to-use configuration with 40+ extensions
- **API Documentation**: Automatic API docs from your code
- **Beautiful Theme**: Professional Furo theme with customizations
- **Code Examples**: Syntax highlighting and copy buttons
- **Diagrams**: Mermaid, PlantUML, and more diagram support
- **Search**: Full-text search functionality
- **Mobile Friendly**: Responsive design for all devices

## 🎯 Use Cases

### Single Package

Perfect for individual Python packages:

```
my-package/
├── src/my_package/
├── tests/
├── pyproject.toml
└── docs/              # ← Created by pydevelop-docs
    ├── source/
    │   ├── conf.py    # ← Pre-configured with 40+ extensions
    │   └── index.rst  # ← Main documentation page
    └── build/         # ← Generated HTML
```

### Monorepo

Great for multi-package repositories:

```
my-monorepo/
├── packages/
│   ├── package-a/
│   │   └── docs/      # ← Individual package docs
│   └── package-b/
│       └── docs/      # ← Individual package docs
├── tools/
└── docs/              # ← Central documentation hub
```

## 🔧 Commands

### `pydevelop-docs`

Launch interactive CLI (recommended for beginners)

### `pydevelop-docs init`

Initialize documentation structure

**Options:**

- `--packages-dir, -d`: Directories to scan for packages
- `--include-root, -r`: Include root-level documentation
- `--packages, -p`: Specific packages to initialize
- `--dry-run, -n`: Preview changes without making them
- `--force, -f`: Overwrite existing documentation

**Examples:**

```bash
# Single package
pydevelop-docs init

# Monorepo with multiple package directories
pydevelop-docs init -d packages -d tools --include-root

# Specific packages only
pydevelop-docs init -p my-package -p my-other-package
```

### `pydevelop-docs build`

Build documentation

**Options:**

- `--clean, -c`: Clean before building
- `--package, -p`: Build specific package
- `--no-parallel`: Disable parallel building

**Examples:**

```bash
# Build all documentation
pydevelop-docs build

# Clean build
pydevelop-docs build --clean

# Build specific package
pydevelop-docs build --package my-package
```

### `pydevelop-docs clean`

Remove all build artifacts

### `pydevelop-docs sync`

Sync documentation between packages

```bash
pydevelop-docs sync source-package target-package
```

## ⚙️ Configuration

Create `.pydevelop-docs.yaml` in your project root for custom settings:

```yaml
# Project structure
settings:
  packages_dir:
    - packages
    - tools
  include_root: true

# Build options
build:
  central_hub: true
  parallel: true
  clean_before_build: false

# Paths
paths:
  docs_folder: "docs"
  source_folder: "source"
  build_folder: "build"

# Theme customization
theme:
  name: "furo"
  dark_mode: true
  sidebar_hide_name: false

# Extensions
extensions:
  autoapi: true
  mermaid: true
  copybutton: true
  # Add any additional extensions here
```

## 📚 Included Extensions

All 40+ extensions are pre-configured and optimized:

### Core Documentation

- `sphinx.ext.autodoc` - Automatic documentation from docstrings
- `sphinx.ext.napoleon` - Google/NumPy style docstrings
- `sphinx.ext.viewcode` - Source code links
- `sphinx.ext.intersphinx` - Cross-project references

### API Documentation

- `autoapi.extension` - Automatic API documentation
- `sphinx_autodoc_typehints` - Type hint support
- `sphinxcontrib.autodoc_pydantic` - Pydantic model docs

### Content & Design

- `myst_parser` - Markdown support
- `sphinx_design` - Bootstrap-style components
- `sphinx_togglebutton` - Collapsible sections
- `sphinx_copybutton` - Copy code buttons
- `sphinx_tabs.tabs` - Tabbed content

### Diagrams & Visualization

- `sphinxcontrib.mermaid` - Mermaid diagrams
- `sphinxcontrib.plantuml` - PlantUML diagrams
- `sphinx.ext.graphviz` - Graphviz diagrams

### Advanced Features

- `sphinx_sitemap` - SEO sitemap generation
- `sphinx_codeautolink` - Automatic code linking
- `sphinx_tippy` - Rich hover tooltips
- `sphinx_last_updated_by_git` - Git-based update tracking
- `sphinx_changelog` - Changelog generation
- `sphinx_issues` - GitHub issue integration

### Utilities

- `sphinx_favicon` - Favicon support
- `notfound.extension` - Custom 404 pages
- `sphinxext.opengraph` - Social media previews
- `sphinx_tags` - Content tagging

[See complete list of 40+ extensions →](https://github.com/haive-ai/pydevelop-docs/blob/main/docs/EXTENSIONS.md)

## 🎨 Customization

### Custom CSS

Add custom styles by creating `docs/source/_static/css/custom.css`:

```css
/* Your custom styles */
.bd-main .bd-content .bd-article-container {
  max-width: 100rem;
}
```

### Custom Templates

Override templates by creating files in `docs/source/_templates/`:

```
docs/source/_templates/
├── layout.html
├── sidebar.html
└── ...
```

### Theme Options

Customize the Furo theme in your `conf.py`:

```python
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#1d4ed8",
    },
    "dark_css_variables": {
        "color-brand-primary": "#60a5fa",
        "color-brand-content": "#3b82f6",
    },
}
```

## 🔄 Integration Examples

### With GitHub Actions

```yaml
name: Documentation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install --with docs

      - name: Build documentation
        run: poetry run pydevelop-docs build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/build/html
```

### With Pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: docs-build
        name: Build documentation
        entry: poetry run pydevelop-docs build
        language: system
        pass_filenames: false
        always_run: true
```

## 🛠️ Development

### Contributing

```bash
# Clone repository
git clone https://github.com/haive-ai/pydevelop-docs
cd pydevelop-docs

# Install in development mode
poetry install --with dev

# Run tests
poetry run pytest

# Build documentation
poetry run pydevelop-docs build

# Run pre-commit hooks
pre-commit run --all-files
```

### Project Structure

```
pydevelop-docs/
├── src/pydevelop_docs/
│   ├── __init__.py       # Main exports
│   ├── cli.py            # Command-line interface
│   ├── config.py         # Sphinx configuration
│   ├── interactive.py    # Interactive CLI
│   ├── builders.py       # Documentation builders
│   ├── autofix.py        # Automatic fixes
│   └── templates/        # File templates
├── docs/                 # Documentation
├── tests/                # Test suite
└── scripts/              # Example scripts
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Read the full docs →](https://pydevelop-docs.readthedocs.io)
- **Issues**: [Report bugs →](https://github.com/haive-ai/pydevelop-docs/issues)
- **Discussions**: [Ask questions →](https://github.com/haive-ai/pydevelop-docs/discussions)
- **Email**: [team@haive.ai](mailto:team@haive.ai)

---

**Made with ❤️ by the Haive Team**

Transform your Python documentation from zero to hero in minutes, not hours.
