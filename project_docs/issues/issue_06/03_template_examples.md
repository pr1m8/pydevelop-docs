# Complete Template Examples for AutoAPI Customization

**Document**: Template Examples  
**Part of**: Issue #6 - AutoAPI Jinja2 Template Improvement  
**Created**: 2025-01-30  
**Scope**: Ready-to-use template examples for different object types

## Table of Contents

1. [Base Layout Template](#base-layout-template)
2. [Pydantic Model Complete Template](#pydantic-model-complete-template)
3. [Agent Class Complete Template](#agent-class-complete-template)
4. [Module Documentation Template](#module-documentation-template)
5. [Function/Method Templates](#functionmethod-templates)
6. [Enum Class Template](#enum-class-template)
7. [Exception Class Template](#exception-class-template)
8. [Dataclass Template](#dataclass-template)

## Base Layout Template

This base template provides the foundation for all other templates with consistent styling and structure.

### File: `_autoapi_templates/python/base/_layout.rst`

```jinja2
{# Base layout template for all AutoAPI documentation #}
{# Import all macros #}
{% from "python/base/_macros.rst" import
    progressive_section,
    render_badges,
    render_inheritance_diagram,
    render_source_link,
    render_navigation,
    safe_attr %}

{# Set up common variables #}
{% set is_private = obj.name.startswith('_') and not obj.name.startswith('__') %}
{% set is_special = obj.name.startswith('__') and obj.name.endswith('__') %}
{% set show_inherited = 'show-inherited-members' in autoapi_options %}
{% set show_private = 'private-members' in autoapi_options %}

{# Main content structure #}
.. _{{ obj.id }}:

{% block header %}
{# Navigation breadcrumb #}
.. container:: breadcrumb

   {% set parts = obj.id.split('.') %}
   {% for i in range(parts|length - 1) %}
   :doc:`{{ parts[:i+1]|join('.') }} <{{ parts[:i+1]|join('/') }}>` {{ '>' if not loop.last else '' }}
   {% endfor %}
   **{{ obj.name }}**

{% endblock header %}

{% block title %}
{{ obj.name }}
{{ "=" * obj.name|length }}
{% endblock title %}

{% block badges %}
{{ render_badges(obj) }}
{% endblock badges %}

{% block summary %}
.. container:: summary-section

   {{ obj.short_description|default('No description available.', true) }}

   {% if obj.file_path %}
   {{ render_source_link(obj) }}
   {% endif %}

{% endblock summary %}

{% block content %}
{# Main content - override in child templates #}
{% endblock content %}

{% block inheritance %}
{% if obj.bases or obj.subclasses %}
{{ progressive_section(
    'Inheritance Hierarchy',
    render_inheritance_diagram(obj),
    obj.id|slugify + '-inheritance',
    'collapsed'
) }}
{% endif %}
{% endblock inheritance %}

{% block members %}
{# Member documentation - override in child templates #}
{% endblock members %}

{% block examples %}
{% if obj.examples %}
.. rubric:: Examples

.. tabs::

   {% for example in obj.examples %}
   .. tab:: Example {{ loop.index }}

      {{ example|indent(6) }}

   {% endfor %}
{% endif %}
{% endblock examples %}

{% block seealso %}
{% if obj.see_also %}
.. seealso::

   {% for ref in obj.see_also %}
   * :doc:`{{ ref.link }}` - {{ ref.description }}
   {% endfor %}
{% endif %}
{% endblock seealso %}

{% block footer %}
.. container:: footer-nav

   {{ render_navigation(obj) }}

.. raw:: html

   <script>
   // Initialize all interactive elements
   document.addEventListener('DOMContentLoaded', function() {
       // Restore collapsed section states
       restoreCollapsedStates();

       // Initialize code highlighting
       if (typeof Prism !== 'undefined') {
           Prism.highlightAll();
       }

       // Initialize tooltips
       initializeTooltips();

       // Track page view
       if (typeof gtag !== 'undefined') {
           gtag('event', 'page_view', {
               page_title: '{{ obj.name }}',
               page_type: '{{ obj.type }}',
               page_module: '{{ obj.module }}'
           });
       }
   });
   </script>

{% endblock footer %}
```

### File: `_autoapi_templates/python/base/_macros.rst`

```jinja2
{# Common macros used across all templates #}

{# Progressive disclosure section #}
{% macro progressive_section(title, content, section_id, default_state='collapsed', priority='normal', badge_count=None) %}
.. raw:: html

   <div class="progressive-section {{ priority }}-priority" data-section-id="{{ section_id }}">
       <button class="section-toggle"
               onclick="toggleSection('{{ section_id }}')"
               aria-expanded="{{ 'true' if default_state == 'expanded' else 'false' }}"
               aria-controls="content-{{ section_id }}">
           <span class="toggle-icon">{{ '▼' if default_state == 'expanded' else '▶' }}</span>
           <span class="section-title">{{ title }}</span>
           {% if badge_count %}
           <span class="section-badge">{{ badge_count }}</span>
           {% endif %}
       </button>
       <div id="content-{{ section_id }}"
            class="section-content"
            style="display: {{ 'block' if default_state == 'expanded' else 'none' }};">

.. container:: section-inner

{{ content|indent(3) }}

.. raw:: html

       </div>
   </div>

{% endmacro %}

{# Render type/feature badges #}
{% macro render_badges(obj) %}
.. container:: badges

   {% if obj.type == 'class' %}
       {% if 'BaseModel' in (obj.bases|map(attribute='name')|list) %}
   .. image:: https://img.shields.io/badge/Pydantic-Model-green
      :alt: Pydantic Model
       {% endif %}
       {% if 'Agent' in (obj.bases|map(attribute='name')|list) %}
   .. image:: https://img.shields.io/badge/Haive-Agent-blue
      :alt: Haive Agent
       {% endif %}
       {% if obj.is_abstract %}
   .. image:: https://img.shields.io/badge/Abstract-Class-orange
      :alt: Abstract Class
       {% endif %}
       {% if obj.is_dataclass %}
   .. image:: https://img.shields.io/badge/Python-Dataclass-purple
      :alt: Dataclass
       {% endif %}
   {% endif %}

   {% if obj.is_async %}
   .. image:: https://img.shields.io/badge/async-await-brightgreen
      :alt: Async Support
   {% endif %}

   {% if obj.is_deprecated %}
   .. image:: https://img.shields.io/badge/status-deprecated-red
      :alt: Deprecated
   {% endif %}

{% endmacro %}

{# Render parameter documentation #}
{% macro render_parameters(parameters, show_types=True, show_defaults=True) %}
{% for param in parameters %}
* **{{ param.name }}**
  {%- if show_types and param.annotation %} ({{ render_type_annotation(param.annotation) }}){% endif %}
  {%- if show_defaults and param.default is defined %} = ``{{ param.default }}``{% endif %}
  {%- if param.description %} -- {{ param.description }}{% endif %}
  {%- if param.optional %} *(optional)*{% endif %}
{% endfor %}
{% endmacro %}

{# Render type annotation with links #}
{% macro render_type_annotation(annotation) %}
{%- if annotation is string -%}
    {%- set parts = parse_type_annotation(annotation) -%}
    {%- for part in parts -%}
        {%- if part.is_link -%}:class:`{{ part.text }}`{%- else -%}{{ part.text }}{%- endif -%}
    {%- endfor -%}
{%- else -%}
    ``{{ annotation }}``
{%- endif -%}
{% endmacro %}

{# Safe attribute access with default #}
{% macro safe_attr(obj, path, default='') -%}
{%- set value = obj -%}
{%- for part in path.split('.') -%}
    {%- if value is mapping and part in value -%}
        {%- set value = value[part] -%}
    {%- elif value is not string and value is not number and part in value -%}
        {%- set value = value[part] -%}
    {%- else -%}
        {{- default -}}
        {%- break -%}
    {%- endif -%}
{%- endfor -%}
{%- if not loop.last -%}{{- value -}}{%- endif -%}
{%- endmacro %}
```

## Pydantic Model Complete Template

A comprehensive template for Pydantic BaseModel classes with field tables, validators, and configuration display.

### File: `_autoapi_templates/python/types/pydantic_model.rst`

```jinja2
{% extends "python/base/_layout.rst" %}

{% block content %}

.. py:class:: {{ obj.name }}{% if obj.bases %}({{ obj.bases|map(attribute='name')|join(', ') }}){% endif %}
   :module: {{ obj.module }}

   {% if obj.docstring %}
   {{ obj.docstring|indent(3) }}
   {% endif %}

   {# Quick field overview #}
   .. container:: model-overview

      .. grid:: 2
         :gutter: 2

         .. grid-item-card:: Field Summary
            :class-card: field-summary-card

            * **Total fields**: {{ obj.fields|length }}
            * **Required fields**: {{ obj.fields|selectattr('required')|list|length }}
            * **Optional fields**: {{ obj.fields|rejectattr('required')|list|length }}
            * **Validated fields**: {{ obj.fields|selectattr('validators')|list|length }}

         .. grid-item-card:: Model Configuration
            :class-card: config-summary-card

            {% set config = obj.model_config|default({}) %}
            * **Extra fields**: {{ config.extra|default('forbid') }}
            * **Validate assignment**: {{ config.validate_assignment|default(false) }}
            * **Frozen**: {{ config.frozen|default(false) }}
            * **Use enum values**: {{ config.use_enum_values|default(false) }}

   {# Detailed field documentation #}
   .. container:: fields-section

      .. list-table:: Model Fields
         :header-rows: 1
         :class: model-fields-table
         :widths: 20 20 10 20 30

         * - Field Name
           - Type
           - Required
           - Default
           - Description
         {% for field in obj.fields|sort(attribute='name') %}
         * - **{{ field.name }}**
           - ``{{ field.annotation|format_type }}``
           - {% if field.required %}✓{% else %}✗{% endif %}
           - {% if not field.required %}``{{ field.default|format_value }}``{% else %}—{% endif %}
           - {{ field.description|default('—', true)|truncate(100) }}
         {% endfor %}

   {# Field details with validation #}
   {% for field in obj.fields|sort(attribute='name') %}
   {% set field_id = obj.id + '.' + field.name %}
   {{ progressive_section(
       'Field: ' + field.name,
       render_pydantic_field_detail(field, field_id),
       field_id|slugify,
       'collapsed',
       'low',
       '🔍'
   ) }}
   {% endfor %}

   {# Validators section #}
   {% set validators = obj.validators|default([]) %}
   {% set field_validators = obj.field_validators|default([]) %}
   {% set root_validators = obj.root_validators|default([]) %}

   {% if validators or field_validators or root_validators %}
   {{ progressive_section(
       'Validators',
       render_pydantic_validators(validators, field_validators, root_validators),
       obj.id|slugify + '-validators',
       'collapsed',
       'medium',
       (validators|length + field_validators|length + root_validators|length)|string
   ) }}
   {% endif %}

   {# Model methods #}
   {% set model_methods = obj.methods|rejectattr('name', 'in', ['__init__', '__str__', '__repr__'])|list %}
   {% if model_methods %}
   {{ progressive_section(
       'Methods',
       render_method_list(model_methods),
       obj.id|slugify + '-methods',
       'collapsed',
       'medium',
       model_methods|length|string
   ) }}
   {% endif %}

   {# Configuration details #}
   {% if obj.model_config %}
   {{ progressive_section(
       'Advanced Configuration',
       render_pydantic_config_detail(obj.model_config),
       obj.id|slugify + '-config',
       'collapsed',
       'low'
   ) }}
   {% endif %}

   {# JSON Schema #}
   {{ progressive_section(
       'JSON Schema',
       render_json_schema_pretty(obj),
       obj.id|slugify + '-schema',
       'collapsed',
       'low'
   ) }}

   {# Usage examples #}
   .. rubric:: Usage Examples

   .. tabs::

      .. tab:: Basic Usage

         .. code-block:: python

            from {{ obj.module }} import {{ obj.name }}

            # Create instance with required fields
            instance = {{ obj.name }}(
            {%- for field in obj.fields if field.required %}
                {{ field.name }}={{ field.example|format_example }},
            {%- endfor %}
            )

            # Access fields
            {%- for field in obj.fields[:3] %}
            print(instance.{{ field.name }})
            {%- endfor %}

      .. tab:: Validation

         .. code-block:: python

            from pydantic import ValidationError

            # Valid instance
            try:
                valid = {{ obj.name }}(
                    {%- for field in obj.fields if field.required %}
                    {{ field.name }}={{ field.example|format_example }},
                    {%- endfor %}
                )
                print("✓ Validation passed")
            except ValidationError as e:
                print(f"✗ Validation failed: {e}")

            # Invalid instance (example)
            try:
                invalid = {{ obj.name }}(
                    # Missing required fields or invalid types
                )
            except ValidationError as e:
                print(f"✗ Expected error: {e}")

      .. tab:: Serialization

         .. code-block:: python

            # Convert to dict
            data_dict = instance.model_dump()
            print(data_dict)

            # Convert to JSON
            json_str = instance.model_dump_json(indent=2)
            print(json_str)

            # Exclude certain fields
            partial = instance.model_dump(exclude={'internal_field'})

            # Include only specific fields
            subset = instance.model_dump(include={'id', 'name'})

      .. tab:: Deserialization

         .. code-block:: python

            # From dict
            data = {
                {%- for field in obj.fields if field.required %}
                '{{ field.name }}': {{ field.example|format_example }},
                {%- endfor %}
            }
            instance = {{ obj.name }}.model_validate(data)

            # From JSON string
            json_str = '{"field": "value"}'
            instance = {{ obj.name }}.model_validate_json(json_str)

            # With validation
            try:
                instance = {{ obj.name }}.model_validate(untrusted_data)
            except ValidationError as e:
                handle_validation_error(e)

{% endblock content %}

{# Macro for rendering field details #}
{% macro render_pydantic_field_detail(field, field_id) %}
.. py:attribute:: {{ field.name }}
   :type: {{ field.annotation }}
   {% if not field.required %}:value: {{ field.default|format_value }}{% endif %}

   {{ field.description|default('No description provided.', true) }}

   {% if field.constraints %}
   **Constraints:**

   {% for constraint, value in field.constraints.items() %}
   * **{{ constraint }}**: ``{{ value }}``
   {% endfor %}
   {% endif %}

   {% if field.validators %}
   **Validators:**

   {% for validator in field.validators %}
   * ``{{ validator.name }}``{% if validator.description %} - {{ validator.description }}{% endif %}
   {% endfor %}
   {% endif %}

   {% if field.examples %}
   **Examples:**

   .. code-block:: python

      {% for example in field.examples %}
      obj.{{ field.name }} = {{ example }}
      {% endfor %}
   {% endif %}

{% endmacro %}
```

## Agent Class Complete Template

A sophisticated template for Haive Agent classes with tools, configuration, and workflow visualization.

### File: `_autoapi_templates/python/types/agent_class.rst`

```jinja2
{% extends "python/base/_layout.rst" %}

{% block content %}

.. py:class:: {{ obj.name }}{% if obj.bases %}({{ obj.bases|map(attribute='name')|join(', ') }}){% endif %}
   :module: {{ obj.module }}

   {% if obj.docstring %}
   {{ obj.docstring|indent(3) }}
   {% endif %}

   {# Agent overview cards #}
   .. container:: agent-overview

      .. grid:: 3
         :gutter: 2

         .. grid-item-card:: Agent Type
            :class-card: agent-type-card

            .. container:: card-content

               .. image:: /_static/icons/agent-{{ detect_agent_type(obj)|lower }}.svg
                  :width: 48
                  :alt: {{ detect_agent_type(obj) }} Agent

               **{{ detect_agent_type(obj) }} Agent**

               {% if obj.is_async %}
               ✓ Async Support
               {% endif %}
               {% if obj.is_streaming %}
               ✓ Streaming Support
               {% endif %}

         .. grid-item-card:: Tools & Capabilities
            :class-card: tools-card

            {% if obj.tools %}
            **{{ obj.tools|length }} Tools Available:**

            {% for tool in obj.tools[:5] %}
            * {{ tool.name }}
            {% endfor %}
            {% if obj.tools|length > 5 %}
            * *... and {{ obj.tools|length - 5 }} more*
            {% endif %}
            {% else %}
            *No tools configured*
            {% endif %}

         .. grid-item-card:: Configuration
            :class-card: config-card

            **Engine**: {{ obj.engine.__class__.__name__|default('AugLLMConfig') }}

            {% set config = obj.engine_config|default({}) %}
            * Model: {{ config.model|default('default') }}
            * Temperature: {{ config.temperature|default('0.7') }}
            {% if config.structured_output_model %}
            * Output: :class:`{{ config.structured_output_model }}`
            {% endif %}

   {# Workflow visualization #}
   {% if obj.workflow or can_infer_workflow(obj) %}
   .. container:: workflow-section

      .. mermaid::
         :caption: Agent Workflow
         :align: center

         graph TD
             Start([User Input]) --> Preprocess[Preprocess Input]
             Preprocess --> MainLogic{Main Agent Logic}

             {% if 'ReactAgent' in obj.bases|map(attribute='name')|list %}
             MainLogic --> Think[Think/Reason]
             Think --> Act[Select Tool]
             Act --> Observe[Execute Tool]
             Observe --> Think
             Think --> |Done| Response[Generate Response]
             {% elif 'SimpleAgent' in obj.bases|map(attribute='name')|list %}
             MainLogic --> Generate[Generate Response]
             Generate --> Response[Return Response]
             {% else %}
             MainLogic --> Custom[Custom Logic]
             Custom --> Response[Return Response]
             {% endif %}

             Response --> End([Output])

             style Start fill:#e1f5fe
             style End fill:#e8f5e9
             style MainLogic fill:#fff3b8

   {% endif %}

   {# Core methods section #}
   .. rubric:: Core Methods

   .. container:: core-methods

      {% set core_method_names = ['run', 'arun', 'invoke', 'ainvoke', '__call__'] %}
      {% for method_name in core_method_names %}
      {% set method = obj.methods|selectattr('name', 'equalto', method_name)|first %}
      {% if method %}

      .. container:: core-method-card

         .. py:method:: {{ method.name }}{{ format_signature(method.signature) }}
            {% if method.is_async %}:async:{% endif %}

            {{ method.short_description|default('Execute the agent.', true) }}

            {% if method.parameters %}
            :Parameters:
               {{ render_parameters(method.parameters)|indent(3) }}
            {% endif %}

            {% if method.returns %}
            :Returns: {{ render_type_annotation(method.returns) }}
               {%- if method.return_description %} -- {{ method.return_description }}{% endif %}
            {% endif %}

            **Example:**

            .. code-block:: python

               {% if method.is_async %}await {% endif %}agent.{{ method.name }}(
                   {%- for param in method.parameters if param.name not in ['self', 'cls'] %}
                   {{ param.name }}={{ param.example|format_example }},
                   {%- endfor %}
               )

      {% endif %}
      {% endfor %}

   {# Tools documentation #}
   {% if obj.tools %}
   {{ progressive_section(
       'Available Tools',
       render_agent_tools(obj.tools),
       obj.id|slugify + '-tools',
       'expanded',
       'high',
       obj.tools|length|string
   ) }}
   {% endif %}

   {# State schema #}
   {% if obj.state_schema %}
   {{ progressive_section(
       'State Schema',
       render_state_schema(obj.state_schema),
       obj.id|slugify + '-state',
       'collapsed',
       'medium'
   ) }}
   {% endif %}

   {# Configuration options #}
   {{ progressive_section(
       'Configuration Options',
       render_agent_config_options(obj),
       obj.id|slugify + '-config',
       'collapsed',
       'medium'
   ) }}

   {# All methods #}
   {% set other_methods = obj.methods|rejectattr('name', 'in', core_method_names)|list %}
   {% if other_methods %}
   {{ progressive_section(
       'Additional Methods',
       render_method_list(other_methods),
       obj.id|slugify + '-methods',
       'collapsed',
       'low',
       other_methods|length|string
   ) }}
   {% endif %}

   {# Integration examples #}
   .. rubric:: Integration Examples

   .. tabs::

      .. tab:: Basic Usage

         .. code-block:: python

            from {{ obj.module }} import {{ obj.name }}
            {% if obj.engine_config %}
            from {{ obj.engine_config.module }} import {{ obj.engine_config.name }}
            {% endif %}

            # Initialize agent
            agent = {{ obj.name }}(
                name="my_agent",
                {% if obj.required_params %}
                {%- for param in obj.required_params %}
                {{ param.name }}={{ param.example|format_example }},
                {%- endfor %}
                {% endif %}
            )

            # Execute agent
            response = {% if obj.has_async %}await {% endif %}agent.run("Hello, how can you help?")
            print(response)

      {% if obj.tools %}
      .. tab:: With Tools

         .. code-block:: python

            # Configure agent with specific tools
            agent = {{ obj.name }}(
                name="agent_with_tools",
                tools=[
                    {%- for tool in obj.tools[:3] %}
                    {{ tool.name }}(),
                    {%- endfor %}
                ]
            )

            # Agent will automatically use tools as needed
            result = {% if obj.has_async %}await {% endif %}agent.run(
                "{{ obj.example_tool_query|default('Use the available tools to help me') }}"
            )

      {% endif %}

      {% if obj.structured_output_model %}
      .. tab:: Structured Output

         .. code-block:: python

            from {{ obj.structured_output_model.module }} import {{ obj.structured_output_model.name }}

            # Agent configured for structured output
            agent = {{ obj.name }}(
                structured_output_model={{ obj.structured_output_model.name }}
            )

            # Get structured response
            result = {% if obj.has_async %}await {% endif %}agent.run("Analyze this data")
            assert isinstance(result, {{ obj.structured_output_model.name }})
            print(result.model_dump())

      {% endif %}

      .. tab:: Advanced Config

         .. code-block:: python

            # Full configuration example
            config = AugLLMConfig(
                model="gpt-4",
                temperature=0.7,
                max_tokens=1000,
                system_message="You are a helpful assistant."
            )

            agent = {{ obj.name }}(
                name="advanced_agent",
                engine=config,
                {% if obj.memory_config %}
                memory={{ obj.memory_config.example }},
                {% endif %}
                {% if obj.callback_config %}
                callbacks=[LoggingCallback(), MetricsCallback()],
                {% endif %}
            )

{% endblock content %}

{# Macro for rendering agent tools #}
{% macro render_agent_tools(tools) %}
.. list-table:: Available Tools
   :header-rows: 1
   :class: tools-table

   * - Tool Name
     - Description
     - Parameters
     - Returns
   {% for tool in tools %}
   * - **{{ tool.name }}**
     - {{ tool.description|truncate(100) }}
     - {% if tool.parameters %}{{ tool.parameters|map(attribute='name')|join(', ') }}{% else %}None{% endif %}
     - {{ tool.return_type|default('str') }}
   {% endfor %}

{% for tool in tools %}
.. container:: tool-detail

   .. rubric:: {{ tool.name }}

   {{ tool.description }}

   {% if tool.parameters %}
   **Parameters:**

   {% for param in tool.parameters %}
   * **{{ param.name }}** ({{ param.type }}){% if param.description %} - {{ param.description }}{% endif %}
   {% endfor %}
   {% endif %}

   **Example Usage:**

   .. code-block:: python

      result = agent.use_tool(
          "{{ tool.name }}",
          {%- for param in tool.parameters %}
          {{ param.name }}={{ param.example|format_example }},
          {%- endfor %}
      )

{% endfor %}
{% endmacro %}
```

## Module Documentation Template

Template for module-level documentation with intelligent organization of contents.

### File: `_autoapi_templates/python/module.rst`

```jinja2
{% extends "python/base/_layout.rst" %}

{% block title %}
{% if obj.type == 'package' %}
:mod:`{{ obj.name }}` Package
{% else %}
:mod:`{{ obj.name }}` Module
{% endif %}
{{ "=" * (obj.name|length + 10) }}
{% endblock %}

{% block content %}

.. py:module:: {{ obj.id }}

   {% if obj.docstring %}
   {{ obj.docstring|indent(3) }}
   {% endif %}

   {# Module overview statistics #}
   .. container:: module-stats

      .. grid:: 4
         :gutter: 2

         .. grid-item::

            **{{ obj.classes|length }}**
            Classes

         .. grid-item::

            **{{ obj.functions|length }}**
            Functions

         .. grid-item::

            **{{ obj.submodules|length }}**
            Submodules

         .. grid-item::

            **{{ obj.all|length if obj.all else 'All' }}**
            Exports

   {# Quick navigation #}
   {% if obj.classes or obj.functions or obj.submodules %}
   .. container:: quick-nav

      **Quick Navigation:**

      {% if obj.classes %}
      * :ref:`Classes <{{ obj.id }}-classes>` ({{ obj.classes|length }})
      {% endif %}
      {% if obj.functions %}
      * :ref:`Functions <{{ obj.id }}-functions>` ({{ obj.functions|length }})
      {% endif %}
      {% if obj.submodules %}
      * :ref:`Submodules <{{ obj.id }}-submodules>` ({{ obj.submodules|length }})
      {% endif %}
      {% if obj.attributes %}
      * :ref:`Module Attributes <{{ obj.id }}-attributes>` ({{ obj.attributes|length }})
      {% endif %}
   {% endif %}

   {# Submodules section #}
   {% if obj.submodules %}
   .. _{{ obj.id }}-submodules:

   Submodules
   ----------

   .. autosummary::
      :toctree: {{ obj.name }}
      :template: module.rst
      :recursive:

      {% for submodule in obj.submodules|sort(attribute='name') %}
      {{ submodule.id }}
      {% endfor %}
   {% endif %}

   {# Classes section with categorization #}
   {% if obj.classes %}
   .. _{{ obj.id }}-classes:

   Classes
   -------

   {% set class_categories = categorize_classes(obj.classes) %}

   {% for category, classes in class_categories.items() %}
   {% if classes %}

   {{ category }}
   {{ "~" * category|length }}

   .. autosummary::
      :toctree: {{ obj.name }}
      :template: class.rst

      {% for class in classes|sort(attribute='name') %}
      {{ class.id }}
      {% endfor %}

   {% endif %}
   {% endfor %}
   {% endif %}

   {# Functions section with categorization #}
   {% if obj.functions %}
   .. _{{ obj.id }}-functions:

   Functions
   ---------

   {% set public_functions = obj.functions|rejectattr('name', 'match', '^_')|list %}
   {% set private_functions = obj.functions|selectattr('name', 'match', '^_')|list %}

   {% if public_functions %}
   Public Functions
   ~~~~~~~~~~~~~~~~

   .. autosummary::
      :toctree: {{ obj.name }}
      :template: function.rst

      {% for func in public_functions|sort(attribute='name') %}
      {{ func.id }}
      {% endfor %}
   {% endif %}

   {% if private_functions and 'private-members' in autoapi_options %}
   Private Functions
   ~~~~~~~~~~~~~~~~~

   .. autosummary::
      :toctree: {{ obj.name }}
      :template: function.rst

      {% for func in private_functions|sort(attribute='name') %}
      {{ func.id }}
      {% endfor %}
   {% endif %}
   {% endif %}

   {# Module attributes #}
   {% if obj.attributes %}
   .. _{{ obj.id }}-attributes:

   Module Attributes
   -----------------

   {% for attr in obj.attributes|sort(attribute='name') %}
   .. py:data:: {{ attr.name }}
      {% if attr.annotation %}:type: {{ attr.annotation }}{% endif %}
      {% if attr.value is defined %}:value: {{ attr.value|format_value }}{% endif %}

      {% if attr.docstring %}
      {{ attr.docstring|indent(6) }}
      {% else %}
      *No description available.*
      {% endif %}

   {% endfor %}
   {% endif %}

   {# Module-level examples #}
   {% if obj.examples %}
   Examples
   --------

   {% for example in obj.examples %}
   {{ example.title|default('Example ' + loop.index|string) }}
   {{ "~" * (example.title|default('Example ' + loop.index|string)|length) }}

   {{ example.content }}

   {% endfor %}
   {% endif %}

{% endblock content %}

{# Helper macro to categorize classes #}
{% macro categorize_classes(classes) %}
{% set categories = {
    'Exceptions': [],
    'Pydantic Models': [],
    'Agents': [],
    'Base Classes': [],
    'Dataclasses': [],
    'Enums': [],
    'Protocols': [],
    'Regular Classes': []
} %}

{% for class in classes %}
    {% if class.is_exception %}
        {% do categories['Exceptions'].append(class) %}
    {% elif is_pydantic_model(class) %}
        {% do categories['Pydantic Models'].append(class) %}
    {% elif is_agent_class(class) %}
        {% do categories['Agents'].append(class) %}
    {% elif class.is_abstract or 'Base' in class.name %}
        {% do categories['Base Classes'].append(class) %}
    {% elif class.is_dataclass %}
        {% do categories['Dataclasses'].append(class) %}
    {% elif 'Enum' in (class.bases|map(attribute='name')|list) %}
        {% do categories['Enums'].append(class) %}
    {% elif 'Protocol' in (class.bases|map(attribute='name')|list) %}
        {% do categories['Protocols'].append(class) %}
    {% else %}
        {% do categories['Regular Classes'].append(class) %}
    {% endif %}
{% endfor %}

{{ categories }}
{% endmacro %}
```

## Function/Method Templates

Templates for documenting functions and methods with rich parameter documentation.

### File: `_autoapi_templates/python/function.rst`

```jinja2
{% extends "python/base/_layout.rst" %}

{% block content %}

.. py:function:: {{ obj.name }}{{ format_signature(obj.signature, multiline=True) }}
   :module: {{ obj.module }}
   {% if obj.is_async %}:async:{% endif %}

   {% if obj.docstring %}
   {{ obj.docstring|indent(3) }}
   {% endif %}

   {# Parameter documentation with rich formatting #}
   {% if obj.parameters %}
   :Parameters:
      {% for param in obj.parameters %}
      {% if param.name not in ['self', 'cls'] %}
      * **{{ param.name }}**
        {%- if param.annotation %} ({{ render_type_annotation(param.annotation) }}){% endif %}
        {%- if param.default is defined %} = ``{{ param.default|format_value }}``{% endif %}
        {%- if param.description %} -- {{ param.description }}{% endif %}

        {% if param.constraints %}
        .. container:: param-constraints

           {% for constraint, value in param.constraints.items() %}
           * {{ constraint }}: ``{{ value }}``
           {% endfor %}
        {% endif %}

        {% if param.examples %}
        .. container:: param-examples

           **Examples:** {% for ex in param.examples %}``{{ ex }}``{% if not loop.last %}, {% endif %}{% endfor %}
        {% endif %}
      {% endif %}
      {% endfor %}
   {% endif %}

   {# Returns documentation #}
   {% if obj.returns %}
   :Returns:
      {{ render_type_annotation(obj.returns) }}
      {%- if obj.return_description %} -- {{ obj.return_description }}{% endif %}

      {% if obj.return_examples %}
      .. container:: return-examples

         **Example returns:**

         .. code-block:: python

            {% for example in obj.return_examples %}
            {{ example }}
            {% endfor %}
      {% endif %}
   {% endif %}

   {# Yields documentation for generators #}
   {% if obj.yields %}
   :Yields:
      {{ render_type_annotation(obj.yields) }}
      {%- if obj.yield_description %} -- {{ obj.yield_description }}{% endif %}
   {% endif %}

   {# Raises documentation #}
   {% if obj.raises %}
   :Raises:
      {% for exception in obj.raises %}
      * **{{ exception.type }}** -- {{ exception.description }}
        {% if exception.conditions %}

        *Raised when:* {{ exception.conditions }}
        {% endif %}
      {% endfor %}
   {% endif %}

   {# Decorators #}
   {% if obj.decorators %}
   .. container:: decorators

      **Decorators:**
      {% for decorator in obj.decorators %}
      * ``{{ decorator }}``
      {% endfor %}
   {% endif %}

   {# Usage examples #}
   {% if obj.examples or can_generate_examples(obj) %}
   .. rubric:: Examples

   .. tabs::

      {% if obj.examples %}
      {% for example in obj.examples %}
      .. tab:: {{ example.title|default('Example ' + loop.index|string) }}

         {{ example.description|indent(9) }}

         .. code-block:: python

            {{ example.code|indent(12) }}

         {% if example.output %}
         **Output:**

         .. code-block:: {{ example.output_type|default('text') }}

            {{ example.output|indent(12) }}
         {% endif %}

      {% endfor %}
      {% else %}
      .. tab:: Basic Usage

         .. code-block:: python

            {% if obj.module != '__main__' %}
            from {{ obj.module }} import {{ obj.name }}

            {% endif %}
            result = {% if obj.is_async %}await {% endif %}{{ obj.name }}(
                {%- for param in obj.parameters if param.name not in ['self', 'cls'] and param.default is not defined %}
                {{ param.name }}={{ generate_example_value(param) }},
                {%- endfor %}
            )
      {% endif %}

   {% endif %}

   {# See also section #}
   {% if obj.see_also %}
   .. seealso::

      {% for ref in obj.see_also %}
      * :func:`{{ ref.link }}` -- {{ ref.description }}
      {% endfor %}
   {% endif %}

   {# Notes section #}
   {% if obj.notes %}
   .. note::

      {{ obj.notes|indent(6) }}
   {% endif %}

   {# Version information #}
   {% if obj.version_added %}
   .. versionadded:: {{ obj.version_added }}
   {% endif %}

   {% if obj.version_changed %}
   .. versionchanged:: {{ obj.version_changed }}
      {{ obj.version_changed_description }}
   {% endif %}

   {% if obj.deprecated %}
   .. deprecated:: {{ obj.deprecated_version }}
      {{ obj.deprecated_description }}
   {% endif %}

{% endblock content %}
```

### File: `_autoapi_templates/python/method.rst`

```jinja2
{# Method template - similar to function but with class context #}
{% extends "python/function.rst" %}

{% block content %}

.. py:method:: {{ obj.name }}{{ format_signature(obj.signature, multiline=True) }}
   {% if obj.is_async %}:async:{% endif %}
   {% if obj.is_classmethod %}:classmethod:{% endif %}
   {% if obj.is_staticmethod %}:staticmethod:{% endif %}
   {% if obj.is_property %}:property:{% endif %}

   {# Rest inherits from function template #}
   {{ super() }}

{% endblock content %}
```

## Enum Class Template

Specialized template for Enum classes with value documentation.

### File: `_autoapi_templates/python/types/enum_class.rst`

```jinja2
{% extends "python/base/_layout.rst" %}

{% block content %}

.. py:class:: {{ obj.name }}{% if obj.bases %}({{ obj.bases|map(attribute='name')|join(', ') }}){% endif %}
   :module: {{ obj.module }}

   {% if obj.docstring %}
   {{ obj.docstring|indent(3) }}
   {% endif %}

   {# Enum value overview #}
   .. container:: enum-overview

      **Total Values:** {{ obj.members|length }}

      {% set value_types = obj.members|map(attribute='value')|map('type')|unique|list %}
      **Value Types:** {{ value_types|join(', ') }}

   {# Value table with grouping #}
   {% set groups = group_enum_values(obj.members) %}

   {% if groups|length == 1 %}
   {# Single group - simple table #}
   .. list-table:: Enumeration Values
      :header-rows: 1
      :class: enum-values-table

      * - Name
        - Value
        - Description
      {% for member in obj.members|sort(attribute='name') %}
      * - **{{ obj.name }}.{{ member.name }}**
        - ``{{ member.value }}``
        - {{ member.description|default('—', true) }}
      {% endfor %}

   {% else %}
   {# Multiple groups - tabbed view #}
   .. tabs::

      {% for group_name, members in groups.items() %}
      .. tab:: {{ group_name }}

         .. list-table::
            :header-rows: 1

            * - Name
              - Value
              - Description
            {% for member in members|sort(attribute='name') %}
            * - **{{ member.name }}**
              - ``{{ member.value }}``
              - {{ member.description|default('—', true) }}
            {% endfor %}

      {% endfor %}
   {% endif %}

   {# Usage examples #}
   .. rubric:: Usage Examples

   .. code-block:: python

      from {{ obj.module }} import {{ obj.name }}

      # Access enum values
      {% for member in obj.members[:3] %}
      {{ member.name|lower }}_value = {{ obj.name }}.{{ member.name }}
      print({{ member.name|lower }}_value)  # Output: {{ obj.name }}.{{ member.name }}
      print({{ member.name|lower }}_value.value)  # Output: {{ member.value }}
      {% endfor %}

      # Check membership
      if some_value in {{ obj.name }}:
          print(f"{some_value} is a valid {{ obj.name }}")

      # Iterate over all values
      for item in {{ obj.name }}:
          print(f"{item.name} = {item.value}")

      # Get by value
      {% if obj.members %}
      item = {{ obj.name }}({{ obj.members[0].value|format_value }})
      assert item == {{ obj.name }}.{{ obj.members[0].name }}
      {% endif %}

   {# Methods if any #}
   {% set custom_methods = obj.methods|rejectattr('name', 'in', ['__str__', '__repr__', '__init__'])|list %}
   {% if custom_methods %}

   .. rubric:: Methods

   {% for method in custom_methods %}
   .. automethod:: {{ obj.id }}.{{ method.name }}
   {% endfor %}
   {% endif %}

   {# Functional API example #}
   {{ progressive_section(
       'Alternative Creation Methods',
       render_enum_functional_api(obj),
       obj.id|slugify + '-functional',
       'collapsed',
       'low'
   ) }}

{% endblock content %}

{# Helper to group enum values #}
{% macro group_enum_values(members) %}
{% set groups = {} %}
{% for member in members %}
    {% set prefix = member.name.split('_')[0] if '_' in member.name else 'Values' %}
    {% if prefix not in groups %}
        {% set _ = groups.update({prefix: []}) %}
    {% endif %}
    {% do groups[prefix].append(member) %}
{% endfor %}

{# Return single group if no meaningful grouping #}
{% if groups|length > 5 or groups|length == 1 %}
    {{ {'All Values': members} }}
{% else %}
    {{ groups }}
{% endif %}
{% endmacro %}

{# Functional API examples #}
{% macro render_enum_functional_api(obj) %}
.. code-block:: python

   from enum import auto

   # Functional API creation
   {{ obj.name }} = Enum(
       '{{ obj.name }}',
       [
           {%- for member in obj.members[:5] %}
           ('{{ member.name }}', {{ member.value|format_value }}),
           {%- endfor %}
           # ...
       ]
   )

   # Auto-value generation
   {{ obj.name }}Auto = Enum(
       '{{ obj.name }}',
       [{% for member in obj.members[:5] %}'{{ member.name }}' {% endfor %}]
   )

{% endmacro %}
```

## Exception Class Template

Template for exception classes with cause and handling documentation.

### File: `_autoapi_templates/python/types/exception_class.rst`

```jinja2
{% extends "python/base/_layout.rst" %}

{% block content %}

.. py:exception:: {{ obj.name }}{% if obj.bases %}({{ obj.bases|map(attribute='name')|join(', ') }}){% endif %}
   :module: {{ obj.module }}

   {% if obj.docstring %}
   {{ obj.docstring|indent(3) }}
   {% endif %}

   {# Exception hierarchy #}
   .. container:: exception-hierarchy

      **Exception Hierarchy:**

      .. code-block:: text

         {% for ancestor in get_exception_hierarchy(obj) %}
         {{ '  ' * loop.index0 }}└─ {{ ancestor.name }}
         {% endfor %}
         {{ '  ' * get_exception_hierarchy(obj)|length }}└─ {{ obj.name }} (this exception)

   {# When raised section #}
   {% if obj.when_raised %}
   .. rubric:: When Raised

   This exception is raised when:

   {% for condition in obj.when_raised %}
   * {{ condition }}
   {% endfor %}
   {% endif %}

   {# Attributes #}
   {% if obj.attributes %}
   .. rubric:: Attributes

   {% for attr in obj.attributes %}
   .. py:attribute:: {{ attr.name }}
      {% if attr.type %}:type: {{ attr.type }}{% endif %}

      {{ attr.description|default('Exception attribute.', true)|indent(6) }}

   {% endfor %}
   {% endif %}

   {# Handling examples #}
   .. rubric:: Handling Examples

   .. tabs::

      .. tab:: Basic Handling

         .. code-block:: python

            from {{ obj.module }} import {{ obj.name }}

            try:
                # Code that might raise {{ obj.name }}
                risky_operation()
            except {{ obj.name }} as e:
                print(f"Caught {{ obj.name }}: {e}")
                # Handle the specific error
                handle_error(e)

      .. tab:: With Context

         .. code-block:: python

            try:
                perform_operation()
            except {{ obj.name }} as e:
                # Log the error with context
                logger.error(
                    "Operation failed",
                    exc_info=True,
                    extra={
                        {% for attr in obj.attributes[:3] %}
                        '{{ attr.name }}': getattr(e, '{{ attr.name }}', None),
                        {% endfor %}
                    }
                )
                # Re-raise or handle
                raise

      {% if obj.attributes %}
      .. tab:: Accessing Attributes

         .. code-block:: python

            try:
                validate_data(data)
            except {{ obj.name }} as e:
                {% for attr in obj.attributes %}
                # Access {{ attr.name }}
                {{ attr.name }} = e.{{ attr.name }}
                print(f"{{ attr.name }}: {{ '{' }}{{ attr.name }}{{ '}' }}")
                {% endfor %}
      {% endif %}

      .. tab:: Raising

         .. code-block:: python

            # Raise with message
            raise {{ obj.name }}("Something went wrong")

            {% if obj.attributes %}
            # Raise with attributes
            raise {{ obj.name }}(
                "Detailed error message",
                {% for attr in obj.attributes[:2] %}
                {{ attr.name }}={{ attr.example|format_example }},
                {% endfor %}
            )
            {% endif %}

            # Raise from another exception
            try:
                dangerous_operation()
            except SomeError as e:
                raise {{ obj.name }}("High-level error") from e

   {# Related exceptions #}
   {% if obj.related_exceptions %}
   .. rubric:: Related Exceptions

   {% for related in obj.related_exceptions %}
   * :exc:`{{ related.name }}` -- {{ related.description }}
   {% endfor %}
   {% endif %}

{% endblock content %}
```

## Dataclass Template

Template for Python dataclasses with field documentation and examples.

### File: `_autoapi_templates/python/types/dataclass.rst`

```jinja2
{% extends "python/base/_layout.rst" %}

{% block content %}

.. py:class:: {{ obj.name }}{% if obj.bases %}({{ obj.bases|map(attribute='name')|join(', ') }}){% endif %}
   :module: {{ obj.module }}

   {% if obj.docstring %}
   {{ obj.docstring|indent(3) }}
   {% endif %}

   {# Dataclass configuration #}
   .. container:: dataclass-config

      **Dataclass Configuration:**

      {% set dc_config = extract_dataclass_config(obj) %}
      * **Frozen**: {{ '✓' if dc_config.frozen else '✗' }} ({{ 'immutable' if dc_config.frozen else 'mutable' }})
      * **Eq**: {{ '✓' if dc_config.eq else '✗' }} ({{ 'generates __eq__' if dc_config.eq else 'no __eq__' }})
      * **Order**: {{ '✓' if dc_config.order else '✗' }} ({{ 'comparable' if dc_config.order else 'not comparable' }})
      * **Slots**: {{ '✓' if dc_config.slots else '✗' }} ({{ 'uses __slots__' if dc_config.slots else 'regular attributes' }})

   {# Fields table #}
   .. list-table:: Dataclass Fields
      :header-rows: 1
      :class: dataclass-fields-table

      * - Field
        - Type
        - Default
        - Factory
        - Description
      {% for field in obj.fields %}
      * - **{{ field.name }}**
        - ``{{ field.type|format_type }}``
        - {% if field.default is not none %}``{{ field.default|format_value }}``{% else %}—{% endif %}
        - {% if field.default_factory %}✓{% else %}—{% endif %}
        - {{ field.description|default('—', true)|truncate(80) }}
      {% endfor %}

   {# Field details #}
   {% for field in obj.fields %}
   .. py:attribute:: {{ field.name }}
      :type: {{ field.type }}
      {% if field.default is not none %}:value: {{ field.default|format_value }}{% endif %}

      {{ field.description|default('No description provided.', true)|indent(6) }}

      {% if field.metadata %}
      .. container:: field-metadata

         **Metadata:**

         {% for key, value in field.metadata.items() %}
         * **{{ key }}**: ``{{ value }}``
         {% endfor %}
      {% endif %}

   {% endfor %}

   {# Methods section #}
   {% set custom_methods = obj.methods|rejectattr('name', 'in', dataclass_generated_methods())|list %}
   {% if custom_methods %}

   .. rubric:: Methods

   {% for method in custom_methods %}
   {{ render_method_summary(method) }}
   {% endfor %}
   {% endif %}

   {# Usage examples #}
   .. rubric:: Usage Examples

   .. tabs::

      .. tab:: Creation

         .. code-block:: python

            from {{ obj.module }} import {{ obj.name }}

            # Create with all fields
            instance = {{ obj.name }}(
                {% for field in obj.fields if field.default is none and not field.default_factory %}
                {{ field.name }}={{ field.example|format_example }},
                {% endfor %}
            )

            # Create with defaults
            minimal = {{ obj.name }}(
                {% for field in obj.fields if field.default is none and not field.default_factory %}
                {{ field.name }}={{ field.example|format_example }}{{ ',' if not loop.last }}
                {% endfor %}
            )

            # Access fields
            {% for field in obj.fields[:3] %}
            print(instance.{{ field.name }})
            {% endfor %}

      .. tab:: Immutability

         .. code-block:: python

            {% if dc_config.frozen %}
            # This dataclass is frozen (immutable)
            instance = {{ obj.name }}(...)

            # This will raise an error:
            try:
                instance.{{ obj.fields[0].name }} = new_value
            except FrozenInstanceError:
                print("Cannot modify frozen dataclass")

            # Use replace() to create modified copy
            from dataclasses import replace
            new_instance = replace(
                instance,
                {{ obj.fields[0].name }}=new_value
            )
            {% else %}
            # This dataclass is mutable
            instance = {{ obj.name }}(...)

            # You can modify fields
            instance.{{ obj.fields[0].name }} = new_value
            {% endif %}

      {% if dc_config.order %}
      .. tab:: Comparison

         .. code-block:: python

            # Dataclass supports ordering
            obj1 = {{ obj.name }}(...)
            obj2 = {{ obj.name }}(...)

            # All comparison operations work
            print(obj1 < obj2)   # Less than
            print(obj1 <= obj2)  # Less than or equal
            print(obj1 > obj2)   # Greater than
            print(obj1 >= obj2)  # Greater than or equal
            print(obj1 == obj2)  # Equal
            print(obj1 != obj2)  # Not equal

            # Sorting works
            objects = [obj2, obj1, obj3]
            sorted_objects = sorted(objects)
      {% endif %}

      .. tab:: Serialization

         .. code-block:: python

            from dataclasses import asdict, astuple
            import json

            # Convert to dictionary
            data_dict = asdict(instance)
            print(data_dict)

            # Convert to tuple
            data_tuple = astuple(instance)
            print(data_tuple)

            # JSON serialization
            json_str = json.dumps(asdict(instance))

            # Create from dict
            new_instance = {{ obj.name }}(**data_dict)

   {# Post-init processing #}
   {% if '__post_init__' in obj.methods|map(attribute='name') %}
   .. note::

      This dataclass implements ``__post_init__`` for additional initialization logic.
      See the method documentation for details.
   {% endif %}

{% endblock content %}

{# Helper to identify dataclass-generated methods #}
{% macro dataclass_generated_methods() %}
[
    '__init__', '__repr__', '__eq__', '__hash__',
    '__lt__', '__le__', '__gt__', '__ge__'
]
{% endmacro %}
```

These complete template examples provide production-ready implementations for all major Python object types, with rich formatting, progressive disclosure, and comprehensive documentation features.
