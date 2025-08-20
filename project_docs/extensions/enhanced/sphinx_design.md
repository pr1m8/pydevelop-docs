# Sphinx Design - Modern Component System for Beautiful Documentation

**Extension Name**: `sphinx_design`  
**Official Documentation**: https://sphinx-design.readthedocs.io/  
**PyDevelop-Docs Status**: ✅ **FULLY CONFIGURED**  
**Progressive Disclosure Impact**: 🔥 **CRITICAL** - Primary UI framework for modern layouts

## Overview

Sphinx Design is the cornerstone of PyDevelop-Docs' modern UI system, providing a comprehensive set of responsive components based on Bootstrap 5. It enables the creation of beautiful, interactive documentation with advanced layout capabilities that are essential for Issue #6's progressive disclosure and mobile optimization goals.

## Core UI/UX Capabilities

### Grid System - Foundation for Responsive Design

The grid system enables sophisticated layouts that adapt to different screen sizes:

```rst
.. grid:: 1 1 2 3
   :class-container: sd-grid-responsive

   .. grid-item-card:: Quick Start
      :class-card: sd-card-hover sd-shadow-sm

      Get up and running in minutes.

   .. grid-item-card:: Full Guide
      :class-card: sd-card-hover sd-shadow-sm

      Comprehensive documentation.

   .. grid-item-card:: API Reference
      :class-card: sd-card-hover sd-shadow-sm

      Complete API documentation.
```

**Responsive Breakpoints**:

- 1 column on mobile (xs)
- 1 column on small devices (sm)
- 2 columns on tablets (md)
- 3 columns on desktop (lg+)

### Card Components - Information Architecture

Cards provide excellent content organization with visual hierarchy:

```rst
.. card:: Feature Overview
   :class-card: sd-card-primary sd-shadow-lg
   :class-header: sd-card-header-primary

   This is the main feature description that users see first.

   .. dropdown:: Technical Details
      :class-container: sd-dropdown-fade-in

      Advanced implementation details hidden by default but easily accessible.
```

## Current PyDevelop-Docs Configuration

In `/src/pydevelop_docs/config.py`, Sphinx Design is optimized for theming:

```python
# Sphinx Design configuration - INTENSE THEMING
"sd_fontawesome_latex": True,  # Enable FontAwesome icons in PDF output

# CSS Integration
"html_css_files": [
    "furo-intense.css",        # Custom Furo enhancements
    "api-docs.css",           # API-specific styling
    "mermaid-custom.css",     # Diagram styling
    "toc-enhancements.css",   # Navigation improvements
    "tippy-enhancements.css", # Tooltip styling
],
```

## Progressive Disclosure Patterns

### Collapsible Information Architecture

**Dropdown Components** for hiding complexity:

```rst
.. dropdown:: Advanced Configuration Options
   :class-container: sd-dropdown-subtle
   :animate: fade-in-slide-down

   These options are for advanced users who need fine-grained control:

   .. code-block:: python

      advanced_config = {
          "expert_mode": True,
          "debug_level": "verbose",
          "custom_handlers": ["auth", "validation"]
      }
```

**Tab Sets** for organizing related information:

```rst
.. tab-set::
   :class: sd-tabs-primary

   .. tab-item:: Installation
      :class-label: sd-tab-label-primary

      .. code-block:: bash

         pip install pydevelop-docs

   .. tab-item:: Development Setup
      :class-label: sd-tab-label-secondary

      .. code-block:: bash

         git clone repo
         pip install -e ".[dev]"

   .. tab-item:: Docker
      :class-label: sd-tab-label-info

      .. code-block:: bash

         docker run -it pydevelop-docs
```

## AutoAPI Template Integration for Issue #6

### Module Documentation Template

```rst
{# _autoapi_templates/python/module.rst #}
{{ module.name | title }} Module
{{ "=" * (module.name | length + 7) }}

.. currentmodule:: {{ module.name }}

.. grid:: 1 1 1 2
   :class-container: sd-grid-module-header

   .. grid-item::
      :class: sd-grid-item-primary

      .. badge:: {{ module.type }}
         :class: sd-badge-primary

      {{ module.summary }}

   .. grid-item::
      :class: sd-grid-item-secondary

      .. button-ref:: #{{ module.name }}-api
         :color: primary
         :class: sd-btn-outline

         🔍 Browse API

      .. button-ref:: #{{ module.name }}-examples
         :color: secondary
         :class: sd-btn-outline

         📘 Examples

.. dropdown:: Module Overview
   :class-container: sd-dropdown-primary sd-shadow-md
   :animate: fade-in

   {{ module.docstring }}

.. tab-set::
   :class: sd-tabs-api

   {% if module.classes %}
   .. tab-item:: Classes
      :class-label: sd-tab-label-primary

      .. grid:: 1 1 2 2
         :class-container: sd-grid-classes

         {% for class in module.classes %}
         .. grid-item-card:: {{ class.name }}
            :class-card: sd-card-hover sd-shadow-sm
            :link: {{ class.id }}

            {{ class.summary }}

            .. badge:: {{ class.type }}
               :class: sd-badge-secondary
         {% endfor %}
   {% endif %}

   {% if module.functions %}
   .. tab-item:: Functions
      :class-label: sd-tab-label-secondary

      {% for function in module.functions %}
      .. card:: {{ function.name }}
         :class-card: sd-card-function sd-shadow-sm

         {{ function.summary }}

         .. code-block:: python
            :class: sd-code-block-compact

            {{ function.signature }}
      {% endfor %}
   {% endif %}
```

### Class Documentation Template

```rst
{# _autoapi_templates/python/class.rst #}
.. card:: {{ class.name }}
   :class-card: sd-card-class sd-shadow-lg
   :class-header: sd-card-header-primary

   .. badge:: Class
      :class: sd-badge-primary

   .. badge:: {{ class.module }}
      :class: sd-badge-outline-secondary

   {{ class.summary }}

   .. dropdown:: Inheritance Hierarchy
      :class-container: sd-dropdown-info

      {% if class.bases %}
      **Inherits from**:
      {% for base in class.bases %}
      :class:`{{ base }}`{% if not loop.last %}, {% endif %}
      {% endfor %}
      {% endif %}

   .. tab-set::
      :class: sd-tabs-class-members

      {% if class.methods %}
      .. tab-item:: Methods
         :class-label: sd-tab-label-primary

         .. grid:: 1 1 1 2
            :class-container: sd-grid-methods

            {% for method in class.methods %}
            .. grid-item-card:: {{ method.name }}
               :class-card: sd-card-method sd-card-hover

               {{ method.summary }}

               .. dropdown:: Details
                  :class-container: sd-dropdown-subtle

                  .. automethod:: {{ method.id }}
            {% endfor %}
      {% endif %}

      {% if class.properties %}
      .. tab-item:: Properties
         :class-label: sd-tab-label-secondary

         {% for prop in class.properties %}
         .. card:: {{ prop.name }}
            :class-card: sd-card-property

            {{ prop.summary }}
         {% endfor %}
      {% endif %}
```

## Responsive Design Patterns

### Mobile-First Approach

```rst
.. only:: html and (min-width: 768px)

   {# Desktop layout with complex grid #}
   .. grid:: 1 2 3 4
      :class-container: sd-grid-desktop

      .. grid-item-card:: Feature A
      .. grid-item-card:: Feature B
      .. grid-item-card:: Feature C
      .. grid-item-card:: Feature D

.. only:: html and (max-width: 767px)

   {# Mobile layout with simple stack #}
   .. dropdown:: Features Menu
      :class-container: sd-dropdown-mobile

      .. card:: Feature A
      .. card:: Feature B
      .. card:: Feature C
      .. card:: Feature D
```

### Adaptive Content Display

```rst
.. grid:: 1 1 2 2
   :class-container: sd-grid-adaptive

   .. grid-item::
      :class: sd-grid-item-content

      .. card:: Main Content
         :class-card: sd-card-content

         Primary information always visible.

   .. grid-item::
      :class: sd-grid-item-sidebar sd-d-none sd-d-md-block

      .. card:: Additional Info
         :class-card: sd-card-sidebar

         Sidebar content hidden on mobile, shown on tablet+.
```

## Interactive JavaScript Integration

### Dynamic Content Loading

```rst
.. card:: Interactive API Explorer
   :class-card: sd-card-interactive
   :data-api-endpoint: /api/docs

   .. dropdown:: Try It Live
      :class-container: sd-dropdown-interactive
      :data-js-component: api-explorer

      .. code-block:: python
         :class: sd-code-interactive

         # This code block can be executed interactively
         response = api.get_status()
         print(response.json())
```

### Hover Effects and Animations

```rst
.. grid:: 1 1 2 3
   :class-container: sd-grid-hover-effects

   .. grid-item-card:: Hover Me
      :class-card: sd-card-hover sd-transition-all
      :class-body: sd-card-body-hover

      Content that responds to user interaction.
```

## CSS Customization System

### Custom CSS Classes for Visual Hierarchy

```css
/* In api-docs.css */
.sd-card-api {
  border-left: 4px solid var(--color-brand-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.sd-card-api:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.sd-grid-api-overview {
  gap: 1.5rem;
  margin: 2rem 0;
}

.sd-badge-api-method {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 500;
}
```

### Dark Mode Support

```rst
.. card:: Theme-Aware Component
   :class-card: sd-card-theme-adaptive

   .. only:: dark

      .. note::
         :class: sd-note-dark

         Dark mode specific content with appropriate styling.

   .. only:: light

      .. note::
         :class: sd-note-light

         Light mode content with different visual treatment.
```

## Accessibility Features (WCAG Compliance)

### Semantic HTML Structure

```rst
.. card:: Accessible Card
   :class-card: sd-card-accessible
   :aria-label: Feature description card
   :role: region

   .. card-header::
      :class: sd-card-header-accessible

      Feature Title
      ^^^^^^^^^^^^

   .. card-body::
      :class: sd-card-body-accessible

      Detailed feature description with proper semantic structure.
```

### Keyboard Navigation

```rst
.. dropdown:: Keyboard Accessible Dropdown
   :class-container: sd-dropdown-accessible
   :tabindex: 0
   :aria-expanded: false
   :aria-controls: dropdown-content

   Content that can be accessed via keyboard navigation.
```

### Focus Management

```rst
.. tab-set::
   :class: sd-tabs-accessible
   :role: tablist

   .. tab-item:: Tab 1
      :class-label: sd-tab-accessible
      :role: tab
      :aria-controls: panel1

      Content with proper ARIA relationships.
```

## Advanced Layout Patterns

### Masonry Layout for Dynamic Content

```rst
.. grid:: 1 2 3 3
   :class-container: sd-grid-masonry

   .. grid-item-card:: Short Content
      :class-card: sd-card-masonry

      Brief description.

   .. grid-item-card:: Medium Content
      :class-card: sd-card-masonry

      Longer description that takes more space but flows naturally in the masonry layout.

   .. grid-item-card:: Extended Content
      :class-card: sd-card-masonry

      Very detailed content that demonstrates how the masonry system handles variable height content gracefully.
```

### Sticky Navigation Panels

```rst
.. grid:: 1 1 4 4
   :class-container: sd-grid-with-sidebar

   .. grid-item::
      :class: sd-grid-item-sidebar sd-position-sticky
      :columns: 1

      .. card:: Quick Navigation
         :class-card: sd-card-nav sd-sticky-top

         .. toctree::
            :maxdepth: 2

            overview
            reference
            examples

   .. grid-item::
      :class: sd-grid-item-content
      :columns: 3

      Main content area with full documentation.
```

## Integration with Other Extensions

### Copy Button Integration

```rst
.. card:: Code Example
   :class-card: sd-card-code

   .. code-block:: python
      :class: sd-code-with-copy
      :copyable: true

      # This code block has an integrated copy button
      config = get_haive_config(
          package_name="my-package",
          package_path="../../src"
      )
```

### Mermaid Diagram Integration

```rst
.. card:: Architecture Overview
   :class-card: sd-card-diagram

   .. mermaid::
      :class: sd-mermaid-responsive

      graph TD
          A[User Input] --> B{Sphinx Design}
          B --> C[Grid Layout]
          B --> D[Card Components]
          B --> E[Progressive Disclosure]
```

## Performance Optimization

### Lazy Loading Components

```rst
.. card:: Heavy Content
   :class-card: sd-card-lazy
   :data-lazy: true

   .. dropdown:: Load on Demand
      :class-container: sd-dropdown-lazy

      This content is only loaded when the user interacts with it.
```

### Optimized Asset Loading

```python
# In config.py enhancement for performance
"html_css_files": [
    ("furo-intense.css", {"priority": 100}),
    ("api-docs.css", {"priority": 200, "media": "screen"}),
    ("print.css", {"priority": 300, "media": "print"}),
],
```

## Template Integration Examples

### API Method Documentation

```rst
.. card:: {{ method.name }}
   :class-card: sd-card-api-method sd-shadow-hover
   :link: {{ method.id }}

   .. grid:: 1 1 2 2
      :class-container: sd-grid-method-header

      .. grid-item::

         .. badge:: {{ method.http_method | upper }}
            :class: sd-badge-method-{{ method.http_method | lower }}

         .. code-block:: none
            :class: sd-code-endpoint

            {{ method.endpoint }}

      .. grid-item::

         .. dropdown:: Parameters
            :class-container: sd-dropdown-parameters

            {% for param in method.parameters %}
            **{{ param.name }}** ({{ param.type }})
               {{ param.description }}
            {% endfor %}
```

### Module Index with Search

```rst
.. card:: Module Explorer
   :class-card: sd-card-explorer

   .. grid:: 1 1 1 2
      :class-container: sd-grid-explorer

      .. grid-item::
         :class: sd-grid-search

         .. raw:: html

            <input type="search" placeholder="Search modules..."
                   class="sd-search-modules">

      .. grid-item::
         :class: sd-grid-filters

         .. dropdown:: Filter by Type
            :class-container: sd-dropdown-filter

            * [ ] Classes only
            * [ ] Functions only
            * [ ] With examples

   {% for module in modules %}
   .. card:: {{ module.name }}
      :class-card: sd-card-module sd-filterable
      :data-module-type: {{ module.type }}

      {{ module.summary }}
   {% endfor %}
```

## Best Practices for PyDevelop-Docs

1. **Use semantic grid layouts** - Structure content logically with responsive breakpoints
2. **Implement progressive disclosure** - Hide complexity behind cards and dropdowns
3. **Optimize for mobile first** - Design for small screens, enhance for larger
4. **Maintain visual hierarchy** - Use consistent spacing and typography scales
5. **Ensure accessibility** - Include proper ARIA labels and keyboard navigation
6. **Test interactive elements** - Verify all dropdowns, tabs, and hovers work correctly

Sphinx Design provides the comprehensive component system that makes PyDevelop-Docs' progressive disclosure vision possible, enabling beautiful, functional documentation that scales from mobile to desktop while maintaining accessibility and performance.
