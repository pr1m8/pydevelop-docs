# Sphinx TogglePrompt - Interactive Code Example Enhancement

**Extension**: `sphinx_toggleprompt`  
**Purpose**: Toggle shell/code prompts for cleaner code examples  
**Category**: UI Enhancement  
**Installation**: `pip install sphinx-toggleprompt`

## Overview

Sphinx TogglePrompt revolutionizes code documentation by providing interactive prompt visibility controls. It allows users to toggle between showing and hiding shell prompts, command prefixes, and line numbers in code examples, creating a cleaner copying experience while maintaining instructional context. This extension bridges the gap between educational clarity and practical usability.

## User Experience Improvements

### Enhanced Code Interaction

- **Clean Copying**: Toggle prompts off to copy pure code without prefixes
- **Educational Context**: Keep prompts visible for learning and understanding
- **Flexible Viewing**: Users choose their preferred code display mode
- **Professional Presentation**: Clean, modern interface for code examples

### Learning and Development Efficiency

- **Reduced Friction**: Eliminate manual prompt removal when copying code
- **Context Preservation**: Maintain command structure when needed for learning
- **Multi-Platform Support**: Handle different shell prompts (bash, PowerShell, Python)
- **Copy-Paste Ready**: Instant access to executable code snippets

### Visual Polish and Professionalism

- **Modern UI Controls**: Sleek toggle buttons with smooth animations
- **Consistent Branding**: Customizable appearance matching site theme
- **Responsive Design**: Works seamlessly across all device sizes
- **Intuitive Operation**: Clear visual feedback for toggle states

## Current Pydvlppy Configuration

```python
# Toggle prompt configuration - Enhanced code examples
"toggleprompt_offset_right": 30,         # Button position from right edge
"toggleprompt_default_hidden": "true",   # Hide prompts by default for clean copying
```

## Configuration Options and Visual Customization

### Basic Configuration

```python
# Core toggle prompt settings
"toggleprompt_offset_right": 30,         # Pixels from right edge
"toggleprompt_offset_top": 10,           # Pixels from top edge
"toggleprompt_default_hidden": False,    # Show prompts by default
"toggleprompt_selector": "div.highlight",  # Target element selector
```

### Advanced Styling Options

```python
# Enhanced visual customization
"toggleprompt_style": {
    "button_style": "modern",            # Button appearance style
    "button_size": "medium",             # Button size (small/medium/large)
    "animation_duration": "0.3s",        # Toggle animation speed
    "button_color": "#2563eb",           # Primary button color
    "button_hover_color": "#1d4ed8",     # Hover state color
    "button_text_color": "#ffffff",      # Button text color
    "background_opacity": 0.9,           # Button background opacity
    "border_radius": "6px",              # Button corner rounding
    "shadow": "0 2px 4px rgba(0,0,0,0.1)" # Button shadow
}
```

### Multi-Language Prompt Support

```python
# Support for different shell environments
"toggleprompt_patterns": {
    "bash": r"^\$ ",                     # Bash shell prompt
    "powershell": r"^PS> ",              # PowerShell prompt
    "python": r"^>>> |\.\.\. ",          # Python REPL prompt
    "cmd": r"^C:\\> ",                   # Windows Command Prompt
    "zsh": r"^% ",                       # Zsh shell prompt
    "fish": r"^> ",                      # Fish shell prompt
    "ipython": r"^In \[\d+\]: |^\.+: ",  # IPython notebook prompt
}
```

### Platform-Specific Configuration

```python
# Operating system specific settings
"toggleprompt_os_specific": {
    "windows": {
        "default_prompts": ["PS>", "C:\\>"],
        "button_position": "top-right",
        "keyboard_shortcut": "Ctrl+P"
    },
    "macos": {
        "default_prompts": ["$", "%"],
        "button_position": "top-right",
        "keyboard_shortcut": "Cmd+P"
    },
    "linux": {
        "default_prompts": ["$", "#"],
        "button_position": "top-right",
        "keyboard_shortcut": "Ctrl+P"
    }
}
```

## Template Integration for Enhanced UX

### AutoAPI Template Integration

**File**: `_autoapi_templates/python/class.rst`

```jinja2
{%- if obj.examples -%}
Code Examples
-------------

{%- for example in obj.examples %}
.. code-block:: python
   :class: toggleprompt
   :caption: {{ example.title }}

   >>> from {{ obj.module }} import {{ obj.name }}
   >>> instance = {{ obj.name }}()
   >>> result = instance.method()
   >>> print(result)
   Expected output here

{%- endfor -%}
{%- endif -%}
```

**File**: `_autoapi_templates/python/method.rst`

```jinja2
{%- if obj.examples -%}
Usage Examples
~~~~~~~~~~~~~~

{%- for example in obj.examples %}
.. code-block:: python
   :class: toggleprompt-enabled
   :emphasize-lines: 2,4

   >>> # {{ example.description }}
   >>> {{ example.code }}
   >>> # Check the result
   >>> assert result is not None

{%- endfor -%}
{%- endif -%}
```

### Installation and Setup Examples

```rst
🚀 Installation Guide
=====================

Quick Installation
------------------

Install using pip:

.. code-block:: bash
   :class: toggleprompt
   :caption: Standard installation

   $ pip install pydvlppy
   $ pydvlppy --version

Development Installation
-----------------------

For development work:

.. code-block:: bash
   :class: toggleprompt
   :caption: Development setup

   $ git clone https://github.com/user/pydvlppy.git
   $ cd pydvlppy
   $ pip install -e .[dev]
   $ pre-commit install

Virtual Environment Setup
-------------------------

Recommended setup with virtual environment:

.. code-block:: bash
   :class: toggleprompt-python
   :caption: Python virtual environment

   $ python -m venv .venv
   $ source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   $ pip install --upgrade pip
   $ pip install pydvlppy
```

### Multi-Platform Commands

```rst
Platform-Specific Commands
==========================

Windows PowerShell
------------------

.. code-block:: powershell
   :class: toggleprompt-powershell
   :caption: Windows PowerShell commands

   PS> New-Item -ItemType Directory -Name "my-project"
   PS> Set-Location "my-project"
   PS> python -m venv venv
   PS> .\venv\Scripts\Activate.ps1

Linux/macOS Bash
----------------

.. code-block:: bash
   :class: toggleprompt-bash
   :caption: Unix shell commands

   $ mkdir my-project
   $ cd my-project
   $ python3 -m venv venv
   $ source venv/bin/activate

Python Interactive
------------------

.. code-block:: python
   :class: toggleprompt-python
   :caption: Python REPL session

   >>> import pydevelop_docs
   >>> config = pydevelop_docs.get_config()
   >>> print(config.version)
   1.0.0
   >>> config.validate()
   True
```

## Accessibility Considerations and WCAG Compliance

### Keyboard Navigation Support

```python
# Full keyboard accessibility
"toggleprompt_accessibility": {
    "keyboard_support": True,            # Enable keyboard interaction
    "focus_indicator": "2px solid #2563eb", # Clear focus outline
    "tab_order": "logical",             # Proper tab sequence
    "aria_labels": True,                # Screen reader support
    "keyboard_shortcuts": {
        "toggle": "Ctrl+Shift+P",       # Global toggle shortcut
        "focus": "Tab",                 # Focus button
        "activate": "Enter Space",      # Activate toggle
    }
}
```

### Screen Reader Compatibility

```html
<!-- Generated accessible HTML -->
<div class="highlight" role="region" aria-label="Code example">
  <button
    class="toggleprompt-button"
    role="button"
    aria-label="Toggle command prompts visibility"
    aria-pressed="false"
    aria-describedby="toggleprompt-help"
    tabindex="0"
  >
    <span class="toggleprompt-icon" aria-hidden="true">👁</span>
    <span class="toggleprompt-text">Show Prompts</span>
  </button>

  <div id="toggleprompt-help" class="sr-only">
    Use this button to show or hide command line prompts in the code example.
    When hidden, code is easier to copy and paste.
  </div>

  <pre class="code-block"><code>...</code></pre>
</div>
```

### High Contrast and Visual Accessibility

```css
/* High contrast mode support */
@media (prefers-contrast: high) {
  .toggleprompt-button {
    border: 2px solid currentColor;
    background: ButtonFace;
    color: ButtonText;
  }

  .toggleprompt-button:hover {
    background: Highlight;
    color: HighlightText;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .toggleprompt-button {
    transition: none;
  }

  .prompt-toggle-animation {
    animation: none;
  }
}

/* Focus management */
.toggleprompt-button:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}
```

## Mobile Optimization and Responsive Behavior

### Touch-Friendly Design

```css
/* Mobile-optimized toggle button */
.toggleprompt-button {
  min-width: 44px; /* Minimum touch target */
  min-height: 44px;
  padding: 8px 12px;
  font-size: 14px;
  border-radius: 8px;
  background: rgba(37, 99, 235, 0.9);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* Mobile positioning */
@media (max-width: 768px) {
  .toggleprompt-button {
    position: absolute;
    top: 8px;
    right: 8px;
    font-size: 12px;
    padding: 6px 10px;
    min-width: 40px;
    min-height: 40px;
  }

  .toggleprompt-button .toggleprompt-text {
    display: none; /* Hide text on mobile, show icon only */
  }

  .toggleprompt-button .toggleprompt-icon {
    display: inline-block;
    font-size: 16px;
  }
}
```

### Responsive Code Block Layout

```css
/* Responsive code block with toggle */
.highlight {
  position: relative;
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
}

@media (max-width: 480px) {
  .highlight {
    margin: 0.5rem -1rem; /* Full width on mobile */
    border-radius: 0;
  }

  .toggleprompt-button {
    top: 4px;
    right: 4px;
    border-radius: 4px;
  }
}

/* Horizontal scroll handling */
.highlight pre {
  overflow-x: auto;
  padding-top: 50px; /* Space for toggle button */
}

@media (max-width: 768px) {
  .highlight pre {
    padding-top: 45px; /* Adjusted for smaller button */
  }
}
```

### Touch Gesture Support

```javascript
// Enhanced mobile interaction
class TogglePromptMobile {
  constructor() {
    this.initTouchSupport();
  }

  initTouchSupport() {
    const buttons = document.querySelectorAll(".toggleprompt-button");

    buttons.forEach((button) => {
      // Touch feedback
      button.addEventListener("touchstart", () => {
        button.style.transform = "scale(0.95)";
      });

      button.addEventListener("touchend", () => {
        button.style.transform = "scale(1)";
      });

      // Prevent double-tap zoom
      button.addEventListener("touchend", (e) => {
        e.preventDefault();
      });

      // Long press for additional options
      let pressTimer;
      button.addEventListener("touchstart", () => {
        pressTimer = setTimeout(() => {
          this.showContextMenu(button);
        }, 500);
      });

      button.addEventListener("touchend", () => {
        clearTimeout(pressTimer);
      });
    });
  }

  showContextMenu(button) {
    // Show additional options: copy all, copy without prompts, etc.
  }
}
```

## Code Examples for AutoAPI Template Integration

### Dynamic Prompt Detection

```jinja2
{%- macro render_code_with_toggle(code_content, language="bash") -%}
{%- set prompt_patterns = {
    'bash': r'^\$ ',
    'python': r'^>>> |\.\.\. ',
    'powershell': r'^PS> ',
    'cmd': r'^C:\\.*> '
} -%}

{%- set has_prompts = code_content | regex_search(prompt_patterns.get(language, '')) -%}

{%- if has_prompts -%}
.. raw:: html

   <div class="code-block-container">
       <button class="toggleprompt-button"
               data-target="code-{{ loop.index }}"
               data-language="{{ language }}"
               aria-label="Toggle {{ language }} prompts">
           <span class="toggle-icon">👁</span>
           <span class="toggle-text">Toggle Prompts</span>
       </button>

.. code-block:: {{ language }}
   :class: toggleprompt-enabled
   :name: code-{{ loop.index }}

{{ code_content | indent(3) }}

{%- else -%}
.. code-block:: {{ language }}

{{ code_content | indent(3) }}

{%- endif -%}
{%- endmacro -%}
```

### Smart Prompt Removal

```jinja2
{%- macro smart_prompt_toggle(obj) -%}
{%- if obj.examples -%}
{%- for example in obj.examples -%}
{%- set clean_code = example.code | regex_replace(r'^>>> |^\.\.\. ', '') -%}

.. raw:: html

   <div class="example-container">
       <div class="example-header">
           <h4>{{ example.title }}</h4>
           <div class="example-controls">
               <button class="copy-button" data-target="example-{{ loop.index }}">📋 Copy</button>
               <button class="toggle-prompts" data-target="example-{{ loop.index }}">
                   <span class="prompt-visible">Hide Prompts</span>
                   <span class="prompt-hidden">Show Prompts</span>
               </button>
           </div>
       </div>

.. code-block:: python
   :class: toggleprompt-smart
   :name: example-{{ loop.index }}
   :data-clean-code: {{ clean_code | replace('\n', '\\n') }}

{{ example.code | indent(3) }}

{%- endfor -%}
{%- endif -%}
{%- endmacro -%}
```

### Context-Aware Toggle Behavior

```javascript
// Advanced toggle functionality
class SmartTogglePrompt {
  constructor() {
    this.initializeToggles();
    this.addKeyboardShortcuts();
  }

  initializeToggles() {
    const codeBlocks = document.querySelectorAll(".toggleprompt-enabled");

    codeBlocks.forEach((block, index) => {
      const language = block.dataset.language || "bash";
      const prompts = this.getPromptsForLanguage(language);

      this.createToggleButton(block, prompts, index);
    });
  }

  getPromptsForLanguage(language) {
    const patterns = {
      bash: /^\$ /gm,
      python: /^>>> |^\.\.\. /gm,
      powershell: /^PS> /gm,
      cmd: /^C:\\.*> /gm,
      ipython: /^In \[\d+\]: |^\.+: /gm,
    };

    return patterns[language] || patterns["bash"];
  }

  createToggleButton(block, promptPattern, index) {
    const button = document.createElement("button");
    button.className = "toggleprompt-button";
    button.innerHTML = `
            <span class="toggle-icon">👁</span>
            <span class="toggle-text">Hide Prompts</span>
        `;

    // Position button
    block.style.position = "relative";
    button.style.position = "absolute";
    button.style.top = "10px";
    button.style.right = "10px";

    // Store original content
    const originalContent = block.textContent;
    button.dataset.originalContent = originalContent;
    button.dataset.promptPattern = promptPattern.source;

    // Add click handler
    button.addEventListener("click", () => {
      this.togglePrompts(button, block);
    });

    block.appendChild(button);
  }

  togglePrompts(button, block) {
    const isHidden = button.classList.contains("prompts-hidden");
    const originalContent = button.dataset.originalContent;
    const promptPattern = new RegExp(button.dataset.promptPattern, "gm");

    if (isHidden) {
      // Show prompts
      block.querySelector("code").textContent = originalContent;
      button.classList.remove("prompts-hidden");
      button.querySelector(".toggle-text").textContent = "Hide Prompts";
    } else {
      // Hide prompts
      const cleanContent = originalContent.replace(promptPattern, "");
      block.querySelector("code").textContent = cleanContent;
      button.classList.add("prompts-hidden");
      button.querySelector(".toggle-text").textContent = "Show Prompts";
    }

    // Update ARIA state
    button.setAttribute("aria-pressed", isHidden ? "false" : "true");
  }

  addKeyboardShortcuts() {
    document.addEventListener("keydown", (e) => {
      if (e.ctrlKey && e.shiftKey && e.key === "P") {
        e.preventDefault();
        this.toggleAllPrompts();
      }
    });
  }

  toggleAllPrompts() {
    const buttons = document.querySelectorAll(".toggleprompt-button");
    const firstButton = buttons[0];
    const shouldHide = !firstButton?.classList.contains("prompts-hidden");

    buttons.forEach((button) => {
      const block = button.closest(".highlight, .code-block-container");
      if (shouldHide !== button.classList.contains("prompts-hidden")) {
        this.togglePrompts(button, block);
      }
    });
  }
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  new SmartTogglePrompt();
});
```

## Performance Impact and Optimization Strategies

### Performance Metrics

- **JavaScript Size**: ~5KB minified and gzipped
- **DOM Impact**: 1 button element per code block
- **Memory Usage**: <1MB for 100+ code blocks
- **Interaction Latency**: <50ms toggle response time

### Optimization Techniques

#### Lazy Loading

```javascript
// Lazy initialization for performance
class LazyTogglePrompt {
  constructor() {
    this.observer = new IntersectionObserver(
      this.handleIntersection.bind(this),
    );
    this.initObserver();
  }

  initObserver() {
    const codeBlocks = document.querySelectorAll(".toggleprompt-enabled");
    codeBlocks.forEach((block) => this.observer.observe(block));
  }

  handleIntersection(entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        this.initializeToggle(entry.target);
        this.observer.unobserve(entry.target);
      }
    });
  }
}
```

#### Memory Management

```javascript
// Efficient content management
class OptimizedTogglePrompt {
  constructor() {
    this.contentCache = new Map();
    this.maxCacheSize = 50;
  }

  cacheContent(blockId, originalContent, cleanContent) {
    if (this.contentCache.size >= this.maxCacheSize) {
      // Remove oldest entry
      const firstKey = this.contentCache.keys().next().value;
      this.contentCache.delete(firstKey);
    }

    this.contentCache.set(blockId, {
      original: originalContent,
      clean: cleanContent,
      timestamp: Date.now(),
    });
  }

  getCachedContent(blockId) {
    return this.contentCache.get(blockId);
  }
}
```

This extension provides a sophisticated, accessible solution for managing code example presentation, enabling users to seamlessly switch between educational and practical views of command-line interfaces and code snippets.
