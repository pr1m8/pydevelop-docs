# Building pydvlp-docs Documentation

This directory contains the documentation source for pydvlp-docs itself.

## 🚀 Quick Build

```bash
# From the docs directory
make html
```

## 📦 Prerequisites

### System Dependencies (Ubuntu/Debian)

```bash
# Install all system dependencies
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    python3-dev \
    graphviz \
    graphviz-dev \
    libgraphviz-dev \
    pkg-config \
    default-jre \
    plantuml \
    imagemagick \
    librsvg2-bin \
    pandoc \
    git
```

### Python Dependencies

```bash
# Install documentation requirements
pip install -r requirements.txt

# Or install pydvlp-docs with docs extras
pip install -e ..[docs]
```

## 🔨 Building Documentation

### Method 1: Using Make (Recommended)

```bash
# Clean previous builds
make clean

# Build HTML documentation
make html

# Build other formats
make latexpdf  # PDF output
make epub      # EPUB output
make linkcheck # Check all external links
```

### Method 2: Using Sphinx Directly

```bash
# Build HTML
sphinx-build -b html source build/html

# With auto-reload for development
sphinx-autobuild source build/html
```

### Method 3: Using the Build Script

```bash
# This installs all dependencies and builds
./build-with-deps.sh
```

## 📝 Configuration

The documentation uses:
- **Theme**: Furo (with dark mode)
- **Extensions**: 40+ Sphinx extensions
- **API Docs**: AutoAPI with hierarchical organization
- **Diagrams**: Mermaid, PlantUML, Graphviz

Configuration is in `source/conf.py` which imports from `pydvlp_docs.config`.

## 🌐 Viewing Documentation

After building:

```bash
# Start local server
python -m http.server 8000 --directory build/html

# Open in browser
open http://localhost:8000
```

## 🐛 Troubleshooting

### Import Errors

If you get import errors for `pydvlp_docs`:

```bash
# Install in development mode from parent directory
cd ..
pip install -e .
```

### Missing pygraphviz

If pygraphviz fails to install:

```bash
# Ubuntu/Debian
sudo apt-get install graphviz graphviz-dev

# macOS
brew install graphviz
pip install --global-option=build_ext \
    --global-option="-I$(brew --prefix graphviz)/include/" \
    --global-option="-L$(brew --prefix graphviz)/lib/" \
    pygraphviz
```

### PlantUML Not Found

```bash
# Ubuntu/Debian
sudo apt-get install default-jre plantuml

# macOS
brew install plantuml
```

## 📚 Documentation Structure

```
docs/
├── source/
│   ├── conf.py           # Sphinx configuration
│   ├── index.rst         # Main documentation index
│   ├── _static/          # CSS/JS assets
│   ├── _templates/       # Custom templates
│   └── guides/           # User guides
├── build/                # Generated output
├── requirements.txt      # Python dependencies
├── apt-requirements.txt  # System dependencies
└── Makefile             # Build commands
```

## 🚀 For Read the Docs

When importing to Read the Docs:
1. The `.readthedocs.yaml` in the root handles configuration
2. System dependencies are installed via `apt_packages`
3. Python dependencies from `docs/requirements.txt`
4. The build will use `docs/source/conf.py`

---

**Note**: This documentation showcases pydvlp-docs eating its own dog food - we use pydvlp-docs to document pydvlp-docs!