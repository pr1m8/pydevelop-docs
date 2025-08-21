# Unified Documentation Implementation Issue

**Created**: 2025-08-13
**Status**: In Progress
**Priority**: High
**Issue Type**: Enhancement

## Problem Statement

Need to implement unified documentation navigation across all packages in monorepo projects using sphinx-collections. Users should be able to navigate between packages with "Back to Hub" functionality and cross-package linking.

## Current Implementation Status

### ✅ Completed

1. **Collections Configuration** - Updated `_get_collections_config()` in `src/pydevelop_docs/config.py`
   - Uses general pattern: `../../../packages/*/docs/build/html/`
   - Copies to `_collections/packages/`
   - Supports any monorepo structure

2. **Central Hub Support** - Already working in `docs/source/conf.py`
   - Uses `get_central_hub_config()`
   - Includes `sphinxcontrib.collections` extension
   - Has proper theme configuration

### ✅ Recently Completed

1. **Template System** - Created general templates for unified documentation
   - `central_hub_conf.py.jinja2` - General central hub configuration
   - `central_hub_index.rst.jinja2` - TOC tree template with package navigation
   - Enhanced `TemplateManager` with unified documentation methods

2. **Auto-Detection** - Package discovery and collections configuration
   - `auto_detect_packages()` method scans packages directory
   - `create_unified_documentation_setup()` creates complete setup
   - General pattern works with any monorepo structure

### 🔄 In Progress

1. **CLI Integration** - Add commands for creating unified documentation
2. **Testing Implementation** - Validate with test-haive-template
3. **Documentation** - Update guides for using unified docs

## Technical Details

### Configuration Changes Made

**File**: `src/pydevelop_docs/config.py`

```python
def _get_collections_config() -> Dict[str, Any]:
    """Get sphinx-collections configuration for central hub."""
    return {
        "collections": {
            "packages": {
                "driver": "copy_folder",
                "source_folder": "../../../packages/*/docs/build/html/",
                "target_folder": "_collections/packages/",
                "active": True,
                "clean": True,
            },
        },
        "collections_clean": True,
        "collections_final_clean": False,
    }
```

### Central Hub Integration

**File**: `docs/source/conf.py` (already working)

```python
from pydevelop_docs.config import get_central_hub_config
config = get_central_hub_config()
globals().update(config)
```

### Theme Options Include Navigation Support

**From**: `_get_complete_theme_options()` (already configured)

```python
"announcement": (
    "🚀 <strong>Haive AI Agent Framework</strong> - Complete monorepo documentation system!"
    if is_central_hub
    else f'🎯 <a href="../../index.html">← Back to Haive Docs</a> | {package_name} - Part of the Haive AI Agent Framework'
),
```

## Requirements

### For Unified Documentation to Work:

1. **Each package must have built documentation**:

   ```bash
   cd packages/package-name/docs
   poetry run sphinx-build -b html source build/html
   ```

2. **Central hub must be built after packages**:

   ```bash
   cd tools/pydvlppy/docs
   poetry run sphinx-build -b html source build
   ```

3. **sphinx-collections must be installed** (already in dependencies)

## Test Plan

### Phase 1: Validate Existing Setup

1. Build documentation for test-haive-template packages
2. Build central hub documentation
3. Verify collections are copied correctly
4. Test navigation between packages

### Phase 2: Enhance Navigation

1. Add proper "Back to Hub" links in individual packages
2. Create package overview pages in central hub
3. Add dependency visualization
4. Test cross-package intersphinx linking

### Phase 3: Documentation and Examples

1. Update pydvlppy README with unified docs instructions
2. Create example monorepo setup guide
3. Add CLI commands for building unified docs
4. Document best practices

## Next Steps

1. **Add CLI Integration**:

   ```bash
   # Proposed commands
   pydvlppy init-hub --packages-dir packages --hub-dir docs
   pydvlppy build-unified --packages-dir packages --hub-dir docs
   ```

2. **Test Current Implementation**:

   ```bash
   cd test-projects/test-haive-template

   # Use new template manager to create unified setup
   from pydevelop_docs.template_manager import TemplateManager
   manager = TemplateManager(Path("."), {"name": "Test Haive Template"})
   manager.create_unified_documentation_setup()

   # Build individual package docs first
   cd packages/testhaive-core/docs && poetry run sphinx-build -b html source build/html
   cd packages/testhaive-agents/docs && poetry run sphinx-build -b html source build/html
   cd packages/testhaive-tools/docs && poetry run sphinx-build -b html source build/html

   # Then build central hub
   cd docs && poetry run sphinx-build -b html source build
   ```

3. **Verify Collections Work**:
   - Check `_collections/packages/` directory is created
   - Verify package docs are copied correctly
   - Test navigation between packages
   - Validate TOC tree structure

## Related Files

- `src/pydevelop_docs/config.py` - Main configuration
- `docs/source/conf.py` - Central hub setup
- `test-projects/test-haive-template/` - Test environment
- `/home/will/Projects/haive/backend/haive/packages/*/docs/` - Real package docs

## Notes

- Keep configuration general, not hardcoded to specific packages
- Use existing patterns from test-haive-template
- sphinx-collections extension already included in dependencies
- Central hub setup already working in docs/source/conf.py

---

**Status Update**: Collections configuration updated to be general. Need to test implementation with actual package builds and enhance navigation.
