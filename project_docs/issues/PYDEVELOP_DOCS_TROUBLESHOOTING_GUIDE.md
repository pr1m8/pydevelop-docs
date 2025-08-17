# PyDevelop-Docs Troubleshooting Guide

**Created**: 2025-08-17
**Purpose**: Fix common issues when building Haive documentation with PyDevelop-Docs
**Status**: Active Guide

## 🚨 Common Issues and Solutions

### 1. Python 3.10 Union Type Errors

**Problem**:

```
TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
```

**Cause**: sphinx-codeautolink can't handle Python 3.10's new union syntax (`str | None`)

**Solution**: PyDevelop-Docs now includes `sphinx_codeautolink_wrapper.py` that catches these errors gracefully.

**How it works**:

```python
# In config.py, we use our wrapper instead of direct extension:
extensions = [
    # ...
    "pydevelop_docs.sphinx_codeautolink_wrapper",  # Not "sphinx_codeautolink"
    # ...
]
```

**If you still get errors**:

1. Check that the wrapper is in the extensions list
2. The build will continue without code linking
3. Documentation still generates successfully

### 2. Build Takes Forever (>5 minutes)

**Problem**: Build hangs or takes extremely long time

**Common Causes**:

1. **Large codebase**: haive-mcp has many modules
2. **AutoAPI processing**: Scanning all Python files
3. **Extension conflicts**: Some extensions slow each other down

**Solutions**:

```bash
# 1. Use -E flag to force clean build
poetry run sphinx-build -b html source build -E

# 2. Disable problem extensions temporarily in conf.py:
# Comment out in get_complete_extensions():
# "sphinx_library",
# "sphinx_icontract",
# "sphinx_needs",

# 3. Build with minimal verbosity
poetry run sphinx-build -b html source build -q

# 4. Check memory usage
watch -n 1 'ps aux | grep sphinx'
```

### 3. CSS/Admonition Styling Issues

**Problem**: All admonitions (notes, warnings) appear with same blue background

**Cause**: CSS variable override forcing single color

**Fixed in**: `config.py` line 652 - removed `color-admonition-background` override

**Verify Fix**:

```python
# In config.py, make sure this line is REMOVED:
# "color-admonition-background": "#e3f2fd",  # REMOVE THIS

# Furo will now handle semantic colors properly
```

### 4. Flat API Documentation (No Hierarchy)

**Problem**: All classes listed alphabetically instead of by module

**Solution**: Set `autoapi_own_page_level = "module"` in config.py

**Verify**:

```python
# In _get_complete_autoapi_config():
"autoapi_own_page_level": "module",  # MUST be "module" not "class"
"autoapi_options": [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",  # Critical for hierarchy
]
```

### 5. Import/Path Issues

**Problem**: Can't find haive packages or PyDevelop-Docs

**Solutions**:

```bash
# 1. Always run from PyDevelop-Docs directory
cd /home/will/Projects/haive/backend/haive/tools/pydevelop-docs

# 2. Use relative paths in scripts
haive_root = Path(__file__).parent.parent.parent
packages_dir = haive_root / "packages"

# 3. Check PYTHONPATH if needed
export PYTHONPATH=/home/will/Projects/haive/backend/haive/tools/pydevelop-docs/src:$PYTHONPATH
```

### 6. Warning Overload (600+ warnings)

**Problem**: Hundreds of warnings making it hard to see real issues

**Common Warning Types**:

- Docstring indentation
- Missing module docstrings
- Duplicate object descriptions
- Invalid references

**Filter Warnings**:

```bash
# Build with filtered output
poetry run sphinx-build -b html source build 2>&1 | grep -v "WARNING: duplicate object description"

# Or suppress in conf.py
suppress_warnings = [
    "autodoc.import_object",
    "autoapi.python_import_resolution",
]
```

## 📋 Step-by-Step Build Process

### 1. Initialize PyDevelop-Docs

```bash
cd /path/to/package
poetry run pydevelop-docs init --force --yes
```

This creates:

- `docs/source/conf.py` - Main configuration
- `docs/source/index.rst` - Homepage
- `docs/source/_static/` - CSS/JS files
- `docs/source/_templates/` - Template overrides

### 2. Build Documentation

```bash
cd docs
poetry run sphinx-build -b html source build -E
```

Flags:

- `-b html` - Build HTML output
- `-E` - Don't use cached environment
- `-q` - Quiet (less output)
- `-v` - Verbose (more output)

### 3. Check Output

```bash
# Verify index.html exists
ls -la build/index.html

# Check for AutoAPI output
ls -la build/autoapi/

# Open in browser
xdg-open build/index.html
```

## 🔧 Configuration Fixes

### Essential conf.py Settings

```python
# 1. Extension order matters!
extensions = [
    "autoapi.extension",  # MUST be early
    "sphinx.ext.autodoc",
    # ...
    "sphinx_toolbox",  # BEFORE autodoc_typehints
    "sphinx_autodoc_typehints",  # AFTER sphinx_toolbox
]

# 2. AutoAPI hierarchical fix
autoapi_own_page_level = "module"  # Not "class"!

# 3. Handle problem files
autoapi_ignore = [
    "**/test_*.py",
    "**/tests/*",
    "**/conftest.py",
    # Add problem files here
]

# 4. Theme settings for Furo
html_theme_options = {
    # Remove unsupported options that cause warnings
    # Keep only Furo-specific options
}
```

### Quick Diagnostic Script

Create `diagnose.py`:

```python
#!/usr/bin/env python3
"""Quick diagnostics for PyDevelop-Docs issues."""

import subprocess
import sys
from pathlib import Path

def check_package(package_path):
    """Run diagnostics on a package."""

    print(f"🔍 Checking {package_path.name}...")

    # Check structure
    checks = {
        "Has pyproject.toml": (package_path / "pyproject.toml").exists(),
        "Has docs/": (package_path / "docs").exists(),
        "Has conf.py": (package_path / "docs/source/conf.py").exists(),
        "Has build/": (package_path / "docs/build").exists(),
    }

    for check, result in checks.items():
        print(f"  {check}: {'✅' if result else '❌'}")

    # Check conf.py for key settings
    if checks["Has conf.py"]:
        conf_path = package_path / "docs/source/conf.py"
        content = conf_path.read_text()

        print("\n  Configuration checks:")
        print(f"    Has wrapper: {'sphinx_codeautolink_wrapper' in content}")
        print(f"    Module pages: {'autoapi_own_page_level' in content}")
        print(f"    Has autoapi: {'autoapi.extension' in content}")

    # Try a quick build
    if checks["Has docs/"]:
        print("\n  🔨 Attempting quick build...")
        result = subprocess.run(
            ["poetry", "run", "sphinx-build", "-M", "help", "source", "build"],
            cwd=package_path / "docs",
            capture_output=True,
            text=True
        )
        print(f"    Build check: {'✅ OK' if result.returncode == 0 else '❌ Failed'}")

if __name__ == "__main__":
    package = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    check_package(package)
```

## 🚀 Performance Tips

### 1. Parallel Builds

```python
# In conf.py
parallel_readthedocs_build = True
parallel_build_jobs = "auto"
```

### 2. Incremental Builds

```bash
# Don't use -E flag for incremental
poetry run sphinx-build -b html source build

# Only rebuild changed files
poetry run sphinx-build -b html source build -a
```

### 3. Disable Heavy Extensions

For faster builds during development:

```python
# Create a fast_conf.py
if os.environ.get("FAST_BUILD"):
    extensions = [
        # Minimal set
        "sphinx.ext.autodoc",
        "autoapi.extension",
        "myst_parser",
    ]
```

## 🎯 Testing Your Fixes

### 1. Test Union Type Handling

```python
# Create test file with union types
def process(data: dict | None) -> str | None:
    """Test function with union types."""
    return str(data) if data else None
```

Build and check for graceful handling.

### 2. Test Admonition Colors

Create test.rst:

```rst
.. note::
   This should be blue

.. warning::
   This should be yellow/orange

.. danger::
   This should be red

.. tip::
   This should be green
```

### 3. Test API Hierarchy

Check `/autoapi/index.html` shows:

```
📦 haive.mcp
├── 📁 mcp.agents
│   └── 📄 MCPAgent
├── 📁 mcp.cli
│   └── 📄 main
└── 📁 mcp.config
    └── 📄 MCPConfig
```

Not:

```
MCPAgent
MCPConfig
main
(all flat)
```

## 🆘 When All Else Fails

1. **Clean Everything**:

   ```bash
   rm -rf docs/build docs/source/autoapi .doctrees
   poetry run pydevelop-docs init --force --yes
   ```

2. **Minimal Build**:

   ```bash
   # Create minimal conf.py for testing
   echo 'project = "Test"
   extensions = ["autoapi.extension"]
   autoapi_dirs = ["../../src"]
   html_theme = "alabaster"' > docs/source/conf_minimal.py

   poetry run sphinx-build -b html -c docs/source -C docs/source docs/build_min
   ```

3. **Check Versions**:

   ```bash
   poetry show | grep -E "(sphinx|autoapi|pydantic|furo)"
   ```

4. **Enable Debug**:
   ```python
   # In conf.py
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

## 📚 Resources

- [Sphinx Docs](https://www.sphinx-doc.org/)
- [AutoAPI Docs](https://sphinx-autoapi.readthedocs.io/)
- [Furo Theme](https://pradyunsg.me/furo/)
- [PyDevelop-Docs Source](https://github.com/yourusername/pydevelop-docs)

---

**Remember**: Most issues come from:

1. Extension conflicts (order matters!)
2. Python 3.10 syntax (use wrapper)
3. Configuration overrides (less is more)
4. Large codebases (be patient)

When in doubt, start simple and add features incrementally!
