# Template Testing for pydevelop-docs

This directory contains comprehensive testing tools for the Jinja2 template system in pydevelop-docs.

## Test Files

### Core Tests

- **`test_templates.py`** - Pytest-based template tests (requires pytest configuration fix)
- **`validate_templates.py`** - Comprehensive validation using djLint + Jinja2 rendering
- **`integration_test.py`** - Integration test demonstrating custom filters with TemplateManager

### Usage

```bash
# Quick validation of all templates
python tests/validate_templates.py

# Integration test with custom filters
python tests/integration_test.py

# Individual template testing (when pytest is fixed)
# python -m pytest tests/test_templates.py -v
```

## Key Findings

### ✅ What's Working

1. **TemplateManager Core** - Basic template rendering works correctly
2. **Critical Bug Fixed** - Added missing `_write_file()` method
3. **Custom Filters** - 27 sophisticated filters available and functional
4. **Advanced Components** - 7 complex template components have valid syntax
5. **Basic Templates** - Quickstart and section templates render correctly

### ⚠️ Issues Found

1. **djLint Warnings** - 6 templates have minor issues (mostly false positives about RST links)
2. **Pytest Configuration** - Inherited pytest config from main project causes conflicts

### 🎨 Available Custom Filters

The backup system contains 27 custom Jinja2 filters for intelligent documentation:

- **Type Detection**: `is_pydantic_model`, `is_agent_class`, `is_tool_class`, `is_enum_class`
- **String Processing**: `format_annotation`, `to_snake_case`, `to_kebab_case`, `truncate_with_ellipsis`
- **Code Analysis**: `get_complexity_score`, `get_decorator_names`, `group_by_category`
- **Template Utilities**: `pluralize`, `create_anchor`, `highlight_code`, `extract_first_sentence`

### 🔧 Template System Architecture

```
src/pydevelop_docs/templates/
├── doc_templates/           # Basic documentation templates
│   ├── quickstart.rst.jinja2
│   ├── section_index.rst.jinja2
│   └── configuration.rst.jinja2
├── central_hub_*.jinja2     # Central hub templates
└── _autoapi_templates_BROKEN_BACKUP/  # Advanced system
    ├── python/_filters/     # 27 custom filters
    ├── python/_components/  # 4 component macros
    ├── python/_macros/      # 2 utility macros
    └── python/_base/        # 2 foundation templates
```

## Integration Example

```python
from pydevelop_docs.template_manager import TemplateManager

# Create manager
manager = TemplateManager(project_path, project_info)

# Load custom filters
from type_filters import FILTERS
for name, func in FILTERS.items():
    manager.env.filters[name] = func

# Use enhanced templates
result = manager.render_template("enhanced_template.j2", context)
```

## Next Steps

1. **Fix djLint Issues** - Review the 6 templates with warnings
2. **Integrate Filters** - Add custom filter loading to main TemplateManager
3. **Restore Advanced System** - Consider enabling the sophisticated backup templates
4. **Add More Tests** - Create tests for complex AutoAPI template scenarios

## Tools Used

- **djLint** - Modern Jinja2 template linter and formatter
- **Jinja2** - Template engine with custom filter support
- **pytest** - Python testing framework (needs config fix)

All tests validate the template system without mocks, using real template rendering and validation.
