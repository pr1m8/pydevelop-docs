# Haive Documentation Tools

Universal documentation initialization and management tool for Python projects.

## Features

- **Universal**: Works with any Python project (single package or monorepo)
- **Complete**: Includes all 43+ Sphinx extensions from PyAutoDoc
- **Smart**: Auto-detects project structure and package manager
- **Ready-to-use**: Generates fully configured documentation

## Installation

```bash
# Install in development mode
pip install -e .

# Or with Poetry
poetry install
```

## Usage

### Initialize Documentation

Run this in any Python project root:

```bash
haive-docs init
```

This will:

1. Analyze your project structure
2. Create `docs/` directory with Sphinx configuration
3. Add all 43+ extensions from PyAutoDoc
4. Generate build scripts and Makefile
5. Add documentation dependencies (if using Poetry)

### Force Overwrite

If documentation already exists:

```bash
haive-docs init --force
```

### List Available Extensions

See all configured Sphinx extensions:

```bash
haive-docs list-extensions
```

## What Gets Created

```
your-project/
├── docs/
│   ├── source/
│   │   ├── conf.py          # Full 600+ line Sphinx config
│   │   ├── index.rst        # Main documentation page
│   │   ├── _static/         # CSS, JS, images
│   │   ├── _templates/      # Custom templates
│   │   ├── api/            # API documentation
│   │   ├── guides/         # User guides
│   │   └── examples/       # Code examples
│   ├── build/              # Generated documentation
│   └── Makefile            # Build commands
└── scripts/
    └── build-docs.sh       # Build script
```

## Project Types Supported

- **Single Package**: Standard Python packages
- **Monorepo**: Multiple packages in one repository
- **Src Layout**: Projects with `src/` directory
- **Flat Layout**: Direct package structure

## Package Managers Supported

- **Poetry**: Full integration with pyproject.toml
- **Setuptools**: Standard setup.py projects
- **Pip**: Requirements.txt based projects
- **PEP 621**: Modern pyproject.toml projects

## Building Documentation

After initialization:

```bash
# With Poetry
cd docs && poetry run make html

# Without Poetry
cd docs && make html

# View documentation
open docs/build/html/index.html
```

## Included Extensions

The tool configures 43+ Sphinx extensions including:

- **Core**: autodoc, autosummary, napoleon, viewcode
- **API**: autoapi, autodoc-typehints, autodoc-pydantic
- **Enhanced**: myst-parser, copybutton, togglebutton, design
- **Diagrams**: mermaid, plantuml, blockdiag, seqdiag
- **Code**: codeautolink, exec-code, runpython
- **UI**: tippy, favicon, emoji, tabs, inline-tabs
- **Utils**: sitemap, last-updated-by-git, opengraph
- **Special**: enum-tools, sphinx-toolbox, intersphinx

## Configuration

The generated `conf.py` includes:

- Full AutoAPI configuration
- Napoleon docstring support (Google & NumPy)
- MyST Markdown extensions
- Intersphinx mappings
- Furo theme with dark mode
- Custom CSS and JavaScript
- Automatic API documentation
- Pydantic model support
- Enum documentation
- Type hint support

## Development

This tool is part of the Haive AI Agent Framework and inherits the complete documentation system from PyAutoDoc.

## License

MIT License - see LICENSE file for details.
