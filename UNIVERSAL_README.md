# PyAutoDoc - Universal Python Documentation Generator

Drop it in any Python project and get beautiful documentation instantly! No configuration needed.

## 🚀 Quick Start (30 seconds)

```bash
# Download and run
curl -O https://raw.githubusercontent.com/yourusername/pyautodoc/main/pyautodoc_simple.py
python pyautodoc_simple.py

# That's it! Your docs are building...
```

## 🎯 Features

- **Zero Configuration** - Just works with any Python project
- **Auto-Discovery** - Finds all your packages automatically
- **Universal** - Works with any project structure
- **Single File** - One Python file, no dependencies for basic use
- **Instant Results** - See your docs in seconds

## 📦 What You Get

PyAutoDoc automatically creates:
- Complete API documentation
- Class and function references  
- Module hierarchy
- Searchable index
- Mobile-friendly HTML

## 🔧 How It Works

1. **Discovers** all Python packages (looks for `__init__.py`)
2. **Extracts** docstrings from your code
3. **Generates** Sphinx documentation
4. **Builds** beautiful HTML output

## 📁 Works With Any Structure

### Simple Package
```
myproject/
├── mypackage/
│   ├── __init__.py
│   └── core.py
└── pyautodoc_simple.py
```

### Src Layout
```
myproject/
├── src/
│   └── mypackage/
│       └── __init__.py
└── pyautodoc_simple.py
```

### Multiple Packages
```
myproject/
├── package1/
│   └── __init__.py
├── package2/
│   └── __init__.py
└── pyautodoc_simple.py
```

### Monorepo
```
myproject/
├── packages/
│   ├── service1/
│   │   └── __init__.py
│   └── service2/
│       └── __init__.py
└── pyautodoc_simple.py
```

## 📝 Commands

Run without arguments for automatic setup and build:
```bash
python pyautodoc_simple.py
```

Or use specific commands:
```bash
python pyautodoc_simple.py setup    # Create docs structure
python pyautodoc_simple.py build    # Build HTML docs
python pyautodoc_simple.py serve    # View at localhost:8000
python pyautodoc_simple.py clean    # Remove docs
```

## 💡 Writing Good Documentation

PyAutoDoc uses your docstrings. Write them like this:

```python
def calculate_total(items: List[float], tax_rate: float = 0.1) -> float:
    """Calculate total with tax.
    
    Args:
        items: List of item prices
        tax_rate: Tax rate to apply (default: 0.1)
        
    Returns:
        Total amount including tax
        
    Example:
        >>> calculate_total([10.0, 20.0], 0.08)
        32.4
    """
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

## 🚀 One-Liner Install

Copy and paste to download and set up:

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/pyautodoc/main/install.py | python3
```

## 📋 Requirements

- Python 3.6+
- Sphinx (installed automatically if missing)

## 🎨 Customization

After running, customize:
- `docs/conf.py` - Sphinx settings
- `docs/index.rst` - Main page
- `docs/*.rst` - Package pages

## 🔍 Troubleshooting

### No packages found?
- Make sure packages have `__init__.py`
- Run from project root

### Import errors?
- Install your package: `pip install -e .`
- Or add to PYTHONPATH

### Want a better theme?
```bash
pip install sphinx-rtd-theme
# Then change html_theme in docs/conf.py
```

## 🌟 Pro Tips

1. **Type Hints** - They show up in docs!
2. **Examples** - Add code examples to docstrings
3. **Module Docs** - Put docstrings at top of files
4. **Cross-refs** - Use `:class:`, `:func:` for links

## 📦 Portable Version

The `pyautodoc_simple.py` file is completely self-contained. You can:
- Email it to colleagues
- Add it to your project
- Put it in your dotfiles
- Share it anywhere

No installation, no dependencies, just Python!

## 🤝 Contributing

This is open source! Feel free to:
- Report issues
- Suggest features
- Submit pull requests
- Fork and customize

## 📄 License

Public domain - use however you like!

---

**Made with ❤️ for Python developers who want docs without the hassle**