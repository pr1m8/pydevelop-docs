# PyAutoDoc Standalone

A zero-configuration documentation generator for Python projects. Just drop it in and run!

## Features

- 🚀 **Zero Configuration** - Works out of the box with any Python project
- 🔍 **Auto-Discovery** - Finds all your Python packages automatically
- 📦 **Any Project Structure** - Supports flat, src, monorepo, and namespace packages
- 🎯 **Single File** - Just one Python file, no dependencies for basic operation
- 🌐 **Built-in Server** - View your docs locally with one command
- 📱 **Responsive** - Mobile-friendly documentation output

## Quick Start

1. **Download** `pyautodoc_standalone.py` to your project root

2. **Initialize** documentation:
   ```bash
   python pyautodoc_standalone.py init
   ```

3. **Install** Sphinx (if not already installed):
   ```bash
   pip install sphinx
   ```

4. **Build** your documentation:
   ```bash
   python pyautodoc_standalone.py build
   ```

5. **View** your documentation:
   ```bash
   python pyautodoc_standalone.py serve
   ```

That's it! Your documentation is now available at http://localhost:8000

## How It Works

PyAutoDoc automatically:

1. **Discovers** all Python packages in your project
2. **Extracts** docstrings from your code
3. **Generates** beautiful HTML documentation
4. **Creates** an API reference with all modules, classes, and functions

## Supported Project Structures

### Single Package
```
myproject/
├── mypackage/
│   ├── __init__.py
│   └── module.py
└── pyautodoc_standalone.py
```

### Src Layout
```
myproject/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
└── pyautodoc_standalone.py
```

### Monorepo
```
myproject/
├── packages/
│   ├── package1/
│   │   └── __init__.py
│   └── package2/
│       └── __init__.py
└── pyautodoc_standalone.py
```

### Namespace Packages
```
myproject/
├── mycompany/
│   ├── package1/
│   │   └── __init__.py
│   └── package2/
│       └── __init__.py
└── pyautodoc_standalone.py
```

## Commands

### init
Initialize documentation structure:
```bash
python pyautodoc_standalone.py init [--force]
```
- `--force`: Overwrite existing documentation

### build
Build documentation:
```bash
python pyautodoc_standalone.py build [--builder BUILDER]
```
- `--builder`: Sphinx builder to use (default: html)

### serve
Serve documentation locally:
```bash
python pyautodoc_standalone.py serve [--port PORT]
```
- `--port`: Port to serve on (default: 8000)

### clean
Clean build artifacts:
```bash
python pyautodoc_standalone.py clean
```

## Writing Documentation

PyAutoDoc uses your Python docstrings to generate documentation. Write clear docstrings using Google or NumPy style:

```python
def process_data(data: dict, validate: bool = True) -> dict:
    """Process input data with optional validation.
    
    Args:
        data: Input data dictionary
        validate: Whether to validate input (default: True)
        
    Returns:
        Processed data dictionary
        
    Raises:
        ValueError: If validation fails
        
    Example:
        >>> result = process_data({'name': 'test'})
        >>> print(result)
        {'name': 'TEST', 'processed': True}
    """
```

## Customization

After running `init`, you can customize:

- `docs/conf.py` - Sphinx configuration
- `docs/index.rst` - Main documentation page
- `docs/modules.rst` - API reference structure

## Optional Enhancements

For better documentation, install:

```bash
# Better theme
pip install sphinx-rtd-theme

# Markdown support
pip install myst-parser

# Type hints in docs
pip install sphinx-autodoc-typehints

# Copy button for code blocks
pip install sphinx-copybutton
```

## Tips

1. **Use Type Hints** - They appear in the documentation
2. **Write Examples** - Include code examples in docstrings
3. **Document Modules** - Add module-level docstrings
4. **Cross-Reference** - Use `:class:`, `:func:`, `:mod:` for links

## Troubleshooting

### No packages found
- Ensure your packages have `__init__.py` files
- Check that you're running from the project root

### Import errors during build
- Make sure your package is importable
- Install your package in development mode: `pip install -e .`

### Sphinx not found
- Install Sphinx: `pip install sphinx`

## License

This tool is released into the public domain. Use it however you like!

## One-Liner Installation

Copy and paste this to download and set up PyAutoDoc:

```bash
curl -O https://raw.githubusercontent.com/yourusername/pyautodoc/main/standalone/pyautodoc_standalone.py && python pyautodoc_standalone.py init
```

Or with wget:

```bash
wget https://raw.githubusercontent.com/yourusername/pyautodoc/main/standalone/pyautodoc_standalone.py && python pyautodoc_standalone.py init
```