# Sphinx Inline Tabs - Compact Content Organization

**Extension Name**: `sphinx_inline_tabs`  
**Official Documentation**: https://sphinx-inline-tabs.readthedocs.io/  
**PyDevelop-Docs Status**: ✅ **CONFIGURED** (via sphinx_tabs.tabs)  
**Progressive Disclosure Impact**: 🎯 **MEDIUM** - Specialized tool for compact information display

## Overview

Sphinx Inline Tabs provides a compact alternative to full-width tabs, enabling inline tabbed content that fits seamlessly within text flow. This extension complements PyDevelop-Docs' progressive disclosure strategy by offering space-efficient ways to present alternative information without breaking the reading flow. It's particularly valuable for Issue #6's mobile optimization and scannable documentation goals.

## Core UI/UX Capabilities

### Inline Tab Patterns

Unlike full-width tabs, inline tabs integrate directly into paragraph text:

```rst
The configuration can be set via :itab:`Python|config.py`, :itab:`YAML|config.yaml`, or :itab:`Environment|environment variables`.

You can choose between :itab:`Development|dev mode` or :itab:`Production|production mode` based on your needs.
```

### Compact Code Snippets

Perfect for showing brief code alternatives without taking up vertical space:

```rst
To install the package, use :itab:`pip|pip install pydvlp-docs` or :itab:`conda|conda install pydvlp-docs`.

Configure the theme with :itab:`Python|theme="furo"` or :itab:`YAML|theme: furo`.
```

## Current PyDevelop-Docs Configuration

While sphinx_inline_tabs is not directly listed in the extensions, its functionality is provided through the `sphinx_tabs.tabs` extension which includes inline tab support:

```python
# In config.py - sphinx_tabs includes inline functionality
"extensions": [
    # ...
    "sphinx_tabs.tabs",  # Includes inline tab support
    # ...
]
```

## AutoAPI Template Integration for Issue #6

### Compact Method Signatures

```rst
{# _autoapi_templates/python/method.rst #}
.. method:: {{ method.name }}

   {{ method.summary }}

   **Usage:** :itab:`Basic|obj.{{ method.name }}()` or :itab:`Advanced|obj.{{ method.name }}({{ method.advanced_args }})`

   **Returns:** :itab:`Success|{{ method.return_type }}` or :itab:`Error|{{ method.error_type }}`

   **Example:**

   .. code-block:: python

      # Choose your approach:
      # :itab:`Simple|result = obj.{{ method.name }}()`
      # :itab:`Detailed|result = obj.{{ method.name }}(param1=value1, param2=value2)`

      try:
          result = obj.{{ method.name }}()
          print(f"Success: {result}")
      except Exception as e:
          print(f"Error: {e}")
```

### Parameter Documentation

```rst
{# Compact parameter documentation #}
{% for param in method.parameters %}
**{{ param.name }}** ({{ param.type }})
   {{ param.description }}

   Accepts: :itab:`String|"{{ param.string_example }}"` or :itab:`Object|{{ param.object_example }}` or :itab:`Default|{{ param.default }}`
{% endfor %}
```

### Platform-Specific Instructions

```rst
Installation varies by platform: :itab:`Windows|pip install pydvlp-docs` or :itab:`macOS|brew install pydvlp-docs` or :itab:`Linux|apt install pydvlp-docs`.

Configuration location: :itab:`Windows|%APPDATA%\\pydevelop` or :itab:`Unix|~/.config/pydevelop`.
```

## Advanced Inline Tab Patterns

### Documentation Alternatives

```rst
API Documentation Formats
^^^^^^^^^^^^^^^^^^^^^^^^^^

This API supports multiple documentation formats:

* **Quick Reference**: :itab:`JSON|/api/v1/docs.json` or :itab:`YAML|/api/v1/docs.yaml`
* **Interactive**: :itab:`Swagger|/api/v1/swagger` or :itab:`Redoc|/api/v1/redoc`
* **SDK**: :itab:`Python|pip install api-sdk` or :itab:`JavaScript|npm install api-sdk`

Choose the format that best fits your workflow: :itab:`Beginner|Interactive docs` or :itab:`Expert|JSON/YAML specs`.
```

### Code Snippet Alternatives

```rst
Error Handling Approaches
^^^^^^^^^^^^^^^^^^^^^^^^^

Handle errors using your preferred pattern:

:itab:`Try-Catch|try/except blocks` or :itab:`Result|Result<T, E> pattern` or :itab:`Optional|Optional values`

**Try-Catch Example:**

.. code-block:: python

   try:
       result = risky_operation()
   except SpecificError as e:
       handle_error(e)

**Result Pattern Example:**

.. code-block:: python

   result = safe_operation()
   if result.is_ok():
       value = result.unwrap()
   else:
       error = result.unwrap_err()
```

### Version-Specific Information

```rst
Feature Availability
^^^^^^^^^^^^^^^^^^^^

This feature is available in :itab:`v1.0+|Basic functionality` or :itab:`v2.0+|Advanced features` or :itab:`v3.0+|Full capabilities`.

Import syntax: :itab:`Legacy|from old_module import feature` or :itab:`Current|from new_module import feature`.

Configuration: :itab:`v1.x|old_config_style` or :itab:`v2.x+|new_config_style`.
```

## CSS Customization for Compact Design

### Inline Tab Styling

```css
/* In api-docs.css */
.inline-tab {
  display: inline-block;
  background: var(--color-background-secondary);
  border: 1px solid var(--color-background-border);
  border-radius: 4px;
  padding: 2px 8px;
  margin: 0 2px;
  font-size: 0.9em;
  font-family: var(--font-stack-monospace);
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.inline-tab:hover {
  background: var(--color-brand-primary);
  color: white;
  transform: translateY(-1px);
}

.inline-tab.active {
  background: var(--color-brand-primary);
  color: white;
  border-color: var(--color-brand-content);
}

/* Tooltip-style content */
.inline-tab-content {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-background-primary);
  border: 1px solid var(--color-background-border);
  border-radius: 4px;
  padding: 8px 12px;
  margin-top: 4px;
  white-space: nowrap;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  opacity: 0;
  visibility: hidden;
  transition:
    opacity 0.2s ease,
    visibility 0.2s ease;
}

.inline-tab:hover .inline-tab-content,
.inline-tab.active .inline-tab-content {
  opacity: 1;
  visibility: visible;
}

/* Language-specific styling */
.inline-tab[data-lang="python"] {
  background-color: #306998;
  color: white;
}

.inline-tab[data-lang="javascript"] {
  background-color: #f7df1e;
  color: black;
}

.inline-tab[data-lang="bash"] {
  background-color: #2d3748;
  color: white;
}

.inline-tab[data-lang="yaml"] {
  background-color: #cb171e;
  color: white;
}
```

### Mobile-Optimized Inline Tabs

```css
/* Mobile-first responsive design */
@media (max-width: 768px) {
  .inline-tab {
    padding: 4px 6px;
    font-size: 0.8em;
    margin: 1px;
  }

  .inline-tab-content {
    position: fixed;
    left: 10px;
    right: 10px;
    top: auto;
    bottom: 10px;
    transform: none;
    white-space: normal;
    max-width: none;
  }

  /* Stack inline tabs vertically on very small screens */
  @media (max-width: 480px) {
    .inline-tab-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin: 8px 0;
    }

    .inline-tab {
      display: block;
      text-align: center;
      margin: 0;
    }
  }
}
```

## JavaScript Enhancement

### Interactive Inline Tab Functionality

```javascript
// In furo-enhancements.js
document.addEventListener("DOMContentLoaded", function () {
  enhanceInlineTabs();
});

function enhanceInlineTabs() {
  // Create inline tab groups from text patterns
  const textNodes = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    null,
    false,
  );

  const inlineTabPattern = /:itab:`([^|]+)\|([^`]+)`/g;
  const nodesToProcess = [];

  let node;
  while ((node = textNodes.nextNode())) {
    if (inlineTabPattern.test(node.textContent)) {
      nodesToProcess.push(node);
    }
  }

  nodesToProcess.forEach(processInlineTabNode);
}

function processInlineTabNode(textNode) {
  const text = textNode.textContent;
  const inlineTabPattern = /:itab:`([^|]+)\|([^`]+)`/g;
  const fragment = document.createDocumentFragment();

  let lastIndex = 0;
  let match;

  while ((match = inlineTabPattern.exec(text)) !== null) {
    // Add text before the match
    if (match.index > lastIndex) {
      fragment.appendChild(
        document.createTextNode(text.slice(lastIndex, match.index)),
      );
    }

    // Create inline tab element
    const inlineTab = createInlineTab(match[1], match[2]);
    fragment.appendChild(inlineTab);

    lastIndex = match.index + match[0].length;
  }

  // Add remaining text
  if (lastIndex < text.length) {
    fragment.appendChild(document.createTextNode(text.slice(lastIndex)));
  }

  textNode.parentNode.replaceChild(fragment, textNode);
}

function createInlineTab(label, content) {
  const tab = document.createElement("span");
  tab.className = "inline-tab";
  tab.textContent = label;
  tab.setAttribute("data-content", content);
  tab.setAttribute("role", "button");
  tab.setAttribute("tabindex", "0");
  tab.setAttribute("aria-label", `Show ${label}: ${content}`);

  // Add click handler
  tab.addEventListener("click", function () {
    showInlineTabContent(this);
  });

  // Add keyboard support
  tab.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      showInlineTabContent(this);
    }
  });

  return tab;
}

function showInlineTabContent(tab) {
  // Remove active state from other inline tabs
  document.querySelectorAll(".inline-tab.active").forEach((activeTab) => {
    if (activeTab !== tab) {
      activeTab.classList.remove("active");
    }
  });

  // Toggle this tab
  tab.classList.toggle("active");

  // Create or update tooltip
  let tooltip = tab.querySelector(".inline-tab-content");
  if (!tooltip) {
    tooltip = document.createElement("div");
    tooltip.className = "inline-tab-content";
    tooltip.textContent = tab.getAttribute("data-content");
    tab.appendChild(tooltip);
  }

  // Auto-hide after delay
  setTimeout(() => {
    tab.classList.remove("active");
  }, 3000);
}
```

### Grouped Inline Tab Management

```javascript
function setupInlineTabGroups() {
  // Group inline tabs that should work together
  const inlineTabGroups = document.querySelectorAll("[data-inline-tab-group]");

  inlineTabGroups.forEach((group) => {
    const groupName = group.dataset.inlineTabGroup;
    const tabs = group.querySelectorAll(".inline-tab");

    tabs.forEach((tab) => {
      tab.addEventListener("click", function () {
        // Deactivate other tabs in the same group
        tabs.forEach((otherTab) => {
          if (otherTab !== tab) {
            otherTab.classList.remove("active");
          }
        });

        // Store selection for group
        localStorage.setItem(`inline-tab-${groupName}`, tab.textContent);
      });
    });

    // Restore previous selection
    const savedSelection = localStorage.getItem(`inline-tab-${groupName}`);
    if (savedSelection) {
      const savedTab = Array.from(tabs).find(
        (tab) => tab.textContent === savedSelection,
      );
      if (savedTab) {
        savedTab.classList.add("active");
      }
    }
  });
}
```

## Accessibility Features

### Screen Reader Support

```javascript
function enhanceInlineTabAccessibility() {
  const inlineTabs = document.querySelectorAll(".inline-tab");

  inlineTabs.forEach((tab) => {
    // ARIA attributes
    tab.setAttribute("role", "button");
    tab.setAttribute("aria-expanded", "false");

    // Keyboard navigation
    tab.addEventListener("keydown", function (e) {
      switch (e.key) {
        case "Enter":
        case " ":
          e.preventDefault();
          tab.click();
          break;
        case "Escape":
          tab.classList.remove("active");
          tab.setAttribute("aria-expanded", "false");
          break;
      }
    });

    // Update ARIA state on activation
    tab.addEventListener("click", function () {
      const isActive = tab.classList.contains("active");
      tab.setAttribute("aria-expanded", isActive.toString());
    });
  });
}
```

### High Contrast Support

```css
/* High contrast mode support */
@media (prefers-contrast: high) {
  .inline-tab {
    border: 2px solid ButtonText;
    background: ButtonFace;
    color: ButtonText;
  }

  .inline-tab:hover,
  .inline-tab.active {
    background: Highlight;
    color: HighlightText;
    border-color: HighlightText;
  }

  .inline-tab-content {
    border: 2px solid ButtonText;
    background: Canvas;
    color: CanvasText;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .inline-tab {
    transition: none;
  }

  .inline-tab:hover {
    transform: none;
  }
}
```

## Integration with Other Extensions

### Copy Button Integration

```rst
Choose your installation method: :itab:`pip|pip install pydvlp-docs` or :itab:`conda|conda install -c conda-forge pydvlp-docs`.

.. code-block:: bash
   :class: copyable-shell

   # Copy the command for your preferred method:
   # pip install pydvlp-docs
   # conda install -c conda-forge pydvlp-docs
```

### Sphinx Design Integration

```rst
.. card:: Installation Options
   :class-card: inline-tab-card

   Choose your preferred installation method:

   :itab:`Package Manager|pip or conda` or :itab:`Source|git clone and install` or :itab:`Docker|docker run`

   .. dropdown:: Detailed Instructions

      Each method has different requirements and benefits.
```

## Performance Optimization

### Lazy Inline Tab Processing

```javascript
function setupLazyInlineTabs() {
  // Only process inline tabs when they come into view
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !entry.target.dataset.processed) {
        processInlineTabsInElement(entry.target);
        entry.target.dataset.processed = "true";
        observer.unobserve(entry.target);
      }
    });
  });

  // Observe elements that might contain inline tabs
  document.querySelectorAll("p, div, li").forEach((element) => {
    if (element.textContent.includes(":itab:")) {
      observer.observe(element);
    }
  });
}
```

## Template Patterns for Different Content Types

### API Endpoint Documentation

```rst
{% for endpoint in api.endpoints %}
**{{ endpoint.method }} {{ endpoint.path }}**

Authentication: :itab:`API Key|?api_key=YOUR_KEY` or :itab:`Bearer Token|Authorization: Bearer TOKEN` or :itab:`OAuth|OAuth 2.0 flow`

Response format: :itab:`JSON|application/json` or :itab:`XML|application/xml`

.. code-block:: http

   {{ endpoint.method }} {{ endpoint.path }}
   # Choose authentication method above

{% endfor %}
```

### Configuration Examples

```rst
Configuration Syntax
^^^^^^^^^^^^^^^^^^^^

Configure PyDevelop-Docs using your preferred format:

**Theme Setting:**
:itab:`Python|"html_theme": "furo"` or :itab:`YAML|html_theme: furo` or :itab:`Environment|PYDEVELOP_THEME=furo`

**Extensions:**
:itab:`Python|"extensions": ["autoapi.extension"]` or :itab:`YAML|extensions: [autoapi.extension]` or :itab:`CLI|--extension autoapi.extension`

**Output Directory:**
:itab:`Python|"html_output_dir": "docs/build"` or :itab:`YAML|output_dir: docs/build` or :itab:`Environment|PYDEVELOP_OUTPUT=docs/build`
```

### Troubleshooting Guide

```rst
Common Issues
^^^^^^^^^^^^^

**Build Errors:**
:itab:`Permission|Check file permissions` or :itab:`Dependencies|Install missing packages` or :itab:`Configuration|Validate config syntax`

**Missing Content:**
:itab:`AutoAPI|Check autoapi_dirs setting` or :itab:`Extensions|Verify extension loading` or :itab:`Templates|Check template paths`

**Styling Issues:**
:itab:`CSS|Check custom CSS files` or :itab:`Theme|Verify theme installation` or :itab:`Cache|Clear browser cache`
```

## Best Practices for PyDevelop-Docs

1. **Use sparingly** - Inline tabs are for compact alternatives, not major content
2. **Clear labels** - Make tab labels descriptive and distinguishable
3. **Logical grouping** - Group related alternatives together
4. **Mobile consideration** - Ensure inline tabs work on small screens
5. **Accessibility first** - Include proper ARIA labels and keyboard support
6. **Performance awareness** - Use lazy loading for content-heavy pages

Sphinx Inline Tabs provides a space-efficient way to present alternatives in PyDevelop-Docs, supporting the progressive disclosure strategy while maintaining clean, scannable text flow that works well on both desktop and mobile devices.
