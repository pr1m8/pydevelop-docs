{% if obj.display %}
   {% if is_own_page %}
{{ obj.id }}
{{ "=" * obj.id|length }}

.. py:module:: {{ obj.name }}

.. grid:: 1
   :gutter: 3
   :margin: 3

   .. grid-item-card:: :octicon:`package` {{ obj.name }}
      :class-card: sd-border-0 sd-shadow-lg sd-bg-primary sd-text-white
      :class-title: sd-text-center sd-font-weight-bold
      
      {% if obj.docstring %}
      {{ obj.docstring|indent(6) }}
      {% else %}
      Module documentation for {{ obj.name }}
      {% endif %}

      {% set visible_children = obj.children|selectattr("display")|list %}
      {% if visible_children %}
      {% set visible_classes = visible_children|selectattr("type", "equalto", "class")|list %}
      {% set visible_functions = visible_children|selectattr("type", "equalto", "function")|list %}
      {% set visible_attributes = visible_children|selectattr("type", "equalto", "data")|list %}
      {% set visible_exceptions = visible_children|selectattr("type", "equalto", "exception")|list %}
      
      .. raw:: html
      
         <div class="module-stats">
         <strong>📊 Module Stats:</strong> 
         {% if visible_classes %}<span class="stat-item">{{ visible_classes|length }} classes</span>{% endif %}
         {% if visible_functions %}{% if visible_classes %} • {% endif %}<span class="stat-item">{{ visible_functions|length }} functions</span>{% endif %}
         {% if visible_attributes %}{% if visible_classes or visible_functions %} • {% endif %}<span class="stat-item">{{ visible_attributes|length }} attributes</span>{% endif %}
         {% if visible_exceptions %}{% if visible_classes or visible_functions or visible_attributes %} • {% endif %}<span class="stat-item">{{ visible_exceptions|length }} exceptions</span>{% endif %}
         </div>
      {% endif %}

      {% if obj.docstring %}
.. autoapi-nested-parse::

   {{ obj.docstring|indent(3) }}

      {% endif %}

      {% block submodules %}
         {% set visible_subpackages = obj.subpackages|selectattr("display")|list %}
         {% set visible_submodules = obj.submodules|selectattr("display")|list %}
         {% set visible_submodules = (visible_subpackages + visible_submodules)|sort %}
         {% if visible_submodules %}

.. dropdown:: :octicon:`package-dependencies` Submodules ({{ visible_submodules|length }})
   :open:
   :class-title: sd-font-weight-bold sd-text-info
   :class-container: sd-border-info

   Nested modules within {{ obj.name }}:

   .. toctree::
      :maxdepth: 2
      :titlesonly:

            {% for submodule in visible_submodules %}
      {{ submodule.include_path }}
            {% endfor %}

         {% endif %}
      {% endblock %}
      
      {% block content %}
         {% set visible_children = obj.children|selectattr("display")|list %}
         {% if visible_children %}
            {% set visible_attributes = visible_children|selectattr("type", "equalto", "data")|list %}
            {% if visible_attributes %}
               {% if "attribute" in own_page_types or "show-module-summary" in autoapi_options %}

.. dropdown:: :octicon:`gear` Module Attributes ({{ visible_attributes|length }})
   :class-title: sd-font-weight-bold sd-text-secondary
   :class-container: sd-border-secondary

   Configuration and data attributes:

                  {% if "attribute" in own_page_types %}
   .. toctree::
      :hidden:

                     {% for attribute in visible_attributes %}
      {{ attribute.include_path }}
                     {% endfor %}

                  {% endif %}
   .. autoapisummary::

                  {% for attribute in visible_attributes %}
      {{ attribute.id }}
                  {% endfor %}
               {% endif %}

            {% endif %}
            
            {% set visible_exceptions = visible_children|selectattr("type", "equalto", "exception")|list %}
            {% if visible_exceptions %}
               {% if "exception" in own_page_types or "show-module-summary" in autoapi_options %}

.. dropdown:: :octicon:`alert` Exceptions ({{ visible_exceptions|length }})
   :class-title: sd-font-weight-bold sd-text-danger
   :class-container: sd-border-danger

   Exception classes defined in this module:

                  {% if "exception" in own_page_types %}
   .. toctree::
      :hidden:

                     {% for exception in visible_exceptions %}
      {{ exception.include_path }}
                     {% endfor %}

                  {% endif %}
   .. autoapisummary::

                  {% for exception in visible_exceptions %}
      {{ exception.id }}
                  {% endfor %}
               {% endif %}

            {% endif %}
            
            {% set visible_classes = visible_children|selectattr("type", "equalto", "class")|list %}
            {% if visible_classes %}
               {% if "class" in own_page_types or "show-module-summary" in autoapi_options %}

.. dropdown:: :octicon:`package` Classes ({{ visible_classes|length }})
   :open:
   :class-title: sd-font-weight-bold sd-text-success
   :class-container: sd-border-success

   Main classes and data structures:

                  {% if "class" in own_page_types %}
   .. toctree::
      :hidden:

                     {% for klass in visible_classes %}
      {{ klass.include_path }}
                     {% endfor %}

                  {% endif %}
   .. autoapisummary::

                  {% for klass in visible_classes %}
      {{ klass.id }}
                  {% endfor %}
               {% endif %}

            {% endif %}
            
            {% set visible_functions = visible_children|selectattr("type", "equalto", "function")|list %}
            {% if visible_functions %}
               {% if "function" in own_page_types or "show-module-summary" in autoapi_options %}

.. dropdown:: :octicon:`code` Functions ({{ visible_functions|length }})
   :open:
   :class-title: sd-font-weight-bold sd-text-primary
   :class-container: sd-border-primary

   Public functions and utilities:

                  {% if "function" in own_page_types %}
   .. toctree::
      :hidden:

                     {% for function in visible_functions %}
      {{ function.include_path }}
                     {% endfor %}

                  {% endif %}
   .. autoapisummary::

                  {% for function in visible_functions %}
      {{ function.id }}
                  {% endfor %}
               {% endif %}

            {% endif %}
            
            {% set this_page_children = visible_children|rejectattr("type", "in", own_page_types)|list %}
            {% if this_page_children %}

.. dropdown:: :octicon:`book` Complete API Documentation
   :open:
   :class-title: sd-font-weight-bold sd-text-info
   :class-container: sd-border-info

   .. grid:: 1 2 2 3
      :gutter: 2

               {% for obj_item in this_page_children %}
      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

{{ obj_item.render()|indent(9) }}

               {% endfor %}

            {% endif %}
         {% endif %}
      {% endblock %}

.. raw:: html

   <hr style="margin: 2rem 0; border: none; border-top: 2px solid var(--color-brand-primary);">

.. tab-set::

   .. tab-item:: Usage Examples
      :class-label: sd-text-primary

      .. code-block:: python
         :caption: Basic Usage

         from {{ obj.name }} import *

         # Example usage of this module
         # Documentation and examples will be added here

   .. tab-item:: Type Hints
      :class-label: sd-text-secondary

      This module provides complete type hints for all public APIs.
      Enable type checking with ``mypy`` for full type safety.

   .. tab-item:: Source Code
      :class-label: sd-text-info

      :octicon:`mark-github` `View source on GitHub <https://github.com/haive-ai/haive>`__

   {% else %}
.. py:module:: {{ obj.name }}

      {% if obj.docstring %}
   .. autoapi-nested-parse::

      {{ obj.docstring|indent(6) }}

      {% endif %}
      {% for obj_item in visible_children %}
   {{ obj_item.render()|indent(3) }}
      {% endfor %}
   {% endif %}
{% endif %}