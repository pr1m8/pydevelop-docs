# PyDevelop-Docs Template Issues Summary

**Date**: 2025-08-15
**Purpose**: Quick reference for all template issues and their status
**Priority**: CRITICAL - Blocking documentation generation

## 🔴 Current Status

Despite having the correct AutoAPI fix (`autoapi_own_page_level = "module"`), documentation generation is still broken due to template system issues.

## 🎯 Key Issues

### 1. **Template Distribution Not Implemented** ❌

- **Problem**: Custom templates exist but are never copied to projects
- **Location**: `/src/pydevelop_docs/templates/_autoapi_templates/`
- **Impact**: Projects always use default sphinx-autoapi templates
- **Fix Required**: Add template copying logic to `cli.py`

### 2. **Multiple Conflicting Template Sets** ⚠️

- **Production Templates**: `/src/pydevelop_docs/templates/_autoapi_templates/`
- **Dev Templates**: `/docs/source/_autoapi_templates/`
- **Hidden Templates**: `/.pydevelop/templates/`
- **Test Templates**: `/test-projects/test-haive-template/docs/source/`
- **Problem**: No clear which is authoritative

### 3. **Template Configuration Disabled** 🔧

- **Current State**: `autoapi_template_dir = None` (line 546 in config.py)
- **Reason**: "Disabled for debugging"
- **Impact**: Even if templates were copied, they wouldn't be used
- **Original Setting**: `autoapi_template_dir = "_autoapi_templates"`

### 4. **Complex Jinja2 Component System** 🌀

- **Structure**:
  ```
  _base/           # foundation.j2, progressive.j2
  _components/     # code_blocks.j2, diagrams.j2, navigation.j2, tooltips.j2
  _filters/        # type_filters.py
  _macros/         # type_specific.j2
  ```
- **Problem**: Non-standard for AutoAPI, overly complex
- **Impact**: May cause template processing issues

### 5. **RST Formatting Broken** 📝

- **Symptoms**: Missing newlines, wrong indentation, malformed directives
- **Example**:
  ```rst
  dataflow
  ========.. py:module:: dataflow    # Missing newline!
  ```
- **Cause**: Unknown template processing issue

## 📊 Configuration States

| Setting                  | config.py     | cli.py                 | docs/conf_modules      | Status      |
| ------------------------ | ------------- | ---------------------- | ---------------------- | ----------- |
| `autoapi_own_page_level` | `"module"` ✅ | -                      | -                      | Correct     |
| `autoapi_template_dir`   | `None` ❌     | `"_autoapi_templates"` | `"_autoapi_templates"` | Conflicting |
| Template copying         | -             | Not implemented ❌     | -                      | Missing     |

## 🛠️ Quick Fixes to Try

### Fix 1: Enable Templates in config.py

```python
# Line 546 in /src/pydevelop_docs/config.py
# Change from:
autoapi_template_dir = None
# To:
autoapi_template_dir = "_autoapi_templates"
```

### Fix 2: Add Template Copying to CLI

```python
# In cli.py, add this method:
def _copy_autoapi_templates(self):
    src = Path(__file__).parent / "templates" / "_autoapi_templates"
    dst = self.project_path / "docs" / "source" / "_autoapi_templates"
    if src.exists():
        shutil.copytree(src, dst, dirs_exist_ok=True)

# Call it in init() after _generate_conf_py()
```

### Fix 3: Bypass PyDevelop-Docs (Test)

```python
# In package conf.py, add directly:
autoapi_own_page_level = "module"
autoapi_dirs = ["../../src"]
# Don't set autoapi_template_dir
```

## 📋 Action Priority

1. **IMMEDIATE**: Test Fix 3 on one package to verify hierarchical structure works
2. **TODAY**: Implement Fix 2 (template copying)
3. **TODAY**: Test Fix 1 (re-enable templates)
4. **THIS WEEK**: Consolidate template sets
5. **NEXT WEEK**: Simplify component system

## 🔍 Debug Commands

```bash
# Check current config
cd packages/haive-dataflow/docs/source
grep autoapi_own_page_level conf.py
grep autoapi_template_dir conf.py

# Test without templates
python -c "from conf import *; print(f'template_dir = {autoapi_template_dir}')"

# Check if templates exist
ls -la _autoapi_templates/

# Build with verbose output
sphinx-build -b html . ../build -v 2>&1 | grep autoapi
```

## ✅ Success Criteria

1. Hierarchical API structure (not flat list)
2. Custom templates distributed and used
3. Clean RST output
4. No template errors in build

## 🚨 Critical Path

The quickest fix is to:

1. Bypass templates entirely (set to None in package conf.py)
2. Ensure `autoapi_own_page_level = "module"` is set
3. Build and verify hierarchical structure works
4. Then tackle template issues

---

**Bottom Line**: The templates are currently more problem than solution. Consider disabling them until basic hierarchical structure works.
