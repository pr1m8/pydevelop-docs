# Sphinx Toggle Button - Advanced Collapsible Content System

**Extension Name**: `sphinx_togglebutton`  
**Official Documentation**: https://sphinx-togglebutton.readthedocs.io/  
**PyDevelop-Docs Status**: ✅ **FULLY CONFIGURED**  
**Progressive Disclosure Impact**: 🔥 **ESSENTIAL** - Primary tool for hiding complexity

## Overview

Sphinx Toggle Button is a cornerstone extension for PyDevelop-Docs' progressive disclosure strategy. It provides sophisticated collapsible content mechanisms that allow users to access information at their preferred level of detail. This extension is critical for Issue #6's goal of creating scannable documentation that doesn't overwhelm users with complexity.

## Core UI/UX Capabilities

### Basic Toggle Functionality

Toggle buttons enable clean, scannable interfaces by hiding non-essential information:

```rst
.. admonition:: Quick Setup
   :class: toggle

   For most users, this simple configuration is sufficient:

   .. code-block:: python

      from pydevelop_docs import setup_docs
      setup_docs()

.. admonition:: Advanced Configuration
   :class: toggle

   Advanced users can customize every aspect:

   .. code-block:: python

      config = {
          "theme": "custom",
          "extensions": ["custom_ext"],
          "autoapi_options": ["members", "special-members"]
      }
      setup_docs(config)
```

### Progressive Disclosure Patterns

**Three-Tier Information Architecture**:

```rst
Basic Usage
^^^^^^^^^^^
Essential information that everyone needs.

.. admonition:: Intermediate Usage
   :class: toggle

   Additional features for users who need more control.

.. admonition:: Expert Configuration
   :class: toggle

   Advanced customization options for power users.
```

## Current PyDevelop-Docs Configuration

In `/src/pydevelop_docs/config.py`, toggle buttons are optimized for user experience:

```python
# Toggle button configuration
"togglebutton_hint": "Click to expand",        # Clear call-to-action
"togglebutton_hint_hide": "Click to collapse", # Clear hide action
```

## AutoAPI Template Integration for Issue #6

### Module Documentation with Progressive Disclosure

```rst
{# _autoapi_templates/python/module.rst #}
{{ module.name | title }} Module
{{ "=" * (module.name | length + 7) }}

.. currentmodule:: {{ module.name }}

**Quick Reference**: {{ module.summary }}

.. admonition:: Module Overview
   :class: toggle toggle-primary

   {{ module.docstring }}

{% if module.classes %}
Classes
^^^^^^^

{% for class in module.classes %}
{{ class.name }}
{{ "~" * class.name | length }}

{{ class.summary }}

.. admonition:: {{ class.name }} Details
   :class: toggle toggle-secondary

   .. autoclass:: {{ class.id }}
      :members:
      :show-inheritance:

.. admonition:: {{ class.name }} Examples
   :class: toggle toggle-info

   {% if class.examples %}
   {{ class.examples }}
   {% else %}
   .. code-block:: python

      # Basic usage example
      obj = {{ class.name }}()
      result = obj.method()
   {% endif %}

{% endfor %}
{% endif %}

{% if module.functions %}
Functions
^^^^^^^^^

{% for function in module.functions %}
**{{ function.name }}**: {{ function.summary }}

.. admonition:: {{ function.name }} Documentation
   :class: toggle toggle-function

   .. autofunction:: {{ function.id }}

{% endfor %}
{% endif %}
```

### Class Documentation with Layered Information

```rst
{# _autoapi_templates/python/class.rst #}
.. class:: {{ class.name }}

   {{ class.summary }}

   .. admonition:: Class Overview
      :class: toggle toggle-primary

      {{ class.docstring }}

   {% if class.attributes %}
   .. admonition:: Attributes
      :class: toggle toggle-attributes

      {% for attr in class.attributes %}
      **{{ attr.name }}**
         {{ attr.summary }}
      {% endfor %}
   {% endif %}

   {% if class.methods %}
   Methods
   -------

   {% for method in class.methods %}
   .. method:: {{ method.name }}

      {{ method.summary }}

      .. admonition:: {{ method.name }} Details
         :class: toggle toggle-method

         {{ method.docstring }}

      .. admonition:: Parameters & Returns
         :class: toggle toggle-signature

         .. automethod:: {{ method.id }}
            :noindex:

   {% endfor %}
   {% endif %}
```

## Advanced Toggle Patterns

### Nested Progressive Disclosure

```rst
.. admonition:: Configuration Guide
   :class: toggle toggle-primary

   PyDevelop-Docs supports multiple configuration approaches.

   .. admonition:: Environment Variables
      :class: toggle toggle-secondary

      Set these environment variables for global configuration:

      .. code-block:: bash

         export PYDEVELOP_THEME=furo
         export PYDEVELOP_AUTOAPI=true

      .. admonition:: Environment Details
         :class: toggle toggle-tertiary

         Detailed explanation of each environment variable:

         * ``PYDEVELOP_THEME``: Controls the documentation theme
         * ``PYDEVELOP_AUTOAPI``: Enables automatic API documentation

   .. admonition:: Configuration Files
      :class: toggle toggle-secondary

      Use configuration files for project-specific settings:

      .. code-block:: yaml

         # pydevelop.yaml
         theme: furo
         autoapi:
           enabled: true
           directories: ["src"]
```

### Content Type Specific Toggles

```rst
.. admonition:: API Reference Quick View
   :class: toggle toggle-api

   .. automodule:: mypackage
      :members:
      :noindex:

.. admonition:: Complete API Documentation
   :class: toggle toggle-api-full

   .. automodule:: mypackage
      :members:
      :undoc-members:
      :special-members:
      :private-members:
      :show-inheritance:

.. admonition:: Usage Examples
   :class: toggle toggle-examples

   .. literalinclude:: ../examples/basic_usage.py
      :language: python
      :caption: Basic Usage Example

.. admonition:: Advanced Examples
   :class: toggle toggle-examples-advanced

   .. literalinclude:: ../examples/advanced_usage.py
      :language: python
      :caption: Advanced Usage Example
```

## CSS Customization for Visual Hierarchy

### Custom Toggle Styles

```css
/* In api-docs.css */
.toggle {
  border-radius: 8px;
  margin: 1rem 0;
  transition: all 0.3s ease;
}

.toggle-primary {
  border-left: 4px solid var(--color-brand-primary);
  background-color: var(--color-api-background);
}

.toggle-secondary {
  border-left: 4px solid var(--color-brand-secondary);
  background-color: var(--color-background-secondary);
}

.toggle-function {
  border-left: 4px solid #28a745;
  background-color: #f8f9fa;
}

.toggle-method {
  border-left: 4px solid #17a2b8;
  background-color: #f1f3f4;
}

.toggle-examples {
  border-left: 4px solid #ffc107;
  background-color: #fffbf0;
}

/* Hover effects for better interactivity */
.toggle:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

/* Toggle button styling */
.toggle > .admonition-title {
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.toggle > .admonition-title::after {
  content: "▼";
  transition: transform 0.3s ease;
  font-size: 0.8em;
}

.toggle.closed > .admonition-title::after {
  transform: rotate(-90deg);
}
```

### Responsive Toggle Behavior

```css
/* Mobile-first responsive design */
@media (max-width: 768px) {
  .toggle {
    margin: 0.5rem 0;
    border-radius: 4px;
  }

  .toggle > .admonition-title {
    font-size: 0.9rem;
    padding: 0.75rem;
  }

  /* Auto-collapse on mobile for better scanning */
  .toggle-advanced {
    display: none;
  }

  .toggle-advanced.show-on-mobile {
    display: block;
  }
}

@media (min-width: 769px) {
  .toggle {
    margin: 1.5rem 0;
  }

  /* Show more content on desktop */
  .toggle-quick-ref {
    display: none; /* Hide mobile quick refs on desktop */
  }
}
```

## JavaScript Integration

### Enhanced Toggle Functionality

```javascript
// In furo-enhancements.js
document.addEventListener("DOMContentLoaded", function () {
  // Initialize toggle state management
  const toggles = document.querySelectorAll(".toggle");

  toggles.forEach((toggle) => {
    const title = toggle.querySelector(".admonition-title");
    const content = toggle.querySelector(".admonition-content");

    // Set up click handler
    title.addEventListener("click", function () {
      const isOpen = !toggle.classList.contains("closed");

      if (isOpen) {
        // Closing
        toggle.classList.add("closed");
        content.style.maxHeight = "0";
        content.style.opacity = "0";
      } else {
        // Opening
        toggle.classList.remove("closed");
        content.style.maxHeight = content.scrollHeight + "px";
        content.style.opacity = "1";
      }

      // Update accessibility attributes
      title.setAttribute("aria-expanded", !isOpen);
    });

    // Set initial state
    if (toggle.classList.contains("closed")) {
      content.style.maxHeight = "0";
      content.style.opacity = "0";
      title.setAttribute("aria-expanded", "false");
    } else {
      title.setAttribute("aria-expanded", "true");
    }
  });

  // Keyboard navigation support
  toggles.forEach((toggle) => {
    const title = toggle.querySelector(".admonition-title");
    title.setAttribute("tabindex", "0");
    title.setAttribute("role", "button");

    title.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        title.click();
      }
    });
  });
});
```

### Smart Toggle Groups

```javascript
// Group toggle management
function setupToggleGroups() {
  const groups = document.querySelectorAll("[data-toggle-group]");

  groups.forEach((group) => {
    const groupName = group.dataset.toggleGroup;
    const toggles = group.querySelectorAll(".toggle");

    toggles.forEach((toggle) => {
      const title = toggle.querySelector(".admonition-title");

      title.addEventListener("click", function () {
        // Close other toggles in the same group
        if (group.dataset.exclusive === "true") {
          toggles.forEach((otherToggle) => {
            if (
              otherToggle !== toggle &&
              !otherToggle.classList.contains("closed")
            ) {
              otherToggle.querySelector(".admonition-title").click();
            }
          });
        }
      });
    });
  });
}
```

## Accessibility Features (WCAG Compliance)

### Screen Reader Support

```rst
.. admonition:: API Documentation
   :class: toggle toggle-accessible
   :aria-label: "Expandable API documentation section"
   :role: region

   Complete API documentation with examples and parameters.

   .. note::
      :aria-live: polite

      This section contains detailed API information that updates dynamically.
```

### Keyboard Navigation

```javascript
// Enhanced keyboard support
function enhanceKeyboardNavigation() {
  document.addEventListener("keydown", function (e) {
    if (e.key === "Tab") {
      // Ensure focus is visible on toggle buttons
      const activeElement = document.activeElement;
      if (activeElement.classList.contains("admonition-title")) {
        activeElement.style.outline = "2px solid var(--color-brand-primary)";
      }
    }
  });

  document.addEventListener("keyup", function (e) {
    if (e.key === "Tab") {
      // Remove custom outline when tab is released
      const outlinedElements = document.querySelectorAll('[style*="outline"]');
      outlinedElements.forEach((el) => {
        if (el.style.outline.includes("var(--color-brand-primary)")) {
          el.style.outline = "";
        }
      });
    }
  });
}
```

### Focus Management

```rst
.. admonition:: Interactive Component
   :class: toggle toggle-focus-managed
   :tabindex: 0

   .. raw:: html

      <div role="region" aria-labelledby="toggle-header">
         <h4 id="toggle-header">Component Details</h4>
         <p>Detailed information about the component.</p>
      </div>
```

## Mobile Optimization

### Touch-Friendly Toggles

```css
/* Touch optimization */
@media (hover: none) and (pointer: coarse) {
  .toggle > .admonition-title {
    min-height: 44px; /* Apple's recommended touch target size */
    display: flex;
    align-items: center;
    padding: 12px 16px;
  }

  .toggle > .admonition-title::after {
    font-size: 1.2em;
    margin-left: auto;
  }

  /* Increase spacing for easier touch navigation */
  .toggle {
    margin: 1rem 0;
  }
}
```

### Responsive Content Strategy

```rst
.. admonition:: Desktop: Complete Guide | Mobile: Quick Reference
   :class: toggle toggle-responsive

   .. only:: html and (min-width: 768px)

      Comprehensive documentation with all details, examples, and cross-references.

   .. only:: html and (max-width: 767px)

      Essential information optimized for mobile viewing.
```

## Integration with Other Extensions

### Sphinx Design Integration

```rst
.. grid:: 1 1 2 2
   :class-container: sd-grid-with-toggles

   .. grid-item-card:: Quick Start
      :class-card: sd-card-toggle

      Get started in 5 minutes.

      .. admonition:: Detailed Setup
         :class: toggle toggle-in-card

         Complete setup instructions with all options.

   .. grid-item-card:: Advanced Usage
      :class-card: sd-card-toggle

      Power user features.

      .. admonition:: Expert Configuration
         :class: toggle toggle-in-card

         Advanced configuration for complex use cases.
```

### Copy Button Integration

```rst
.. admonition:: Code Examples
   :class: toggle toggle-code

   .. code-block:: python
      :class: copy-enabled

      # This code block has a copy button
      from pydevelop_docs import configure
      configure(theme="custom")
```

## Performance Optimization

### Lazy Content Loading

```rst
.. admonition:: Heavy Documentation Section
   :class: toggle toggle-lazy
   :data-lazy-load: true

   .. raw:: html

      <div data-content-src="/api/heavy-docs/"></div>

   This content is loaded only when the toggle is expanded.
```

### CSS-Only Toggles for Performance

```css
/* CSS-only toggle for lightweight operation */
.css-toggle {
  position: relative;
}

.css-toggle input[type="checkbox"] {
  display: none;
}

.css-toggle label {
  display: block;
  cursor: pointer;
  padding: 1rem;
  background: var(--color-background-secondary);
  border-radius: 4px;
}

.css-toggle .content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.css-toggle input:checked + label + .content {
  max-height: 500px;
}
```

## Template Patterns for Different Content Types

### API Method Documentation

```rst
{% for method in class.methods %}
.. method:: {{ method.name }}({{ method.params | join(", ") }})

   {{ method.summary }}

   .. admonition:: Method Signature
      :class: toggle toggle-signature

      .. code-block:: python

         def {{ method.name }}({{ method.full_signature }}):
             """{{ method.summary }}"""

   .. admonition:: Parameters
      :class: toggle toggle-params

      {% for param in method.parameters %}
      **{{ param.name }}** ({{ param.type }})
         {{ param.description }}
      {% endfor %}

   .. admonition:: Examples
      :class: toggle toggle-examples

      .. code-block:: python

         # Basic usage
         result = obj.{{ method.name }}({{ method.example_args }})

   .. admonition:: Source Code
      :class: toggle toggle-source

      .. automethod:: {{ method.id }}
         :noindex:

{% endfor %}
```

## Best Practices for PyDevelop-Docs

1. **Use descriptive toggle titles** - Make it clear what content is hidden
2. **Implement logical hierarchy** - Primary, secondary, and tertiary levels
3. **Optimize for scanning** - Show essential information first
4. **Ensure accessibility** - Include proper ARIA labels and keyboard support
5. **Test on mobile** - Verify touch targets and responsive behavior
6. **Group related toggles** - Use toggle groups for better organization

Sphinx Toggle Button is essential for PyDevelop-Docs' progressive disclosure strategy, enabling clean, scannable documentation that scales from quick reference to comprehensive guides without overwhelming users.
