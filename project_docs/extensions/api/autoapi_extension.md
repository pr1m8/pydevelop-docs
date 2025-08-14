# AutoAPI Extension - Advanced Automatic API Documentation

**Extension**: `autoapi.extension`  
**Version**: 3.6.0+  
**Category**: API Documentation (Core)  
**Priority**: Critical (Must be first in extension list)

## Purpose and Core Capabilities

AutoAPI is the cornerstone of modern Sphinx API documentation, providing automatic generation of comprehensive API documentation directly from Python source code. Unlike traditional autodoc, AutoAPI parses source code statically, making it more reliable and offering advanced organizational features.

### Key Advantages Over Standard Autodoc

1. **Static Analysis**: No imports required - safer for complex codebases
2. **Hierarchical Organization**: Native support for package/module structure
3. **Template Customization**: Full Jinja2 template system for custom layouts
4. **Cross-Reference Support**: Automatic linking between modules and classes
5. **Performance**: Faster builds through optimized parsing

## Configuration in PyDevelop-Docs

### Current Implementation

```python
# In config.py - Complete AutoAPI configuration
def _get_complete_autoapi_config(package_path: str) -> Dict[str, Any]:
    return {
        "autoapi_type": "python",
        "autoapi_dirs": [package_path],
        "autoapi_template_dir": "_autoapi_templates",
        "autoapi_add_toctree_entry": True,
        "autoapi_generate_api_docs": True,
        "autoapi_keep_files": True,

        # ✅ HIERARCHICAL ORGANIZATION FIX - The key setting!
        "autoapi_own_page_level": "module",  # Keep classes with their modules

        "autoapi_options": [
            "members",
            "undoc-members",
            "show-inheritance",
            "show-module-summary",  # Critical for hierarchical organization
            "private-members",
            "special-members",
            "imported-members",
        ],
        "autoapi_python_class_content": "both",
        "autoapi_add_class_diagram": True,
        "autoapi_class_diagram_depth": 2,
        "autoapi_member_order": "groupwise",
        "autoapi_root": "autoapi",
        "autoapi_toctree_depth": 3,
        "autoapi_ignore": [
            "**/test_*.py",
            "**/tests/*",
            "**/conftest.py",
            "**/engine_node_test/**",
        ],
    }
```

### CLI Template Implementation

```python
# In cli.py template
autoapi_dirs = {autoapi_dirs}
autoapi_type = "python"
autoapi_template_dir = "_autoapi_templates"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]
autoapi_python_class_content = "both"
autoapi_member_order = "groupwise"
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_keep_files = True
autoapi_own_page_level = "module"  # ✅ HIERARCHICAL FIX INCLUDED
```

## Advanced Configuration Options

### Page Level Control (Critical for Issue #6)

```python
# Controls what gets individual pages vs grouped content
autoapi_own_page_level = "module"    # ✅ RECOMMENDED - Hierarchical structure
autoapi_own_page_level = "class"     # Default - Creates page explosion
autoapi_own_page_level = "function"  # Too granular - hundreds of files
autoapi_own_page_level = "attribute" # Extremely granular - avoid
```

### Template Directory Structure

```
_autoapi_templates/
├── python/
│   ├── index.rst          # Main API index page
│   ├── module.rst         # Individual module pages
│   ├── class.rst          # Class documentation
│   ├── function.rst       # Function documentation
│   ├── data.rst           # Data/attribute documentation
│   └── package.rst        # Package-level documentation
├── base.rst               # Base template
└── layout.html            # HTML layout template
```

### Member Organization Options

```python
autoapi_member_order = "alphabetical"  # A-Z sorting
autoapi_member_order = "groupwise"     # ✅ RECOMMENDED - By type then A-Z
autoapi_member_order = "bysource"      # Source code order
```

## Template Integration Opportunities (Issue #6 Focus)

### Custom Index Template

```jinja2
{# _autoapi_templates/python/index.rst #}
{% set packages = autoapi_objects | selectattr("type", "equalto", "package") | list %}
{% set modules = autoapi_objects | selectattr("type", "equalto", "module") | list %}

API Reference
=============

{% if packages %}
Package Documentation
--------------------

{% for package in packages | sort(attribute='name') %}
.. toctree::
   :maxdepth: 2

   {{ package.id }}

{% endfor %}
{% endif %}

{% if modules %}
Module Reference
---------------

{% for module in modules | sort(attribute='name') %}
.. toctree::
   :maxdepth: 1

   {{ module.id }}

{% endfor %}
{% endif %}
```

### Enhanced Module Template

```jinja2
{# _autoapi_templates/python/module.rst #}
{% if obj.docstring %}
{{ obj.docstring | indent(0, True) }}
{% endif %}

{% if obj.classes %}
Classes
-------

{% for class in obj.classes | sort(attribute='name') %}
.. autoclass:: {{ class.id }}
   :members:
   :show-inheritance:
   :special-members: __init__

   {% if class.docstring %}
   {{ class.docstring | indent(3, True) }}
   {% endif %}

{% endfor %}
{% endif %}

{% if obj.functions %}
Functions
---------

{% for function in obj.functions | sort(attribute='name') %}
.. autofunction:: {{ function.id }}

{% endfor %}
{% endif %}
```

### Progressive Disclosure Template

```jinja2
{# Enhanced class template with collapsible sections #}
.. class:: {{ obj.id }}

   {% if obj.docstring %}
   {{ obj.docstring | indent(3, True) }}
   {% endif %}

   {% if obj.methods %}
   .. dropdown:: Methods ({{ obj.methods | length }})
      :animate: fade-in

      {% for method in obj.methods | sort(attribute='name') %}
      .. automethod:: {{ method.id }}
      {% endfor %}
   {% endif %}

   {% if obj.attributes %}
   .. dropdown:: Attributes ({{ obj.attributes | length }})
      :animate: fade-in

      {% for attr in obj.attributes | sort(attribute='name') %}
      .. autoattribute:: {{ attr.id }}
      {% endfor %}
   {% endif %}
```

## Jinja2 Filters and Tests for Templates

### Built-in AutoAPI Filters

```jinja2
{# Object filtering #}
{{ autoapi_objects | selectattr("type", "equalto", "class") | list }}
{{ obj.children | selectattr("docstring") | list }}
{{ obj.methods | rejectattr("name", "startswith", "_") | list }}

{# Sorting and grouping #}
{{ obj.members | sort(attribute='name') }}
{{ obj.members | groupby('type') }}

{# String manipulation #}
{{ obj.docstring | indent(4, True) }}
{{ obj.name | replace("_", " ") | title }}
```

### Custom Filters for Enhanced Templates

```python
# In template_filters.py (custom additions)
def visibility_filter(members, visibility="public"):
    """Filter members by visibility."""
    if visibility == "public":
        return [m for m in members if not m.name.startswith("_")]
    elif visibility == "private":
        return [m for m in members if m.name.startswith("_") and not m.name.startswith("__")]
    elif visibility == "special":
        return [m for m in members if m.name.startswith("__")]
    return members

def type_priority_sort(members):
    """Sort members by type priority."""
    priority = {"property": 1, "method": 2, "attribute": 3}
    return sorted(members, key=lambda m: (priority.get(m.type, 99), m.name))
```

### Type-Specific Rendering Strategies

```jinja2
{# Conditional rendering based on object type #}
{% if obj.type == "class" %}
   {# Rich class documentation #}
   {% include "class_detailed.rst" %}
{% elif obj.type == "function" %}
   {# Streamlined function docs #}
   {% include "function_simple.rst" %}
{% elif obj.type == "module" %}
   {# Module overview with TOC #}
   {% include "module_hierarchical.rst" %}
{% endif %}

{# Pydantic model special handling #}
{% if "BaseModel" in (obj.bases | map(attribute='name') | list) %}
.. admonition:: Pydantic Model
   :class: tip

   This class is a Pydantic model with automatic validation.

   {% if obj.schema %}
   **JSON Schema**: Available for serialization/validation
   {% endif %}
{% endif %}
```

## Performance Optimization for Template Rendering

### Template Caching Strategy

```python
# In conf.py - Template performance optimization
autoapi_template_cache = True           # Enable template caching
autoapi_template_cache_size = 1000      # Cache up to 1000 templates
autoapi_keep_files = True               # Preserve generated files for incremental builds
```

### Conditional Generation

```python
# Skip documentation for specific patterns
autoapi_ignore = [
    "**/test_*.py",          # Test files
    "**/tests/*",            # Test directories
    "**/*_test.py",          # Test modules
    "**/conftest.py",        # Pytest config
    "**/migrations/*",       # Database migrations
    "**/node_modules/*",     # JavaScript dependencies
]

# Skip specific member types for performance
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    # Remove these for faster builds:
    # "private-members",     # Skip private members
    # "special-members",     # Skip __dunder__ methods
]
```

### Incremental Building

```python
# Optimize for large projects
autoapi_generate_api_docs = True
autoapi_keep_files = True               # Keep generated .rst files
autoapi_template_dir = "_autoapi_templates"

# Use dependency tracking
autoapi_python_use_implicit_namespaces = True
autoapi_add_toctree_entry = True
autoapi_toctree_depth = 2               # Limit depth for performance
```

## Integration with Other Extensions

### With sphinx-autodoc-typehints

```python
# Ensure proper loading order
extensions = [
    "autoapi.extension",          # MUST be before autodoc extensions
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",   # Type hints for AutoAPI objects
]

# Configure type hint integration
autodoc_typehints = "description"        # Show types in descriptions
typehints_fully_qualified = False        # Use short type names
```

### With sphinxcontrib.autodoc_pydantic

```python
# Pydantic model integration
autodoc_pydantic_model_show_json = True
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_field_list_validators = True

# Template integration
autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
    "special-members",   # Include Pydantic special methods
]
```

## Code Examples and Practical Implementation

### Basic AutoAPI Setup

```python
# Minimal configuration
extensions = ["autoapi.extension"]

autoapi_type = "python"
autoapi_dirs = ["../src"]
autoapi_own_page_level = "module"
autoapi_options = ["members", "show-inheritance"]
```

### Advanced Monorepo Configuration

```python
# Multi-package setup
autoapi_dirs = [
    "../packages/core/src",
    "../packages/agents/src",
    "../packages/tools/src",
]

autoapi_ignore = [
    "**/tests/*",
    "**/test_*",
    "**/conftest.py",
    # Package-specific ignores
    "**/core/deprecated/*",
    "**/agents/experimental/*",
]

# Custom template directory
autoapi_template_dir = "_autoapi_templates"

# Performance optimizations
autoapi_keep_files = True
autoapi_add_class_diagram = False  # Disable for large projects
```

### Template Customization Example

```bash
# Copy default templates for customization
python -c "
import autoapi
import shutil
from pathlib import Path

template_dir = Path(autoapi.__file__).parent / 'templates'
target_dir = Path('docs/source/_autoapi_templates')
shutil.copytree(template_dir, target_dir, dirs_exist_ok=True)
print(f'Templates copied to {target_dir}')
"
```

## Current Implementation Status in PyDevelop-Docs

### ✅ Completed Features

1. **Hierarchical Organization**: `autoapi_own_page_level = "module"` implemented
2. **Template Directory**: `_autoapi_templates` configured in both config.py and CLI
3. **Comprehensive Options**: Full option set for complete documentation
4. **Performance Optimization**: Ignore patterns and caching configured
5. **Integration**: Proper loading order with other extensions

### 🔄 In Progress (Issue #6)

1. **Custom Templates**: Need to create custom Jinja2 templates in `_autoapi_templates/`
2. **Progressive Disclosure**: Implement collapsible sections for large APIs
3. **Type-Specific Rendering**: Custom templates for Pydantic models, agents, tools
4. **Enhanced Navigation**: Better cross-references and organization

### 📅 Planned Enhancements

1. **Template Inheritance**: Base templates with package-specific overrides
2. **Interactive Elements**: Expand/collapse, filtering, search within API docs
3. **Custom Directives**: Domain-specific documentation patterns
4. **Performance Monitoring**: Template rendering metrics and optimization

## Official Documentation and Resources

- **Primary Documentation**: https://sphinx-autoapi.readthedocs.io/
- **Template Reference**: https://sphinx-autoapi.readthedocs.io/en/latest/reference/templates.html
- **Configuration Guide**: https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html
- **GitHub Repository**: https://github.com/readthedocs/sphinx-autoapi
- **Template Examples**: https://github.com/readthedocs/sphinx-autoapi/tree/main/autoapi/templates
- **Jinja2 Documentation**: https://jinja.palletsprojects.com/ (for template syntax)

## Best Practices for Large Projects

1. **Use `autoapi_own_page_level = "module"`** for manageable file counts
2. **Implement strategic `autoapi_ignore` patterns** for performance
3. **Keep templates simple** - complexity impacts build time
4. **Cache generated files** with `autoapi_keep_files = True`
5. **Monitor build performance** and optimize templates as needed
6. **Use progressive disclosure** for large APIs with many members
7. **Implement type-specific templates** for better user experience

The AutoAPI extension is the foundation of modern Python API documentation, and its template system provides unlimited customization possibilities for creating beautiful, organized, and user-friendly API references.
