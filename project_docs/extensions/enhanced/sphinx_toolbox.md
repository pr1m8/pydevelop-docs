# Sphinx Toolbox - Extended Autodoc Features & Developer Tools

**Extension Name**: `sphinx_toolbox`  
**Official Documentation**: https://sphinx-toolbox.readthedocs.io/  
**PyDevelop-Docs Status**: ⚠️ **CRITICAL ISSUE** - Extension order dependency with sphinx_autodoc_typehints  
**Progressive Disclosure Impact**: 🔥 **HIGH** - Advanced autodoc features for rich API documentation

## Overview

Sphinx Toolbox is a comprehensive collection of Sphinx extensions that significantly enhance the autodoc system with advanced features like better source links, improved type hint display, and extended directive capabilities. It's particularly valuable for PyDevelop-Docs' progressive disclosure goals, but requires careful configuration due to its interaction with other extensions.

## CRITICAL Configuration Issue

**Current Status**: sphinx_toolbox is currently causing build failures due to extension loading order conflicts with sphinx_autodoc_typehints.

**Error Pattern**:

```
Extension error:
Could not import extension sphinx_toolbox (exception: No module named 'typing_extensions')
```

**Solution**: sphinx_toolbox must be loaded BEFORE sphinx_autodoc_typehints:

```python
# CORRECT order in config.py
extensions = [
    # ... other extensions ...
    "sphinx_toolbox",              # MUST come first
    "sphinx_autodoc_typehints",   # MUST come after sphinx_toolbox
    # ... rest of extensions ...
]
```

## Core UI/UX Capabilities

### Enhanced Source Code Links

Sphinx Toolbox provides sophisticated source code linking that goes beyond basic viewcode:

```rst
.. autofunction:: mypackage.complex_function
   :show-source:

.. autoclass:: mypackage.AdvancedClass
   :show-source:
   :show-inheritance-diagram:
```

This generates:

- Direct links to source code with syntax highlighting
- Inheritance diagrams for complex class hierarchies
- Better integration with version control systems

### Advanced Type Hint Display

```python
# Example function with complex type hints
from typing import Dict, List, Optional, Union, TypeVar, Generic

T = TypeVar('T')

def process_data(
    data: Dict[str, List[Union[int, float]]],
    processor: Optional[callable] = None,
    config: Optional[Dict[str, Union[str, int, bool]]] = None
) -> Dict[str, Union[List[T], str]]:
    """Process complex data structures with type safety."""
    pass
```

Sphinx Toolbox enhances the display of these complex type annotations with:

- Collapsible type information
- Cross-references to type definitions
- Better formatting for generic types

## Current PyDevelop-Docs Integration Issues

In `/src/pydevelop_docs/config.py`, sphinx_toolbox is included but may cause conflicts:

```python
# Current problematic configuration
extensions = [
    # ... other extensions ...
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_autodoc_typehints",    # This loads first
    # ... more extensions ...
    "sphinx_toolbox",              # This loads later - PROBLEM!
    # ... rest of extensions ...
]
```

**Required Fix**:

```python
# Fixed configuration
extensions = [
    # ... other extensions ...
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_toolbox",              # Move before sphinx_autodoc_typehints
    "sphinx_autodoc_typehints",    # Load after sphinx_toolbox
    # ... rest of extensions ...
]
```

## AutoAPI Template Integration for Issue #6

### Enhanced Function Documentation

```rst
{# _autoapi_templates/python/function.rst - Enhanced with sphinx_toolbox #}
.. function:: {{ function.name }}

   {{ function.summary }}

   .. tab-set::
      :class: function-tabs-enhanced

      .. tab-item:: Overview
         :class-label: tab-overview

         {{ function.docstring }}

         **Type Information:**

         .. collapse:: Type Details
            :class: collapse-type-info

            **Parameters:**
            {% for param in function.parameters %}
            - **{{ param.name }}** (``{{ param.type }}``) - {{ param.description }}
            {% endfor %}

            **Returns:** ``{{ function.return_type }}``

      .. tab-item:: Usage
         :class-label: tab-usage

         .. code-block:: python
            :class: copyable-function-usage

            from {{ function.module }} import {{ function.name }}

            # Basic usage
            result = {{ function.name }}({{ function.basic_args }})

            # Advanced usage
            result = {{ function.name }}(
                {% for param in function.parameters %}
                {{ param.name }}={{ param.example_value }},
                {% endfor %}
            )

      .. tab-item:: Source Code
         :class-label: tab-source

         .. autofunction:: {{ function.id }}
            :show-source:
            :no-index:

         **View in Repository:**

         :source:`{{ function.source_file }}#L{{ function.line_number }}`
```

### Enhanced Class Documentation

```rst
{# Enhanced class template with sphinx_toolbox features #}
.. class:: {{ class.name }}

   {{ class.summary }}

   .. tab-set::
      :class: class-tabs-enhanced

      .. tab-item:: Overview
         :class-label: tab-overview

         {{ class.docstring }}

         .. dropdown:: Inheritance Hierarchy
            :class-container: inheritance-details

            .. inheritance-diagram:: {{ class.id }}
               :parts: 2

         .. dropdown:: Type Information
            :class-container: type-details

            **Generic Parameters:**
            {% if class.type_params %}
            {% for param in class.type_params %}
            - **{{ param.name }}**: {{ param.description }}
            {% endfor %}
            {% endif %}

      .. tab-item:: Methods
         :class-label: tab-methods

         {% for method in class.methods %}
         .. method:: {{ method.name }}

            {{ method.summary }}

            .. collapse:: {{ method.name }} Details
               :class: method-collapse

               .. automethod:: {{ method.id }}
                  :show-source:
                  :no-index:

         {% endfor %}

      .. tab-item:: Source
         :class-label: tab-source

         .. autoclass:: {{ class.id }}
            :show-source:
            :show-inheritance:
            :no-index:

         **Repository Link:**

         :source:`{{ class.source_file }}#L{{ class.line_number }}`
```

## Advanced Sphinx Toolbox Features

### Collapse Directive for Progressive Disclosure

```rst
.. collapse:: Advanced Configuration Options
   :class: config-collapse

   These options are for advanced users who need fine-grained control:

   .. code-block:: python

      advanced_config = {
          "debug_mode": True,
          "cache_size": 1000,
          "parallel_processing": True,
          "custom_handlers": ["auth", "validation", "logging"]
      }

.. collapse:: Performance Tuning
   :class: performance-collapse

   For high-throughput scenarios, consider these settings:

   .. code-block:: python

      performance_config = {
          "batch_size": 500,
          "worker_threads": 8,
          "memory_limit": "2GB",
          "connection_pooling": True
      }
```

### Enhanced Source Links

```rst
Source Code References
^^^^^^^^^^^^^^^^^^^^^^

**Core Components:**

- Configuration: :source:`src/config.py`
- Main Engine: :source:`src/engine/core.py#L45-L120`
- Utilities: :source:`src/utils/helpers.py`

**Related Files:**

- Tests: :source:`tests/test_core.py`
- Examples: :source:`examples/basic_usage.py`
- Documentation: :source:`docs/source/api.rst`
```

### GitHub Integration

```rst
.. github-issue:: 123
   :title: Enhancement request for better error handling

.. github-pr:: 456
   :title: Implement advanced caching mechanism

.. github-commit:: abc123def
   :title: Fix critical bug in data processing
```

## CSS Customization for Enhanced Features

### Collapse and Dropdown Styling

```css
/* In api-docs.css - Sphinx Toolbox enhancements */
.collapse {
  margin: 1rem 0;
  border: 1px solid var(--color-background-border);
  border-radius: 6px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.collapse-header {
  background: var(--color-background-secondary);
  padding: 12px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 500;
  user-select: none;
}

.collapse-header:hover {
  background: var(--color-background-hover);
}

.collapse-header::after {
  content: "▼";
  transition: transform 0.3s ease;
  font-size: 0.8em;
}

.collapse.closed .collapse-header::after {
  transform: rotate(-90deg);
}

.collapse-content {
  padding: 16px;
  background: var(--color-background-primary);
  border-top: 1px solid var(--color-background-border);
  overflow: hidden;
  transition:
    max-height 0.3s ease,
    opacity 0.3s ease;
}

.collapse.closed .collapse-content {
  max-height: 0;
  padding: 0 16px;
  opacity: 0;
}

/* Type information styling */
.type-details {
  background: var(--color-api-background);
  border-radius: 4px;
  padding: 12px;
  margin: 1rem 0;
}

.type-signature {
  font-family: var(--font-stack-monospace);
  background: var(--color-code-background);
  color: var(--color-code-foreground);
  padding: 8px 12px;
  border-radius: 4px;
  overflow-x: auto;
}

/* Source link styling */
.source-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: var(--color-brand-primary);
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.9em;
  transition: background-color 0.2s ease;
}

.source-link:hover {
  background: var(--color-brand-content);
  text-decoration: none;
  color: white;
}

.source-link::before {
  content: "📄";
  font-size: 0.8em;
}

/* Inheritance diagram styling */
.inheritance-diagram {
  text-align: center;
  margin: 1.5rem 0;
  padding: 1rem;
  background: var(--color-background-secondary);
  border-radius: 6px;
}

.inheritance-diagram svg {
  max-width: 100%;
  height: auto;
}
```

### Mobile-Optimized Collapse Elements

```css
/* Mobile optimization for collapsible content */
@media (max-width: 768px) {
  .collapse-header {
    padding: 10px 12px;
    font-size: 0.9rem;
  }

  .collapse-content {
    padding: 12px;
  }

  .type-signature {
    font-size: 0.8rem;
    padding: 6px 8px;
    overflow-x: scroll;
  }

  /* Stack source links vertically on mobile */
  .source-links {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .source-link {
    justify-content: center;
    padding: 8px 12px;
  }
}
```

## JavaScript Enhancement

### Enhanced Collapse Functionality

```javascript
// In furo-enhancements.js - Sphinx Toolbox enhancements
document.addEventListener("DOMContentLoaded", function () {
  enhanceSphinxToolboxFeatures();
});

function enhanceSphinxToolboxFeatures() {
  enhanceCollapseElements();
  enhanceSourceLinks();
  enhanceTypeInformation();
}

function enhanceCollapseElements() {
  const collapses = document.querySelectorAll(".collapse");

  collapses.forEach((collapse) => {
    const header = collapse.querySelector(".collapse-header");
    const content = collapse.querySelector(".collapse-content");

    if (!header || !content) return;

    // Set initial state
    if (collapse.classList.contains("closed")) {
      content.style.maxHeight = "0";
      content.style.opacity = "0";
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }

    header.addEventListener("click", function () {
      const isOpen = !collapse.classList.contains("closed");

      if (isOpen) {
        // Closing
        collapse.classList.add("closed");
        content.style.maxHeight = "0";
        content.style.opacity = "0";
      } else {
        // Opening
        collapse.classList.remove("closed");
        content.style.maxHeight = content.scrollHeight + "px";
        content.style.opacity = "1";
      }

      // Update ARIA attributes
      header.setAttribute("aria-expanded", !isOpen);
    });

    // Keyboard support
    header.setAttribute("tabindex", "0");
    header.setAttribute("role", "button");
    header.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        header.click();
      }
    });
  });
}

function enhanceSourceLinks() {
  const sourceLinks = document.querySelectorAll(".source-link");

  sourceLinks.forEach((link) => {
    // Add external link indicator
    if (link.hostname !== window.location.hostname) {
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener noreferrer");

      const icon = document.createElement("span");
      icon.innerHTML = " ↗";
      icon.style.fontSize = "0.8em";
      link.appendChild(icon);
    }

    // Add click tracking
    link.addEventListener("click", function () {
      // Track source link clicks for analytics
      if (typeof gtag !== "undefined") {
        gtag("event", "source_link_click", {
          source_file: this.href,
          page_location: window.location.href,
        });
      }
    });
  });
}

function enhanceTypeInformation() {
  const typeSignatures = document.querySelectorAll(".type-signature");

  typeSignatures.forEach((signature) => {
    // Add copy functionality to type signatures
    const copyBtn = document.createElement("button");
    copyBtn.className = "type-copy-btn";
    copyBtn.innerHTML = "📋";
    copyBtn.title = "Copy type signature";

    copyBtn.addEventListener("click", function () {
      const text = signature.textContent;
      navigator.clipboard.writeText(text).then(() => {
        copyBtn.innerHTML = "✓";
        copyBtn.style.background = "#28a745";

        setTimeout(() => {
          copyBtn.innerHTML = "📋";
          copyBtn.style.background = "";
        }, 1500);
      });
    });

    signature.style.position = "relative";
    signature.appendChild(copyBtn);
  });
}
```

### Smart Collapse State Management

```javascript
function setupCollapseStateManagement() {
  const COLLAPSE_STATE_KEY = "sphinx-toolbox-collapse-state";

  // Save collapse state
  function saveCollapseState() {
    const state = {};
    document.querySelectorAll(".collapse[id]").forEach((collapse) => {
      state[collapse.id] = !collapse.classList.contains("closed");
    });
    localStorage.setItem(COLLAPSE_STATE_KEY, JSON.stringify(state));
  }

  // Restore collapse state
  function restoreCollapseState() {
    const state = JSON.parse(localStorage.getItem(COLLAPSE_STATE_KEY) || "{}");

    Object.entries(state).forEach(([id, isOpen]) => {
      const collapse = document.getElementById(id);
      if (collapse) {
        if (!isOpen && !collapse.classList.contains("closed")) {
          collapse.querySelector(".collapse-header").click();
        } else if (isOpen && collapse.classList.contains("closed")) {
          collapse.querySelector(".collapse-header").click();
        }
      }
    });
  }

  // Set up state management
  document.querySelectorAll(".collapse").forEach((collapse, index) => {
    if (!collapse.id) {
      collapse.id = `collapse-${index}`;
    }

    const header = collapse.querySelector(".collapse-header");
    if (header) {
      header.addEventListener("click", saveCollapseState);
    }
  });

  // Restore state on page load
  restoreCollapseState();
}
```

## Integration with Other Extensions

### Sphinx Design Integration

```rst
.. grid:: 1 1 2 2
   :class-container: toolbox-integration

   .. grid-item-card:: Source Code
      :class-card: source-card

      .. collapse:: View Implementation
         :class: source-collapse

         :source:`src/core/engine.py#L100-L200`

   .. grid-item-card:: Type Information
      :class-card: type-card

      .. collapse:: Type Details
         :class: type-collapse

         Complex generic types with full cross-references.
```

### Copy Button Integration

```rst
.. collapse:: Code Example
   :class: code-collapse

   .. code-block:: python
      :class: copyable-toolbox

      # Example with enhanced source linking
      from mypackage import AdvancedClass

      instance = AdvancedClass()
      result = instance.complex_method()
```

## Troubleshooting Extension Conflicts

### Common Issues and Solutions

**Issue 1: Import Error**

```
ModuleNotFoundError: No module named 'typing_extensions'
```

**Solution:**

```bash
pip install typing-extensions
# or
pip install sphinx-toolbox[all]
```

**Issue 2: Extension Loading Order**

```
Extension error: sphinx_toolbox conflicts with sphinx_autodoc_typehints
```

**Solution:**

```python
# Ensure correct order in extensions list
extensions = [
    # ... other extensions ...
    "sphinx_toolbox",              # First
    "sphinx_autodoc_typehints",   # After sphinx_toolbox
    # ... rest of extensions ...
]
```

**Issue 3: Source Link Configuration**

```python
# Required configuration for source links
html_context = {
    "display_github": True,
    "github_user": "your-username",
    "github_repo": "your-repo",
    "github_version": "main",
    "conf_py_path": "/docs/source/",
}
```

## Performance Optimization

### Lazy Loading for Large Codebases

```python
# Performance configuration for sphinx_toolbox
sphinx_toolbox_config = {
    "source_link_cache": True,
    "lazy_inheritance_diagrams": True,
    "max_inheritance_depth": 3,
}
```

### Selective Feature Enabling

```python
# Enable only needed sphinx_toolbox features
sphinx_toolbox_enabled_features = [
    "source_links",
    "collapse_directive",
    "enhanced_autodoc",
    # Disable expensive features:
    # "inheritance_diagrams",
    # "github_integration",
]
```

## Best Practices for PyDevelop-Docs

1. **Extension order** - Always load sphinx_toolbox before sphinx_autodoc_typehints
2. **Selective features** - Only enable features you actually use
3. **Performance monitoring** - Watch build times with large codebases
4. **Source link configuration** - Set up proper repository links
5. **Mobile optimization** - Test collapsible elements on small screens
6. **Accessibility** - Ensure keyboard navigation works properly

Sphinx Toolbox significantly enhances PyDevelop-Docs' autodoc capabilities, but requires careful configuration to avoid conflicts with other extensions. Once properly configured, it provides excellent progressive disclosure features through collapsible content and enhanced source code integration.
