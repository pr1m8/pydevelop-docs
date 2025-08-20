# CLI Configuration Consolidation

**Date**: 2025-08-13
**Status**: ✅ Implemented
**Impact**: Major - Single source of truth for all configuration

## Problem Solved

The CLI had 400+ lines of hardcoded Sphinx configuration that duplicated what was in `config.py`. This led to:

- Configuration drift (CLI missing hierarchical fix)
- Maintenance burden (update in two places)
- Inconsistent behavior

## Solution Implemented

### 1. New Method: `_generate_conf_py_from_config()`

Creates conf.py that imports configuration at runtime:

```python
from pydevelop_docs.config import get_haive_config

# Get the standardized configuration
_config = get_haive_config(project, path)

# Apply all configuration settings
for key, value in _config.items():
    if key not in ["project", "copyright", "author", "release"]:
        globals()[key] = value
```

### 2. CLI Flag: `--use-shared-config`

- Default: True (uses shared config)
- `--use-inline-config` for legacy behavior
- Seamless migration path

### 3. Benefits

- **Single source of truth**: `config.py` is the master
- **Automatic updates**: All fixes propagate immediately
- **Consistent behavior**: Same config everywhere
- **Easier maintenance**: Update once, apply everywhere

## Implementation Details

### Modified Files

1. **cli.py**:
   - Added `_generate_conf_py_from_config()` method
   - Modified `_generate_conf_py()` to return content
   - Added CLI flag handling
   - Updated initialization flow

2. **Generated conf.py**:
   - Imports from `pydevelop_docs.config`
   - Applies config dynamically
   - Allows project-specific overrides

### Key Code Changes

```python
# In DocsInitializer.initialize()
if self.doc_config.get("use_shared_config", True):
    conf_content = self._generate_conf_py_from_config()
else:
    conf_content = self._generate_conf_py()

# Write the configuration
conf_path = self.project_path / "docs" / "source" / "conf.py"
conf_path.write_text(conf_content)
```

## Testing Results

✅ **Verified Working**:

- Hierarchical API structure maintained
- All 40+ extensions loaded correctly
- Configuration properly applied
- No duplicate maintenance needed

## Future Considerations

1. **Deprecation Path**: Eventually remove inline config option
2. **Performance**: Runtime import has minimal overhead
3. **Flexibility**: Projects can still override specific settings
