# AutoAPI Template Customization Research

**Created**: 2025-01-30  
**Purpose**: Deep dive into sphinx-autoapi template system for Issue #6  
**Status**: Research Complete

## AutoAPI Template Architecture

### Template Directory Structure

AutoAPI organizes templates by language and object type:

```
autoapi/templates/
└── python/
    ├── module.rst          # Module documentation
    ├── package.rst         # Package documentation
    ├── class.rst           # Class documentation
    ├── function.rst        # Function documentation
    ├── method.rst          # Method documentation
    ├── property.rst        # Property documentation
    ├── attribute.rst       # Attribute documentation
    ├── data.rst            # Module-level variables
    └── exception.rst       # Exception classes
```

### Template Search Path

1. **Custom templates** (if `autoapi_template_dir` is set)
2. **Default templates** in AutoAPI package
3. Templates are selected based on object type

### Setting Custom Template Directory

```python
# conf.py
autoapi_template_dir = '_autoapi_templates'
```

## Context Variables in AutoAPI Templates

### Global Variables Available

```jinja2
autoapi_options          # List of enabled options from conf.py
include_summaries        # Boolean - whether to show summaries
obj                      # The main object being documented
own_page_types           # List of object types that get own pages
sphinx_version           # Sphinx version information
```

### Object (`obj`) Attributes

#### Universal Attributes

```jinja2
obj.id                   # Full dotted path (e.g., "package.module.Class")
obj.name                 # Simple name (e.g., "Class")
obj.type                 # Object type: "module", "class", "function", etc.
obj.docstring           # Full documentation string
obj.short_description   # First line of docstring
obj.file_path           # Path to source file
obj.line_number         # Line number in source
obj.display             # Whether to display this object
```

#### Module/Package Attributes

```jinja2
obj.all                  # __all__ list if defined
obj.children             # All child objects
obj.submodules          # Direct submodules
obj.subpackages         # Direct subpackages
obj.functions           # Module-level functions
obj.classes             # Module-level classes
obj.exceptions          # Module exceptions
obj.attributes          # Module-level attributes
```

#### Class Attributes

```jinja2
obj.bases               # List of base class objects
obj.docstring           # Class docstring
obj.methods             # List of method objects
obj.attributes          # List of attribute objects
obj.properties          # List of property objects
obj.is_abstract         # Boolean - is abstract class
obj.is_dataclass        # Boolean - is dataclass
obj.is_exception        # Boolean - inherits from Exception
obj.decorators          # List of decorator names
obj.metaclass           # Metaclass name if any
```

#### Function/Method Attributes

```jinja2
obj.args                # List of argument names
obj.defaults            # List of default values
obj.signature           # Full signature string
obj.parameters          # List of parameter objects
obj.returns             # Return type annotation
obj.return_annotation   # Raw return annotation
obj.yields              # Yield type if generator
obj.raises              # List of exceptions raised
obj.is_async            # Boolean - async function
obj.is_generator        # Boolean - generator function
obj.is_static_method    # Boolean - @staticmethod
obj.is_class_method     # Boolean - @classmethod
obj.is_property         # Boolean - @property
obj.decorators          # List of decorators
```

#### Parameter Object Attributes

```jinja2
param.name              # Parameter name
param.annotation        # Type annotation
param.default           # Default value
param.kind              # Parameter kind (positional, keyword, etc.)
```

## Customizing the Jinja2 Environment

### Using autoapi_prepare_jinja_env

```python
# conf.py

def autoapi_prepare_jinja_env(jinja_env):
    """Customize the Jinja2 environment for AutoAPI."""

    # Add custom filters
    jinja_env.filters['format_annotation'] = format_type_annotation
    jinja_env.filters['shorten'] = lambda s, n=50: s[:n] + '...' if len(s) > n else s
    jinja_env.filters['extract_module'] = lambda id: '.'.join(id.split('.')[:-1])

    # Add custom tests
    jinja_env.tests['pydantic_model'] = lambda obj: any('BaseModel' in b.name for b in obj.bases or [])
    jinja_env.tests['async_function'] = lambda obj: getattr(obj, 'is_async', False)

    # Add global functions
    jinja_env.globals['get_icon'] = get_object_icon
    jinja_env.globals['format_signature'] = format_function_signature

    # Add custom variables
    jinja_env.globals.update({
        'theme_color': '#2980b9',
        'show_private': False,
        'group_by_type': True
    })

# Example helper functions
def format_type_annotation(annotation):
    """Format type annotations for better readability."""
    if not annotation:
        return ''
    # Convert typing hints to simpler forms
    annotation = str(annotation)
    annotation = annotation.replace('typing.', '')
    annotation = annotation.replace('Optional[', '[')
    return annotation

def get_object_icon(obj_type):
    """Return an icon for different object types."""
    icons = {
        'class': '🏛️',
        'function': '⚡',
        'method': '🔧',
        'property': '📦',
        'module': '📁',
        'package': '📂'
    }
    return icons.get(obj_type, '📄')
```

## Template Customization Patterns

### 1. Progressive Disclosure

```jinja2
{# Show essential info first #}
<div class="api-essential">
    <h{{ level }}>{{ obj.name }}</h{{ level }}>
    <p class="summary">{{ obj.short_description }}</p>
</div>

{# Hide details in collapsible sections #}
{% if obj.docstring != obj.short_description %}
<details class="api-details">
    <summary>Full Description</summary>
    <div class="docstring">
        {{ obj.docstring|rst_to_html }}
    </div>
</details>
{% endif %}
```

### 2. Type-Specific Rendering

```jinja2
{# Detect special class types #}
{% if obj|pydantic_model %}
    {# Render as Pydantic model with field table #}
    {% include 'python/partials/pydantic_model.rst' %}
{% elif obj.is_exception %}
    {# Render as exception with inheritance chain #}
    {% include 'python/partials/exception.rst' %}
{% elif obj.is_dataclass %}
    {# Render as dataclass with field definitions #}
    {% include 'python/partials/dataclass.rst' %}
{% else %}
    {# Standard class rendering #}
    {% include 'python/partials/standard_class.rst' %}
{% endif %}
```

### 3. Smart Method Grouping

```jinja2
{# Group methods by type #}
{% set public_methods = obj.methods|selectattr('name')|reject('match', '^_')|list %}
{% set private_methods = obj.methods|selectattr('name')|select('match', '^_')|list %}
{% set properties = obj.properties %}

{% if public_methods %}
Public Methods
--------------
{% for method in public_methods|sort(attribute='name') %}
    {% include 'python/method.rst' %}
{% endfor %}
{% endif %}

{% if properties %}
Properties
----------
{% for prop in properties|sort(attribute='name') %}
    {% include 'python/property.rst' %}
{% endfor %}
{% endif %}
```

### 4. Enhanced Signature Display

```jinja2
{# Custom signature formatting #}
.. py:{{ obj.type }}:: {{ obj.name }}
   {%- if obj.args %}(
   {%- for arg in obj.args %}
      {{ arg }}
      {%- if obj.defaults[loop.index0] is defined %} = {{ obj.defaults[loop.index0] }}{% endif %}
      {%- if not loop.last %},{% endif %}
   {%- endfor %})
   {%- endif %}
   {%- if obj.returns %} -> {{ obj.returns|format_annotation }}{% endif %}
```

## Common Customization Pitfalls

### 1. Template Extension Issue

```jinja2
{# ❌ DON'T DO THIS - Causes infinite recursion #}
{% extends 'python/class.rst' %}

{# ✅ DO THIS - Copy and modify #}
{# Copy entire default template and customize #}
```

### 2. Missing Attribute Checks

```jinja2
{# ❌ Unsafe - might error if bases is None #}
{% for base in obj.bases %}

{# ✅ Safe - check existence first #}
{% if obj.bases %}
    {% for base in obj.bases %}
```

### 3. reStructuredText Formatting

```jinja2
{# ❌ Wrong - indentation matters in rST #}
{% if obj.parameters %}
:Parameters:
{% for param in obj.parameters %}
* {{ param.name }}
{% endfor %}
{% endif %}

{# ✅ Correct - proper indentation #}
{% if obj.parameters %}
:Parameters:
   {% for param in obj.parameters %}
   * {{ param.name }}
   {% endfor %}
{% endif %}
```

## Performance Optimization

### 1. Cache Expensive Operations

```python
# In autoapi_prepare_jinja_env
@lru_cache(maxsize=128)
def get_inheritance_tree(class_id):
    """Cache inheritance tree calculation."""
    # Expensive tree building logic
    return tree

jinja_env.globals['get_inheritance_tree'] = get_inheritance_tree
```

### 2. Minimize Template Logic

```jinja2
{# ❌ Complex logic in template #}
{% set sorted_methods = [] %}
{% for method in obj.methods %}
    {% if not method.name.startswith('_') and method.is_public %}
        {% do sorted_methods.append(method) %}
    {% endif %}
{% endfor %}

{# ✅ Use filters and Python functions #}
{% set sorted_methods = obj.methods|public_only|sort(attribute='name') %}
```

## Next Steps for Implementation

1. **Create template directory structure**

   ```bash
   mkdir -p _autoapi_templates/python/partials
   ```

2. **Copy default templates to customize**

   ```bash
   cp -r /path/to/autoapi/templates/python/* _autoapi_templates/python/
   ```

3. **Set up Jinja2 environment customization** in conf.py

4. **Create type-specific partial templates**

5. **Test with sample documentation**

6. **Iterate on design and functionality**
