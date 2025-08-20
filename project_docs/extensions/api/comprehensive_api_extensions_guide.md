# Comprehensive API Documentation Extensions Guide

**PyDevelop-Docs API Extension System**  
**Version**: 1.0  
**Purpose**: Complete reference for all 6 API documentation extensions  
**Focus**: Template integration, customization, and Issue #6 AutoAPI improvement

---

## Quick Reference Table

| Extension                        | Purpose             | Template Integration   | Performance Impact | Priority |
| -------------------------------- | ------------------- | ---------------------- | ------------------ | -------- |
| `autoapi.extension`              | Auto API generation | ✅ Full Jinja2 support | High               | Critical |
| `sphinxcontrib.autodoc_pydantic` | Pydantic models     | ✅ Custom templates    | Medium             | High     |
| `sphinx_autodoc_typehints`       | Type annotations    | ⚠️ Limited templates   | Low                | High     |
| `sphinx.ext.autosummary`         | Summary tables      | ✅ Custom templates    | Low                | Medium   |
| `sphinx.ext.autosectionlabel`    | Auto labels         | ❌ No templates        | Minimal            | Low      |
| `seed_intersphinx_mapping`       | Auto intersphinx    | ❌ No templates        | Minimal            | Medium   |

---

# 1. AutoAPI Extension - Core API Documentation

**Extension**: `autoapi.extension`  
**Priority**: Critical (Must be first)  
**Template Support**: Full Jinja2 system

## Purpose and Capabilities

AutoAPI is the cornerstone extension providing automatic API documentation generation through static code analysis. Unlike autodoc, it doesn't require imports, making it safer and more reliable.

### Key Features

- **Hierarchical Organization**: Native package/module structure support
- **Template Customization**: Complete Jinja2 template system
- **Static Analysis**: No runtime imports required
- **Cross-References**: Automatic linking between components

## Current PyDevelop-Docs Configuration

```python
# In config.py - Complete AutoAPI setup
{
    "autoapi_type": "python",
    "autoapi_dirs": [package_path],
    "autoapi_template_dir": "_autoapi_templates",
    "autoapi_own_page_level": "module",  # ✅ HIERARCHICAL FIX
    "autoapi_options": [
        "members",
        "undoc-members",
        "show-inheritance",
        "show-module-summary",  # Critical for organization
        "private-members",
        "special-members",
        "imported-members",
    ],
    "autoapi_python_class_content": "both",
    "autoapi_member_order": "groupwise",
    "autoapi_root": "autoapi",
    "autoapi_toctree_depth": 3,
    "autoapi_ignore": [
        "**/test_*.py",
        "**/tests/*",
        "**/conftest.py",
    ],
}
```

## Template Structure for Issue #6

```
_autoapi_templates/
├── python/
│   ├── index.rst          # Main API index - CUSTOMIZE FOR PACKAGES
│   ├── module.rst         # Module pages - CORE TEMPLATE
│   ├── class.rst          # Class documentation - RICH CONTENT
│   ├── function.rst       # Function documentation
│   └── package.rst        # Package-level docs
├── base.rst               # Base template with common elements
└── layout.html            # HTML layout template
```

### Custom Index Template Example

```jinja2
{# _autoapi_templates/python/index.rst #}
{% set packages = autoapi_objects | selectattr("type", "equalto", "package") | list %}
{% set modules = autoapi_objects | selectattr("type", "equalto", "module") | list %}

{{ "API Reference" | heading }}

{% if packages %}
{{ "Package Documentation" | heading(2) }}

{% for package in packages | sort(attribute='name') %}
.. toctree::
   :maxdepth: 2
   :caption: {{ package.name | title }}

   {{ package.id }}

{% endfor %}
{% endif %}

{% if modules %}
{{ "Module Reference" | heading(2) }}

.. grid:: 2
   :gutter: 2

   {% for module in modules | sort(attribute='name') %}
   .. grid-item-card:: {{ module.name }}
      :link: {{ module.id }}

      {{ module.summary or "Module documentation" }}

   {% endfor %}

{% endif %}
```

### Enhanced Module Template with Progressive Disclosure

```jinja2
{# _autoapi_templates/python/module.rst #}
{{ obj.name | heading }}

{% if obj.docstring %}
{{ obj.docstring | indent(0, True) }}
{% endif %}

{% set public_classes = obj.classes | rejectattr("name", "startswith", "_") | list %}
{% set public_functions = obj.functions | rejectattr("name", "startswith", "_") | list %}

{% if public_classes %}
{{ "Classes" | heading(2) }}

{% for class in public_classes | sort(attribute='name') %}
.. dropdown:: {{ class.name }}
   :animate: fade-in-slide-down
   :class-title: sd-fs-5

   .. autoclass:: {{ class.id }}
      :members:
      :show-inheritance:
      :special-members: __init__

{% endfor %}
{% endif %}

{% if public_functions %}
{{ "Functions" | heading(2) }}

.. grid:: 1 2 2 3
   :gutter: 2

   {% for function in public_functions | sort(attribute='name') %}
   .. grid-item-card:: ``{{ function.name }}``
      :class-header: sd-bg-info sd-text-white

      .. autofunction:: {{ function.id }}

   {% endfor %}
{% endif %}
```

## Performance Optimization

```python
# Template caching and performance
autoapi_template_cache = True
autoapi_keep_files = True                # Incremental builds
autoapi_add_class_diagram = False        # Skip for large projects
autoapi_toctree_depth = 2                # Limit depth
```

---

# 2. Sphinxcontrib Autodoc Pydantic - Model Documentation

**Extension**: `sphinxcontrib.autodoc_pydantic`  
**Priority**: High  
**Template Support**: Custom autodoc templates

## Purpose and Capabilities

Specialized extension for documenting Pydantic models with rich field information, validation details, and JSON schema integration.

### Key Features

- **Field Documentation**: Automatic field constraint documentation
- **Validator Display**: Show custom validators and their logic
- **JSON Schema**: Generate and display JSON schemas
- **Configuration Summary**: Model configuration details

## Current PyDevelop-Docs Configuration

```python
# Complete Pydantic configuration
{
    "autodoc_pydantic_model_show_json": True,
    "autodoc_pydantic_model_show_config_summary": True,
    "autodoc_pydantic_model_show_validator_summary": True,
    "autodoc_pydantic_model_show_field_summary": True,
    "autodoc_pydantic_model_show_validator_members": True,
    "autodoc_pydantic_field_list_validators": True,
    "autodoc_pydantic_field_show_constraints": True,
    "autodoc_pydantic_model_erdantic_figure": False,      # Skip diagrams
    "autodoc_pydantic_model_erdantic_figure_collapsed": False,
}
```

## Template Integration Opportunities

### Custom Pydantic Class Template

```jinja2
{# _autoapi_templates/python/pydantic_class.rst #}
{% if "BaseModel" in (obj.bases | map(attribute='name') | list) %}

.. admonition:: Pydantic Model
   :class: tip

   This class uses Pydantic for automatic data validation and serialization.

.. tab-set::

   .. tab-item:: Model Details

      .. autoclass:: {{ obj.id }}
         :members:
         :show-inheritance:

   .. tab-item:: Field Summary

      .. autopydantic_model:: {{ obj.id }}
         :model-show-field-summary:

   .. tab-item:: JSON Schema

      .. autopydantic_model:: {{ obj.id }}
         :model-show-json:

{% else %}
{# Regular class template #}
.. autoclass:: {{ obj.id }}
   :members:
   :show-inheritance:
{% endif %}
```

### Configuration Detection

```python
# In custom template filters
def is_pydantic_model(obj):
    """Detect if object is a Pydantic model."""
    if hasattr(obj, 'bases'):
        base_names = [base.name for base in obj.bases]
        return 'BaseModel' in base_names or 'pydantic.BaseModel' in base_names
    return False
```

## Advanced Pydantic Features

### Field Constraint Display

```python
# Enhanced field documentation
autodoc_pydantic_field_show_constraints = True
autodoc_pydantic_field_list_validators = True

# Custom field template
{
    "field_template": """
**{{ field.name }}**: {{ field.type }}
{% if field.constraints %}
- Constraints: {{ field.constraints | join(", ") }}
{% endif %}
{% if field.validators %}
- Validators: {{ field.validators | join(", ") }}
{% endif %}
""",
}
```

---

# 3. Sphinx Autodoc Typehints - Type Annotation Documentation

**Extension**: `sphinx_autodoc_typehints`  
**Priority**: High  
**Template Support**: Limited (via autodoc)

## Purpose and Capabilities

Enhances autodoc with rich type hint documentation, supporting modern Python typing features like generics, unions, and complex annotations.

### Key Features

- **Rich Type Display**: Format complex type annotations beautifully
- **Generic Support**: Handle `List[str]`, `Dict[str, Any]`, etc.
- **Union Types**: Display `Union[str, int]` and `Optional[str]` clearly
- **Return Type Documentation**: Automatic return type formatting

## Current PyDevelop-Docs Configuration

```python
# Type hints configuration
{
    "typehints_fully_qualified": False,      # Use short names (str vs builtins.str)
    "typehints_use_signature": True,         # Show types in signatures
    "autodoc_typehints": "description",      # Types in parameter descriptions
    "autodoc_typehints_format": "short",     # Short format for readability
}
```

## Integration with AutoAPI Templates

### Type-Aware Function Template

```jinja2
{# Enhanced function template with type awareness #}
{% if obj.type == "function" %}
.. function:: {{ obj.name }}({{ obj.parameters | join(", ") }})
{% if obj.return_type %}
   :returns: {{ obj.return_type }}
   :rtype: {{ obj.return_type }}
{% endif %}

   {% if obj.docstring %}
   {{ obj.docstring | indent(3, True) }}
   {% endif %}

   {% if obj.parameters %}
   **Parameters:**

   {% for param in obj.parameters %}
   - **{{ param.name }}** ({{ param.type or "Any" }}) -- {{ param.description or "No description" }}
   {% endfor %}
   {% endif %}

{% endif %}
```

### Type Hint Processing

```python
# Custom type hint formatting
def format_type_hint(type_annotation):
    """Format type hints for display."""
    if not type_annotation:
        return "Any"

    # Handle common patterns
    type_str = str(type_annotation)

    # Simplify common types
    simplifications = {
        "typing.List": "List",
        "typing.Dict": "Dict",
        "typing.Union": "Union",
        "typing.Optional": "Optional",
        "builtins.str": "str",
        "builtins.int": "int",
    }

    for full_name, short_name in simplifications.items():
        type_str = type_str.replace(full_name, short_name)

    return type_str
```

## Performance Considerations

```python
# Optimize type hint processing
typehints_document_rtype = True          # Document return types
typehints_defaults = "comma"             # Format for defaults
autodoc_preserve_defaults = True         # Keep default values
```

---

# 4. Sphinx Ext Autosummary - Summary Table Generation

**Extension**: `sphinx.ext.autosummary`  
**Priority**: Medium  
**Template Support**: Full template customization

## Purpose and Capabilities

Generates comprehensive summary tables for modules, classes, and functions, providing quick overviews and navigation aids.

### Key Features

- **Module Summaries**: Table of all module contents
- **Class Summaries**: Method and attribute tables
- **Function Summaries**: Parameter and return type tables
- **Custom Templates**: Fully customizable table layouts

## Current PyDevelop-Docs Configuration

```python
# Autosummary in extensions list
extensions = [
    "sphinx.ext.autosummary",
    # ... other extensions
]

# Configuration
{
    "autosummary_generate": True,           # Generate stub files
    "autosummary_imported_members": True,   # Include imported members
    "autosummary_mock_imports": [],         # Mock these imports
}
```

## Template Integration Examples

### Custom Module Summary Template

```jinja2
{# _templates/autosummary/module.rst #}
{{ fullname | escape | underline}}

.. automodule:: {{ fullname }}

   {% block functions %}
   {% if functions %}
   Functions
   ---------

   .. autosummary::
      :toctree: {{ objname }}
   {% for item in functions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   Classes
   -------

   .. autosummary::
      :toctree: {{ objname }}
      :template: autosummary/class.rst
   {% for item in classes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
```

### Enhanced Class Summary

```jinja2
{# _templates/autosummary/class.rst #}
{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :show-inheritance:

   {% block methods %}
   {% if methods %}

   Methods Summary
   ~~~~~~~~~~~~~~~

   .. autosummary::
      :nosignatures:
   {% for item in methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}

   Methods Detail
   ~~~~~~~~~~~~~~

   {% for item in methods %}
   .. automethod:: {{ name }}.{{ item }}
   {% endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}

   Attributes
   ~~~~~~~~~~

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
```

## Integration with AutoAPI

```jinja2
{# In AutoAPI module template - use autosummary #}
{% if obj.classes %}
{{ "Classes" | heading(2) }}

.. autosummary::
   :toctree: {{ obj.name }}_classes
   :template: autosummary/class.rst

{% for class in obj.classes | sort(attribute='name') %}
   {{ class.id }}
{% endfor %}

{% endif %}
```

---

# 5. Sphinx Ext Autosectionlabel - Automatic Section Labels

**Extension**: `sphinx.ext.autosectionlabel`  
**Priority**: Low  
**Template Support**: None (automatic processing)

## Purpose and Capabilities

Automatically generates labels for all sections, enabling easy cross-referencing without manual label creation.

### Key Features

- **Automatic Labels**: Every heading gets a referenceable label
- **Unique Naming**: Handles duplicate section names across files
- **Cross-File References**: Link to any section from anywhere
- **Prefix Support**: Add prefixes to avoid conflicts

## Current PyDevelop-Docs Configuration

```python
# In extensions list
extensions = [
    "sphinx.ext.autosectionlabel",
    # ... other extensions
]

# Configuration (minimal needed)
{
    "autosectionlabel_prefix_document": True,    # Add filename prefix
    "autosectionlabel_maxdepth": 3,             # Only label up to h3
}
```

## Usage in Templates

```jinja2
{# AutoAPI templates can reference auto-generated labels #}
{{ "Classes" | heading(2) }}

For configuration options, see :ref:`configuration:Configuration Guide`.

{% for class in obj.classes %}
.. _{{ obj.name }}.{{ class.name }}:

{{ class.name | heading(3) }}

Cross-reference this class: :ref:`{{ obj.name }}.{{ class.name }}`

{% endfor %}
```

## No Template Customization Needed

This extension works automatically - no custom templates required. It processes all generated documentation and adds labels.

---

# 6. Seed Intersphinx Mapping - Auto Intersphinx Population

**Extension**: `seed_intersphinx_mapping`  
**Priority**: Medium  
**Template Support**: None (configuration-based)

## Purpose and Capabilities

Automatically populates intersphinx mappings by reading dependencies from `pyproject.toml`, eliminating manual intersphinx configuration.

### Key Features

- **Automatic Discovery**: Reads dependencies from pyproject.toml
- **Smart Mapping**: Maps package names to documentation URLs
- **Conflict Resolution**: Handles multiple versions and sources
- **Performance**: Caches mapping data

## Current PyDevelop-Docs Configuration

```python
# In extensions list
extensions = [
    "sphinx.ext.intersphinx",         # Must be before seed_intersphinx_mapping
    "seed_intersphinx_mapping",       # Auto-populate from pyproject.toml
    # ... other extensions
]

# Configuration
{
    "pkg_requirements_source": "pyproject",     # Read from pyproject.toml
    "repository_root": "../..",                # Path to repo root
    "intersphinx_mapping": {
        # Manual mappings (these override auto-discovered ones)
        "python": ("https://docs.python.org/3", None),
        "sphinx": ("https://www.sphinx-doc.org/en/master", None),
    },
}
```

## Benefits for Template Cross-References

```jinja2
{# Templates can now reference external packages automatically #}
{% if obj.type == "function" and "pydantic" in (obj.parameters | map(attribute='type') | join(' ')) %}

.. note::
   This function works with :class:`pydantic.BaseModel` objects.
   See the `Pydantic documentation <pydantic:BaseModel>` for details.

{% endif %}

{# Reference typing module automatically #}
{% for param in obj.parameters %}
{% if "List" in param.type or "Dict" in param.type %}

   **{{ param.name }}**: See :mod:`typing` for type annotation details.

{% endif %}
{% endfor %}
```

## No Direct Template Integration

This extension works at the configuration level - templates benefit from automatic cross-references but don't need special customization.

---

# Consolidated Configuration Example

## Complete Extension Setup

```python
# Extensions in optimal order
extensions = [
    # Core (AutoAPI MUST be first)
    "autoapi.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "seed_intersphinx_mapping",
    "sphinx.ext.autosectionlabel",

    # Enhanced API
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_autodoc_typehints",

    # ... other extensions
]

# Unified API configuration
api_config = {
    # AutoAPI (Primary)
    "autoapi_type": "python",
    "autoapi_dirs": [package_path],
    "autoapi_template_dir": "_autoapi_templates",
    "autoapi_own_page_level": "module",
    "autoapi_options": [
        "members", "undoc-members", "show-inheritance",
        "show-module-summary", "special-members"
    ],

    # Autosummary
    "autosummary_generate": True,
    "autosummary_imported_members": True,

    # Type hints
    "typehints_fully_qualified": False,
    "typehints_use_signature": True,
    "autodoc_typehints": "description",

    # Pydantic
    "autodoc_pydantic_model_show_json": True,
    "autodoc_pydantic_field_show_constraints": True,
    "autodoc_pydantic_model_show_config_summary": True,

    # Auto section labels
    "autosectionlabel_prefix_document": True,
    "autosectionlabel_maxdepth": 3,

    # Intersphinx auto-population
    "pkg_requirements_source": "pyproject",
    "repository_root": "../..",
}
```

## Template Directory Structure (Issue #6 Implementation)

```
docs/source/
├── _autoapi_templates/           # AutoAPI custom templates
│   ├── python/
│   │   ├── index.rst            # Main API index
│   │   ├── module.rst           # Module documentation
│   │   ├── class.rst            # Class documentation
│   │   ├── function.rst         # Function documentation
│   │   └── pydantic_class.rst   # Pydantic model template
│   └── base.rst                 # Base template
├── _templates/                   # Standard Sphinx templates
│   └── autosummary/             # Autosummary templates
│       ├── module.rst           # Module summary template
│       └── class.rst            # Class summary template
└── _static/                      # CSS and JS assets
    ├── api-docs.css             # API-specific styling
    └── js/
        └── api-enhancements.js   # API interactivity
```

## Performance Optimization Summary

```python
# Performance-optimized configuration
performance_config = {
    # AutoAPI optimization
    "autoapi_keep_files": True,              # Incremental builds
    "autoapi_add_class_diagram": False,      # Skip for large projects
    "autoapi_toctree_depth": 2,              # Limit depth

    # Template caching
    "autoapi_template_cache": True,

    # Selective documentation
    "autoapi_ignore": [
        "**/test_*.py", "**/tests/*", "**/conftest.py"
    ],

    # Type hint optimization
    "autodoc_typehints_format": "short",
    "typehints_defaults": "comma",

    # Autosummary optimization
    "autosummary_mock_imports": [],          # Add problematic imports here
}
```

---

# Quick Implementation Checklist for Issue #6

## Phase 1: Template Infrastructure

- [ ] Create `_autoapi_templates/python/` directory
- [ ] Copy default AutoAPI templates as base
- [ ] Create custom `index.rst` with package organization
- [ ] Implement progressive disclosure in `module.rst`

## Phase 2: Content Enhancement

- [ ] Add Pydantic-specific templates
- [ ] Integrate autosummary for overview tables
- [ ] Enhance type hint display
- [ ] Add cross-references with autosectionlabel

## Phase 3: Advanced Features

- [ ] Implement tabbed interfaces for complex classes
- [ ] Add search and filtering within API docs
- [ ] Create responsive grid layouts
- [ ] Add interactive examples

## Phase 4: Performance & Polish

- [ ] Optimize template rendering performance
- [ ] Add template caching strategies
- [ ] Test with large codebases
- [ ] Document template customization guide

This comprehensive guide provides everything needed to understand, configure, and customize the 6 API documentation extensions in PyDevelop-Docs, with special focus on the template system for Issue #6 improvements.
