# PyAutoDoc

A powerful, extensible documentation system for Python projects and monorepos, built on Sphinx with advanced features for automatic API documentation, cross-package linking, and beautiful theming.

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

# Install dependencies
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
├── pyautodoc_simple.py     # ⭐ Main tool - drop in any project!
├── install.py              # One-line installer
├── docs/                   # Documentation
├── standalone/             # Standalone versions
├── scripts/               # Utility scripts
└── shared-docs-config/    # Advanced configuration
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed structure.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or poetry
- Git

### From Source

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### With Poetry

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

## Usage

### Build All Documentation

```bash
# Parallel build (default)
python scripts/build-monorepo-docs.py

# Clean build
python scripts/build-monorepo-docs.py --clean

# Sequential build
python scripts/build-monorepo-docs.py --no-parallel
```

### Build Specific Package

```bash
# Build single package
python scripts/build-monorepo-docs.py --package haive-core

# Build multiple packages
python scripts/build-monorepo-docs.py -p haive-core -p haive-ml
```

### Advanced Options

```bash
# Custom worker count
python scripts/build-monorepo-docs.py -j 8

# Skip root documentation
python scripts/build-monorepo-docs.py --no-root

# Help
python scripts/build-monorepo-docs.py --help
```

## Adding New Packages

1. Create package structure:
```bash
mkdir -p packages/my-package/{src,docs,tests}
```

2. Add documentation configuration:
```python
# packages/my-package/docs/conf.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "shared-docs-config"))
from shared_config_simple import get_base_config

config = get_base_config(
    package_name="my-package",
    package_path=str(Path(__file__).parents[1] / "src"),
    is_root=False
)

globals().update(config)
```

3. Build documentation:
```bash
python scripts/build-monorepo-docs.py --package my-package
```

## Key Features Explained

### Automatic Dependency Documentation Links

Thanks to `seed-intersphinx-mapping`, PyAutoDoc automatically creates documentation links for all your dependencies:

- No manual configuration needed
- Reads from `pyproject.toml`
- Works with Poetry, setuptools, and more
- Supports 100+ popular packages

Example:
```python
# In your code
import numpy as np
import pandas as pd

# In your docs, these links work automatically:
# :py:func:`numpy.array`
# :py:class:`pandas.DataFrame`
```

### Security Features

#### API Endpoints

- **Rate Limiting** - Configurable request limits per time window
- **Input Validation** - Size limits and type checking  
- **Thread Safety** - Lock-based protection for concurrent requests
- **Error Sanitization** - Safe error messages for clients

#### Build System

- **Path Validation** - Secure file operations
- **Context Managers** - Safe directory changes
- **Error Recovery** - Graceful handling of build failures

## Configuration

### Shared Configuration

The shared configuration system provides:
- Consistent settings across packages
- Theme customization
- Extension management
- Cross-package linking
- Automatic dependency mapping

### Package-Specific Settings

Each package can override:
- Theme colors
- Additional extensions
- Custom templates
- Build options

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/pyautodoc.git
cd pyautodoc

# Install in development mode
pip install -e .

# Run tests
pytest tests/

# Run linters
flake8 src/
mypy src/
```

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```python
   # In conf.py, ensure src path is added
   sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
   ```

2. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Build Failures**
   ```bash
   # Clean and rebuild
   python scripts/build-monorepo-docs.py --clean
   ```

4. **Missing Intersphinx Links**
   ```bash
   # Check if seed-intersphinx-mapping is working
   python scripts/test-intersphinx-seed.py
   ```

### Debug Mode

```bash
# Enable debug output
export PYAUTODOC_DEBUG=1
python scripts/build-monorepo-docs.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- [Sphinx](https://www.sphinx-doc.org/) - Documentation generator
- [sphinx-autoapi](https://github.com/readthedocs/sphinx-autoapi) - Automatic API documentation
- [seed-intersphinx-mapping](https://github.com/sphinx-contrib/seed-intersphinx-mapping) - Automatic dependency linking
- [Furo](https://github.com/pradyunsg/furo) - Beautiful documentation theme
- Many other amazing Sphinx extensions

## Support

- 📧 Email: support@pyautodoc.example.com
- 💬 Discord: [Join our community](https://discord.gg/pyautodoc)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/pyautodoc/issues)