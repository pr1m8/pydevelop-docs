# Common Fixes - Quick Reference

**Purpose**: Quick lookup for common documentation build issues

## Import Errors

### Fix: Module Not Found

```python
# In conf.py - Add to sys.path
sys.path.insert(0, str(Path("../../packages/haive-core/src")))
sys.path.insert(0, str(Path("../../packages/haive-agents/src")))
```

### Fix: Circular Import

```python
# In the module causing issues
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from haive.core import Engine  # Only imported for type checking
```

### Fix: Missing **init**.py

```bash
# Check all namespace packages have __init__.py
find packages -name "haive" -type d ! -exec test -e {}/__init__.py \; -print
```

## AutoAPI Issues

### Fix: Too Many Files

```python
autoapi_ignore = [
    "**/test*",
    "**/tests/**",
    "**/examples/**",
    "**/supervisor/**",  # If too many variants
    "**/*_test.py",
    "**/demo*.py",
]
```

### Fix: Wrong Module Paths

```python
# Ensure src in path BEFORE autoapi_dirs
for package in packages:
    sys.path.insert(0, f"{package}/src")

# Enable namespace support
autoapi_python_use_implicit_namespaces = True
```

### Fix: Duplicate Objects

```python
# In __init__.py files, be explicit
from .module import SpecificClass
__all__ = ["SpecificClass"]  # Don't use wildcards
```

## CSS/Layout Issues

### Fix: Sidebar Too Wide

```css
/* In custom CSS */
:root {
  --sidebar-width: 19rem; /* Not 30.5rem */
}

/* Remove any hardcoded widths */
```

### Fix: Content Pushed Right

```css
/* Remove these */
.content {
  margin-left: 320px !important; /* DELETE */
}

/* Use relative positioning */
.content {
  margin-left: calc(var(--sidebar-width) + 2rem);
}
```

### Fix: Code Blocks Narrow

```css
.highlight pre {
  overflow-x: auto;
  max-width: 100%; /* Use available width */
  white-space: pre;
}
```

## Extension Errors

### Fix: Extension Has No Setup

```python
# Check if extension is installed
# Remove from conf.py if not needed
extensions = [
    # "sphinx_tabs",  # Remove if not installed
    "myst_parser",
    "autoapi.extension",
]
```

### Fix: Unknown Event

```python
# In setup() function
def setup(app):
    if "autoapi.extension" in app.config.extensions:
        app.connect("autoapi-skip-member", skip_handler)
```

## Build Performance

### Fix: Slow Builds

```python
# Enable caching
autoapi_keep_files = True

# Parallel building
# Command line: sphinx-build -j auto

# Reduce file processing
autoapi_ignore = ["**/test*", "**/example*"]
```

### Fix: Memory Issues

```python
# Process packages separately
# First build: just haive-core
# Second build: add haive-agents
# etc.
```

## File Encoding Issues

### Fix: Unicode Errors

```python
# Add to exclude_patterns
exclude_patterns = [
    "**/*.ipynb",  # Notebooks often have encoding issues
    "**/*.json",
    "**/test_data/**",
]
```

## Missing References

### Fix: Intersphinx

```python
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    # Add other projects
}
```

### Fix: Nitpicky Mode

```python
# Disable during development
nitpicky = False

# Or ignore specific references
nitpick_ignore = [
    ("py:class", "SomeExternalClass"),
]
```

## Quick Debug Commands

### Check Imports Work

```bash
python -c "import sys; sys.path.insert(0, 'packages/haive-core/src'); from haive.core import *; print('✅ Success')"
```

### Find Problem Files

```bash
# Files with most errors (estimate)
grep -l "test_" packages/haive-agents/src/haive/agents/**/*.py | wc -l
```

### Test Minimal Build

```bash
# Backup current conf
cp docs/source/conf.py docs/source/conf_backup.py

# Use minimal conf
cp docs/source/conf_minimal.py docs/source/conf.py

# Test build
sphinx-build -b html docs/source docs/build/html
```

### Clean Build

```bash
# Full clean
rm -rf docs/build
rm -rf docs/source/api  # If using autoapi_keep_files

# Clean sphinx cache
rm -rf docs/source/_build
```

## Emergency Fixes

### When Nothing Works

1. Start with minimal conf.py
2. Disable all extensions except myst_parser
3. Remove all custom CSS
4. Build with just index.rst
5. Add complexity incrementally

### Rollback Strategy

```bash
# Always backup before changes
cp docs/source/conf.py "docs/source/conf_$(date +%Y%m%d_%H%M%S).py"

# Restore last working
git checkout HEAD -- docs/source/conf.py
```

### Nuclear Option

```bash
# Complete reset
git clean -fdx docs/
git checkout HEAD -- docs/
# Reinstall dependencies
pip install -r docs/requirements.txt
```
