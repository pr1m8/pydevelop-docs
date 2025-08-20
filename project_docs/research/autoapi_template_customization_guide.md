# Sphinx AutoAPI Template Customization Guide

**Created**: 2025-01-30
**Purpose**: Comprehensive guide for customizing Sphinx AutoAPI templates
**Version**: Based on sphinx-autoapi 3.6.0
**Status**: Research Complete

## Table of Contents

1. [AutoAPI Template Architecture](#autoapi-template-architecture)
2. [Template Context Variables](#template-context-variables)
3. [Template Customization Process](#template-customization-process)
4. [Jinja2 Environment Configuration](#jinja2-environment-configuration)
5. [Object Attributes Reference](#object-attributes-reference)
6. [Best Practices](#best-practices)
7. [Common Pitfalls](#common-pitfalls)
8. [Advanced Patterns](#advanced-patterns)

## AutoAPI Template Architecture

### Template Directory Structure

AutoAPI uses a hierarchical template structure organized by language type:

```
_autoapi_templates/
└── python/
    ├── index.rst           # Main API index page
    ├── module.rst          # Module documentation
    ├── package.rst         # Package documentation
    ├── class.rst           # Class documentation
    ├── function.rst        # Function documentation
    ├── method.rst          # Method documentation
    ├── attribute.rst       # Attribute documentation
    ├── property.rst        # Property documentation
    ├── data.rst            # Module-level variable
    └── exception.rst       # Exception class
```

### Template Search Path

AutoAPI searches for templates in this order:

1. Custom template directory (if `autoapi_template_dir` is set)
2. Default templates in `autoapi/templates/` within the package

### Template Naming Convention

Templates are located using the pattern: `{language}/{type}.rst`

- `language`: Usually "python" for Python projects
- `type`: Object type (class, function, module, etc.)

## Template Context Variables

### Standard Context Variables

Every template receives these context variables:

```python
{
    'autoapi_options': list,        # Configuration options
    'include_summaries': bool,      # Include summary tables
    'obj': PythonPythonMapper,      # The object being documented
    'own_page_types': set,          # Types with own pages
    'sphinx_version': tuple,        # Sphinx version info
}
```

### Configuration Options in Context

The `autoapi_options` list may contain:

- `'members'` - Show module/class members
- `'undoc-members'` - Include undocumented members
- `'private-members'` - Include private members (\_private)
- `'special-members'` - Include special methods (**init**, etc.)
- `'show-inheritance'` - Show class inheritance
- `'show-module-summary'` - Show module summary tables
- `'imported-members'` - Show imported objects

## Template Customization Process

### 1. Setting Up Custom Templates

```python
# In conf.py
autoapi_template_dir = '_autoapi_templates'  # Relative or absolute path
```

### 2. Creating Template Structure

```bash
mkdir -p _autoapi_templates/python
cp -r /path/to/autoapi/templates/python/* _autoapi_templates/python/
```

### 3. Customizing Templates

Example custom class template (`_autoapi_templates/python/class.rst`):

```jinja2
{# Custom class template with enhanced features #}
{% if not obj.display %}
:orphan:
{% endif %}

{{ obj.name }}
{{ "=" * obj.name|length }}

{# Type detection #}
{% set bases_str = obj.bases|join(' ') %}
{% set is_pydantic = 'BaseModel' in bases_str %}
{% set is_dataclass = '@dataclass' in (obj.docstring or '') %}
{% set is_agent = 'Agent' in bases_str %}

{# Custom rendering based on type #}
{% if is_pydantic %}
.. py:class:: {{ obj.name }}
   :module: {{ obj.module }}

   **Pydantic Model**

   {% if obj.docstring %}
   {{ obj.docstring|indent(3, True) }}
   {% endif %}

   **Fields:**

   {% for member in obj.children if member.type == 'attribute' %}
   * **{{ member.name }}**: {{ member.annotation or 'Any' }}
     {% if member.docstring %}
     - {{ member.docstring|truncate(100) }}
     {% endif %}
   {% endfor %}

{% elif is_agent %}
.. py:class:: {{ obj.name }}
   :module: {{ obj.module }}

   **Agent Class**

   {% if obj.docstring %}
   {{ obj.docstring|indent(3, True) }}
   {% endif %}

   **Configuration:**

   {% for attr in obj.children if attr.name in ['engine', 'tools', 'prompt_template'] %}
   * **{{ attr.name }}**: {{ attr.annotation or 'Not specified' }}
   {% endfor %}

{% else %}
.. py:class:: {{ obj.name }}
   :module: {{ obj.module }}

   {% if obj.docstring %}
   {{ obj.docstring|indent(3, True) }}
   {% endif %}
{% endif %}

{# Methods section with grouping #}
{% set methods = obj.children|selectattr('type', 'equalto', 'method')|list %}
{% if methods %}

**Methods:**

{% for method in methods|sort(attribute='name') %}
.. py:method:: {{ method.name }}{{ method.args }}

   {% if method.docstring %}
   {{ method.docstring|indent(3, True) }}
   {% endif %}
{% endfor %}
{% endif %}
```

## Jinja2 Environment Configuration

### Setting Up autoapi_prepare_jinja_env

```python
# In conf.py
def autoapi_prepare_jinja_env(jinja_env):
    """Customize Jinja2 environment for AutoAPI templates."""

    # Add custom filters
    jinja_env.filters['format_type'] = format_type_annotation
    jinja_env.filters['github_link'] = create_github_link
    jinja_env.filters['truncate_smart'] = truncate_at_sentence

    # Add custom tests
    jinja_env.tests['pydantic_model'] = is_pydantic_model
    jinja_env.tests['public_api'] = is_public_api
    jinja_env.tests['deprecated'] = is_deprecated

    # Add global functions
    jinja_env.globals['get_icon'] = get_type_icon
    jinja_env.globals['group_by_kind'] = group_members_by_kind

    # Add custom variables
    jinja_env.globals['project_name'] = 'PyDevelop-Docs'
    jinja_env.globals['api_version'] = '3.0.0'
```

### Custom Filter Examples

```python
def format_type_annotation(annotation):
    """Format type annotations for better readability."""
    if not annotation:
        return 'Any'

    # Simplify Union types
    annotation = annotation.replace('Union[', '').replace(']', '')
    annotation = annotation.replace('Optional[', '').rstrip(']') + ' | None'

    # Format long annotations
    if len(annotation) > 50:
        parts = annotation.split(',')
        return ',\n    '.join(parts)

    return annotation

def create_github_link(obj):
    """Create GitHub link to source code."""
    if hasattr(obj, 'file_path') and obj.file_path:
        base_url = "https://github.com/user/repo/blob/main"
        return f"{base_url}/{obj.file_path}#L{obj.line_number}"
    return None

def truncate_at_sentence(text, length=100):
    """Truncate text at sentence boundary."""
    if len(text) <= length:
        return text

    # Find sentence end near length
    end_marks = ['. ', '! ', '? ']
    for mark in end_marks:
        pos = text.find(mark, length - 20, length + 20)
        if pos != -1:
            return text[:pos + 1]

    return text[:length] + '...'
```

### Custom Test Examples

```python
def is_pydantic_model(obj):
    """Check if object is a Pydantic model."""
    if hasattr(obj, 'bases'):
        bases_str = ' '.join(str(base) for base in obj.bases)
        return 'BaseModel' in bases_str or 'BaseSettings' in bases_str
    return False

def is_public_api(obj):
    """Check if object is part of public API."""
    if hasattr(obj, 'name'):
        return not obj.name.startswith('_')
    return True

def is_deprecated(obj):
    """Check if object is marked as deprecated."""
    if hasattr(obj, 'docstring') and obj.docstring:
        return 'deprecated' in obj.docstring.lower()
    return False
```

### Global Function Examples

```python
def get_type_icon(obj_type):
    """Return icon for object type."""
    icons = {
        'class': '🏛️',
        'function': '⚡',
        'method': '🔧',
        'property': '📦',
        'module': '📁',
        'package': '📦',
        'exception': '⚠️',
    }
    return icons.get(obj_type, '📄')

def group_members_by_kind(members):
    """Group members by their kind."""
    groups = {
        'properties': [],
        'methods': [],
        'attributes': [],
        'class_methods': [],
        'static_methods': [],
    }

    for member in members:
        if member.type == 'property':
            groups['properties'].append(member)
        elif member.type == 'method':
            if hasattr(member, 'is_classmethod') and member.is_classmethod:
                groups['class_methods'].append(member)
            elif hasattr(member, 'is_staticmethod') and member.is_staticmethod:
                groups['static_methods'].append(member)
            else:
                groups['methods'].append(member)
        elif member.type == 'attribute':
            groups['attributes'].append(member)

    return groups
```

## Object Attributes Reference

### Common Object Attributes

All AutoAPI objects have these base attributes:

```python
obj.name            # Short name (e.g., "MyClass")
obj.id              # Fully qualified name (e.g., "package.module.MyClass")
obj.type            # Object type: 'class', 'function', 'module', etc.
obj.docstring       # Full docstring text
obj.short_description  # First line of docstring
obj.summary         # Processed summary
obj.file_path       # Source file path
obj.line_number     # Line number in source
```

### Class-Specific Attributes

```python
obj.bases           # List of base class names
obj.children        # All child objects (methods, attributes, etc.)
obj.methods         # List of method objects
obj.attributes      # List of attribute objects
obj.properties      # List of property objects
obj.is_abstract     # True if abstract class
obj.decorators      # List of decorator names
obj.metaclass       # Metaclass name if any
```

### Function/Method Attributes

```python
obj.args            # Function arguments as string
obj.returns         # Return type annotation
obj.return_description  # Return description from docstring
obj.raises          # List of exceptions raised
obj.signature       # Full signature string
obj.is_async        # True if async function
obj.is_classmethod  # True if @classmethod
obj.is_staticmethod # True if @staticmethod
obj.decorators      # List of decorators
```

### Module/Package Attributes

```python
obj.all             # Contents of __all__
obj.children        # All module contents
obj.submodules      # Child modules
obj.subpackages     # Child packages
obj.functions       # Module-level functions
obj.classes         # Module-level classes
obj.variables       # Module-level variables
```

## Best Practices

### 1. Progressive Enhancement

Start with default templates and gradually customize:

```jinja2
{# Start simple #}
{% include "python/class.rst" %}

{# Add enhancements #}
{% if obj is pydantic_model %}
  .. note:: This is a Pydantic model with automatic validation.
{% endif %}
```

### 2. Type Detection Patterns

```jinja2
{# Robust type detection #}
{% set base_names = obj.bases|map(attribute='name')|list %}
{% set is_pydantic = 'BaseModel' in base_names or 'BaseSettings' in base_names %}
{% set is_enum = 'Enum' in base_names or 'IntEnum' in base_names %}
{% set has_dataclass_decorator = obj.decorators and '@dataclass' in obj.decorators|join('') %}
```

### 3. Conditional Rendering

```jinja2
{# Show different content based on options #}
{% if 'private-members' in autoapi_options %}
  {% set members = obj.children %}
{% else %}
  {% set members = obj.children|rejectattr('name', 'match', '^_')|list %}
{% endif %}
```

### 4. Performance Optimization

```jinja2
{# Cache expensive operations #}
{% set sorted_methods = obj.methods|sort(attribute='name') %}
{% set public_methods = sorted_methods|rejectattr('name', 'match', '^_')|list %}

{# Use the cached results #}
{% for method in public_methods %}
  {# render method #}
{% endfor %}
```

## Common Pitfalls

### 1. Template Inheritance Issues

**Problem**: Extending default templates causes RecursionError

```jinja2
{# DON'T DO THIS #}
{% extends "python/class.rst" %}
```

**Solution**: Copy and modify entire template

### 2. Missing Context Checks

**Problem**: Accessing undefined attributes

```jinja2
{# This may fail #}
{{ obj.bases[0] }}
```

**Solution**: Always check existence

```jinja2
{% if obj.bases %}
  {{ obj.bases[0] }}
{% endif %}
```

### 3. Whitespace Issues

**Problem**: Extra whitespace in reStructuredText

```jinja2
{% for item in items %}
{{ item }}
{% endfor %}
```

**Solution**: Use whitespace control

```jinja2
{%- for item in items %}
{{ item }}
{%- endfor %}
```

### 4. Complex Logic in Templates

**Problem**: Templates become unmaintainable
**Solution**: Move logic to Python functions in `autoapi_prepare_jinja_env`

## Advanced Patterns

### 1. Multi-Stage Template Processing

```python
def autoapi_prepare_jinja_env(jinja_env):
    """Multi-stage template processing."""

    class TemplateProcessor:
        def __init__(self):
            self.processed_objects = set()

        def process_obj(self, obj):
            """Process object before rendering."""
            if obj.id not in self.processed_objects:
                # Add custom attributes
                obj.custom_category = self.categorize(obj)
                obj.complexity_score = self.calculate_complexity(obj)
                self.processed_objects.add(obj.id)
            return obj

        def categorize(self, obj):
            """Categorize object by type."""
            if hasattr(obj, 'bases'):
                bases_str = ' '.join(str(b) for b in obj.bases)
                if 'ABC' in bases_str:
                    return 'abstract'
                elif 'BaseModel' in bases_str:
                    return 'pydantic'
                elif 'Exception' in bases_str:
                    return 'exception'
            return 'standard'

        def calculate_complexity(self, obj):
            """Calculate complexity score."""
            score = 0
            if hasattr(obj, 'children'):
                score += len(obj.children)
            if hasattr(obj, 'methods'):
                score += len(obj.methods) * 2
            return score

    processor = TemplateProcessor()
    jinja_env.filters['process'] = processor.process_obj
```

### 2. Dynamic Template Selection

```jinja2
{# Dynamic template selection based on object properties #}
{% set template_name = 'standard_class.rst' %}
{% if obj is pydantic_model %}
  {% set template_name = 'pydantic_class.rst' %}
{% elif obj is dataclass %}
  {% set template_name = 'dataclass_class.rst' %}
{% elif 'ABC' in obj.bases|join(' ') %}
  {% set template_name = 'abstract_class.rst' %}
{% endif %}

{% include 'python/partials/' ~ template_name %}
```

### 3. Macro Libraries

Create reusable macro libraries (`_autoapi_templates/python/macros.rst`):

```jinja2
{# Reusable macro library #}
{% macro render_parameters(params, show_types=True, show_defaults=True) %}
  {% if params %}
  :Parameters:
    {% for param in params %}
    * **{{ param.name }}**
      {%- if show_types and param.annotation %} ({{ param.annotation }}){% endif %}
      {%- if show_defaults and param.default %} = {{ param.default }}{% endif %}
      {%- if param.description %} -- {{ param.description }}{% endif %}
    {% endfor %}
  {% endif %}
{% endmacro %}

{% macro render_inheritance_diagram(obj, style='mermaid') %}
  {% if obj.bases and style == 'mermaid' %}
  .. mermaid::

     graph TD
       {% for base in obj.bases %}
       {{ base }} --> {{ obj.name }}
       {% endfor %}

       classDef current fill:#f9f,stroke:#333,stroke-width:4px
       class {{ obj.name }} current
  {% endif %}
{% endmacro %}
```

### 4. Context Enrichment

```python
def enrich_context(app, pagename, templatename, context, doctree):
    """Enrich template context with additional data."""
    if 'autoapi' in pagename:
        # Add project-wide statistics
        context['total_classes'] = count_classes()
        context['total_functions'] = count_functions()
        context['api_coverage'] = calculate_coverage()

        # Add navigation helpers
        context['next_class'] = get_next_class(context.get('obj'))
        context['prev_class'] = get_prev_class(context.get('obj'))

def setup(app):
    app.connect('html-page-context', enrich_context)
```

## Summary

Sphinx AutoAPI template customization provides powerful capabilities for creating beautiful, informative API documentation. Key points:

1. **Template Structure**: Follow the `language/type.rst` pattern
2. **Context Variables**: Rich object data available in templates
3. **Jinja2 Environment**: Extensible with filters, tests, and globals
4. **Object Attributes**: Comprehensive metadata for all Python objects
5. **Best Practices**: Start simple, use type detection, optimize performance
6. **Advanced Patterns**: Multi-stage processing, dynamic templates, macro libraries

With these tools and patterns, you can create API documentation that is both beautiful and highly functional, tailored to your project's specific needs.
