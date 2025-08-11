# PyAutoDoc

A powerful, extensible documentation system for Python monorepos, built on Sphinx with advanced features for automatic API documentation, cross-package linking, and beautiful theming.

## Features

- 🚀 **Automatic API Documentation** - Extracts docstrings and generates comprehensive API docs
- 📦 **Monorepo Support** - Build documentation for multiple packages with cross-references
- 🎨 **Beautiful Themes** - Customizable themes with package-specific branding
- 🔗 **Cross-Package Linking** - Automatic intersphinx references between packages
- ⚡ **Parallel Building** - Build multiple packages concurrently for speed
- 🛡️ **Security First** - Built-in rate limiting, input validation, and safe operations
- 📊 **Rich Extensions** - 70+ Sphinx extensions pre-configured
- 📄 **Multiple Formats** - Generate HTML, PDF, ePub, and more
- 🔮 **Auto Dependency Links** - Automatic documentation links for all dependencies via seed-intersphinx-mapping

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/pyautodoc.git
cd pyautodoc

# Install dependencies with Poetry
poetry install --with docs

# Or with pip
pip install -r requirements.txt

# Build all documentation
python scripts/build-monorepo-docs.py

# View the documentation
open _build/html/index.html
```

## Documentation

- 📖 [User Guide](docs/user-guide.md) - Getting started and basic usage
- 🔧 [Developer Guide](docs/developer-guide.md) - Architecture and extending PyAutoDoc
- 🌐 [API Endpoints Guide](docs/api-endpoints-guide.md) - Using the secure API endpoints
- 🔮 [Seed Intersphinx Guide](docs/seed-intersphinx-guide.md) - Automatic dependency documentation linking

## Project Structure

```
pyautodoc/
├── docs/                    # Documentation
│   ├── source/             # Main Sphinx source files
│   ├── config/             # YAML configuration system
│   └── *.md               # User guides
├── packages/               # Example packages
│   ├── haive-core/        # Core package
│   ├── haive-ml/          # ML package
│   └── haive-api/         # API package
├── shared-docs-config/     # Shared Sphinx configuration
│   ├── shared_config.py   # Main config
│   └── shared_config_simple.py # Simplified config
├── scripts/               # Build scripts
│   └── build-monorepo-docs.py # Main build script
└── src/                   # Example source code
```

## How It Works

PyAutoDoc provides a sophisticated documentation system for Python monorepos:

1. **Shared Configuration**: Common Sphinx settings across all packages
2. **Package Discovery**: Automatically finds and documents all packages
3. **Dependency Resolution**: Builds packages in the correct order
4. **Cross-References**: Automatic linking between packages
5. **Parallel Builds**: Fast documentation generation

## Configuration

Each package needs a `docs/conf.py` file:

```python
import sys
from pathlib import Path

# Add shared config to path
sys.path.insert(0, str(Path(__file__).parents[2] / "shared-docs-config"))

# Import shared configuration
from shared_config_simple import get_base_config

# Get base configuration
config = get_base_config(
    package_name="haive-core",
    package_path=str(Path(__file__).parents[1] / "src"),
    is_root=False
)

# Apply configuration
globals().update(config)

# Package-specific customizations
extensions.append('autoapi.extension')
autoapi_dirs = [str(Path(__file__).parents[1] / "src")]
```

## Building Documentation

### Build All Packages

```bash
python scripts/build-monorepo-docs.py
```

### Build Specific Package

```bash
python scripts/build-monorepo-docs.py --package haive-core
```

### Build Options

```bash
# Clean build
python scripts/build-monorepo-docs.py --clean

# Sequential build (no parallelization)
python scripts/build-monorepo-docs.py --no-parallel

# Custom worker count
python scripts/build-monorepo-docs.py -j 8
```

## Adding New Packages

1. Create package structure:

```
packages/new-package/
├── src/
│   └── new_package/
│       └── __init__.py
├── docs/
│   └── conf.py
└── pyproject.toml
```

2. Configure documentation in `docs/conf.py` (see Configuration section)

3. Build documentation:

```bash
python scripts/build-monorepo-docs.py --package new-package
```

## Advanced Features

### Custom Themes

Each package can have its own color scheme:

```python
# In shared_config.py
PACKAGE_THEMES = {
    'haive-core': PackageColors('#dc3545', '#c82333'),
    'haive-ml': PackageColors('#28a745', '#218838'),
    'haive-api': PackageColors('#007bff', '#0056b3'),
}
```

### Extension Management

Over 70 Sphinx extensions are pre-configured, including:

- AutoAPI for automatic API documentation
- Pydantic for model documentation
- MyST for Markdown support
- And many more...

## Requirements

- Python 3.8+
- Poetry or pip
- Sphinx and extensions (installed automatically)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:

- [Sphinx](https://www.sphinx-doc.org/) - Documentation generator
- [sphinx-autoapi](https://github.com/readthedocs/sphinx-autoapi) - Automatic API documentation
- [seed-intersphinx-mapping](https://github.com/sphinx-contrib/seed-intersphinx-mapping) - Automatic dependency linking
- [Furo](https://github.com/pradyunsg/furo) - Beautiful documentation theme
- Many other amazing Sphinx extensions
