# Union Type Error Fix Guide - Pydvlppy

**Created**: 2025-08-15
**Status**: Active Implementation
**Issue**: Python 3.10 union type syntax breaking documentation builds

## 🚨 Problem Summary

The new Python 3.10 union type syntax (`str | None`) is causing TypeError in sphinx_codeautolink when building documentation for haive-core and haive-agents packages.

## ✅ Verified Solutions

### Solution 1: Update Dependencies (RECOMMENDED)

Based on our research, the issue is primarily with version compatibility:

```bash
# Check current versions
poetry show sphinx
poetry show sphinx-codeautolink

# Update to compatible versions
poetry add --group docs "sphinx>=5.3"
poetry add --group docs "sphinx-codeautolink>=0.15.0"
```

**Key Requirements**:

- Sphinx >= 5.3 (has union type operator support)
- sphinx-codeautolink >= 0.15.0 (Python 3.10 support)
- Run Sphinx under Python 3.10 itself

### Solution 2: Disable sphinx_codeautolink (QUICK FIX)

If updating doesn't work, temporarily disable the extension:

```python
# In pydevelop_docs/config.py, comment out:
# "sphinx_codeautolink",

# Or conditionally disable for problematic packages:
if package_name in ["haive-core", "haive-agents"]:
    extensions.remove("sphinx_codeautolink")
```

### Solution 3: Add Future Annotations Import

For packages using union syntax but running on older Python:

```python
# Add to the top of affected Python files:
from __future__ import annotations
```

This defers annotation evaluation and can prevent runtime TypeErrors.

### Solution 4: Configure sphinx_codeautolink to Skip Problematic Patterns

Add to config:

```python
# Skip files with known union type issues
codeautolink_custom_blocks = {
    "skip_pattern": r"\w+\s*\|\s*None",
}

# Or exclude specific directories
codeautolink_exclude = [
    "*/engine/agent/*",
    "*/core/engine/*"
]
```

### Solution 5: Convert Union Syntax (LAST RESORT)

If all else fails, create a pre-processor to convert syntax:

```python
# convert_unions.py
import re
from pathlib import Path

def convert_union_to_typing(content: str) -> str:
    """Convert X | Y syntax to Union[X, Y]."""
    # Simple pattern for | None
    content = re.sub(r'(\w+)\s*\|\s*None', r'Optional[\1]', content)

    # Pattern for X | Y
    content = re.sub(r'(\w+)\s*\|\s*(\w+)', r'Union[\1, \2]', content)

    # Add imports if needed
    if 'Union[' in content or 'Optional[' in content:
        if 'from typing import' not in content:
            content = 'from typing import Union, Optional\n' + content

    return content

# Run before build
for py_file in Path("src").rglob("*.py"):
    original = py_file.read_text()
    converted = convert_union_to_typing(original)
    if original != converted:
        py_file.write_text(converted)
```

## 🔧 Implementation Steps

### Step 1: Check Python Version

```bash
poetry run python --version
# Should be Python 3.10 or higher
```

### Step 2: Update Dependencies

```bash
# Update pyproject.toml
poetry add --group docs "sphinx>=5.3" "sphinx-codeautolink>=0.15.0"
poetry install --with docs
```

### Step 3: Test Build with Updated Dependencies

```bash
# Test haive-core first
cd /home/will/Projects/haive/backend/haive/packages/haive-core
poetry run sphinx-build -b html docs/source docs/build

# Check for union type errors
grep -i "unsupported operand" docs/build/*.log
```

### Step 4: If Still Failing, Apply Quick Fix

```python
# In src/pydevelop_docs/config.py, around line 487:
# Conditionally remove sphinx_codeautolink for problem packages
problem_packages = ["haive-core", "haive-agents"]
if any(pkg in str(package_path) for pkg in problem_packages):
    if "sphinx_codeautolink" in extensions:
        extensions.remove("sphinx_codeautolink")
        print(f"⚠️  Disabled sphinx_codeautolink for {package_name} due to union type issues")
```

## 📊 Testing Strategy

### Create Test File

```python
# test_union_types.py
"""Test various union type syntaxes."""
from typing import Union, Optional
from __future__ import annotations

class TestUnions:
    # Modern syntax
    modern_simple: str | None = None
    modern_multi: int | str | float = 0

    # Legacy syntax
    legacy_simple: Optional[str] = None
    legacy_multi: Union[int, str, float] = 0

    def modern_method(self, data: dict | list) -> str | None:
        """Method with modern union types."""
        return "test"

    def legacy_method(self, data: Union[dict, list]) -> Optional[str]:
        """Method with legacy union types."""
        return "test"
```

### Run Test Build

```bash
# Create test project
mkdir -p test-union-types
cd test-union-types
echo "from test_union_types import TestUnions" > __init__.py

# Initialize docs
poetry run pydvlppy init

# Build and check for errors
poetry run pydvlppy build 2>&1 | grep -i "unsupported"
```

## 🎯 Expected Outcomes

1. **Best Case**: Updated dependencies resolve all union type errors
2. **Acceptable**: sphinx_codeautolink disabled but docs build successfully
3. **Fallback**: Union syntax converted to legacy format

## 🚨 Known Limitations

1. **autodoc_type_aliases**: Won't work with union operator in Sphinx < 5.3
2. **Cross-references**: May be lost if sphinx_codeautolink is disabled
3. **Forward references**: `int | "Foo"` requires string annotation: `"int | Foo"`

## 📈 Verification Commands

```bash
# Verify Sphinx version supports union types
poetry run python -c "import sphinx; print(f'Sphinx {sphinx.__version__}')"

# Verify Python version
poetry run python -c "import sys; print(f'Python {sys.version}')"

# Test union type support
poetry run python -c "
def test(x: str | None) -> int | str:
    return 1
print('Union types supported!')
"

# Check if sphinx_codeautolink is the issue
poetry run python -c "
import sphinx_codeautolink
print(f'sphinx_codeautolink version: {sphinx_codeautolink.__version__}')
"
```

## 🔗 References

- [PEP 604 - Union Operators](https://www.python.org/dev/peps/pep-0604/)
- [Sphinx Issue #9562](https://github.com/sphinx-doc/sphinx/issues/9562)
- [Sphinx Issue #8775](https://github.com/sphinx-doc/sphinx/issues/8775)
- [sphinx-codeautolink Release Notes](https://sphinx-codeautolink.readthedocs.io/en/latest/release_notes.html)

---

**Next Steps**:

1. Check current Sphinx version
2. Update dependencies if needed
3. Test build with updated versions
4. Apply conditional disabling if necessary
