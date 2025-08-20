# Intelligent Template System Architecture

**Created**: 2025-01-30  
**Purpose**: Master template system design leveraging all 45+ extensions with Jinja2  
**Status**: Architecture Design

## Template System Philosophy

Our intelligent template system combines:

- **Jinja2's Power**: Full templating capabilities
- **Extension Integration**: All 45+ Sphinx extensions
- **Progressive Enhancement**: Start simple, enhance progressively
- **Type Awareness**: Different rendering for different object types
- **Mobile-First**: Responsive design built-in
- **Performance**: Optimized for large documentation sets

## Core Architecture

### 1. Template Hierarchy

```
_autoapi_templates/
├── python/
│   ├── _base/                      # Base templates for inheritance
│   │   ├── foundation.j2           # Core HTML/RST structure
│   │   ├── progressive.j2          # Progressive disclosure base
│   │   └── responsive.j2           # Mobile-responsive base
│   │
│   ├── _components/                # Reusable component library
│   │   ├── navigation.j2           # sphinx_treeview integration
│   │   ├── diagrams.j2             # mermaid, graphviz integration
│   │   ├── code_blocks.j2          # copybutton, exec_code integration
│   │   ├── metadata.j2             # SEO, opengraph integration
│   │   ├── interactive.j2          # tabs, toggles, tippy integration
│   │   └── media.j2                # images, videos, emojis
│   │
│   ├── _filters/                   # Custom Jinja2 filters
│   │   ├── type_filters.py         # Type annotation formatting
│   │   ├── doc_filters.py          # Documentation processing
│   │   └── extension_filters.py    # Extension-specific filters
│   │
│   ├── _macros/                    # Macro library
│   │   ├── sphinx_design.j2        # Card, grid, dropdown macros
│   │   ├── code_rendering.j2       # Enhanced code display
│   │   ├── type_specific.j2        # Type-aware rendering
│   │   └── accessibility.j2        # A11y enhancements
│   │
│   ├── module.rst                  # Smart module template
│   ├── class.rst                   # Intelligent class template
│   ├── function.rst                # Enhanced function template
│   ├── method.rst                  # Rich method template
│   ├── attribute.rst               # Detailed attribute template
│   └── index.rst                   # Beautiful index template
│
└── config/
    ├── jinja_env.py                # Jinja2 environment setup
    ├── extension_registry.py       # Extension configuration
    └── template_config.yaml        # Template behavior config
```

### 2. Master Base Template

```jinja2
{# _base/foundation.j2 - Core template with ALL extension integration #}

{# Extension capability detection #}
{% set has_mermaid = 'sphinxcontrib.mermaid' in extensions %}
{% set has_design = 'sphinx_design' in extensions %}
{% set has_toggles = 'sphinx_togglebutton' in extensions %}
{% set has_tabs = 'sphinx_tabs' in extensions %}
{% set has_copybutton = 'sphinx_copybutton' in extensions %}

{# Template blocks for inheritance #}
{% block document %}
{{ obj.name }}
{{ "=" * obj.name|length }}

{# Metadata integration (SEO, social) #}
{% block metadata %}
{% if 'sphinxcontrib.opengraph' in extensions %}
.. meta::
   :description: {{ obj.short_description|truncate(160) }}
   :keywords: {{ obj.type }}, {{ obj.module }}, {{ project }}
   :og:title: {{ obj.name }} - {{ project }} Documentation
   :og:description: {{ obj.short_description }}
   :og:type: article
{% endif %}
{% endblock metadata %}

{# Navigation enhancement #}
{% block navigation %}
{% if 'sphinx_treeview' in extensions %}
.. raw:: html

   <div class="treeview-context" data-current="{{ obj.id }}">
   </div>
{% endif %}
{% endblock navigation %}

{# Main content with progressive disclosure #}
{% block content %}
{% if has_design and has_toggles %}
    {{ render_progressive_content() }}
{% else %}
    {{ render_standard_content() }}
{% endif %}
{% endblock content %}

{# Footer with timestamps and edit links #}
{% block footer %}
{% if 'sphinx_last_updated_by_git' in extensions %}
.. container:: document-meta

   Last updated: |today|
   {% if 'sphinx.ext.githubpages' in extensions %}
   `Edit on GitHub <{{ github_edit_url }}>`_
   {% endif %}
{% endif %}
{% endblock footer %}
{% endblock document %}
```

### 3. Component Library Integration

```jinja2
{# _components/diagrams.j2 - Smart diagram rendering #}

{% macro render_class_diagram(obj) %}
{% if has_mermaid %}
    {# Use Mermaid for modern, interactive diagrams #}
    .. mermaid::
       :caption: {{ obj.name }} Class Structure
       :align: center

       classDiagram
       {% for base in obj.bases %}
       {{ base.name }} <|-- {{ obj.name }}
       {% endfor %}

       class {{ obj.name }} {
           {% for attr in obj.attributes[:5] %}
           +{{ attr.name }}{% if attr.annotation %}: {{ attr.annotation }}{% endif %}
           {% endfor %}
           {% if obj.attributes|length > 5 %}
           ...
           {% endif %}
           {% for method in obj.methods[:5] %}
           +{{ method.name }}(){% if method.returns %}: {{ method.returns }}{% endif %}
           {% endfor %}
           {% if obj.methods|length > 5 %}
           ...
           {% endif %}
       }
{% elif 'sphinx.ext.inheritance_diagram' in extensions %}
    {# Fallback to graphviz #}
    .. inheritance-diagram:: {{ obj.id }}
       :parts: 1
{% endif %}
{% endmacro %}

{% macro render_sequence_diagram(interactions) %}
{% if has_mermaid %}
    .. mermaid::

       sequenceDiagram
       {% for interaction in interactions %}
       {{ interaction.from }} ->> {{ interaction.to }}: {{ interaction.message }}
       {% endfor %}
{% endif %}
{% endmacro %}
```

### 4. Progressive Disclosure System

```jinja2
{# _components/interactive.j2 - Progressive disclosure with multiple extensions #}

{% macro progressive_class_display(obj) %}
{# Level 1: Essential Information (Always visible) #}
.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: {{ obj.name }}
      :class-header: bg-primary text-white
      :class-body: essential-info

      {{ obj.short_description }}

      .. code-block:: python
         :class: no-copybutton

         {{ obj.signature }}

{# Level 2: Common Use Cases (One click away) #}
{% if obj.examples %}
.. dropdown:: Quick Examples
   :animate: fade-in-slide-down
   :class-container: examples-section

   .. tab-set::

      {% for example in obj.examples %}
      .. tab-item:: {{ example.title }}

         .. code-block:: python
            :class: copybutton

            {{ example.code }}

         {% if example.output %}
         **Output:**

         .. code-block:: text

            {{ example.output }}
         {% endif %}
      {% endfor %}
{% endif %}

{# Level 3: Detailed API (Expandable sections) #}
.. dropdown:: Full API Reference
   :animate: fade-in-slide-down
   :open:

   .. tab-set::

      {% if obj.methods %}
      .. tab-item:: Methods ({{ obj.methods|length }})

         {% for method in obj.methods|sort(attribute='name') %}
         .. toggle::

            .. py:method:: {{ method.name }}{{ method.signature }}

               {{ method.docstring }}
         {% endfor %}
      {% endif %}

      {% if obj.attributes %}
      .. tab-item:: Attributes ({{ obj.attributes|length }})

         {{ render_attributes_table(obj.attributes) }}
      {% endif %}

      {% if obj.properties %}
      .. tab-item:: Properties ({{ obj.properties|length }})

         {% for prop in obj.properties %}
         .. toggle::

            {{ render_property(prop) }}
         {% endfor %}
      {% endif %}

{# Level 4: Advanced Information (Deep dive) #}
{% if obj.source_code %}
.. dropdown:: Source Code
   :animate: fade-in-slide-down
   :class-container: source-code-section

   .. literalinclude:: {{ obj.file }}
      :pyobject: {{ obj.name }}
      :class: copybutton
      :linenos:
      :emphasize-lines: {{ obj.important_lines|join(',') }}
{% endif %}
{% endmacro %}
```

### 5. Type-Specific Intelligence

```jinja2
{# _macros/type_specific.j2 - Smart rendering based on object type #}

{% macro render_by_type(obj) %}
{% set base_names = obj.bases|map(attribute='name')|list %}

{% if 'BaseModel' in base_names %}
    {{ render_pydantic_model(obj) }}
{% elif 'Agent' in base_names %}
    {{ render_ai_agent(obj) }}
{% elif 'Tool' in base_names %}
    {{ render_langchain_tool(obj) }}
{% elif 'Enum' in base_names %}
    {{ render_enum_class(obj) }}
{% elif 'Exception' in base_names %}
    {{ render_exception_class(obj) }}
{% elif obj.is_dataclass %}
    {{ render_dataclass(obj) }}
{% else %}
    {{ render_standard_class(obj) }}
{% endif %}
{% endmacro %}

{% macro render_pydantic_model(obj) %}
.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: Pydantic Model: {{ obj.name }}
      :class-header: bg-info

      .. mermaid::

         graph LR
         A[Input Data] --> B[{{ obj.name }}]
         B --> C[Validated Output]

         style B fill:#e1f5fe,stroke:#01579b,stroke-width:2px

      **Field Definitions:**

      .. list-table::
         :header-rows: 1
         :class: field-definitions

         * - Field
           - Type
           - Required
           - Description
         {% for field in obj.fields %}
         * - ``{{ field.name }}``
           - :py:data:`{{ field.type }}`
           - {% if field.required %}✓{% else %}✗{% endif %}
           - {{ field.description|default('—') }}
         {% endfor %}

      {% if obj.validators %}
      .. admonition:: Validators
         :class: tip

         {% for validator in obj.validators %}
         * **{{ validator.name }}**: {{ validator.fields|join(', ') }}
         {% endfor %}
      {% endif %}
{% endmacro %}
```

### 6. Extension-Specific Enhancements

```jinja2
{# Extension feature detection and progressive enhancement #}

{% macro enhance_with_extensions(content, obj) %}
{# Code enhancement #}
{% if 'sphinx_copybutton' in extensions %}
    {% set content = content|add_copybutton %}
{% endif %}

{% if 'sphinx_codeautolink' in extensions %}
    {% set content = content|add_codelinks(obj.imports) %}
{% endif %}

{# Visual enhancement #}
{% if 'sphinxemoji' in extensions %}
    {% set content = content|add_contextual_emojis(obj.type) %}
{% endif %}

{% if 'sphinx_tippy' in extensions %}
    {% set content = content|add_tooltips(obj.terms) %}
{% endif %}

{# Structural enhancement #}
{% if 'sphinx_panels' in extensions or 'sphinx_design' in extensions %}
    {% set content = wrap_in_responsive_grid(content) %}
{% endif %}

{{ content }}
{% endmacro %}
```

### 7. Mobile-Responsive Design

```jinja2
{# _base/responsive.j2 - Mobile-first responsive design #}

{% macro responsive_layout(obj) %}
.. raw:: html

   <div class="responsive-api-container">
      <style>
      @media (max-width: 768px) {
         .responsive-api-container {
            padding: 1rem;
         }
         .method-signature {
            font-size: 0.9rem;
            overflow-x: auto;
         }
         .toggle-button {
            width: 100%;
            text-align: left;
         }
      }
      </style>
   </div>

{# Mobile-optimized content #}
.. container:: mobile-friendly

   {% if is_mobile_view %}
       {{ render_mobile_optimized(obj) }}
   {% else %}
       {{ render_desktop_optimized(obj) }}
   {% endif %}
{% endmacro %}
```

### 8. Performance Optimization

```jinja2
{# Lazy loading and performance features #}

{% macro lazy_load_heavy_content(obj) %}
{% if obj.methods|length > 20 %}
    {# Use virtual scrolling for large lists #}
    .. raw:: html

       <div class="virtual-scroll-container" data-item-count="{{ obj.methods|length }}">
          <div class="loading-placeholder">Loading {{ obj.methods|length }} methods...</div>
       </div>

       <script>
       // Lazy load methods as user scrolls
       document.addEventListener('DOMContentLoaded', function() {
           new VirtualMethodList('{{ obj.id }}', {{ obj.methods|tojson }});
       });
       </script>
{% else %}
    {# Render normally for small lists #}
    {% for method in obj.methods %}
        {{ render_method(method) }}
    {% endfor %}
{% endif %}
{% endmacro %}
```

## Implementation Strategy

### Phase 1: Core Template System (Day 1)

1. Set up Jinja2 environment with custom filters
2. Create base template hierarchy
3. Implement component library structure

### Phase 2: Extension Integration (Day 2-3)

1. Map all 45+ extensions to template features
2. Create extension-aware macros
3. Build progressive enhancement system

### Phase 3: Type-Specific Templates (Day 4)

1. Implement intelligent type detection
2. Create specialized renderers
3. Add domain-specific enhancements

### Phase 4: Interactive Features (Day 5)

1. Add JavaScript enhancements
2. Implement lazy loading
3. Create mobile optimizations

### Phase 5: Polish & Optimization (Day 6)

1. Performance testing
2. Accessibility audit
3. Cross-browser testing

## Configuration Integration

```python
# In conf.py - Configure the intelligent template system

import os
import sys
sys.path.insert(0, os.path.abspath('_autoapi_templates/_filters'))

# AutoAPI configuration
autoapi_template_dir = '_autoapi_templates'
autoapi_own_page_level = 'module'

# Configure Jinja2 environment
def autoapi_prepare_jinja_env(jinja_env):
    # Import custom filters
    from type_filters import (
        format_annotation, add_copybutton,
        add_codelinks, detect_type_category
    )
    from doc_filters import (
        extract_examples, process_docstring,
        extract_important_lines
    )
    from extension_filters import (
        check_extension, add_contextual_emojis,
        wrap_in_responsive_grid
    )

    # Register filters
    jinja_env.filters.update({
        'format_annotation': format_annotation,
        'add_copybutton': add_copybutton,
        'add_codelinks': add_codelinks,
        'detect_type_category': detect_type_category,
        'extract_examples': extract_examples,
        'process_docstring': process_docstring,
        'extract_important_lines': extract_important_lines,
        'check_extension': check_extension,
        'add_contextual_emojis': add_contextual_emojis,
        'wrap_in_responsive_grid': wrap_in_responsive_grid,
    })

    # Add global functions
    jinja_env.globals.update({
        'extensions': extensions,  # Make extensions list available
        'project': project,
        'is_mobile_view': lambda: False,  # Could detect from request
        'render_progressive_content': render_progressive_content,
        'render_standard_content': render_standard_content,
    })

    # Add tests
    jinja_env.tests.update({
        'public': lambda obj: not obj.name.startswith('_'),
        'pydantic_model': lambda obj: 'BaseModel' in [b.name for b in obj.bases],
        'ai_agent': lambda obj: 'Agent' in [b.name for b in obj.bases],
    })
```

## Template Usage Examples

### Example 1: AI Agent Class

```jinja2
{# Intelligent rendering of an AI agent class #}
{% extends "python/_base/progressive.j2" %}

{% block content %}
{{ super() }}

{# AI-specific enhancements #}
{% if obj.tools %}
.. admonition:: Available Tools
   :class: ai-tools

   .. mermaid::

      graph TD
      A[{{ obj.name }}] --> B{Tools}
      {% for tool in obj.tools %}
      B --> {{ loop.index }}[{{ tool.name }}]
      {% endfor %}
{% endif %}

{% if obj.prompts %}
.. dropdown:: Prompt Templates
   :animate: fade-in

   {% for prompt in obj.prompts %}
   .. code-block:: text
      :caption: {{ prompt.name }}

      {{ prompt.template }}
   {% endfor %}
{% endif %}
{% endblock %}
```

### Example 2: Pydantic Model with Validation

```jinja2
{# Smart Pydantic model documentation #}
{% if obj|is_pydantic_model %}
.. grid:: 1 1 2 3
   :gutter: 3

   .. grid-item-card:: Model Schema
      :columns: 12 12 8 8

      .. code-block:: python
         :class: copybutton

         {{ obj.schema_json(indent=2) }}

   .. grid-item-card:: Validation Rules
      :columns: 12 12 4 4

      {% for validator in obj.validators %}
      .. admonition:: {{ validator.name }}
         :class: validation-rule

         **Fields**: {{ validator.fields|join(', ') }}

         {{ validator.description }}
      {% endfor %}

   .. grid-item-card:: Example Usage
      :columns: 12

      .. exec_code::
         :language: python

         from {{ obj.module }} import {{ obj.name }}

         # Create instance
         instance = {{ obj.name }}(
             {% for field in obj.fields[:3] %}
             {{ field.name }}={{ field.example|repr }},
             {% endfor %}
         )

         print(instance.model_dump_json(indent=2))
{% endif %}
```

## Benefits of This System

1. **Intelligent Rendering**: Automatically selects best presentation based on object type
2. **Extension Synergy**: Leverages all 45+ extensions cohesively
3. **Progressive Disclosure**: Information revealed as needed
4. **Mobile-First**: Responsive design built into every template
5. **Performance**: Lazy loading and virtual scrolling for large docs
6. **Maintainable**: Clear separation of concerns and reusable components
7. **Extensible**: Easy to add new object types or rendering patterns

## Next Steps

1. Create the template directory structure
2. Implement core Jinja2 filters and functions
3. Build the component library
4. Create type-specific templates
5. Test with real Haive documentation
