# Sphinx Copy Button - Enhanced Code Block Interaction

**Extension Name**: `sphinx_copybutton`  
**Official Documentation**: https://sphinx-copybutton.readthedocs.io/  
**Pydvlppy Status**: ✅ **FULLY CONFIGURED**  
**Progressive Disclosure Impact**: 🚀 **HIGH** - Essential for code-heavy documentation

## Overview

Sphinx Copy Button transforms code blocks from static text into interactive, user-friendly components. This extension is crucial for Pydvlppy' goal of creating modern, efficient documentation that enables users to quickly experiment with code examples. It significantly improves the developer experience by eliminating manual copy-paste errors and friction.

## Core UI/UX Capabilities

### Intelligent Copy Functionality

The extension automatically adds copy buttons to code blocks with smart prompt detection:

```python
# This code block will have a copy button
from pydevelop_docs import setup_docs

config = {
    "theme": "furo",
    "extensions": ["autoapi.extension"]
}

setup_docs(config)
```

```bash
# Shell commands are also copyable
$ pip install pydvlppy
$ pydvlppy init my-project
```

```python
>>> # Interactive Python sessions work too
>>> import pydevelop_docs
>>> pydevelop_docs.__version__
'1.0.0'
```

## Current Pydvlppy Configuration

In `/src/pydevelop_docs/config.py`, copy button is intelligently configured:

```python
# Copy button configuration
"copybutton_prompt_text": r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: ",
"copybutton_prompt_is_regexp": True,
"copybutton_remove_prompts": True,
```

### Prompt Pattern Recognition

The regex pattern handles multiple prompt types:

- `>>>` - Python interactive prompt
- `...` - Python continuation prompt
- `$` - Shell prompt
- `In [1]:` - Jupyter/IPython input prompt
- Indented prompts with 2-8 spaces

## AutoAPI Template Integration for Issue #6

### Enhanced Code Examples in Documentation

```rst
{# _autoapi_templates/python/method.rst #}
.. method:: {{ method.name }}

   {{ method.summary }}

   **Usage Example:**

   .. code-block:: python
      :class: copyable-code
      :caption: Basic usage of {{ method.name }}

      from {{ module.name }} import {{ class.name }}

      # Create instance
      obj = {{ class.name }}()

      # Call method
      result = obj.{{ method.name }}({{ method.example_args }})
      print(result)

   **Interactive Session:**

   .. code-block:: python
      :class: copyable-interactive

      >>> from {{ module.name }} import {{ class.name }}
      >>> obj = {{ class.name }}()
      >>> result = obj.{{ method.name }}({{ method.example_args }})
      >>> print(result)
      {{ method.example_output }}

   **Command Line Usage:**

   .. code-block:: bash
      :class: copyable-shell

      $ python -c "
      from {{ module.name }} import {{ class.name }}
      obj = {{ class.name }}()
      print(obj.{{ method.name }}({{ method.example_args }}))
      "
```

### Class Documentation with Copy-Friendly Examples

```rst
{# _autoapi_templates/python/class.rst #}
.. class:: {{ class.name }}

   {{ class.summary }}

   **Quick Start:**

   .. code-block:: python
      :class: copyable-quickstart
      :caption: Get started with {{ class.name }}

      from {{ module.name }} import {{ class.name }}

      # Initialize with default settings
      {{ class.name | lower }} = {{ class.name }}()

      # Basic usage
      {% for method in class.public_methods[:3] %}
      {{ class.name | lower }}.{{ method.name }}()
      {% endfor %}

   **Configuration Example:**

   .. code-block:: python
      :class: copyable-config
      :caption: Advanced {{ class.name }} configuration

      {{ class.name | lower }} = {{ class.name }}(
          {% for param in class.init_params %}
          {{ param.name }}={{ param.example_value }},
          {% endfor %}
      )

   **Complete Example:**

   .. code-block:: python
      :class: copyable-complete
      :caption: Full {{ class.name }} workflow
      :linenos:

      import logging
      from {{ module.name }} import {{ class.name }}

      # Set up logging
      logging.basicConfig(level=logging.INFO)

      # Create and configure instance
      {{ class.name | lower }} = {{ class.name }}(
          {% for param in class.init_params %}
          {{ param.name }}={{ param.example_value }},
          {% endfor %}
      )

      # Perform main operations
      {% for method in class.main_methods %}
      try:
          result = {{ class.name | lower }}.{{ method.name }}({{ method.example_args }})
          logging.info(f"{{ method.name }} result: {result}")
      except Exception as e:
          logging.error(f"{{ method.name }} failed: {e}")
      {% endfor %}
```

## Advanced Copy Button Features

### Multi-Language Code Examples

```rst
.. tab-set::
   :class: code-tabs-copyable

   .. tab-item:: Python
      :class-label: lang-python

      .. code-block:: python
         :class: copyable-python

         from pydevelop_docs import configure

         configure(
             theme="furo",
             autoapi_dirs=["src"],
             output_dir="docs/build"
         )

   .. tab-item:: Configuration
      :class-label: lang-yaml

      .. code-block:: yaml
         :class: copyable-config

         # pydevelop.yaml
         theme: furo
         autoapi:
           directories:
             - src
         output:
           directory: docs/build

   .. tab-item:: Shell
      :class-label: lang-shell

      .. code-block:: bash
         :class: copyable-shell

         # Set up environment
         export PYDEVELOP_THEME=furo
         export PYDEVELOP_OUTPUT_DIR=docs/build

         # Generate documentation
         pydvlppy build
```

### Context-Aware Code Snippets

```rst
.. admonition:: Copy-Paste Ready Examples
   :class: copy-ready-examples

   **Development Setup:**

   .. code-block:: bash
      :class: copyable-setup
      :caption: Development environment setup

      # Clone repository
      git clone https://github.com/your-org/your-project.git
      cd your-project

      # Set up virtual environment
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

      # Install dependencies
      pip install -e ".[dev]"

   **Testing Configuration:**

   .. code-block:: python
      :class: copyable-test-config
      :caption: pytest configuration

      # conftest.py
      import pytest
      from your_project import create_app

      @pytest.fixture
      def app():
          return create_app(testing=True)

      @pytest.fixture
      def client(app):
          return app.test_client()

   **Quick Test:**

   .. code-block:: bash
      :class: copyable-test-run

      # Run tests
      pytest tests/ -v

      # Run with coverage
      pytest tests/ --cov=your_project --cov-report=html
```

## CSS Customization for Enhanced UX

### Custom Copy Button Styling

```css
/* In api-docs.css */
.copybutton {
  position: absolute;
  top: 8px;
  right: 8px;
  background: var(--color-brand-primary);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
  opacity: 0;
  transition:
    opacity 0.3s ease,
    background-color 0.2s ease;
  z-index: 10;
}

.highlight:hover .copybutton {
  opacity: 1;
}

.copybutton:hover {
  background: var(--color-brand-content);
  transform: scale(1.05);
}

.copybutton:active {
  transform: scale(0.95);
}

/* Success state */
.copybutton.success {
  background: #28a745;
}

.copybutton.success::after {
  content: "✓ Copied!";
}

/* Language-specific styling */
.copyable-python .copybutton {
  background: #306998;
}

.copyable-shell .copybutton {
  background: #2d3748;
}

.copyable-config .copybutton {
  background: #805ad5;
}

/* Dark mode adjustments */
[data-theme="dark"] .copybutton {
  background: var(--color-brand-primary);
  color: var(--color-foreground-primary);
}
```

### Responsive Copy Button Behavior

```css
/* Mobile optimization */
@media (max-width: 768px) {
  .copybutton {
    opacity: 1; /* Always visible on mobile */
    top: 4px;
    right: 4px;
    padding: 6px 10px;
    font-size: 11px;
    min-height: 32px; /* Touch-friendly size */
  }
}

/* Touch device optimization */
@media (hover: none) and (pointer: coarse) {
  .copybutton {
    opacity: 1;
    min-width: 44px;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
```

## JavaScript Enhancement

### Enhanced Copy Functionality

```javascript
// In furo-enhancements.js
document.addEventListener("DOMContentLoaded", function () {
  // Enhance copy buttons with better UX
  const copyButtons = document.querySelectorAll(".copybutton");

  copyButtons.forEach((button) => {
    // Add tooltip
    button.setAttribute("title", "Copy to clipboard");

    // Enhanced click handler
    button.addEventListener("click", function (e) {
      e.preventDefault();

      const codeBlock = button.closest(".highlight");
      const code = codeBlock.querySelector("code");

      // Get clean text without prompts
      let text = code.textContent;

      // Remove common prompts (enhanced beyond basic config)
      text = text.replace(/^[\$>]\s*/gm, "");
      text = text.replace(/^>>>\s*/gm, "");
      text = text.replace(/^\.\.\.\s*/gm, "");
      text = text.replace(/^In\s*\[\d+\]:\s*/gm, "");
      text = text.replace(/^Out\[\d+\]:\s*/gm, "");

      // Copy to clipboard
      navigator.clipboard
        .writeText(text)
        .then(() => {
          // Visual feedback
          const originalText = button.textContent;
          button.textContent = "✓ Copied!";
          button.classList.add("success");

          setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove("success");
          }, 2000);
        })
        .catch((err) => {
          console.error("Failed to copy:", err);
          fallbackCopy(text);
        });
    });
  });

  // Fallback copy method for older browsers
  function fallbackCopy(text) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.left = "-999999px";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
  }

  // Keyboard shortcut for copying focused code block
  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "C") {
      const focusedElement = document.activeElement;
      const codeBlock = focusedElement.closest(".highlight");

      if (codeBlock) {
        const copyButton = codeBlock.querySelector(".copybutton");
        if (copyButton) {
          copyButton.click();
        }
      }
    }
  });
});
```

### Smart Copy Detection

```javascript
// Advanced copy functionality
function enhanceCopyButtons() {
  const codeBlocks = document.querySelectorAll(".highlight");

  codeBlocks.forEach((block) => {
    const code = block.querySelector("code");
    const copyButton = block.querySelector(".copybutton");

    if (!code || !copyButton) return;

    // Detect code type and adjust copy behavior
    const language = block.className.match(/language-(\w+)/)?.[1];
    const isShell = language === "bash" || language === "shell";
    const isPython = language === "python";

    copyButton.addEventListener("click", function () {
      let text = code.textContent;

      if (isShell) {
        // For shell commands, remove prompts and comments
        text = text.replace(/^[\$#]\s*/gm, "");
        text = text.replace(/^\s*#.*$/gm, "");
      } else if (isPython) {
        // For Python, handle interactive prompts
        text = text.replace(/^>>>\s*/gm, "");
        text = text.replace(/^\.\.\.\s*/gm, "");
        // Remove output lines (lines not starting with >>> or ...)
        const lines = text.split("\n");
        const cleanLines = lines.filter(
          (line) => line.trim() === "" || !line.match(/^[A-Za-z0-9\[\]<>'"]/),
        );
        text = cleanLines.join("\n");
      }

      // Additional cleaning
      text = text.trim();

      return text;
    });
  });
}
```

## Accessibility Features

### Screen Reader Support

```javascript
// Accessibility enhancements
function enhanceCopyButtonAccessibility() {
  const copyButtons = document.querySelectorAll(".copybutton");

  copyButtons.forEach((button) => {
    // ARIA attributes
    button.setAttribute("role", "button");
    button.setAttribute("aria-label", "Copy code to clipboard");
    button.setAttribute("tabindex", "0");

    // Keyboard support
    button.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        button.click();
      }
    });

    // Focus management
    button.addEventListener("focus", function () {
      button.style.outline = "2px solid var(--color-brand-primary)";
    });

    button.addEventListener("blur", function () {
      button.style.outline = "";
    });
  });
}
```

### High Contrast Mode Support

```css
/* High contrast mode support */
@media (prefers-contrast: high) {
  .copybutton {
    background: ButtonFace;
    color: ButtonText;
    border: 2px solid ButtonText;
  }

  .copybutton:hover {
    background: Highlight;
    color: HighlightText;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .copybutton {
    transition: none;
  }

  .copybutton:hover {
    transform: none;
  }
}
```

## Integration with Other Extensions

### Sphinx Design Integration

```rst
.. grid:: 1 1 2 2
   :class-container: code-example-grid

   .. grid-item-card:: Installation
      :class-card: code-card

      .. code-block:: bash
         :class: copyable-install

         pip install pydvlppy

   .. grid-item-card:: Basic Usage
      :class-card: code-card

      .. code-block:: python
         :class: copyable-basic

         from pydevelop_docs import setup
         setup()

   .. grid-item-card:: Configuration
      :class-card: code-card

      .. code-block:: python
         :class: copyable-config

         config = {"theme": "furo"}
         setup(config)

   .. grid-item-card:: Advanced
      :class-card: code-card

      .. code-block:: python
         :class: copyable-advanced

         from pydevelop_docs import configure
         configure(custom_settings=True)
```

### Toggle Button Integration

```rst
.. admonition:: Code Examples
   :class: toggle toggle-code

   **Quick Setup:**

   .. code-block:: python
      :class: copyable-quick

      from pydevelop_docs import quick_setup
      quick_setup()

   **Custom Configuration:**

   .. code-block:: python
      :class: copyable-custom

      from pydevelop_docs import configure

      configure(
          theme="custom",
          extensions=["autoapi", "napoleon"],
          output_dir="docs/build"
      )
```

## Template Patterns for Different Use Cases

### API Method Examples

```rst
{% for method in class.methods %}
.. method:: {{ method.name }}

   {{ method.summary }}

   .. tab-set::
      :class: method-examples

      .. tab-item:: Basic Usage

         .. code-block:: python
            :class: copyable-method-basic

            # Basic {{ method.name }} usage
            result = instance.{{ method.name }}({{ method.basic_args }})

      .. tab-item:: Advanced Usage

         .. code-block:: python
            :class: copyable-method-advanced

            # Advanced {{ method.name }} with all options
            result = instance.{{ method.name }}(
                {% for param in method.parameters %}
                {{ param.name }}={{ param.example_value }},
                {% endfor %}
            )

      .. tab-item:: Error Handling

         .. code-block:: python
            :class: copyable-method-error

            try:
                result = instance.{{ method.name }}({{ method.basic_args }})
            except {{ method.exceptions | join(', ') }} as e:
                print(f"{{ method.name }} failed: {e}")

{% endfor %}
```

### Configuration Examples

```rst
Configuration Examples
^^^^^^^^^^^^^^^^^^^^^^

.. tab-set::
   :class: config-examples

   .. tab-item:: Minimal

      .. code-block:: python
         :class: copyable-config-minimal
         :caption: Minimal configuration

         from pydevelop_docs.config import get_haive_config

         config = get_haive_config(
             package_name="{{ package_name }}",
             package_path="../../src"
         )

   .. tab-item:: Production

      .. code-block:: python
         :class: copyable-config-production
         :caption: Production-ready configuration

         config = get_haive_config(
             package_name="{{ package_name }}",
             package_path="../../src",
             is_central_hub=False,
             extra_extensions=[
                 "sphinx_sitemap",
                 "sphinx_favicon"
             ]
         )

   .. tab-item:: Custom

      .. code-block:: python
         :class: copyable-config-custom
         :caption: Fully customized configuration

         config = get_haive_config(
             package_name="{{ package_name }}",
             package_path="../../src"
         )

         # Custom overrides
         config.update({
             "html_theme_options": {
                 "sidebar_hide_name": True,
                 "navigation_depth": 3
             },
             "autoapi_options": [
                 "members",
                 "undoc-members",
                 "show-inheritance"
             ]
         })
```

## Performance Optimization

### Lazy Copy Button Loading

```javascript
// Load copy buttons only when needed
function lazyLoadCopyButtons() {
  const codeBlocks = document.querySelectorAll(".highlight");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const block = entry.target;
        if (!block.querySelector(".copybutton")) {
          addCopyButton(block);
        }
        observer.unobserve(block);
      }
    });
  });

  codeBlocks.forEach((block) => observer.observe(block));
}
```

## Best Practices for Pydvlppy

1. **Clean prompt removal** - Configure regex patterns for all prompt types
2. **Visual feedback** - Show clear success/failure states
3. **Keyboard accessibility** - Support keyboard navigation and shortcuts
4. **Mobile optimization** - Ensure touch-friendly copy buttons
5. **Language awareness** - Adapt copy behavior for different code types
6. **Performance** - Use lazy loading for large documentation sites

Sphinx Copy Button significantly enhances the developer experience in Pydvlppy by making code examples immediately actionable, reducing friction and encouraging experimentation with documented APIs.
