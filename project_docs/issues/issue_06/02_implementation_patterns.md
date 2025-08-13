# Implementation Patterns for AutoAPI Jinja2 Templates

**Document**: Implementation Patterns  
**Part of**: Issue #6 - AutoAPI Jinja2 Template Improvement  
**Created**: 2025-01-30  
**Scope**: Practical patterns and code examples for template implementation

## Table of Contents

1. [Progressive Disclosure Patterns](#progressive-disclosure-patterns)
2. [Type-Specific Template Patterns](#type-specific-template-patterns)
3. [Visual Enhancement Patterns](#visual-enhancement-patterns)
4. [Responsive Design Patterns](#responsive-design-patterns)
5. [Performance Optimization Patterns](#performance-optimization-patterns)
6. [Error Handling Patterns](#error-handling-patterns)
7. [Testing Patterns](#testing-patterns)

## Progressive Disclosure Patterns

Progressive disclosure is a fundamental UX principle that reveals information gradually, preventing overwhelming users with too much detail at once. Here are practical patterns for implementing this in AutoAPI templates.

### Pattern 1: Collapsible Sections with State Memory

```jinja2
{# _autoapi_templates/python/components/_progressive_section.rst #}
{% macro progressive_section(title, content, section_id, default_state='collapsed', priority='normal') %}
.. raw:: html

   <div class="progressive-section {{ priority }}-priority" data-section-id="{{ section_id }}">
       <button class="section-toggle"
               onclick="toggleSection('{{ section_id }}')"
               aria-expanded="{{ 'true' if default_state == 'expanded' else 'false' }}"
               aria-controls="content-{{ section_id }}">
           <span class="toggle-icon">{{ '▼' if default_state == 'expanded' else '▶' }}</span>
           {{ title }}
           <span class="section-badge">{{ content|count_items }}</span>
       </button>
       <div id="content-{{ section_id }}"
            class="section-content"
            style="display: {{ 'block' if default_state == 'expanded' else 'none' }}">
           {{ content|indent(4) }}
       </div>
   </div>

   <script>
   function toggleSection(sectionId) {
       const button = document.querySelector(`[data-section-id="${sectionId}"] .section-toggle`);
       const content = document.getElementById(`content-${sectionId}`);
       const isExpanded = button.getAttribute('aria-expanded') === 'true';

       // Toggle state
       button.setAttribute('aria-expanded', !isExpanded);
       content.style.display = isExpanded ? 'none' : 'block';
       button.querySelector('.toggle-icon').textContent = isExpanded ? '▶' : '▼';

       // Save state to localStorage
       localStorage.setItem(`autoapi-section-${sectionId}`, !isExpanded);
   }

   // Restore saved states on load
   document.addEventListener('DOMContentLoaded', function() {
       const savedState = localStorage.getItem('autoapi-section-{{ section_id }}');
       if (savedState !== null) {
           const shouldExpand = savedState === 'true';
           const button = document.querySelector('[data-section-id="{{ section_id }}"] .section-toggle');
           if (shouldExpand !== (button.getAttribute('aria-expanded') === 'true')) {
               toggleSection('{{ section_id }}');
           }
       }
   });
   </script>

{% endmacro %}
```

### Pattern 2: Smart Summary with Expandable Details

```jinja2
{# Template for class documentation with smart summaries #}
{% macro render_class_with_summary(obj) %}
{{ obj.name }}
{{ "=" * obj.name|length }}

.. py:class:: {{ obj.name }}{% if obj.bases %}({{ obj.bases|join(', ') }}){% endif %}
   :module: {{ obj.module }}

   {# Executive summary - always visible #}
   .. container:: class-summary

      {{ obj.short_description|default("No description available.", true) }}

      .. container:: quick-info

         {% if obj.bases %}
         **Inherits from:** {{ obj.bases|map(attribute='name')|join(', ') }}
         {% endif %}

         **Key Features:**

         * {{ obj.methods|selectattr('is_public')|list|length }} public methods
         * {{ obj.properties|length }} properties
         * {{ obj.attributes|selectattr('is_public')|list|length }} public attributes
         {% if obj.is_abstract %}
         * Abstract base class
         {% endif %}

   {# Detailed documentation - collapsible #}
   {% if obj.docstring and obj.docstring != obj.short_description %}
   {{ progressive_section(
       'Full Documentation',
       obj.docstring|rst_process,
       obj.id|slugify + '-docs',
       'collapsed'
   ) }}
   {% endif %}

   {# Constructor - high priority, default expanded #}
   {% set init_method = obj.methods|selectattr('name', 'equalto', '__init__')|first %}
   {% if init_method and init_method.parameters %}
   {{ progressive_section(
       'Constructor Parameters',
       render_parameters(init_method.parameters),
       obj.id|slugify + '-init',
       'expanded',
       'high'
   ) }}
   {% endif %}

   {# Methods grouped by category #}
   {% set method_groups = obj.methods|group_by_category %}

   {% if method_groups.public_methods %}
   {{ progressive_section(
       'Public Methods',
       render_method_group(method_groups.public_methods),
       obj.id|slugify + '-public-methods',
       'collapsed'
   ) }}
   {% endif %}

   {% if method_groups.properties %}
   {{ progressive_section(
       'Properties',
       render_property_group(method_groups.properties),
       obj.id|slugify + '-properties',
       'collapsed'
   ) }}
   {% endif %}

{% endmacro %}
```

### Pattern 3: Contextual Information Density

```jinja2
{# Adaptive detail level based on context #}
{% macro render_method_adaptive(method, context='full') %}
{% if context == 'summary' %}
    {# Minimal info for method lists #}
    * :meth:`{{ method.name }}` - {{ method.short_description|default('', true)|truncate(60) }}
{% elif context == 'card' %}
    {# Medium detail for method cards #}
    .. container:: method-card

       .. rubric:: {{ method.name }}{{ method.signature|format_short }}

       {{ method.short_description|default('No description.', true) }}

       {% if method.parameters %}
       *{{ method.parameters|length }} parameters*
       {% endif %}
       {% if method.returns %}
       *Returns:* ``{{ method.returns }}``
       {% endif %}
{% else %}
    {# Full detail for dedicated method documentation #}
    .. py:method:: {{ method.name }}{{ method.signature }}
       :module: {{ method.module }}
       {% if method.is_async %}:async:{% endif %}
       {% if method.is_classmethod %}:classmethod:{% endif %}
       {% if method.is_staticmethod %}:staticmethod:{% endif %}

       {{ method.docstring|indent(3) }}

       {% if method.parameters %}
       :Parameters:
          {{ render_parameters(method.parameters)|indent(3) }}
       {% endif %}

       {% if method.returns %}
       :Returns:
          :class:`{{ method.returns }}` -- {{ method.return_description|default('', true) }}
       {% endif %}

       {% if method.raises %}
       :Raises:
          {{ render_exceptions(method.raises)|indent(3) }}
       {% endif %}

       {% if method.examples %}
       .. rubric:: Examples

       {{ render_examples(method.examples)|indent(3) }}
       {% endif %}
{% endif %}
{% endmacro %}
```

## Type-Specific Template Patterns

Different Python object types require specialized rendering approaches. Here are patterns for common types in the Haive framework.

### Pattern 1: Pydantic Model Template

```jinja2
{# _autoapi_templates/python/types/pydantic_model.rst #}
{% extends "python/base/_layout.rst" %}

{% block content %}
{{ obj.name }}
{{ "=" * obj.name|length }}

.. py:class:: {{ obj.name }}{% if obj.bases %}({{ obj.bases|join(', ') }}){% endif %}
   :module: {{ obj.module }}

   {# Pydantic model badge #}
   .. container:: model-badges

      .. image:: https://img.shields.io/badge/Pydantic-Model-green
         :alt: Pydantic Model
      {% if obj.config.frozen %}
      .. image:: https://img.shields.io/badge/frozen-immutable-blue
         :alt: Frozen Model
      {% endif %}

   {{ obj.short_description }}

   {# Field summary table #}
   .. container:: field-summary

      .. list-table:: Model Fields
         :header-rows: 1
         :class: field-table

         * - Field
           - Type
           - Required
           - Default
           - Description
         {% for field in obj.fields %}
         * - **{{ field.name }}**
           - ``{{ field.type|format_type }}``
           - {{ '✓' if field.required else '✗' }}
           - {{ field.default|format_default|default('—', true) }}
           - {{ field.description|truncate(50) }}
         {% endfor %}

   {# Detailed field documentation #}
   {% if obj.fields %}
   .. rubric:: Field Details

   {% for field in obj.fields %}
   .. attribute:: {{ field.name }}
      :type: {{ field.type }}
      {% if not field.required %}:value: {{ field.default|format_default }}{% endif %}

      {{ field.description|indent(3) }}

      {% if field.validators %}
      **Validators:**

      {% for validator in field.validators %}
      * ``{{ validator.name }}`` - {{ validator.description }}
      {% endfor %}
      {% endif %}

      {% if field.constraints %}
      **Constraints:**

      {{ render_field_constraints(field.constraints)|indent(3) }}
      {% endif %}
   {% endfor %}
   {% endif %}

   {# Model configuration #}
   {% if obj.config %}
   {{ progressive_section(
       'Model Configuration',
       render_pydantic_config(obj.config),
       obj.id|slugify + '-config',
       'collapsed'
   ) }}
   {% endif %}

   {# Validators and root validators #}
   {% set validators = obj.methods|selectattr('is_validator')|list %}
   {% if validators %}
   {{ progressive_section(
       'Validators',
       render_validator_group(validators),
       obj.id|slugify + '-validators',
       'collapsed'
   ) }}
   {% endif %}

   {# JSON Schema #}
   {{ progressive_section(
       'JSON Schema',
       render_json_schema(obj.schema()),
       obj.id|slugify + '-schema',
       'collapsed'
   ) }}

   {# Usage examples #}
   .. rubric:: Usage Examples

   .. code-block:: python

      # Create instance with all fields
      instance = {{ obj.name }}(
      {% for field in obj.fields %}
          {{ field.name }}={{ field.example|format_example }},
      {% endfor %}
      )

      # Validation example
      try:
          invalid = {{ obj.name }}(
              # Invalid data here
          )
      except ValidationError as e:
          print(e)

      # Export to JSON
      json_data = instance.model_dump_json()

      # Create from JSON
      loaded = {{ obj.name }}.model_validate_json(json_data)

{% endblock %}
```

### Pattern 2: Agent Class Template

```jinja2
{# _autoapi_templates/python/types/agent_class.rst #}
{% extends "python/base/_layout.rst" %}

{% block content %}
{{ obj.name }}
{{ "=" * obj.name|length }}

.. py:class:: {{ obj.name }}{% if obj.bases %}({{ obj.bases|join(', ') }}){% endif %}
   :module: {{ obj.module }}

   {# Agent type badges #}
   .. container:: agent-badges

      {% set agent_type = detect_agent_type(obj) %}
      .. image:: https://img.shields.io/badge/Agent-{{ agent_type }}-blue
         :alt: {{ agent_type }} Agent
      {% if obj.has_async %}
      .. image:: https://img.shields.io/badge/async-supported-green
         :alt: Async Support
      {% endif %}

   {{ obj.short_description }}

   {# Agent capabilities summary #}
   .. container:: agent-capabilities

      .. grid:: 2
         :gutter: 3

         .. grid-item-card:: Tools & Integrations
            :class-card: capability-card

            {% if obj.tools %}
            **Available Tools:**

            {% for tool in obj.tools %}
            * :class:`{{ tool.name }}` - {{ tool.description|truncate(50) }}
            {% endfor %}
            {% else %}
            *No tools configured*
            {% endif %}

         .. grid-item-card:: Configuration
            :class-card: capability-card

            **Engine:** {{ obj.engine_type|default('AugLLMConfig', true) }}

            **Key Settings:**

            * Temperature: {{ obj.temperature|default('0.7', true) }}
            * Max tokens: {{ obj.max_tokens|default('default', true) }}
            {% if obj.structured_output_model %}
            * Output model: :class:`{{ obj.structured_output_model }}`
            {% endif %}

   {# State schema visualization #}
   {% if obj.state_schema %}
   .. container:: state-schema

      .. mermaid::
         :caption: Agent State Schema

         classDiagram
             class {{ obj.state_schema.name }} {
                 {% for field in obj.state_schema.fields %}
                 +{{ field.type }} {{ field.name }}
                 {% endfor %}
             }
             {% for related in obj.state_schema.relationships %}
             {{ obj.state_schema.name }} --> {{ related }}
             {% endfor %}
   {% endif %}

   {# Workflow diagram #}
   {% if obj.workflow_steps %}
   .. mermaid::
      :caption: Agent Workflow

      graph TD
          {% for step in obj.workflow_steps %}
          {{ step.id }}[{{ step.label }}]
          {% if step.next %}
          {{ step.id }} --> {{ step.next }}
          {% endif %}
          {% endfor %}
   {% endif %}

   {# Core methods with special rendering #}
   .. rubric:: Core Agent Methods

   {% set core_methods = ['run', 'arun', 'invoke', '__call__'] %}
   {% for method_name in core_methods %}
       {% set method = obj.methods|selectattr('name', 'equalto', method_name)|first %}
       {% if method %}

   .. container:: core-method

      {{ render_method_adaptive(method, 'card') }}

       {% endif %}
   {% endfor %}

   {# Tool integration examples #}
   {% if obj.tools %}
   .. rubric:: Tool Integration Examples

   .. tabs::

      {% for tool in obj.tools[:3] %}  {# Show first 3 tools #}
      .. tab:: {{ tool.name }}

         .. code-block:: python

            # Using {{ tool.name }} tool
            agent = {{ obj.name }}()
            result = agent.run("{{ tool.example_query }}")

            # The agent will use {{ tool.name }} to:
            # {{ tool.description }}

      {% endfor %}
   {% endif %}

   {# Advanced configuration #}
   {{ progressive_section(
       'Advanced Configuration',
       render_agent_configuration(obj),
       obj.id|slugify + '-advanced',
       'collapsed'
   ) }}

   {# All methods grouped #}
   {{ progressive_section(
       'All Methods',
       render_method_group(obj.methods),
       obj.id|slugify + '-methods',
       'collapsed'
   ) }}

{% endblock %}
```

### Pattern 3: Enum Class Template

```jinja2
{# _autoapi_templates/python/types/enum_class.rst #}
{% extends "python/base/_layout.rst" %}

{% block content %}
{{ obj.name }}
{{ "=" * obj.name|length }}

.. py:class:: {{ obj.name }}{% if obj.bases %}({{ obj.bases|join(', ') }}){% endif %}
   :module: {{ obj.module }}

   {{ obj.short_description }}

   {# Enum values in a nice table #}
   .. list-table:: Enumeration Values
      :header-rows: 1
      :class: enum-table

      * - Name
        - Value
        - Description
      {% for member in obj.members %}
      * - **{{ member.name }}**
        - ``{{ member.value }}``
        - {{ member.description|default('—', true) }}
      {% endfor %}

   {# Quick reference code block #}
   .. rubric:: Quick Reference

   .. code-block:: python

      from {{ obj.module }} import {{ obj.name }}

      # Access values
      {% for member in obj.members[:3] %}
      {{ member.name.lower() }} = {{ obj.name }}.{{ member.name }}  # {{ member.value }}
      {% endfor %}

      # Check membership
      if value in {{ obj.name }}:
          print(f"{value} is a valid {{ obj.name }}")

      # Iterate over all values
      for item in {{ obj.name }}:
          print(f"{item.name} = {item.value}")

   {# Value groups if applicable #}
   {% set groups = obj.members|group_by_prefix %}
   {% if groups|length > 1 %}
   .. rubric:: Value Groups

   .. tabs::

      {% for prefix, members in groups.items() %}
      .. tab:: {{ prefix|title }}

         {% for member in members %}
         * **{{ member.name }}** = ``{{ member.value }}``
         {% endfor %}

      {% endfor %}
   {% endif %}

{% endblock %}
```

## Visual Enhancement Patterns

Visual enhancements make documentation more scannable and pleasant to use. Here are patterns for improving the visual presentation.

### Pattern 1: Smart Syntax Highlighting

```jinja2
{# Macro for enhanced code highlighting #}
{% macro highlight_code(code, language='python', emphasis_lines=None, caption=None) %}
.. container:: code-block-container

   {% if caption %}
   .. rubric:: {{ caption }}
   {% endif %}

   .. code-block:: {{ language }}
      :linenos:
      {% if emphasis_lines %}:emphasize-lines: {{ emphasis_lines }}{% endif %}
      :class: highlight-{{ language }}

      {{ code|dedent }}

   .. container:: code-actions

      .. raw:: html

         <button class="copy-button" onclick="copyCode(this)" title="Copy code">
             📋 Copy
         </button>
         <button class="expand-button" onclick="expandCode(this)" title="Toggle expand">
             🔍 Expand
         </button>

.. raw:: html

   <style>
   .code-block-container {
       position: relative;
       margin: 1em 0;
   }

   .code-actions {
       position: absolute;
       top: 0;
       right: 0;
       display: flex;
       gap: 0.5em;
       opacity: 0;
       transition: opacity 0.2s;
   }

   .code-block-container:hover .code-actions {
       opacity: 1;
   }

   .copy-button, .expand-button {
       padding: 0.25em 0.5em;
       border: 1px solid #ddd;
       background: white;
       cursor: pointer;
       font-size: 0.875em;
   }

   .copy-button:hover, .expand-button:hover {
       background: #f0f0f0;
   }
   </style>

   <script>
   function copyCode(button) {
       const codeBlock = button.closest('.code-block-container').querySelector('pre');
       const code = codeBlock.textContent;
       navigator.clipboard.writeText(code).then(() => {
           button.textContent = '✓ Copied!';
           setTimeout(() => button.textContent = '📋 Copy', 2000);
       });
   }

   function expandCode(button) {
       const codeBlock = button.closest('.code-block-container').querySelector('pre');
       codeBlock.classList.toggle('expanded');
       button.textContent = codeBlock.classList.contains('expanded') ? '🔍 Collapse' : '🔍 Expand';
   }
   </script>

{% endmacro %}
```

### Pattern 2: Visual Type Annotations

```jinja2
{# Enhanced type annotation rendering #}
{% macro render_type_annotation(annotation, link=True) %}
{% set formatted = format_type_annotation(annotation) %}
{% if link %}
    {% for type_name, type_info in extract_types(formatted).items() %}
        {% if type_info.is_builtin %}
            <span class="type-builtin">{{ type_name }}</span>
        {% elif type_info.is_generic %}
            <span class="type-generic">{{ type_name }}</span>
        {% elif type_info.is_custom %}
            :class:`{{ type_info.full_name }} <span class="type-custom">{{ type_name }}</span>`
        {% else %}
            <span class="type-unknown">{{ type_name }}</span>
        {% endif %}
    {% endfor %}
{% else %}
    <code class="type-annotation">{{ formatted }}</code>
{% endif %}

.. raw:: html

   <style>
   .type-builtin {
       color: #0066cc;
       font-weight: 500;
   }

   .type-generic {
       color: #6a0dad;
       font-weight: 500;
   }

   .type-custom {
       color: #008850;
       font-weight: 600;
   }

   .type-unknown {
       color: #666;
       font-style: italic;
   }

   .type-annotation {
       background: #f8f8f8;
       padding: 0.1em 0.3em;
       border-radius: 3px;
       font-size: 0.95em;
   }
   </style>

{% endmacro %}
```

### Pattern 3: Interactive Inheritance Diagrams

```jinja2
{# Mermaid-based inheritance diagram with interactivity #}
{% macro render_inheritance_diagram(obj) %}
{% if obj.bases or obj.subclasses %}
.. container:: inheritance-container

   .. mermaid::
      :caption: Class Inheritance Hierarchy
      :align: center

      graph TB
          {% for base in obj.bases %}
          {{ base.name }}["{{ base.name }}"]:::baseClass --> {{ obj.name }}
          {% endfor %}

          {{ obj.name }}["<b>{{ obj.name }}</b>"]:::currentClass

          {% for subclass in obj.subclasses %}
          {{ obj.name }} --> {{ subclass.name }}["{{ subclass.name }}"]:::subClass
          {% endfor %}

          classDef baseClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
          classDef currentClass fill:#fff3b8,stroke:#f57c00,stroke-width:3px;
          classDef subClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;

          click {{ obj.name }} "{{ obj.id }}.html" "View {{ obj.name }} documentation"
          {% for base in obj.bases %}
          click {{ base.name }} "{{ base.id }}.html" "View {{ base.name }} documentation"
          {% endfor %}
          {% for subclass in obj.subclasses %}
          click {{ subclass.name }} "{{ subclass.id }}.html" "View {{ subclass.name }} documentation"
          {% endfor %}

   .. container:: inheritance-legend

      .. raw:: html

         <div class="legend">
             <span class="legend-item">
                 <span class="color-box base-class"></span> Base Classes
             </span>
             <span class="legend-item">
                 <span class="color-box current-class"></span> Current Class
             </span>
             <span class="legend-item">
                 <span class="color-box sub-class"></span> Subclasses
             </span>
         </div>

         <style>
         .legend {
             display: flex;
             gap: 1em;
             margin-top: 0.5em;
             font-size: 0.875em;
         }

         .legend-item {
             display: flex;
             align-items: center;
             gap: 0.3em;
         }

         .color-box {
             width: 20px;
             height: 15px;
             border: 1px solid #999;
         }

         .base-class { background: #e1f5fe; }
         .current-class { background: #fff3b8; }
         .sub-class { background: #f3e5f5; }
         </style>

{% endif %}
{% endmacro %}
```

## Responsive Design Patterns

Modern documentation must work across all devices. Here are patterns for responsive AutoAPI templates.

### Pattern 1: Mobile-First Method Cards

```jinja2
{# Responsive method card layout #}
{% macro render_method_card_responsive(method) %}
.. raw:: html

   <div class="method-card">
       <div class="method-header">
           <h4 class="method-name">{{ method.name }}</h4>
           <div class="method-badges">
               {% if method.is_async %}
               <span class="badge async">async</span>
               {% endif %}
               {% if method.is_classmethod %}
               <span class="badge classmethod">@classmethod</span>
               {% endif %}
               {% if method.is_property %}
               <span class="badge property">property</span>
               {% endif %}
           </div>
       </div>

       <div class="method-signature">
           <code>{{ method.signature|format_responsive }}</code>
       </div>

       <div class="method-description">
           {{ method.short_description|default('No description available.', true) }}
       </div>

       <div class="method-details">
           {% if method.parameters %}
           <details class="parameters-details">
               <summary>Parameters ({{ method.parameters|length }})</summary>
               <ul class="parameter-list">
               {% for param in method.parameters %}
                   <li>
                       <strong>{{ param.name }}</strong>
                       {% if param.type %}: <code>{{ param.type }}</code>{% endif %}
                       {% if param.description %} - {{ param.description }}{% endif %}
                   </li>
               {% endfor %}
               </ul>
           </details>
           {% endif %}

           {% if method.returns %}
           <div class="method-returns">
               <strong>Returns:</strong> <code>{{ method.returns }}</code>
           </div>
           {% endif %}
       </div>
   </div>

   <style>
   .method-card {
       border: 1px solid #e0e0e0;
       border-radius: 8px;
       padding: 1rem;
       margin-bottom: 1rem;
       background: #fafafa;
   }

   .method-header {
       display: flex;
       justify-content: space-between;
       align-items: center;
       flex-wrap: wrap;
       gap: 0.5rem;
       margin-bottom: 0.5rem;
   }

   .method-name {
       margin: 0;
       font-size: 1.1rem;
       color: #1976d2;
   }

   .method-badges {
       display: flex;
       gap: 0.25rem;
   }

   .badge {
       padding: 0.2rem 0.5rem;
       border-radius: 4px;
       font-size: 0.75rem;
       font-weight: 500;
   }

   .badge.async { background: #e3f2fd; color: #1565c0; }
   .badge.classmethod { background: #f3e5f5; color: #6a1b9a; }
   .badge.property { background: #e8f5e9; color: #2e7d32; }

   .method-signature {
       background: #f5f5f5;
       padding: 0.5rem;
       border-radius: 4px;
       overflow-x: auto;
       margin-bottom: 0.75rem;
   }

   .method-signature code {
       white-space: nowrap;
       font-size: 0.875rem;
   }

   .method-description {
       margin-bottom: 0.75rem;
       line-height: 1.5;
   }

   .parameters-details {
       background: white;
       padding: 0.5rem;
       border-radius: 4px;
       margin-bottom: 0.5rem;
   }

   .parameter-list {
       margin: 0.5rem 0 0 1rem;
       padding-left: 1rem;
   }

   /* Mobile responsiveness */
   @media (max-width: 768px) {
       .method-card {
           padding: 0.75rem;
       }

       .method-header {
           flex-direction: column;
           align-items: flex-start;
       }

       .method-signature {
           font-size: 0.8rem;
       }

       .method-name {
           font-size: 1rem;
       }
   }
   </style>

{% endmacro %}
```

### Pattern 2: Responsive Table Layout

```jinja2
{# Responsive table that transforms on mobile #}
{% macro render_responsive_table(headers, rows, caption=None) %}
.. raw:: html

   <div class="responsive-table-container">
       {% if caption %}
       <h4 class="table-caption">{{ caption }}</h4>
       {% endif %}

       <table class="responsive-table">
           <thead>
               <tr>
                   {% for header in headers %}
                   <th>{{ header }}</th>
                   {% endfor %}
               </tr>
           </thead>
           <tbody>
               {% for row in rows %}
               <tr>
                   {% for cell in row %}
                   <td data-label="{{ headers[loop.index0] }}">{{ cell }}</td>
                   {% endfor %}
               </tr>
               {% endfor %}
           </tbody>
       </table>
   </div>

   <style>
   .responsive-table-container {
       margin: 1rem 0;
       overflow-x: auto;
   }

   .table-caption {
       margin-bottom: 0.5rem;
       color: #555;
   }

   .responsive-table {
       width: 100%;
       border-collapse: collapse;
       background: white;
       box-shadow: 0 1px 3px rgba(0,0,0,0.1);
   }

   .responsive-table th,
   .responsive-table td {
       padding: 0.75rem;
       text-align: left;
       border-bottom: 1px solid #e0e0e0;
   }

   .responsive-table th {
       background: #f5f5f5;
       font-weight: 600;
       color: #333;
   }

   .responsive-table tr:hover {
       background: #f9f9f9;
   }

   /* Mobile layout */
   @media (max-width: 768px) {
       .responsive-table thead {
           display: none;
       }

       .responsive-table tr {
           display: block;
           margin-bottom: 1rem;
           border: 1px solid #e0e0e0;
           border-radius: 4px;
       }

       .responsive-table td {
           display: block;
           text-align: right;
           padding-left: 50%;
           position: relative;
           border-bottom: 1px solid #f0f0f0;
       }

       .responsive-table td:last-child {
           border-bottom: none;
       }

       .responsive-table td::before {
           content: attr(data-label);
           position: absolute;
           left: 0.75rem;
           width: 45%;
           text-align: left;
           font-weight: 600;
           color: #666;
       }
   }
   </style>

{% endmacro %}
```

### Pattern 3: Touch-Friendly Navigation

```jinja2
{# Mobile-optimized navigation for class members #}
{% macro render_mobile_nav(obj) %}
.. raw:: html

   <nav class="mobile-nav">
       <div class="nav-header">
           <h3>Quick Navigation</h3>
           <button class="nav-toggle" aria-label="Toggle navigation">☰</button>
       </div>

       <div class="nav-content">
           {% if obj.methods %}
           <section class="nav-section">
               <h4>Methods</h4>
               <ul class="nav-list">
                   {% for method in obj.methods|selectattr('is_public')|sort(attribute='name') %}
                   <li>
                       <a href="#{{ method.id }}" class="nav-link">
                           {{ method.name }}
                           {% if method.is_async %}
                           <span class="nav-badge">async</span>
                           {% endif %}
                       </a>
                   </li>
                   {% endfor %}
               </ul>
           </section>
           {% endif %}

           {% if obj.properties %}
           <section class="nav-section">
               <h4>Properties</h4>
               <ul class="nav-list">
                   {% for prop in obj.properties|sort(attribute='name') %}
                   <li>
                       <a href="#{{ prop.id }}" class="nav-link">{{ prop.name }}</a>
                   </li>
                   {% endfor %}
               </ul>
           </section>
           {% endif %}
       </div>
   </nav>

   <style>
   .mobile-nav {
       position: sticky;
       top: 0;
       background: white;
       border: 1px solid #e0e0e0;
       border-radius: 8px;
       margin-bottom: 2rem;
       z-index: 100;
   }

   .nav-header {
       display: flex;
       justify-content: space-between;
       align-items: center;
       padding: 1rem;
       border-bottom: 1px solid #e0e0e0;
   }

   .nav-header h3 {
       margin: 0;
       font-size: 1.1rem;
   }

   .nav-toggle {
       display: none;
       background: none;
       border: none;
       font-size: 1.5rem;
       cursor: pointer;
   }

   .nav-content {
       max-height: 400px;
       overflow-y: auto;
       padding: 1rem;
   }

   .nav-section {
       margin-bottom: 1.5rem;
   }

   .nav-section h4 {
       margin: 0 0 0.5rem 0;
       color: #666;
       font-size: 0.9rem;
       text-transform: uppercase;
   }

   .nav-list {
       list-style: none;
       margin: 0;
       padding: 0;
   }

   .nav-link {
       display: block;
       padding: 0.5rem 0.75rem;
       color: #333;
       text-decoration: none;
       border-radius: 4px;
       transition: background 0.2s;
   }

   .nav-link:hover {
       background: #f0f0f0;
   }

   .nav-badge {
       display: inline-block;
       padding: 0.1rem 0.3rem;
       background: #e3f2fd;
       color: #1565c0;
       font-size: 0.75rem;
       border-radius: 3px;
       margin-left: 0.5rem;
   }

   /* Mobile behavior */
   @media (max-width: 768px) {
       .nav-toggle {
           display: block;
       }

       .nav-content {
           display: none;
           position: absolute;
           top: 100%;
           left: 0;
           right: 0;
           background: white;
           border: 1px solid #e0e0e0;
           border-top: none;
           border-radius: 0 0 8px 8px;
           box-shadow: 0 4px 6px rgba(0,0,0,0.1);
       }

       .nav-content.active {
           display: block;
       }

       .mobile-nav {
           position: relative;
           margin-bottom: 1rem;
       }
   }
   </style>

   <script>
   document.addEventListener('DOMContentLoaded', function() {
       const toggle = document.querySelector('.nav-toggle');
       const content = document.querySelector('.nav-content');

       toggle.addEventListener('click', function() {
           content.classList.toggle('active');
           this.textContent = content.classList.contains('active') ? '✕' : '☰';
       });

       // Close nav when clicking outside
       document.addEventListener('click', function(e) {
           if (!e.target.closest('.mobile-nav')) {
               content.classList.remove('active');
               toggle.textContent = '☰';
           }
       });
   });
   </script>

{% endmacro %}
```

## Performance Optimization Patterns

Performance is crucial for large documentation projects. Here are patterns to keep templates fast.

### Pattern 1: Lazy Loading for Heavy Content

```jinja2
{# Lazy load expensive content like examples and diagrams #}
{% macro lazy_load_section(title, content_id, loader_func) %}
.. raw:: html

   <div class="lazy-section" data-content-id="{{ content_id }}">
       <h3>{{ title }}</h3>
       <div class="lazy-placeholder">
           <div class="spinner"></div>
           <p>Loading {{ title|lower }}...</p>
       </div>
       <div class="lazy-content" style="display: none;"></div>
   </div>

   <script>
   (function() {
       const observer = new IntersectionObserver((entries) => {
           entries.forEach(entry => {
               if (entry.isIntersecting) {
                   const section = entry.target;
                   const contentId = section.dataset.contentId;

                   // Load content
                   fetch(`/api/autoapi/content/${contentId}`)
                       .then(response => response.text())
                       .then(content => {
                           const placeholder = section.querySelector('.lazy-placeholder');
                           const contentDiv = section.querySelector('.lazy-content');

                           placeholder.style.display = 'none';
                           contentDiv.innerHTML = content;
                           contentDiv.style.display = 'block';

                           // Trigger syntax highlighting
                           if (window.Prism) {
                               Prism.highlightAllUnder(contentDiv);
                           }
                       });

                   observer.unobserve(section);
               }
           });
       }, { rootMargin: '100px' });

       document.querySelectorAll('.lazy-section').forEach(section => {
           observer.observe(section);
       });
   })();
   </script>

   <style>
   .lazy-placeholder {
       display: flex;
       align-items: center;
       justify-content: center;
       padding: 2rem;
       background: #f5f5f5;
       border-radius: 8px;
   }

   .spinner {
       width: 24px;
       height: 24px;
       border: 3px solid #ddd;
       border-top-color: #333;
       border-radius: 50%;
       animation: spin 1s linear infinite;
       margin-right: 1rem;
   }

   @keyframes spin {
       to { transform: rotate(360deg); }
   }
   </style>

{% endmacro %}
```

### Pattern 2: Template Fragment Caching

```python
# Template helper for caching expensive operations
from functools import lru_cache
from jinja2 import Environment
import hashlib

class CachedTemplateHelpers:
    """Cached template helpers for performance."""

    @staticmethod
    @lru_cache(maxsize=1000)
    def render_inheritance_tree(class_id: str, max_depth: int = 5):
        """Cache inheritance tree rendering."""
        # Expensive tree calculation
        tree = build_inheritance_tree(class_id, max_depth)
        return format_tree_as_mermaid(tree)

    @staticmethod
    @lru_cache(maxsize=500)
    def group_methods_smart(methods_hash: str):
        """Cache method grouping logic."""
        # Methods are passed as hash for cache key
        methods = retrieve_methods_by_hash(methods_hash)

        groups = {
            'constructors': [],
            'properties': [],
            'public_methods': [],
            'private_methods': [],
            'special_methods': [],
            'static_methods': [],
            'class_methods': [],
        }

        for method in methods:
            if method.name == '__init__':
                groups['constructors'].append(method)
            elif method.is_property:
                groups['properties'].append(method)
            # ... more grouping logic

        return groups

    @staticmethod
    def get_methods_hash(methods):
        """Create stable hash for method list."""
        method_ids = sorted(m.id for m in methods)
        return hashlib.md5(''.join(method_ids).encode()).hexdigest()


# Register with Jinja2
def register_cached_helpers(env: Environment):
    helpers = CachedTemplateHelpers()
    env.globals['render_inheritance_tree'] = helpers.render_inheritance_tree
    env.globals['group_methods_smart'] = helpers.group_methods_smart
    env.filters['methods_hash'] = helpers.get_methods_hash
```

### Pattern 3: Conditional Rendering Based on Size

```jinja2
{# Optimize rendering for large classes #}
{% macro render_class_optimized(obj) %}
{% set is_large = obj.methods|length > 50 or obj.attributes|length > 50 %}

{% if is_large %}
    {# Large class - use pagination and search #}
    {{ render_large_class_with_search(obj) }}
{% else %}
    {# Normal class - standard rendering #}
    {{ render_standard_class(obj) }}
{% endif %}
{% endmacro %}

{% macro render_large_class_with_search(obj) %}
.. raw:: html

   <div class="large-class-container">
       <div class="search-box">
           <input type="text"
                  placeholder="Search methods, properties, attributes..."
                  class="member-search"
                  data-class-id="{{ obj.id }}">
       </div>

       <div class="member-stats">
           <span>{{ obj.methods|length }} methods</span>
           <span>{{ obj.properties|length }} properties</span>
           <span>{{ obj.attributes|length }} attributes</span>
       </div>

       <div class="members-container" data-page-size="20">
           <!-- Members loaded dynamically -->
       </div>

       <div class="pagination">
           <!-- Pagination controls -->
       </div>
   </div>

   <script>
   // Implement virtual scrolling for large member lists
   class MemberList {
       constructor(classId) {
           this.classId = classId;
           this.pageSize = 20;
           this.currentPage = 1;
           this.init();
       }

       async init() {
           this.members = await this.loadMembers();
           this.render();
           this.attachListeners();
       }

       async loadMembers() {
           const response = await fetch(`/api/autoapi/members/${this.classId}`);
           return response.json();
       }

       render() {
           const start = (this.currentPage - 1) * this.pageSize;
           const end = start + this.pageSize;
           const pageMembers = this.filteredMembers.slice(start, end);

           // Render only visible members
           this.renderMembers(pageMembers);
           this.renderPagination();
       }

       // ... more implementation
   }
   </script>

{% endmacro %}
```

## Error Handling Patterns

Robust error handling ensures templates don't break the documentation build.

### Pattern 1: Safe Attribute Access

```jinja2
{# Macro for safe attribute access with fallbacks #}
{% macro safe_attr(obj, attr_path, default='') %}
{%- set parts = attr_path.split('.') -%}
{%- set value = obj -%}
{%- for part in parts -%}
    {%- if value is mapping and part in value -%}
        {%- set value = value[part] -%}
    {%- elif value is object and value|attr(part) is defined -%}
        {%- set value = value|attr(part) -%}
    {%- else -%}
        {%- set value = default -%}
        {%- break -%}
    {%- endif -%}
{%- endfor -%}
{{ value }}
{%- endmacro %}

{# Usage examples #}
{{ safe_attr(obj, 'config.name', 'Unknown') }}
{{ safe_attr(obj, 'deeply.nested.attribute', 'N/A') }}
```

### Pattern 2: Graceful Degradation

```jinja2
{# Template with graceful degradation #}
{% macro render_with_fallback(obj) %}
{% try %}
    {# Try advanced rendering #}
    {{ render_advanced_class(obj) }}
{% except %}
    {# Fallback to simple rendering #}
    .. warning::

       Advanced rendering failed. Showing simplified view.

    {{ obj.name }}
    {{ "=" * obj.name|length }}

    .. py:class:: {{ obj.name }}
       :module: {{ obj.module }}

       {{ obj.docstring|default('No documentation available.', true) }}

       {# Basic member listing #}
       {% if obj.methods %}
       **Methods:**

       {% for method in obj.methods %}
       * ``{{ method.name }}{{ method.signature|default('()', true) }}``
       {% endfor %}
       {% endif %}
{% endtry %}
{% endmacro %}
```

### Pattern 3: Validation and Error Messages

```jinja2
{# Input validation with helpful error messages #}
{% macro validate_and_render(obj) %}
{% set errors = [] %}

{# Validate required fields #}
{% if not obj.name %}
    {% do errors.append('Object missing required "name" field') %}
{% endif %}

{% if not obj.type %}
    {% do errors.append('Object missing required "type" field') %}
{% endif %}

{% if obj.type == 'class' and not obj.module %}
    {% do errors.append('Class object missing required "module" field') %}
{% endif %}

{# Display errors if any #}
{% if errors %}
.. error::

   Failed to render {{ obj.id|default('unknown object', true) }}:

   {% for error in errors %}
   * {{ error }}
   {% endfor %}

   Raw object data:

   .. code-block:: json

      {{ obj|tojson(indent=2) }}

{% else %}
    {# Render normally #}
    {{ render_object(obj) }}
{% endif %}
{% endmacro %}
```

## Testing Patterns

Testing ensures templates work correctly across different scenarios.

### Pattern 1: Template Unit Tests

```python
# tests/test_templates.py
import pytest
from jinja2 import Environment, DictLoader
from pydevelop_docs.template_helpers import register_all_helpers

class TestAutoAPITemplates:
    """Test AutoAPI custom templates."""

    @pytest.fixture
    def env(self):
        """Create test Jinja2 environment."""
        env = Environment(loader=DictLoader({
            'test_progressive.rst': '''
                {%- from "macros.rst" import progressive_section -%}
                {{ progressive_section(title, content, 'test-id') }}
            ''',
            'macros.rst': '''
                {%- macro progressive_section(title, content, id) -%}
                .. container:: {{ id }}

                   {{ title }}
                   {{ content }}
                {%- endmacro -%}
            '''
        }))
        register_all_helpers(env)
        return env

    def test_progressive_section_rendering(self, env):
        """Test progressive section macro."""
        template = env.get_template('test_progressive.rst')
        result = template.render(
            title='Test Section',
            content='Test content here'
        )

        assert '.. container:: test-id' in result
        assert 'Test Section' in result
        assert 'Test content here' in result

    def test_type_detection(self, env):
        """Test type detection for different objects."""
        from pydevelop_docs.template_helpers import TypeDetector

        # Pydantic model
        pydantic_obj = {
            'type': 'class',
            'bases': [{'name': 'BaseModel'}]
        }
        assert TypeDetector.detect_class_type(pydantic_obj) == 'pydantic_model'

        # Agent class
        agent_obj = {
            'type': 'class',
            'bases': [{'name': 'ReactAgent'}]
        }
        assert TypeDetector.detect_class_type(agent_obj) == 'agent_class'

        # Enum
        enum_obj = {
            'type': 'class',
            'bases': [{'name': 'Enum'}]
        }
        assert TypeDetector.detect_class_type(enum_obj) == 'enum_class'

    def test_safe_attribute_access(self, env):
        """Test safe attribute access patterns."""
        template = env.from_string('''
            {%- from "macros.rst" import safe_attr -%}
            {{ safe_attr(obj, 'nested.attr', 'default') }}
        ''')

        # Nested attribute exists
        result = template.render(obj={'nested': {'attr': 'value'}})
        assert result.strip() == 'value'

        # Nested attribute missing
        result = template.render(obj={'nested': {}})
        assert result.strip() == 'default'

        # Parent missing
        result = template.render(obj={})
        assert result.strip() == 'default'
```

### Pattern 2: Visual Regression Tests

```python
# tests/test_visual_regression.py
import pytest
from selenium import webdriver
from PIL import Image
import imagehash
import os

class TestVisualRegression:
    """Visual regression tests for template changes."""

    @pytest.fixture
    def driver(self):
        """Create Selenium webdriver."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()

    def test_class_documentation_appearance(self, driver):
        """Test visual appearance of class documentation."""
        # Build test documentation
        build_test_docs()

        # Load class documentation page
        driver.get('file:///path/to/test/docs/MyClass.html')

        # Take screenshot
        screenshot_path = 'tests/screenshots/class_doc_current.png'
        driver.save_screenshot(screenshot_path)

        # Compare with baseline
        baseline_path = 'tests/screenshots/class_doc_baseline.png'
        if os.path.exists(baseline_path):
            current = Image.open(screenshot_path)
            baseline = Image.open(baseline_path)

            # Calculate perceptual hash difference
            hash_current = imagehash.average_hash(current)
            hash_baseline = imagehash.average_hash(baseline)
            difference = hash_current - hash_baseline

            # Allow small differences (lighting, antialiasing)
            assert difference < 5, f"Visual difference detected: {difference}"
        else:
            # First run - save as baseline
            os.rename(screenshot_path, baseline_path)
            pytest.skip("Baseline created")
```

### Pattern 3: Performance Benchmarks

```python
# tests/test_performance.py
import pytest
import time
from pathlib import Path

class TestTemplatePerformance:
    """Performance benchmarks for templates."""

    def test_template_render_time(self, large_project):
        """Test template rendering performance."""
        start_time = time.time()

        # Render all templates
        rendered_count = 0
        for obj in large_project.objects:
            template = get_template_for_object(obj)
            result = template.render(obj=obj)
            rendered_count += 1

        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / rendered_count

        # Assert performance requirements
        assert avg_time < 0.1, f"Average render time {avg_time}s exceeds 100ms limit"
        assert total_time < 60, f"Total render time {total_time}s exceeds 1 minute"

        # Log performance metrics
        print(f"Rendered {rendered_count} objects in {total_time:.2f}s")
        print(f"Average time per object: {avg_time*1000:.2f}ms")

    def test_memory_usage(self, large_project):
        """Test memory usage during rendering."""
        import psutil
        import os

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Render templates
        for obj in large_project.objects:
            template = get_template_for_object(obj)
            result = template.render(obj=obj)

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Assert memory requirements
        assert memory_increase < 500, f"Memory increased by {memory_increase}MB"

        print(f"Memory usage: {initial_memory}MB -> {final_memory}MB")
```

This comprehensive guide to implementation patterns provides practical, production-ready code for creating sophisticated AutoAPI templates with Jinja2.
