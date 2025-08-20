# Phase 0 Implementation - Critical Fixes

**Status**: Starting implementation  
**Date**: 2025-01-30

## Task 1: Move Templates to Distribution Location

### Current State

- Templates exist in `/docs/source/_autoapi_templates/`
- Need to move to `/src/pydevelop_docs/templates/_autoapi_templates/`

### Implementation Steps

1. **Create target directory structure**

```bash
mkdir -p src/pydevelop_docs/templates/_autoapi_templates/python
```

2. **Copy existing templates**

```bash
cp -r docs/source/_autoapi_templates/* src/pydevelop_docs/templates/_autoapi_templates/
```

3. **Verify structure**

```bash
ls -la src/pydevelop_docs/templates/_autoapi_templates/python/
# Should show: class.rst, dataclass.rst, module.rst
```

## Task 2: Add Template Copying to CLI

### Implementation

Need to add `_copy_autoapi_templates()` method to the CLI class and call it during initialization.

```python
def _copy_autoapi_templates(self):
    """Copy custom AutoAPI templates to project documentation."""
    template_source = Path(__file__).parent / "templates" / "_autoapi_templates"
    template_target = self.docs_source_path / "_autoapi_templates"

    if template_source.exists():
        # Remove existing templates if they exist
        if template_target.exists():
            shutil.rmtree(template_target)

        # Copy new templates
        shutil.copytree(template_source, template_target)
        self.console.print("[green]✅[/green] Copied custom AutoAPI templates")
        self.logger.debug(f"Copied AutoAPI templates from {template_source} to {template_target}")
    else:
        self.console.print("[yellow]⚠️[/yellow] AutoAPI templates not found in package")
        self.logger.warning(f"AutoAPI templates not found at {template_source}")
```

### Integration Point

Add to `_generate_structure()` method after static files are copied.

## Task 3: Fix Extension Loading Order

### Current Issue

- `sphinx_toolbox` must load before `sphinx_autodoc_typehints`
- Currently may be in wrong order

### Fix Location

- In `config.py` line ~449 in `_get_complete_extensions()`
- Also needs fixing in `cli.py` hardcoded config

## Next Steps

1. Execute the template move
2. Implement the CLI changes
3. Test with a sample project
4. Verify templates are distributed correctly
