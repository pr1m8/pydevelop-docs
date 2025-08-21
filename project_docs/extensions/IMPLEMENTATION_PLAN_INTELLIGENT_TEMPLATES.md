# Implementation Plan: Intelligent Template System

**Created**: 2025-01-30  
**Purpose**: Step-by-step implementation guide for the intelligent template system  
**Status**: Ready for Implementation

## Quick Start Implementation

### Step 1: Create Template Directory Structure (15 minutes)

```bash
cd /home/will/Projects/haive/backend/haive/tools/pydvlppy/src/pydevelop_docs/templates

# Create the intelligent template structure
mkdir -p _autoapi_templates/python/{_base,_components,_filters,_macros}

# Create base templates
touch _autoapi_templates/python/_base/{foundation.j2,progressive.j2,responsive.j2}
touch _autoapi_templates/python/_components/{navigation.j2,diagrams.j2,code_blocks.j2,metadata.j2,interactive.j2,media.j2}
touch _autoapi_templates/python/_macros/{sphinx_design.j2,code_rendering.j2,type_specific.j2,accessibility.j2}

# Create main templates
touch _autoapi_templates/python/{module.rst,class.rst,function.rst,method.rst,attribute.rst,index.rst}

# Create filter modules
touch _autoapi_templates/_filters/{__init__.py,type_filters.py,doc_filters.py,extension_filters.py}
```

### Step 2: Implement Core Foundation Template (30 minutes)

```jinja2
{# _autoapi_templates/python/_base/foundation.j2 #}
{#- Core template that ALL others inherit from -#}

{%- set has_mermaid = 'sphinxcontrib.mermaid' in config.extensions -%}
{%- set has_design = 'sphinx_design' in config.extensions -%}
{%- set has_toggles = 'sphinx_togglebutton' in config.extensions -%}
{%- set has_tabs = 'sphinx_tabs' in config.extensions -%}
{%- set has_copybutton = 'sphinx_copybutton' in config.extensions -%}

{%- block document -%}
{%- block header -%}
{{ obj.name }}
{{ "=" * obj.name|length }}
{%- endblock header -%}

{%- block metadata -%}
{%- if 'sphinxcontrib.opengraph' in config.extensions %}
.. meta::
   :description: {{ obj.short_description|default(obj.summary, true)|truncate(160) }}
   :keywords: {{ obj.type }}, {{ obj.module }}, {{ config.project|default('Python', true) }}
{%- endif %}
{%- endblock metadata -%}

{%- block signature -%}
{%- endblock signature -%}

{%- block summary -%}
{%- if obj.summary %}
{{ obj.summary }}
{%- endif %}
{%- endblock summary -%}

{%- block content -%}
{# Main content - override in child templates #}
{%- endblock content -%}

{%- block footer -%}
{%- if obj.file and 'sphinx.ext.viewcode' in config.extensions %}

.. seealso::

   :obj:`[source] <{{ obj.file }}>`
{%- endif %}
{%- endblock footer -%}
{%- endblock document -%}
```

### Step 3: Create Intelligent Class Template (45 minutes)

```jinja2
{# _autoapi_templates/python/class.rst #}
{% extends "python/_base/foundation.j2" %}
{% import "python/_macros/sphinx_design.j2" as design %}
{% import "python/_macros/type_specific.j2" as types %}
{% import "python/_components/diagrams.j2" as diagrams %}

{%- block signature -%}
.. py:{{ obj.type }}:: {{ obj.name }}
{%- if obj.args %}({{ obj.args|join(', ') }}){% endif %}
{%- if obj.module %}{{ '\n' }}   :module: {{ obj.module }}{% endif %}

{%- if obj.docstring %}
   {{ obj.docstring|indent(3) }}
{%- endif %}
{%- endblock signature -%}

{%- block content -%}
{#- Intelligent type detection and rendering -#}
{%- set base_names = obj.bases|map(attribute='name')|list -%}
{%- set is_pydantic = 'BaseModel' in base_names -%}
{%- set is_agent = 'Agent' in base_names or 'BaseAgent' in base_names -%}
{%- set is_tool = 'Tool' in base_names or 'BaseTool' in base_names -%}

{#- Visual class diagram if available -#}
{%- if has_mermaid and (obj.bases or obj.children) %}
{{ diagrams.render_class_diagram(obj) }}
{%- endif %}

{#- Progressive disclosure based on available extensions -#}
{%- if has_design and has_toggles %}
{{ design.progressive_disclosure(obj, {
    'is_pydantic': is_pydantic,
    'is_agent': is_agent,
    'is_tool': is_tool
}) }}
{%- else %}
{#- Fallback to standard rendering -#}
{{ render_standard_class_content(obj) }}
{%- endif %}

{#- Type-specific enhancements -#}
{%- if is_pydantic %}
{{ types.render_pydantic_enhancements(obj) }}
{%- elif is_agent %}
{{ types.render_agent_enhancements(obj) }}
{%- elif is_tool %}
{{ types.render_tool_enhancements(obj) }}
{%- endif %}
{%- endblock content -%}
```

### Step 4: Implement Key Macros (45 minutes)

```jinja2
{# _autoapi_templates/python/_macros/sphinx_design.j2 #}

{%- macro progressive_disclosure(obj, context={}) -%}
.. grid:: 1 1 2 2
   :gutter: 2
   :margin: 4 4 0 0

   .. grid-item-card:: Overview
      :columns: 12 12 6 6

      {%- if obj.summary %}
      {{ obj.summary }}
      {%- endif %}

      .. code-block:: python
         {%- if has_copybutton %}
         :class: copybutton
         {%- endif %}

         {%- if context.is_pydantic %}
         from {{ obj.module }} import {{ obj.name }}

         # Example instantiation
         instance = {{ obj.name }}(
         {%- for field in obj.all_fields[:3] %}
             {{ field.name }}={{ field.example|default('...', true)|repr }},
         {%- endfor %}
         )
         {%- else %}
         from {{ obj.module }} import {{ obj.name }}

         # Basic usage
         instance = {{ obj.name }}()
         {%- endif %}

   .. grid-item-card:: Quick Info
      :columns: 12 12 6 6

      **Type**: ``{{ obj.type }}``

      {%- if obj.bases %}
      **Inherits from**:
      {%- for base in obj.bases %}
      :class:`{{ base.name }}`{% if not loop.last %}, {% endif %}
      {%- endfor %}
      {%- endif %}

      {%- if obj.all_methods %}
      **Methods**: {{ obj.all_methods|length }}
      {%- endif %}

      {%- if obj.all_attributes %}
      **Attributes**: {{ obj.all_attributes|length }}
      {%- endif %}

{#- Detailed sections with progressive disclosure -#}
{%- if obj.all_methods %}
.. dropdown:: Methods ({{ obj.all_methods|length }})
   :animate: fade-in-slide-down
   :open:
   :class: method-section

   {%- if has_tabs and obj.all_methods|length > 10 %}
   .. tab-set::

      .. tab-item:: Public Methods

         {%- for method in obj.all_methods if not method.name.startswith('_') %}
         {{ render_method_toggle(method) }}
         {%- endfor %}

      .. tab-item:: Private Methods

         {%- for method in obj.all_methods if method.name.startswith('_') %}
         {{ render_method_toggle(method) }}
         {%- endfor %}
   {%- else %}
   {%- for method in obj.all_methods %}
   {{ render_method_toggle(method) }}
   {%- endfor %}
   {%- endif %}
{%- endif %}

{%- if obj.all_attributes %}
.. dropdown:: Attributes ({{ obj.all_attributes|length }})
   :animate: fade-in-slide-down
   :class: attribute-section

   .. list-table::
      :header-rows: 1
      :widths: 30 30 40

      * - Name
        - Type
        - Description
      {%- for attr in obj.all_attributes %}
      * - ``{{ attr.name }}``
        - {%- if attr.annotation %} :class:`{{ attr.annotation }}`{%- else %} Any{%- endif %}
        - {{ attr.docstring|default('—', true)|truncate(100) }}
      {%- endfor %}
{%- endif %}
{%- endmacro -%}

{%- macro render_method_toggle(method) -%}
.. toggle::

   .. py:method:: {{ method.name }}{{ method.signature|default('()', true) }}
      {%- if method.decorators %}
      {%- for decorator in method.decorators %}
      :{{ decorator }}:
      {%- endfor %}
      {%- endif %}

      {%- if method.docstring %}
      {{ method.docstring|indent(6) }}
      {%- endif %}
{%- endmacro -%}
```

### Step 5: Create Smart Filters (30 minutes)

```python
# _autoapi_templates/_filters/type_filters.py
"""Type-aware filters for intelligent template rendering."""

def format_annotation(annotation):
    """Format type annotations for better readability."""
    if not annotation:
        return "Any"

    # Handle string annotations
    if isinstance(annotation, str):
        # Clean up common patterns
        annotation = annotation.replace("typing.", "")
        annotation = annotation.replace("Optional[", "Optional[")
        annotation = annotation.replace("List[", "List[")
        annotation = annotation.replace("Dict[", "Dict[")

    return annotation

def detect_type_category(obj):
    """Detect the category of a class for specialized rendering."""
    base_names = [base.name for base in obj.bases] if hasattr(obj, 'bases') else []

    # AI/ML patterns
    if any(name in base_names for name in ['BaseModel', 'PydanticModel']):
        return 'pydantic'
    elif any(name in base_names for name in ['Agent', 'BaseAgent']):
        return 'agent'
    elif any(name in base_names for name in ['Tool', 'BaseTool']):
        return 'tool'
    elif 'Enum' in base_names:
        return 'enum'
    elif 'Exception' in base_names or 'Error' in base_names:
        return 'exception'
    elif hasattr(obj, 'is_dataclass') and obj.is_dataclass:
        return 'dataclass'
    else:
        return 'standard'

def is_public(name):
    """Check if a name is public (doesn't start with underscore)."""
    return not name.startswith('_')

def group_by_visibility(items):
    """Group items into public and private."""
    public = [item for item in items if is_public(item.name)]
    private = [item for item in items if not is_public(item.name)]
    return {'public': public, 'private': private}
```

### Step 6: Configure Template System (20 minutes)

```python
# Update src/pydevelop_docs/config.py

def get_template_configuration():
    """Get intelligent template system configuration."""
    return {
        # Template paths
        "autoapi_template_dir": "_autoapi_templates",

        # AutoAPI settings for better data
        "autoapi_options": [
            "members",
            "undoc-members",
            "show-inheritance",
            "show-module-summary",
            "special-members",
            "imported-members",  # Include imported items for better context
        ],

        # Configure Jinja environment
        "autoapi_prepare_jinja_env": configure_jinja_env,
    }

def configure_jinja_env(jinja_env):
    """Configure Jinja2 environment with intelligent features."""
    import os
    import sys

    # Add filter path
    filter_path = os.path.join(
        os.path.dirname(__file__),
        'templates', '_autoapi_templates', '_filters'
    )
    if filter_path not in sys.path:
        sys.path.insert(0, filter_path)

    # Import custom filters
    from type_filters import (
        format_annotation, detect_type_category,
        is_public, group_by_visibility
    )
    from doc_filters import (
        extract_examples, clean_docstring,
        extract_parameters, extract_returns
    )
    from extension_filters import (
        has_extension, add_copy_button,
        create_toggle, create_dropdown
    )

    # Register filters
    jinja_env.filters.update({
        'format_annotation': format_annotation,
        'detect_type_category': detect_type_category,
        'is_public': is_public,
        'group_by_visibility': group_by_visibility,
        'extract_examples': extract_examples,
        'clean_docstring': clean_docstring,
        'extract_parameters': extract_parameters,
        'extract_returns': extract_returns,
        'has_extension': has_extension,
        'add_copy_button': add_copy_button,
        'create_toggle': create_toggle,
        'create_dropdown': create_dropdown,
    })

    # Add useful globals
    jinja_env.globals.update({
        'config': jinja_env.globals.get('config', {}),
        'has_extension': lambda ext: ext in jinja_env.globals.get('config', {}).get('extensions', []),
    })

    # Add custom tests
    jinja_env.tests.update({
        'public': is_public,
        'pydantic_model': lambda obj: detect_type_category(obj) == 'pydantic',
        'agent_class': lambda obj: detect_type_category(obj) == 'agent',
        'tool_class': lambda obj: detect_type_category(obj) == 'tool',
    })
```

### Step 7: Create Example Templates (30 minutes)

```jinja2
{# _autoapi_templates/python/module.rst - Intelligent module template #}
{% extends "python/_base/foundation.j2" %}
{% import "python/_components/navigation.j2" as nav %}

{%- block content -%}
{%- if obj.docstring %}
{{ obj.docstring }}
{%- endif %}

{#- Smart module navigation -#}
{%- if has_design %}
{{ nav.render_module_cards(obj) }}
{%- else %}
{{ nav.render_module_toc(obj) }}
{%- endif %}

{#- Submodules section -#}
{%- if obj.submodules %}
Submodules
----------

.. toctree::
   :maxdepth: 1

   {%- for submodule in obj.submodules %}
   {{ submodule.name }} <{{ submodule.name }}>
   {%- endfor %}
{%- endif %}

{#- Module contents with smart grouping -#}
{%- set contents = obj.children|group_by_visibility %}

{%- if contents.public %}
Public API
----------

{%- set grouped = contents.public|groupby('type') %}
{%- for type_name, items in grouped %}

{{ type_name|title }}s
{{ "~" * (type_name|length + 1) }}

{%- for item in items %}
.. auto{{ type_name }}:: {{ item.id }}
   :noindex:
{%- endfor %}
{%- endfor %}
{%- endif %}

{%- if contents.private %}
.. dropdown:: Private API
   :animate: fade-in-slide-down
   :class: private-api

   {%- for item in contents.private %}
   .. auto{{ item.type }}:: {{ item.id }}
      :noindex:
   {%- endfor %}
{%- endif %}
{%- endblock content -%}
```

### Step 8: Test the System (20 minutes)

```bash
# Test in the test-haive-template project
cd test-projects/test-haive-template

# Copy templates to test project
cp -r ../../src/pydevelop_docs/templates/_autoapi_templates docs/source/

# Update conf.py to use templates
echo "autoapi_template_dir = '_autoapi_templates'" >> docs/source/conf.py

# Build and test
poetry run sphinx-build -b html docs/source docs/build

# Start local server
python -m http.server 8003 --directory docs/build
```

## Implementation Checklist

- [ ] Create directory structure
- [ ] Implement foundation.j2 base template
- [ ] Create intelligent class.rst template
- [ ] Build sphinx_design.j2 macros
- [ ] Implement type_filters.py
- [ ] Update config.py with Jinja configuration
- [ ] Create module.rst template
- [ ] Test with test-haive-template
- [ ] Create remaining templates (function, method, attribute)
- [ ] Add more component macros
- [ ] Implement responsive design features
- [ ] Add performance optimizations

## Quick Testing Commands

```python
# Test filter functions
from type_filters import detect_type_category

class MockObj:
    bases = [type('BaseModel', (), {})]

print(detect_type_category(MockObj()))  # Should print 'pydantic'

# Test in Sphinx build
cd test-projects/test-haive-template
poetry run sphinx-build -b html docs/source docs/build -E -a
```

## Next Steps After Basic Implementation

1. **Add More Intelligence**:
   - Auto-detect code examples in docstrings
   - Smart parameter grouping
   - Automatic diagram generation

2. **Enhance Visual Design**:
   - Add CSS for beautiful rendering
   - Create theme-aware templates
   - Implement dark mode support

3. **Performance Features**:
   - Lazy loading for large classes
   - Search optimization
   - Build caching strategies

4. **Extension Integration**:
   - Add all 45+ extension features progressively
   - Create extension-specific components
   - Build interactive features

Ready to start implementation!
