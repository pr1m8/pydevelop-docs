# Jinja2 Research for AutoAPI Template Customization

**Created**: 2025-01-30  
**Purpose**: Comprehensive Jinja2 research for Issue #6 - AutoAPI template improvement  
**Status**: Research Complete

## 1. Core Jinja2 Concepts

### Template Syntax Basics

#### Variables and Expressions

```jinja2
{{ variable }}                  # Simple variable output
{{ user.name }}                 # Attribute access
{{ items[0] }}                  # Index access
{{ dict['key'] }}               # Dictionary access
{{ obj.method() }}              # Method calls
{{ 2 + 2 }}                     # Math expressions
```

#### Control Structures

```jinja2
{# Conditionals #}
{% if obj.methods %}
    <h2>Methods</h2>
    ...
{% elif obj.attributes %}
    <h2>Attributes Only</h2>
{% else %}
    <p>No members found</p>
{% endif %}

{# Loops #}
{% for method in obj.methods %}
    <div class="method">
        {{ method.name }}{{ method.signature }}
        {# Loop variables available #}
        {% if loop.first %}<hr>{% endif %}
        {% if loop.last %}<hr>{% endif %}
        Index: {{ loop.index }} of {{ loop.length }}
    </div>
{% endfor %}

{# Loop with condition #}
{% for item in items if item.is_public %}
    {{ item }}
{% endfor %}
```

#### Template Inheritance

```jinja2
{# base_class.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{% block summary %}
{{ obj.short_description }}
{% endblock %}

{% block content %}
Default content here
{% endblock %}

{# pydantic_class.rst #}
{% extends "base_class.rst" %}

{% block content %}
.. pydantic-model:: {{ obj.name }}
   :module: {{ obj.module }}

   {% if obj.fields %}
   **Fields:**
   {% for field in obj.fields %}
   * **{{ field.name }}** ({{ field.type }}): {{ field.description }}
   {% endfor %}
   {% endif %}
{% endblock %}
```

### Macros (Reusable Components)

```jinja2
{# Define reusable macro #}
{% macro render_parameters(params, show_types=True) %}
    {% if params %}
    :Parameters:
        {% for param in params %}
        * **{{ param.name }}**
          {%- if show_types and param.type %} ({{ param.type }}){% endif %}
          {%- if param.description %} -- {{ param.description }}{% endif %}
        {% endfor %}
    {% endif %}
{% endmacro %}

{# Use macro #}
{{ render_parameters(obj.parameters) }}
```

### Filters

```jinja2
{{ obj.name|upper }}                    # CLASSNAME
{{ obj.name|lower }}                    # classname
{{ obj.name|title }}                    # Classname
{{ obj.docstring|truncate(100) }}       # First 100 chars...
{{ obj.docstring|wordwrap(72) }}        # Wrap at 72 chars
{{ items|length }}                      # Count items
{{ items|join(', ') }}                  # item1, item2, item3
{{ value|default('N/A') }}              # Default if None/undefined
{{ text|indent(4) }}                    # Indent by 4 spaces
{{ html|safe }}                         # Don't escape HTML
```

### Whitespace Control

```jinja2
{# Remove whitespace before/after #}
{%- if condition -%}
    content
{%- endif -%}

{# Preserve whitespace #}
{% raw %}
    {{ this won't be processed }}
{% endraw %}
```

## 2. AutoAPI-Specific Context

### Available Variables in AutoAPI Templates

#### Main Object (`obj`)

```jinja2
obj.name                # Object name (e.g., "MyClass")
obj.type                # Type: "class", "function", "module", "method", "attribute"
obj.id                  # Full dotted path (e.g., "package.module.MyClass")
obj.docstring          # Full docstring
obj.short_description  # First line of docstring
obj.summary            # Processed summary
obj.file               # Source file path
obj.encoding           # File encoding
obj.line               # Line number in source
```

#### Class-Specific Attributes

```jinja2
obj.bases              # List of base classes
obj.methods            # List of method objects
obj.attributes         # List of attribute objects
obj.properties         # List of property objects
obj.is_abstract        # True if abstract class
obj.decorators         # List of decorators
obj.metaclass          # Metaclass if any
```

#### Method/Function Attributes

```jinja2
obj.parameters         # List of parameter objects
obj.returns            # Return type annotation
obj.return_description # Return description from docstring
obj.raises             # List of exceptions raised
obj.signature          # Full signature string
obj.is_staticmethod    # True if @staticmethod
obj.is_classmethod     # True if @classmethod
obj.is_async           # True if async function
```

#### Module Attributes

```jinja2
obj.all                # __all__ exports
obj.children           # All child objects
obj.submodules         # Child modules
obj.subpackages        # Child packages
```

### AutoAPI Configuration Variables

```jinja2
autoapi_options        # List of enabled options
include_summaries      # Whether to show summaries
own_page_types         # Which types get own pages
display               # Display settings
```

## 3. Custom Template Patterns for AutoAPI

### Progressive Disclosure Pattern

```jinja2
{# _autoapi_templates/python/class.rst #}

{{ obj.name }}
{{ "=" * obj.name|length }}

{# Essential information first #}
.. py:class:: {{ obj.name }}{% if obj.args %}({{ obj.args|join(', ') }}){% endif %}
   :module: {{ obj.module }}

   {% if obj.short_description %}
   {{ obj.short_description }}
   {% endif %}

{# Collapsible sections for details #}
{% if obj.docstring and obj.docstring != obj.short_description %}
.. dropdown:: Full Description
   :animate: fade-in-slide-down

   {{ obj.docstring|indent(3) }}
{% endif %}

{% if obj.parameters %}
.. dropdown:: Constructor Parameters ({{ obj.parameters|length }})
   :animate: fade-in-slide-down

   {{ render_parameters(obj.parameters)|indent(3) }}
{% endif %}

{% if obj.methods %}
.. dropdown:: Methods ({{ obj.methods|length }})
   :animate: fade-in-slide-down
   :open:

   {% for method in obj.methods %}
   .. automethod:: {{ method.id }}
   {% endfor %}
{% endif %}
```

### Type-Specific Rendering

```jinja2
{# Detect and render based on type #}
{% if 'BaseModel' in obj.bases|map(attribute='name')|list %}
    {# Pydantic Model - Special rendering #}
    {% include 'python/pydantic_model.rst' %}
{% elif 'Agent' in obj.bases|map(attribute='name')|list %}
    {# Agent class - Show tools, engine config #}
    {% include 'python/agent_class.rst' %}
{% elif 'Enum' in obj.bases|map(attribute='name')|list %}
    {# Enum - Show values clearly #}
    {% include 'python/enum_class.rst' %}
{% else %}
    {# Standard class rendering #}
    {% include 'python/standard_class.rst' %}
{% endif %}
```

### Enhanced Method Display

```jinja2
{% macro render_method(method) %}
.. py:method:: {{ method.name }}{{ method.signature }}
   {% if method.is_async %}:async:{% endif %}
   {% if method.is_classmethod %}:classmethod:{% endif %}
   {% if method.is_staticmethod %}:staticmethod:{% endif %}

   {% if method.short_description %}
   {{ method.short_description }}
   {% endif %}

   {% if method.parameters %}
   :Parameters:
      {% for param in method.parameters %}
      * **{{ param.name }}**
        {%- if param.annotation %} ({{ param.annotation }}){% endif %}
        {%- if param.default %} = ``{{ param.default }}``{% endif %}
        {%- if param.description %} -- {{ param.description }}{% endif %}
      {% endfor %}
   {% endif %}

   {% if method.returns %}
   :Returns: {{ method.returns }}
      {% if method.return_description %}{{ method.return_description }}{% endif %}
   {% endif %}

   {% if method.raises %}
   :Raises:
      {% for exception in method.raises %}
      * **{{ exception.type }}** -- {{ exception.description }}
      {% endfor %}
   {% endif %}
{% endmacro %}
```

### Smart Inheritance Diagram

```jinja2
{% if obj.bases %}
.. mermaid::
   :caption: Class Hierarchy
   :align: center

   graph TD
      {% for base in obj.bases %}
      {{ base.name }} --> {{ obj.name }}
      {% endfor %}

      style {{ obj.name }} fill:#f9f,stroke:#333,stroke-width:4px
{% endif %}
```

## 4. Implementation Strategy

### Template Directory Structure

```
_autoapi_templates/
└── python/
    ├── module.rst          # Module template
    ├── class.rst          # Generic class template
    ├── function.rst       # Function template
    ├── attribute.rst      # Attribute template
    ├── method.rst         # Method template
    ├── _base.rst          # Base template for inheritance
    ├── _macros/           # Reusable macros
    │   ├── common.rst
    │   ├── parameters.rst
    │   └── members.rst
    └── _partials/         # Type-specific templates
        ├── pydantic_model.rst
        ├── agent_class.rst
        ├── enum_class.rst
        └── standard_class.rst
```

### Configuration in conf.py

```python
# Set custom template directory
autoapi_template_dir = '_autoapi_templates'

# Customize Jinja environment
def autoapi_prepare_jinja_env(jinja_env):
    # Add custom filters
    jinja_env.filters['format_type'] = format_type_annotation
    jinja_env.filters['github_link'] = create_github_link

    # Add global functions
    jinja_env.globals['get_icon'] = get_type_icon
    jinja_env.globals['is_pydantic'] = is_pydantic_model

    # Add tests
    jinja_env.tests['public'] = lambda obj: not obj.name.startswith('_')
```

## 5. Best Practices

### Performance Considerations

1. Keep logic simple in templates
2. Pre-process complex data in Python
3. Use template caching when possible
4. Minimize template inheritance depth

### Debugging Tips

```jinja2
{# Debug output #}
<pre>{{ obj|pprint }}</pre>

{# Check variable existence #}
{% if obj.some_attr is defined %}
    {{ obj.some_attr }}
{% endif %}

{# Type checking #}
{{ obj.type }}  {# See what type this is #}
{{ obj.bases|map(attribute='name')|list }}  {# List base class names #}
```

### Common Gotchas

1. AutoAPI doesn't support extending default templates (causes recursion)
2. Must copy entire template and modify
3. Some Sphinx directives require specific formatting
4. Whitespace matters in reStructuredText output

## Next Steps

1. Set up test environment with sample classes
2. Create base template structure
3. Implement progressive disclosure system
4. Design beautiful visual layouts
5. Test with real Haive documentation
