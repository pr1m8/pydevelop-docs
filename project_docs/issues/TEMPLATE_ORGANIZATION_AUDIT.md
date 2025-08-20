# PyDevelop-Docs Template Organization Audit

**Date**: 2025-01-15
**Purpose**: Complete audit of template organization and fix plan
**Status**: Critical - Templates are the root cause of documentation failures

## 🔍 Template Locations Found

### 1. Main Templates Directory

**Location**: `/src/pydevelop_docs/templates/`

**Contents**:

```
templates/
├── _autoapi_templates/          # PLANNED but NOT IMPLEMENTED
├── central_hub_conf.py         # Central hub configuration template
├── changelog.rst               # Changelog template
└── static/                     # Static files templates
    ├── css/
    └── js/
```

**Issue**: The `_autoapi_templates/` directory is referenced but doesn't exist!

### 2. Documentation Templates

**Location**: `/docs/source/_templates/`

**Contents**:

- Custom Sphinx templates for PyDevelop-Docs own documentation
- NOT distributed to projects

### 3. Referenced Template Directory

**Location**: `_autoapi_templates` (relative path in configs)

**Status**: Referenced in multiple places but doesn't exist in projects

### 4. Test Project Templates

**Location**: `/test-projects/test-haive-template/docs/source/_templates/`

**Contents**: Various test templates not part of main distribution

## 🔴 Critical Issues Identified

### Issue 1: Template Distribution Not Implemented

**Problem**: Templates are NOT copied during `pydvlp-docs init`

**Evidence**: In `cli.py`:

```python
def init_command(...):
    # Creates conf.py from template
    # But does NOT copy _autoapi_templates directory!
```

**Impact**: Projects reference templates that don't exist

### Issue 2: Template Configuration Confusion

**Three Different Configurations**:

1. **config.py**:

   ```python
   "autoapi_template_dir": None  # Disabled for debugging
   ```

2. **conf_modules/autoapi.py**:

   ```python
   autoapi_template_dir = "_autoapi_templates"  # References non-existent dir
   ```

3. **Generated conf.py**:
   ```python
   # Gets config from get_haive_config() but templates missing
   ```

### Issue 3: RST Generation Broken

**Symptoms in generated files**:

```rst
dataflow
========.. py:module:: dataflow    # BROKEN: Missing newline
Submodules
----------                        # BROKEN: Wrong dash encoding
.. toctree::
   :maxdepth: 1   dataflow.api   # BROKEN: All on one line
```

### Issue 4: No Clear Template Authority

**Multiple Sources**:

- Which templates should be used?
- What's the inheritance order?
- How do custom templates override defaults?

## 🏗️ Template System Architecture

### Intended Flow (Not Working)

1. PyDevelop-Docs has master templates
2. `init` command copies templates to project
3. Project uses local `_autoapi_templates/`
4. AutoAPI uses custom templates for generation

### Actual Flow (Current)

1. PyDevelop-Docs has templates (incomplete)
2. `init` does NOT copy templates ❌
3. Projects reference non-existent templates ❌
4. AutoAPI falls back to defaults (broken output) ❌

## 🔧 Fix Implementation Plan

### Phase 1: Bypass Templates (Immediate Fix)

**In each package's conf.py**, add directly:

```python
# Bypass pydvlp-docs temporarily
extensions = [
    "autoapi.extension",  # Must be first
    # ... other extensions
]

autoapi_type = "python"
autoapi_dirs = ["../../src"]
autoapi_own_page_level = "module"  # THE KEY FIX
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]
# DO NOT set autoapi_template_dir
```

### Phase 2: Fix Template Distribution

**In pydvlp-docs cli.py**:

```python
def init_command(...):
    # ... existing code ...

    # Add template copying
    if include_autoapi_templates:
        template_src = PACKAGE_DIR / "templates" / "_autoapi_templates"
        template_dst = docs_dir / "source" / "_autoapi_templates"
        if template_src.exists():
            shutil.copytree(template_src, template_dst)
```

### Phase 3: Create Missing Templates

**Create `/src/pydevelop_docs/templates/_autoapi_templates/`**:

```
_autoapi_templates/
├── python/
│   ├── module.rst
│   ├── class.rst
│   ├── function.rst
│   └── package.rst
└── index.rst
```

### Phase 4: Fix Configuration

**Update config.py**:

```python
# Re-enable templates after they exist
"autoapi_template_dir": "_autoapi_templates",
```

## 📊 Testing Strategy

### Test 1: Vanilla AutoAPI

```bash
# Remove all template references
cd packages/haive-dataflow/docs
rm -rf source/_autoapi_templates
rm -rf source/_templates/autoapi
# Add minimal config to conf.py
# Build and verify hierarchy works
```

### Test 2: With Templates

```bash
# Copy templates manually first
# Test with autoapi_template_dir set
# Verify output format is correct
```

### Test 3: Full Integration

```bash
# Use pydvlp-docs init
# Verify templates are copied
# Build docs and check structure
```

## 🎯 Success Metrics

1. **Hierarchical API structure** (not flat)
2. **Clean RST formatting** (proper newlines)
3. **Templates distributed** (exist in projects)
4. **Configuration clarity** (single source)

## 🚨 Why This Matters

The template system is preventing the AutoAPI hierarchical fix from working. Even though the configuration is correct (`autoapi_own_page_level = "module"`), the broken template system is corrupting the output.

## 📝 Action Items

1. **Immediate**: Apply Phase 1 bypass to haive-dataflow
2. **Today**: Implement Phase 2 template distribution
3. **Tomorrow**: Create Phase 3 missing templates
4. **This Week**: Complete Phase 4 configuration fix

---

**Root Cause**: PyDevelop-Docs has templates but doesn't distribute them, causing projects to reference non-existent templates and breaking AutoAPI output.
