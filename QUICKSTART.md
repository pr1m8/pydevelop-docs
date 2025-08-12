# PyDevelop-Docs Quick Start Guide

Get beautiful documentation for your Python project in under 5 minutes.

## 🚀 Super Quick Start

```bash
# 1. Install
poetry add --group docs pydevelop-docs

# 2. Initialize docs
poetry run pydevelop-docs init

# 3. Build docs
poetry run pydevelop-docs build

# 4. View docs
open docs/build/html/index.html
```

That's it! Your documentation is ready.

## 🎯 What Just Happened?

PyDevelop-docs automatically:

1. **Detected your project structure** (single package or monorepo)
2. **Created a `docs/` folder** with complete Sphinx configuration
3. **Pre-configured 40+ extensions** for professional documentation
4. **Set up the Furo theme** with dark mode and responsive design
5. **Generated API documentation** from your code automatically
6. **Added all the advanced features** like copy buttons, diagrams, search

## 📁 What Files Were Created?

```
docs/
├── source/
│   ├── conf.py              # ← Complete Sphinx config (40+ extensions!)
│   ├── index.rst            # ← Main documentation page
│   ├── _static/            # ← Custom CSS, JS, images
│   ├── _templates/         # ← Custom Sphinx templates
│   └── _autoapi_templates/ # ← API documentation templates
├── build/                  # ← Generated HTML (after building)
│   └── html/
│       └── index.html      # ← Your documentation!
└── Makefile               # ← Build commands
```

## 🔧 Common Next Steps

### Add Content

Edit `docs/source/index.rst` to add your own content:

```rst
My Awesome Project
==================

Welcome to my project's documentation!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/index
   changelog

About
-----

This project does amazing things...

Installation
------------

.. code-block:: bash

   pip install my-awesome-project
```

### Customize Theme

Edit the colors in `docs/source/conf.py`:

```python
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#007acc",      # Your brand color
        "color-brand-content": "#005c99",     # Slightly darker
    },
}
```

### Add Custom CSS

Create `docs/source/_static/css/custom.css`:

```css
/* Your custom styles */
.wy-nav-content {
  max-width: 1200px; /* Wider content */
}

.highlight {
  border-radius: 8px; /* Rounded code blocks */
}
```

### Build Automatically

Add this to your `pyproject.toml`:

```toml
[tool.poe.tasks]
docs = "pydevelop-docs build"
docs-serve = "cd docs/build/html && python -m http.server 8000"
```

## 🎨 Features You Get

- **📖 Automatic API Docs**: All your classes and functions documented
- **🎨 Beautiful Theme**: Professional Furo theme with dark mode
- **📋 Copy Buttons**: One-click code copying
- **🔍 Full-Text Search**: Find anything instantly
- **📱 Mobile Friendly**: Looks great on all devices
- **🔗 Cross-References**: Links between docs and code
- **📊 Diagrams**: Mermaid, PlantUML support
- **🏷️ Type Hints**: Beautiful type annotation display
- **📈 SEO Optimized**: Meta tags, sitemaps, social previews
- **📝 Markdown Support**: Write docs in Markdown or reStructuredText

## 🔧 Advanced Usage

### Monorepo Setup

For projects with multiple packages:

```bash
# Initialize docs for all packages
pydevelop-docs init --packages-dir packages --packages-dir tools --include-root

# Build all packages
pydevelop-docs build

# Build specific package
pydevelop-docs build --package my-specific-package
```

### Custom Configuration

Create `.pydevelop-docs.yaml`:

```yaml
settings:
  packages_dir: [packages, tools]
  include_root: true

build:
  parallel: true
  clean_before_build: true

theme:
  dark_mode: true
  sidebar_hide_name: false
```

### CI/CD Integration

Add to `.github/workflows/docs.yml`:

```yaml
name: Documentation

on: [push, pull_request]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.12"

      - name: Install Poetry
        run: pip install poetry

      - name: Install dependencies
        run: poetry install --with docs

      - name: Build documentation
        run: poetry run pydevelop-docs build

      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/build/html
```

## 🆘 Troubleshooting

### Build Errors

If you get extension errors:

```bash
# Clean and rebuild
pydevelop-docs clean
pydevelop-docs build --clean
```

### Import Errors

Make sure your package is importable:

```bash
# From your project root
python -c "import your_package_name"
```

### Missing Dependencies

Install all documentation dependencies:

```bash
poetry install --with docs
```

## 🎯 Pro Tips

1. **Use the interactive CLI**: Just run `pydevelop-docs` for guided setup
2. **Write good docstrings**: They become your API documentation automatically
3. **Use type hints**: They make your docs much more readable
4. **Add examples in docstrings**: They show up beautifully in the docs
5. **Keep it simple**: The tools handle the complexity for you

## 📚 Learn More

- [Full Documentation](https://pydevelop-docs.readthedocs.io)
- [Extension Reference](docs/EXTENSIONS.md)
- [Customization Guide](docs/CUSTOMIZATION.md)
- [Examples Repository](https://github.com/haive-ai/pydevelop-docs-examples)

## 🚀 You're Ready!

Your documentation is now set up with professional-grade features. Focus on writing great content - the tools handle everything else.

**Happy documenting! 📚✨**
