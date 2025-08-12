# PyDevelop Documentation Tools

Universal Python documentation generator with full PyAutoDoc configuration (43+ Sphinx extensions).

## Features

- 🚀 **Quick Start**: Interactive CLI - just run `pydevelop-docs`
- 📦 **Universal**: Works with any Python project structure
- 🏗️ **Monorepo Support**: Document multiple packages at once
- 🎨 **Beautiful Themes**: Pre-configured with Furo and dark mode
- 🔧 **Zero Config**: Smart auto-detection of project structure
- 📚 **43+ Extensions**: Full PyAutoDoc configuration included

## Installation

```bash
pip install pydevelop-docs

# Or with Poetry
poetry add --group dev pydevelop-docs
```

## Quick Start

### Interactive Mode (Recommended)

```bash
pydevelop-docs
```

This launches an interactive CLI that guides you through:

- Project analysis
- Documentation initialization
- Dependency management
- Building documentation

### Command Line

#### Single Package

```bash
# Initialize docs for current package
pydevelop-docs init --include-root

# Build documentation
pydevelop-docs build
```

#### Monorepo

```bash
# Initialize docs for all packages
pydevelop-docs init --packages-dir packages --packages-dir tools --include-root

# Build all packages
pydevelop-docs build

# Build specific package
pydevelop-docs build --package haive-core
```

## Commands

### `pydevelop-docs init`

Initialize documentation structure.

```bash
# Options
--packages-dir, -d    # Directories to scan for packages
--include-root, -r    # Include root-level documentation
--packages, -p        # Specific packages to initialize
--dry-run, -n        # Preview changes without making them
--force, -f          # Overwrite existing documentation
```

### `pydevelop-docs build`

Build documentation.

```bash
# Options
--clean, -c          # Clean before building
--package, -p        # Build specific package
--no-parallel        # Disable parallel building
--config, -f         # Use custom config file
```

### `pydevelop-docs clean`

Remove all build artifacts.

### `pydevelop-docs sync`

Sync documentation between packages.

```bash
pydevelop-docs sync source-package target-package
```

## Configuration

Create `.pydevelop-docs.yaml` in your project root:

```yaml
settings:
  packages_dir:
    - packages
    - tools
  include_root: true

build:
  central_hub: true
  parallel: true

paths:
  docs_folder: "docs"
  source_folder: "source"
```

## Project Structures Supported

### Single Package

```
my-package/
├── src/
│   └── my_package/
├── tests/
├── docs/           # Created by pydevelop-docs
└── pyproject.toml
```

### Monorepo

```
my-monorepo/
├── packages/
│   ├── package-a/
│   │   └── docs/   # Created by pydevelop-docs
│   └── package-b/
│       └── docs/   # Created by pydevelop-docs
├── tools/
└── docs/           # Central hub (optional)
```

## What Gets Created

```
docs/
├── source/
│   ├── conf.py         # Full Sphinx configuration
│   ├── index.rst       # Main documentation page
│   ├── _static/        # CSS, JS, images
│   └── _templates/     # Custom templates
├── build/              # Generated documentation
└── Makefile            # Build commands
```

## Included Extensions

All 43+ PyAutoDoc extensions are pre-configured:

- **Core**: autodoc, autosummary, napoleon, viewcode, intersphinx
- **API**: sphinx-autoapi, autodoc-typehints, autodoc-pydantic
- **Enhancements**: myst-parser, copybutton, togglebutton, design
- **Diagrams**: mermaid, plantuml, blockdiag, seqdiag
- **Features**: codeautolink, exec-code, tippy, favicon, emoji
- **And many more...**

## Building Documentation

After initialization:

```bash
# Using Make
cd docs && make html

# Using Poetry
cd docs && poetry run make html

# Using pydevelop-docs
pydevelop-docs build
```

## Examples

See the `scripts/` directory for example workflows:

- `example-single.sh` - Single package workflow
- `example-monorepo.sh` - Monorepo workflow

## Development

```bash
# Clone repository
git clone https://github.com/haive/pydevelop-docs
cd pydevelop-docs

# Install in development mode
poetry install

# Run tests
poetry run pytest
```

## License

MIT License - see LICENSE file for details.
