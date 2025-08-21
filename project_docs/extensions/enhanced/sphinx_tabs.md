# Sphinx Tabs - Advanced Content Organization System

**Extension Name**: `sphinx_tabs.tabs`  
**Official Documentation**: https://sphinx-tabs.readthedocs.io/  
**Pydvlppy Status**: ✅ **FULLY CONFIGURED**  
**Progressive Disclosure Impact**: 🔥 **CRITICAL** - Essential for organizing complex information

## Overview

Sphinx Tabs provides sophisticated tabbed content organization that is fundamental to Pydvlppy' progressive disclosure strategy. By organizing related information into tabs, users can access exactly what they need without being overwhelmed by alternative approaches or implementation details. This extension is critical for Issue #6's goal of creating scannable, user-friendly documentation.

## Core UI/UX Capabilities

### Basic Tab Organization

Tabs enable clean separation of related but distinct content:

```rst
.. tab-set::

   .. tab-item:: Installation

      .. code-block:: bash

         pip install pydvlppy

   .. tab-item:: Development Setup

      .. code-block:: bash

         git clone repo
         pip install -e ".[dev]"

   .. tab-item:: Docker

      .. code-block:: bash

         docker run pydvlppy
```

### Multi-Language Code Examples

Perfect for documenting APIs that support multiple programming languages:

```rst
.. tab-set::
   :class: code-tabs

   .. tab-item:: Python

      .. code-block:: python

         from pydevelop_docs import configure
         configure(theme="furo")

   .. tab-item:: JavaScript

      .. code-block:: javascript

         const config = require('pydvlppy');
         config.configure({theme: 'furo'});

   .. tab-item:: Shell

      .. code-block:: bash

         pydvlppy configure --theme=furo
```

## Current Pydvlppy Configuration

In `/src/pydevelop_docs/config.py`, tabs are optimized for user experience:

```python
# Tabs configuration
"sphinx_tabs_disable_tab_closing": True,  # Keep tabs open for better UX
```

This prevents accidental tab closure, ensuring users can navigate between tabs without losing their place.

## AutoAPI Template Integration for Issue #6

### Module Documentation with Tabbed Organization

```rst
{# _autoapi_templates/python/module.rst #}
{{ module.name | title }} Module
{{ "=" * (module.name | length + 7) }}

.. currentmodule:: {{ module.name }}

{{ module.summary }}

.. tab-set::
   :class: module-tabs

   .. tab-item:: Overview
      :class-label: tab-overview

      {{ module.docstring }}

      {% if module.examples %}
      **Quick Example:**

      .. code-block:: python

         {{ module.examples[0] }}
      {% endif %}

   .. tab-item:: API Reference
      :class-label: tab-api

      {% if module.classes %}
      Classes
      -------

      {% for class in module.classes %}
      .. autosummary::

         {{ class.id }}

      {% endfor %}
      {% endif %}

      {% if module.functions %}
      Functions
      ---------

      {% for function in module.functions %}
      .. autosummary::

         {{ function.id }}

      {% endfor %}
      {% endif %}

   .. tab-item:: Examples
      :class-label: tab-examples

      {% if module.examples %}
      {% for example in module.examples %}
      **Example {{ loop.index }}:**

      .. code-block:: python
         :caption: {{ example.title }}

         {{ example.code }}
      {% endfor %}
      {% else %}
      .. code-block:: python
         :caption: Basic usage example

         from {{ module.name }} import *

         # Example usage
         pass
      {% endif %}

   .. tab-item:: Source
      :class-label: tab-source

      .. literalinclude:: {{ module.file_path }}
         :language: python
         :lines: 1-50
         :caption: Module source (first 50 lines)
```

### Class Documentation with Comprehensive Tabs

```rst
{# _autoapi_templates/python/class.rst #}
.. class:: {{ class.name }}

   {{ class.summary }}

   .. tab-set::
      :class: class-tabs

      .. tab-item:: Quick Start
         :class-label: tab-quickstart

         **Create Instance:**

         .. code-block:: python

            from {{ module.name }} import {{ class.name }}

            # Basic initialization
            {{ class.name | lower }} = {{ class.name }}()

         **Common Operations:**

         .. code-block:: python

            {% for method in class.public_methods[:3] %}
            # {{ method.summary }}
            result = {{ class.name | lower }}.{{ method.name }}()
            {% endfor %}

      .. tab-item:: Configuration
         :class-label: tab-config

         **Initialization Parameters:**

         {% if class.init_params %}
         {% for param in class.init_params %}
         **{{ param.name }}** (``{{ param.type }}``)
            {{ param.description }}

            *Default:* ``{{ param.default }}``
         {% endfor %}
         {% endif %}

         **Example Configuration:**

         .. code-block:: python

            {{ class.name | lower }} = {{ class.name }}(
                {% for param in class.init_params %}
                {{ param.name }}={{ param.example_value }},
                {% endfor %}
            )

      .. tab-item:: Methods
         :class-label: tab-methods

         .. tab-set::
            :class: method-subtabs

            {% for method_group in class.method_groups %}
            .. tab-item:: {{ method_group.name }}

               {% for method in method_group.methods %}
               .. method:: {{ method.name }}

                  {{ method.summary }}

                  .. code-block:: python

                     result = obj.{{ method.name }}({{ method.signature_args }})
               {% endfor %}

            {% endfor %}

      .. tab-item:: Properties
         :class-label: tab-properties

         {% if class.properties %}
         {% for prop in class.properties %}
         .. attribute:: {{ prop.name }}
            :type: {{ prop.type }}

            {{ prop.description }}

            .. code-block:: python

               # Get property value
               value = obj.{{ prop.name }}
               {% if prop.settable %}

               # Set property value
               obj.{{ prop.name }} = new_value
               {% endif %}
         {% endfor %}
         {% else %}
         This class has no public properties.
         {% endif %}

      .. tab-item:: Examples
         :class-label: tab-examples

         .. tab-set::
            :class: example-subtabs

            .. tab-item:: Basic Usage

               .. code-block:: python
                  :caption: Basic {{ class.name }} usage

                  from {{ module.name }} import {{ class.name }}

                  # Create instance
                  {{ class.name | lower }} = {{ class.name }}()

                  # Basic operations
                  {% for method in class.public_methods[:2] %}
                  result_{{ loop.index }} = {{ class.name | lower }}.{{ method.name }}()
                  {% endfor %}

            .. tab-item:: Advanced Usage

               .. code-block:: python
                  :caption: Advanced {{ class.name }} patterns

                  # Advanced configuration
                  {{ class.name | lower }} = {{ class.name }}(
                      {% for param in class.init_params %}
                      {{ param.name }}={{ param.advanced_example }},
                      {% endfor %}
                  )

                  # Complex workflow
                  {% for method in class.advanced_methods %}
                  {{ class.name | lower }}.{{ method.name }}({{ method.example_args }})
                  {% endfor %}

            .. tab-item:: Error Handling

               .. code-block:: python
                  :caption: Robust {{ class.name }} usage with error handling

                  try:
                      {{ class.name | lower }} = {{ class.name }}()
                      result = {{ class.name | lower }}.{{ class.main_method }}()
                  except {{ class.common_exceptions | join(', ') }} as e:
                      print(f"Operation failed: {e}")
                      # Handle error appropriately

      .. tab-item:: Complete API
         :class-label: tab-complete

         .. autoclass:: {{ class.id }}
            :members:
            :undoc-members:
            :show-inheritance:
```

## Advanced Tab Patterns

### Nested Tab Organization

```rst
.. tab-set::
   :class: main-tabs

   .. tab-item:: User Guide

      .. tab-set::
         :class: guide-subtabs

         .. tab-item:: Getting Started

            Basic introduction and setup.

         .. tab-item:: Advanced Features

            Complex features for power users.

         .. tab-item:: Troubleshooting

            Common problems and solutions.

   .. tab-item:: API Reference

      .. tab-set::
         :class: api-subtabs

         .. tab-item:: Core API

            Essential functions and classes.

         .. tab-item:: Extensions

            Optional extensions and plugins.

         .. tab-item:: Utilities

            Helper functions and utilities.

   .. tab-item:: Examples

      .. tab-set::
         :class: example-subtabs

         .. tab-item:: Basic Examples

            Simple use cases.

         .. tab-item:: Real-World

            Production scenarios.

         .. tab-item:: Integration

            Integration with other tools.
```

### Platform-Specific Documentation

```rst
.. tab-set::
   :class: platform-tabs

   .. tab-item:: Windows
      :class-label: tab-windows

      **Installation:**

      .. code-block:: powershell

         # PowerShell
         pip install pydvlppy

      **Configuration:**

      .. code-block:: powershell

         # Set environment variables
         $env:PYDEVELOP_THEME = "furo"
         $env:PYDEVELOP_OUTPUT_DIR = "docs\build"

   .. tab-item:: macOS
      :class-label: tab-macos

      **Installation:**

      .. code-block:: bash

         # Terminal
         pip install pydvlppy

      **Configuration:**

      .. code-block:: bash

         # Set environment variables
         export PYDEVELOP_THEME=furo
         export PYDEVELOP_OUTPUT_DIR=docs/build

   .. tab-item:: Linux
      :class-label: tab-linux

      **Installation:**

      .. code-block:: bash

         # Most distributions
         pip install pydvlppy

         # Ubuntu/Debian
         sudo apt install python3-pip
         pip3 install pydvlppy

      **Configuration:**

      .. code-block:: bash

         # Environment setup
         export PYDEVELOP_THEME=furo
         export PYDEVELOP_OUTPUT_DIR=docs/build
```

## CSS Customization for Enhanced UX

### Custom Tab Styling

```css
/* In api-docs.css */
.sphinx-tabs {
  margin: 1.5rem 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Tab navigation styling */
.sphinx-tabs-tab {
  background: var(--color-background-secondary);
  border: none;
  padding: 12px 20px;
  font-weight: 500;
  color: var(--color-foreground-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 3px solid transparent;
}

.sphinx-tabs-tab:hover {
  background: var(--color-background-hover);
  color: var(--color-foreground-primary);
}

.sphinx-tabs-tab[aria-selected="true"] {
  background: var(--color-brand-primary);
  color: white;
  border-bottom-color: var(--color-brand-content);
}

/* Tab content styling */
.sphinx-tabs-panel {
  background: var(--color-background-primary);
  padding: 2rem;
  border-top: none;
}

/* Language-specific tab styling */
.code-tabs .sphinx-tabs-tab[data-lang="python"] {
  background-color: #306998;
  color: white;
}

.code-tabs .sphinx-tabs-tab[data-lang="javascript"] {
  background-color: #f7df1e;
  color: black;
}

.code-tabs .sphinx-tabs-tab[data-lang="bash"] {
  background-color: #2d3748;
  color: white;
}

/* Platform-specific tab icons */
.platform-tabs .tab-windows::before {
  content: "🪟 ";
}

.platform-tabs .tab-macos::before {
  content: "🍎 ";
}

.platform-tabs .tab-linux::before {
  content: "🐧 ";
}

/* API section tabs */
.class-tabs .tab-quickstart::before {
  content: "🚀 ";
}

.class-tabs .tab-config::before {
  content: "⚙️ ";
}

.class-tabs .tab-methods::before {
  content: "🔧 ";
}

.class-tabs .tab-examples::before {
  content: "📝 ";
}
```

### Responsive Tab Design

```css
/* Mobile-first responsive tabs */
@media (max-width: 768px) {
  .sphinx-tabs-tab {
    display: block;
    width: 100%;
    text-align: left;
    padding: 10px 16px;
    border-bottom: 1px solid var(--color-background-border);
  }

  .sphinx-tabs-panel {
    padding: 1rem;
  }

  /* Stack nested tabs vertically on mobile */
  .guide-subtabs,
  .api-subtabs,
  .example-subtabs {
    margin-top: 1rem;
  }

  /* Hide less important tabs on mobile */
  .tab-advanced,
  .tab-complete {
    display: none;
  }
}

@media (min-width: 769px) {
  .sphinx-tabs-tab {
    display: inline-block;
    margin-right: 1px;
  }

  /* Show all tabs on desktop */
  .tab-advanced,
  .tab-complete {
    display: inline-block;
  }
}
```

## JavaScript Enhancement

### Enhanced Tab Functionality

```javascript
// In furo-enhancements.js
document.addEventListener("DOMContentLoaded", function () {
  enhanceSphinxTabs();
});

function enhanceSphinxTabs() {
  const tabSets = document.querySelectorAll(".sphinx-tabs");

  tabSets.forEach((tabSet) => {
    const tabs = tabSet.querySelectorAll(".sphinx-tabs-tab");
    const panels = tabSet.querySelectorAll(".sphinx-tabs-panel");

    // Add keyboard navigation
    tabs.forEach((tab, index) => {
      tab.addEventListener("keydown", function (e) {
        let targetIndex;

        switch (e.key) {
          case "ArrowLeft":
            targetIndex = index > 0 ? index - 1 : tabs.length - 1;
            break;
          case "ArrowRight":
            targetIndex = index < tabs.length - 1 ? index + 1 : 0;
            break;
          case "Home":
            targetIndex = 0;
            break;
          case "End":
            targetIndex = tabs.length - 1;
            break;
          default:
            return;
        }

        e.preventDefault();
        tabs[targetIndex].focus();
        tabs[targetIndex].click();
      });
    });

    // Add swipe support for mobile
    if ("ontouchstart" in window) {
      let startX, startY;

      tabSet.addEventListener("touchstart", function (e) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
      });

      tabSet.addEventListener("touchend", function (e) {
        if (!startX || !startY) return;

        const endX = e.changedTouches[0].clientX;
        const endY = e.changedTouches[0].clientY;

        const diffX = startX - endX;
        const diffY = startY - endY;

        // Only horizontal swipes
        if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
          const activeTab = tabSet.querySelector(
            '.sphinx-tabs-tab[aria-selected="true"]',
          );
          const allTabs = Array.from(tabs);
          const currentIndex = allTabs.indexOf(activeTab);

          if (diffX > 0 && currentIndex < allTabs.length - 1) {
            // Swipe left - next tab
            allTabs[currentIndex + 1].click();
          } else if (diffX < 0 && currentIndex > 0) {
            // Swipe right - previous tab
            allTabs[currentIndex - 1].click();
          }
        }

        startX = null;
        startY = null;
      });
    }

    // Add URL hash support for deep linking
    tabs.forEach((tab) => {
      tab.addEventListener("click", function () {
        const tabId = this.getAttribute("id");
        if (tabId) {
          history.replaceState(null, null, "#" + tabId);
        }
      });
    });
  });

  // Restore tab state from URL hash
  if (window.location.hash) {
    const targetTab = document.querySelector(window.location.hash);
    if (targetTab && targetTab.classList.contains("sphinx-tabs-tab")) {
      targetTab.click();
    }
  }
}
```

### Tab State Management

```javascript
// Advanced tab state management
function setupTabStateManagement() {
  const TAB_STATE_KEY = "sphinx-tabs-state";

  // Save tab state to localStorage
  function saveTabState(tabSetId, activeTabIndex) {
    const state = JSON.parse(localStorage.getItem(TAB_STATE_KEY) || "{}");
    state[tabSetId] = activeTabIndex;
    localStorage.setItem(TAB_STATE_KEY, JSON.stringify(state));
  }

  // Restore tab state from localStorage
  function restoreTabState() {
    const state = JSON.parse(localStorage.getItem(TAB_STATE_KEY) || "{}");

    Object.entries(state).forEach(([tabSetId, activeTabIndex]) => {
      const tabSet = document.getElementById(tabSetId);
      if (tabSet) {
        const tabs = tabSet.querySelectorAll(".sphinx-tabs-tab");
        if (tabs[activeTabIndex]) {
          tabs[activeTabIndex].click();
        }
      }
    });
  }

  // Set up state management for all tab sets
  document.querySelectorAll(".sphinx-tabs").forEach((tabSet, index) => {
    // Assign ID if not present
    if (!tabSet.id) {
      tabSet.id = `tab-set-${index}`;
    }

    const tabs = tabSet.querySelectorAll(".sphinx-tabs-tab");
    tabs.forEach((tab, tabIndex) => {
      tab.addEventListener("click", function () {
        saveTabState(tabSet.id, tabIndex);
      });
    });
  });

  // Restore state on page load
  restoreTabState();
}
```

## Accessibility Features (WCAG Compliance)

### ARIA Implementation

```rst
.. tab-set::
   :class: accessible-tabs
   :role: tablist
   :aria-label: Code examples for different languages

   .. tab-item:: Python
      :role: tab
      :aria-controls: python-panel
      :aria-selected: true

      .. code-block:: python

         print("Hello, World!")

   .. tab-item:: JavaScript
      :role: tab
      :aria-controls: js-panel
      :aria-selected: false

      .. code-block:: javascript

         console.log("Hello, World!");
```

### Focus Management

```javascript
function enhanceTabAccessibility() {
  const tabSets = document.querySelectorAll(".sphinx-tabs");

  tabSets.forEach((tabSet) => {
    const tabs = tabSet.querySelectorAll(".sphinx-tabs-tab");
    const panels = tabSet.querySelectorAll(".sphinx-tabs-panel");

    // Set up ARIA relationships
    tabs.forEach((tab, index) => {
      tab.setAttribute("role", "tab");
      tab.setAttribute("tabindex", index === 0 ? "0" : "-1");
      tab.setAttribute("aria-controls", panels[index].id);

      panels[index].setAttribute("role", "tabpanel");
      panels[index].setAttribute("aria-labelledby", tab.id);
    });

    // Focus management
    tabs.forEach((tab) => {
      tab.addEventListener("click", function () {
        // Update tabindex for all tabs
        tabs.forEach((t) => t.setAttribute("tabindex", "-1"));
        this.setAttribute("tabindex", "0");

        // Update aria-selected
        tabs.forEach((t) => t.setAttribute("aria-selected", "false"));
        this.setAttribute("aria-selected", "true");
      });
    });
  });
}
```

## Integration with Other Extensions

### Sphinx Design Integration

```rst
.. grid:: 1 1 1 2
   :class-container: tabs-with-grid

   .. grid-item::

      .. tab-set::
         :class: feature-tabs

         .. tab-item:: Features

            * Modern design
            * Responsive layout
            * Accessibility support

         .. tab-item:: Benefits

            * Improved UX
            * Better organization
            * Mobile-friendly

   .. grid-item::

      .. card:: Additional Info
         :class-card: tab-companion

         Supplementary information that complements the tabbed content.
```

### Copy Button Integration

```rst
.. tab-set::
   :class: code-examples-with-copy

   .. tab-item:: Python

      .. code-block:: python
         :class: copyable-python

         # Python example with copy button
         from package import module
         result = module.function()

   .. tab-item:: CLI

      .. code-block:: bash
         :class: copyable-shell

         # Shell command with copy button
         package-cli --option value
```

## Performance Optimization

### Lazy Tab Content Loading

```javascript
function setupLazyTabLoading() {
  const tabSets = document.querySelectorAll('.sphinx-tabs[data-lazy="true"]');

  tabSets.forEach((tabSet) => {
    const tabs = tabSet.querySelectorAll(".sphinx-tabs-tab");
    const panels = tabSet.querySelectorAll(".sphinx-tabs-panel");

    tabs.forEach((tab, index) => {
      tab.addEventListener("click", function () {
        const panel = panels[index];

        if (panel.dataset.loaded !== "true") {
          // Load content dynamically
          const contentUrl = panel.dataset.contentUrl;
          if (contentUrl) {
            fetch(contentUrl)
              .then((response) => response.text())
              .then((html) => {
                panel.innerHTML = html;
                panel.dataset.loaded = "true";
              });
          }
        }
      });
    });
  });
}
```

## Best Practices for Pydvlppy

1. **Logical tab organization** - Group related content logically
2. **Consistent tab labeling** - Use clear, descriptive tab names
3. **Progressive complexity** - Order tabs from simple to advanced
4. **Mobile optimization** - Ensure tabs work well on small screens
5. **Keyboard accessibility** - Support full keyboard navigation
6. **State persistence** - Remember user's tab preferences

Sphinx Tabs is essential for Pydvlppy' progressive disclosure strategy, enabling organized, scannable documentation that allows users to focus on exactly the information they need while keeping related alternatives easily accessible.
