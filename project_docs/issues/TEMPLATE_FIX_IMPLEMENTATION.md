# PyDevelop-Docs Template Fix Implementation

**Date**: 2025-01-15
**Purpose**: Fix template distribution and AutoAPI formatting issues
**Status**: Ready for implementation

## 🎯 Root Cause Confirmed

The `_autoapi_templates` directory exists in pydvlp-docs but is NEVER copied to projects during initialization. This causes AutoAPI to reference non-existent templates, breaking the documentation generation.

## 🔧 The Fix

### 1. Update `_copy_static_files` Method

**File**: `/src/pydevelop_docs/cli.py`
**Location**: After line 341 in `_copy_static_files` method

**Add this code**:

```python
    def _copy_static_files(self):
        """Copy static assets from templates."""
        static_files = [
            # ... existing files ...
        ]

        for src, dest in static_files:
            src_path = self.template_path / src
            dest_path = self.project_path / dest
            if src_path.exists():
                shutil.copy2(src_path, dest_path)

        # ADD THIS: Copy AutoAPI templates
        autoapi_src = self.template_path / "_autoapi_templates"
        autoapi_dst = self.project_path / "docs" / "source" / "_autoapi_templates"

        if autoapi_src.exists() and autoapi_src.is_dir():
            # Remove existing templates if force mode
            if autoapi_dst.exists() and self.force:
                shutil.rmtree(autoapi_dst)

            # Copy the entire template directory
            if not autoapi_dst.exists():
                shutil.copytree(autoapi_src, autoapi_dst)
                if self.display:
                    self.display.debug(f"Copied AutoAPI templates to {autoapi_dst}")
```

### 2. Ensure Configuration Uses Templates

**File**: `/src/pydevelop_docs/config.py`
**Location**: In the AutoAPI configuration section

**Change**:

```python
# FROM:
"autoapi_template_dir": None,  # Disabled for debugging

# TO:
"autoapi_template_dir": "_autoapi_templates",
```

### 3. Remove Conflicting Configuration

**File**: `/docs/source/conf_modules/autoapi.py`
**Action**: DELETE this file entirely to avoid conflicts

## 🧪 Testing Plan

### Test 1: Template Distribution

```bash
cd /tmp/test-pydevelop
mkdir test-project && cd test-project
poetry init -n
poetry add pydvlp-docs --path /home/will/Projects/haive/backend/haive/tools/pydvlp-docs
poetry run pydvlp-docs init --force

# Verify templates copied
ls -la docs/source/_autoapi_templates/
# Should see: python/ directory with templates
```

### Test 2: Documentation Build

```bash
# Create test module
mkdir -p src/test_pkg
echo "'''Test package'''" > src/test_pkg/__init__.py
echo "class TestClass:\n    '''Test class'''\n    pass" > src/test_pkg/core.py

# Build docs
poetry run sphinx-build -b html docs/source docs/build

# Check generated RST
cat docs/source/autoapi/test_pkg/index.rst
# Should have proper formatting with newlines
```

### Test 3: Apply to haive-dataflow

```bash
cd /home/will/Projects/haive/backend/haive/packages/haive-dataflow
poetry run pydvlp-docs init --force
poetry run sphinx-build -b html docs/source docs/build

# Verify hierarchical structure in browser
python -m http.server 8001 --directory docs/build
```

## 🚀 Implementation Steps

### Step 1: Apply the Fix

1. Edit `cli.py` to add template copying
2. Edit `config.py` to enable templates
3. Delete conflicting `conf_modules/autoapi.py`

### Step 2: Test Locally

1. Test with a minimal project
2. Verify templates are copied
3. Check RST formatting is correct

### Step 3: Deploy to Packages

1. Run `pydvlp-docs init --force` on each package
2. Rebuild documentation
3. Verify hierarchical structure works

## 📊 Expected Results

### Before Fix

- No `_autoapi_templates` directory in projects
- Broken RST formatting
- Flat API structure

### After Fix

- `_autoapi_templates` directory properly distributed
- Clean RST formatting with proper newlines
- Hierarchical API navigation

## 🎨 Template Structure Being Copied

```
_autoapi_templates/
├── python/
│   ├── _base/
│   │   ├── foundation.j2
│   │   └── progressive.j2
│   ├── _components/
│   │   ├── code_blocks.j2
│   │   ├── diagrams.j2
│   │   ├── navigation.j2
│   │   └── tooltips.j2
│   ├── _filters/
│   │   ├── __init__.py
│   │   └── type_filters.py
│   ├── _macros/
│   │   └── type_specific.j2
│   ├── attribute.rst
│   ├── class.rst
│   ├── function.rst
│   ├── index.rst
│   ├── method.rst
│   └── module.rst
```

## ⚠️ Potential Issues

1. **Existing Templates**: If projects already have `_autoapi_templates`, need to handle conflicts
2. **Template Compatibility**: Ensure templates work with current AutoAPI version
3. **Path Issues**: Verify paths work on all platforms (Windows/Linux/Mac)

## 🔍 Verification Commands

```bash
# Check if templates exist in pydvlp-docs
ls -la /home/will/Projects/haive/backend/haive/tools/pydvlp-docs/src/pydevelop_docs/templates/_autoapi_templates/

# After fix, check if templates are copied
ls -la docs/source/_autoapi_templates/

# Verify configuration
poetry run python -c "from conf import *; print(f'autoapi_template_dir = {autoapi_template_dir}')"

# Check generated RST format
head -20 docs/source/autoapi/*/index.rst
```

## ✅ Success Criteria

1. Templates are automatically copied during `pydvlp-docs init`
2. RST files have proper formatting (newlines, indentation)
3. API documentation shows hierarchical structure
4. No more "flat" API reference

---

**Next Action**: Implement the fix in `cli.py` and test with haive-dataflow
