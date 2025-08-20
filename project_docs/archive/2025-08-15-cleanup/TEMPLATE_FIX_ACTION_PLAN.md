# PyDevelop-Docs Template Fix Action Plan

**Created**: 2025-08-15
**Purpose**: Step-by-step plan to fix template issues
**Priority**: CRITICAL

## 🎯 Goal

Get AutoAPI hierarchical documentation working by fixing template distribution and configuration issues.

## 📋 Step-by-Step Fix Plan

### Step 1: Test Without Templates (Verify Core Fix Works)

**Location**: Any haive package (e.g., haive-dataflow)
**File**: `packages/haive-dataflow/docs/source/conf.py`

```python
# Add these lines directly to conf.py:
autoapi_own_page_level = "module"
autoapi_type = "python"
autoapi_dirs = ["../../src"]
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
# DO NOT set autoapi_template_dir

# Comment out or remove:
# from pydevelop_docs.config import get_haive_config
# config = get_haive_config(...)
# globals().update(config)
```

**Test**:

```bash
cd packages/haive-dataflow/docs
sphinx-build -b html source build -E
# Check build/autoapi/index.html for hierarchical structure
```

**Expected**: Hierarchical API structure should work

### Step 2: Re-enable Templates in config.py

**Location**: `/src/pydevelop_docs/config.py`
**Line**: 546

```python
# Change from:
autoapi_template_dir = None

# To:
autoapi_template_dir = "_autoapi_templates"

# And uncomment line 551:
"autoapi_template_dir": autoapi_template_dir,  # Re-enable this
```

### Step 3: Add Template Copying to CLI

**Location**: `/src/pydevelop_docs/cli.py`
**After line 342** (end of `_copy_static_files` method)

```python
def _copy_autoapi_templates(self):
    """Copy custom AutoAPI templates to project."""
    template_src = self.template_path / "_autoapi_templates"
    template_dst = self.project_path / "docs" / "source" / "_autoapi_templates"

    if template_src.exists():
        # Create destination directory
        template_dst.mkdir(parents=True, exist_ok=True)

        # Copy entire template directory
        shutil.copytree(template_src, template_dst, dirs_exist_ok=True)

        self.console.print(
            f"[green]✓[/green] Copied AutoAPI templates to {template_dst.relative_to(self.project_path)}"
        )
    else:
        self.console.print(
            "[yellow]⚠[/yellow] No custom AutoAPI templates found in pydvlp-docs"
        )
```

**In the `initialize` method** (around line 306), add after `_copy_static_files()`:

```python
# Copy static files
self._copy_static_files()

# Copy AutoAPI templates
self._copy_autoapi_templates()  # ADD THIS LINE
```

### Step 4: Simplify Template Structure (Optional)

**Location**: `/src/pydevelop_docs/templates/_autoapi_templates/python/`

Consider removing the complex component system temporarily:

- Remove `_base/`, `_components/`, `_macros/` directories
- Keep only the main `.rst` templates
- Focus on getting basic functionality working

### Step 5: Test Full Integration

1. **Create a test project**:

   ```bash
   cd /tmp
   mkdir test-pydevelop
   cd test-pydevelop
   pydvlp-docs init --monorepo
   ```

2. **Verify templates were copied**:

   ```bash
   ls -la docs/source/_autoapi_templates/
   ```

3. **Build documentation**:

   ```bash
   cd docs
   sphinx-build -b html source build
   ```

4. **Check output**:
   - Verify hierarchical structure in `build/autoapi/index.html`
   - Check for template errors in build log

## 🔍 Debugging Checklist

### If templates aren't copied:

- [ ] Check `template_src` path is correct
- [ ] Verify templates exist in pydvlp-docs package
- [ ] Check file permissions

### If templates are copied but not used:

- [ ] Verify `autoapi_template_dir` is set in conf.py
- [ ] Check for typos in directory name
- [ ] Look for template errors in sphinx build output

### If RST formatting is broken:

- [ ] Check Jinja2 whitespace handling in templates
- [ ] Verify template syntax is correct
- [ ] Test with minimal template first

## 📊 Validation Tests

### Test 1: Template Distribution

```python
# After running pydvlp-docs init
import os
assert os.path.exists("docs/source/_autoapi_templates/python/module.rst")
```

### Test 2: Configuration

```python
# In generated conf.py
assert 'autoapi_template_dir = "_autoapi_templates"' in open("docs/source/conf.py").read()
```

### Test 3: Hierarchical Structure

```python
# After building docs
# Check that API structure is hierarchical, not flat
```

## 🚀 Implementation Order

1. **First**: Test Step 1 to verify core fix works
2. **Second**: Implement Step 3 (template copying)
3. **Third**: Re-enable templates (Step 2)
4. **Fourth**: Test full integration
5. **Optional**: Simplify templates if issues persist

## ✅ Success Criteria

- [ ] Hierarchical API structure works (not flat list)
- [ ] Templates are copied during `pydvlp-docs init`
- [ ] Custom templates are used during build
- [ ] No template errors in build log
- [ ] Clean RST output without formatting issues

## 🔗 Related Files

- **Config**: `/src/pydevelop_docs/config.py`
- **CLI**: `/src/pydevelop_docs/cli.py`
- **Templates**: `/src/pydevelop_docs/templates/_autoapi_templates/`
- **Issues**: `/project_docs/issues/TEMPLATE_CONFIGURATION_MESS_ANALYSIS.md`

---

**Note**: Start with the simplest fix (Step 1) to verify the core hierarchical structure works before dealing with template complexity.
