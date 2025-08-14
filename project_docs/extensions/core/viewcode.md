# sphinx.ext.viewcode - Source Code Links

**Extension**: `sphinx.ext.viewcode`  
**Priority**: Core Foundation (Position 3 in extensions list)  
**Official Documentation**: [sphinx.ext.viewcode](https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html)  
**Status in PyDevelop-Docs**: ✅ Implemented with enhanced source linking

## Overview

`sphinx.ext.viewcode` adds source code links to documented Python objects, allowing readers to view the actual implementation directly from the documentation. This extension creates a bridge between documentation and source code, enhancing developer understanding and trust in the documented APIs.

## Core Capabilities

### 1. Source Code Linking

- **Direct Links**: Clickable `[source]` links next to documented objects
- **Syntax Highlighting**: Full Python syntax highlighting in source views
- **Line Highlighting**: Specific line ranges highlighted for documented objects
- **Module Views**: Complete module source code with navigation

### 2. Source Code Pages

- **Dedicated Source Pages**: Separate pages for each module's source code
- **Cross-Navigation**: Easy navigation between documentation and source
- **Search Integration**: Source code content included in documentation search
- **Mobile Responsive**: Source code views work well on all devices

### 3. Smart Filtering

- **Selective Inclusion**: Control which modules get source links
- **Pattern Matching**: Include/exclude source links based on module patterns
- **Build Optimization**: Option to disable source generation for faster builds

## Configuration in PyDevelop-Docs

### Current Implementation

```python
# In config.py - viewcode included in core extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",  # Adds source code links
    # ... other extensions
]

# Basic viewcode configuration (uses defaults)
# No additional configuration needed for basic functionality
```

### Enhanced Configuration Options

```python
# Advanced viewcode configuration for PyDevelop-Docs
viewcode_import = None  # Auto-detect import path
viewcode_enable_epub = True  # Include source in EPUB builds
viewcode_follow_imported_members = True  # Show source for imported members

# Custom source link templates
viewcode_source_mapping = {
    'haive.core': 'https://github.com/haive-ai/haive/blob/main/packages/haive-core/src/haive/core',
    'haive.agents': 'https://github.com/haive-ai/haive/blob/main/packages/haive-agents/src/haive/agents',
    'haive.tools': 'https://github.com/haive-ai/haive/blob/main/packages/haive-tools/src/haive/tools',
}

# Exclude patterns for source code generation
viewcode_ignore_patterns = [
    '**/test_*.py',
    '**/tests/*',
    '**/*_test.py',
    '**/conftest.py',
    '**/node_test/**',  # Test directories
]
```

## Template Integration Opportunities

### 1. Custom Source Link Templates

```jinja2
{# _autoapi_templates/python/class.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% endif %}

{# Enhanced source link with line numbers #}
{% if obj.source_file %}
.. py:class:: {{ obj.id }}

   {% if obj.docstring %}
   {{ obj.docstring|prepare_docstring|indent(3) }}
   {% endif %}

   **Source Code:** `View on GitHub <{{ github_base_url }}/{{ obj.source_file }}#L{{ obj.start_line }}-L{{ obj.end_line }}>`_

   .. literalinclude:: {{ obj.source_file }}
      :language: python
      :lines: {{ obj.start_line }}-{{ obj.end_line }}
      :linenos:
      :emphasize-lines: {{ obj.definition_line }}
{% endif %}
```

### 2. Enhanced Module Templates

```jinja2
{# _autoapi_templates/python/module.rst #}
{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% endif %}

{# Module source overview #}
{% if obj.source_file %}
**Module Source:** :source:`{{ obj.name }}`

.. admonition:: Quick Source Preview
   :class: note

   .. literalinclude:: {{ obj.source_file }}
      :language: python
      :lines: 1-20
      :linenos:

   `View complete source <_modules/{{ obj.name|replace('.', '/') }}.html>`_
{% endif %}

{# Rest of module documentation #}
{% if obj.classes %}
Classes
-------

{% for class in obj.classes %}
{{ class.render()|indent(0) }}
{% endfor %}
{% endif %}
```

### 3. Interactive Source Code Blocks

```jinja2
{# Enhanced source code presentation #}
{% macro render_source_section(obj) %}
{% if obj.source_available %}
.. container:: source-code-section

   .. container:: source-toggle

      **Source Code** `[show/hide] <javascript:void(0)>`_

   .. container:: source-content
      :class: hidden

      .. code-block:: python
         :linenos:
         :emphasize-lines: {{ obj.definition_lines }}

         {{ obj.source_code }}

      **File:** ``{{ obj.source_file }}`` (lines {{ obj.start_line }}-{{ obj.end_line }})
{% endif %}
{% endmacro %}
```

## Best Practices for PyDevelop-Docs

### 1. Source Code Quality Standards

```python
class AgentBase:
    """Base class for all Haive agents.

    This class demonstrates well-documented code that benefits from
    viewcode integration. The source link allows readers to see the
    complete implementation alongside the documentation.
    """

    def __init__(self, name: str, config: AgentConfig) -> None:
        """Initialize agent with configuration.

        Args:
            name: Unique identifier for this agent instance.
            config: Configuration object with model and tool settings.
        """
        self.name = name
        self.config = config
        self._state = AgentState()

    def run(self, input_data: str) -> AgentResult:
        """Execute agent with input data.

        This method shows how viewcode links help readers understand
        the relationship between documentation and implementation.

        Args:
            input_data: Input string for agent processing.

        Returns:
            AgentResult: Complete execution result with metadata.
        """
        # Implementation details visible via [source] link
        return self._process_input(input_data)
```

### 2. Documentation-Source Alignment

```python
def create_multi_agent_workflow(
    agents: List[Agent],
    coordination_pattern: str = "sequential"
) -> MultiAgentWorkflow:
    """Create a coordinated multi-agent workflow.

    The source code link for this function allows readers to see
    exactly how the coordination patterns are implemented, building
    trust and understanding.

    Args:
        agents: List of configured agent instances.
        coordination_pattern: How agents should be coordinated.

    Returns:
        MultiAgentWorkflow: Ready-to-execute workflow.

    Example:
        The viewcode extension allows readers to verify this example
        by examining the actual implementation:

        >>> agents = [SimpleAgent("a1"), ReactAgent("a2")]
        >>> workflow = create_multi_agent_workflow(agents)
        >>> workflow.coordination_pattern
        'sequential'
    """
    # Readers can see this implementation via [source] link
    workflow = MultiAgentWorkflow()
    workflow.add_agents(agents)
    workflow.set_coordination(coordination_pattern)
    return workflow
```

### 3. Source Code Organization

```python
# File: haive/core/agents/base.py
"""Agent base classes with comprehensive source linking.

This module demonstrates optimal organization for viewcode integration.
Each class and function is well-documented and benefits from direct
source code access.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class Agent(ABC):
    """Abstract base class for all agents.

    Source link reveals the complete interface contract that all
    agents must implement, providing clarity for both users and
    implementers.
    """

    @abstractmethod
    def run(self, input_data: Any) -> Dict[str, Any]:
        """Execute agent with input data.

        Source link shows this is an abstract method that must be
        implemented by all agent subclasses.
        """
        pass
```

## Enhancement Opportunities

### 1. GitHub Integration

```python
def setup_github_source_links(app):
    """Setup enhanced GitHub source linking."""

    def create_github_link(filename, line_start, line_end=None):
        """Create GitHub source link with line numbers."""
        base_url = "https://github.com/haive-ai/haive/blob/main"
        if line_end:
            return f"{base_url}/{filename}#L{line_start}-L{line_end}"
        else:
            return f"{base_url}/{filename}#L{line_start}"

    app.add_config_value('github_source_link_template', create_github_link, 'env')

def setup(app):
    setup_github_source_links(app)
```

### 2. Source Code Analytics

```python
def analyze_source_coverage(app, exception):
    """Analyze source code coverage in documentation."""
    if exception:
        return

    # Count documented vs undocumented source files
    documented_files = set()
    total_source_files = set()

    # Gather statistics
    for pagename, context in app.env.all_docs.items():
        if hasattr(context, 'source_links'):
            documented_files.update(context.source_links)

    # Report coverage
    coverage_percent = len(documented_files) / len(total_source_files) * 100
    app.info(f"Source code coverage: {coverage_percent:.1f}%")

def setup(app):
    app.connect('build-finished', analyze_source_coverage)
```

### 3. Interactive Source Exploration

```python
def add_source_exploration_features(app):
    """Add interactive source exploration capabilities."""

    # Add JavaScript for source code folding
    app.add_js_file('source-explorer.js')

    # Add CSS for source code styling
    app.add_css_file('source-explorer.css')

    # Custom source code directive
    from docutils.core import publish_doctree
    from docutils.parsers.rst import directives

    class SourceExplorerDirective(directives.Directive):
        """Enhanced source code display directive."""

        required_arguments = 1  # Module name
        optional_arguments = 0
        option_spec = {
            'lines': str,
            'highlight': str,
            'fold': directives.flag,
        }

        def run(self):
            # Implementation for enhanced source display
            pass

    app.add_directive('source-explorer', SourceExplorerDirective)
```

## Current Implementation Status

### ✅ Working Features

- [x] **Basic source linking** - `[source]` links functional
- [x] **Source page generation** - Dedicated source pages created
- [x] **Syntax highlighting** - Python code properly highlighted
- [x] **Mobile compatibility** - Source views work on all devices
- [x] **Search integration** - Source content searchable

### 🔄 Enhancement Opportunities

- [ ] **GitHub integration** - Direct links to repository source
- [ ] **Line number precision** - More accurate line highlighting
- [ ] **Source analytics** - Track source code documentation coverage
- [ ] **Interactive features** - Code folding, copy buttons, permalinks
- [ ] **Performance optimization** - Lazy loading for large source files

### 📋 Template Integration Tasks

1. **Enhanced AutoAPI templates** with better source code presentation
2. **GitHub source linking** for direct repository access
3. **Interactive source features** for improved user experience
4. **Source code quality metrics** for documentation coverage tracking

## Integration with AutoAPI

### Source Information Access

```jinja2
{# Access source information in AutoAPI templates #}
{% if obj.source_file_path %}
.. admonition:: Source Code
   :class: source-info

   **File:** ``{{ obj.source_file_path }}``
   **Lines:** {{ obj.source_line_start }}-{{ obj.source_line_end }}

   :source:`View Source <{{ obj.module_name }}>`
{% endif %}
```

### Enhanced Rendering

```jinja2
{# Custom source code presentation #}
{% macro render_with_source(obj) %}
<div class="api-object-with-source">
   <div class="api-documentation">
      {{ obj.render_documentation() }}
   </div>

   {% if obj.source_available %}
   <div class="source-code-panel">
      <h4>Source Code</h4>
      {{ obj.render_source_code() }}

      <div class="source-links">
         <a href="{{ obj.github_url }}" target="_blank">View on GitHub</a> |
         <a href="{{ obj.source_page_url }}">Full Source</a>
      </div>
   </div>
   {% endif %}
</div>
{% endmacro %}
```

## Performance Considerations

### Build Time Optimization

```python
# Optimize viewcode for faster builds
viewcode_enable_epub = False  # Disable EPUB source inclusion
viewcode_follow_imported_members = False  # Don't follow imports

# Selective source generation
def should_include_source(module_name):
    """Determine if module should have source links."""
    exclude_patterns = ['test_', 'conftest', '__pycache__']
    return not any(pattern in module_name for pattern in exclude_patterns)

viewcode_include_test = should_include_source
```

### Memory Usage

```python
# Reduce memory usage for large codebases
viewcode_source_suffix = '.py'  # Only process Python files
viewcode_import = False  # Don't import modules for source extraction
```

## Troubleshooting

### Common Issues

1. **Missing Source Links**: Check module import paths and file accessibility
2. **Broken Source Pages**: Verify source file paths and permissions
3. **Performance Issues**: Large files may slow builds - consider exclusion patterns
4. **Line Number Accuracy**: Ensure source files match documented versions

### Debug Configuration

```python
# Debug viewcode processing
import logging
logging.getLogger('sphinx.ext.viewcode').setLevel(logging.DEBUG)

# Verify source file discovery
viewcode_debug = True  # Custom debug flag
```

## CSS Integration

### Source Code Styling

```css
/* Enhanced source code presentation */
.source-code-section {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  margin: 1em 0;
}

.source-toggle {
  background: #f8f9fa;
  padding: 0.5em 1em;
  border-bottom: 1px solid #e0e0e0;
  cursor: pointer;
}

.source-content {
  padding: 1em;
}

.source-content.hidden {
  display: none;
}

/* GitHub link styling */
.source-links {
  margin-top: 1em;
  padding-top: 0.5em;
  border-top: 1px solid #e0e0e0;
}

.source-links a {
  margin-right: 1em;
  color: #0066cc;
  text-decoration: none;
}
```

## JavaScript Enhancements

### Interactive Source Features

```javascript
// source-explorer.js - Enhanced source code interaction
document.addEventListener("DOMContentLoaded", function () {
  // Add copy buttons to source code blocks
  document.querySelectorAll(".highlight").forEach(function (block) {
    const button = document.createElement("button");
    button.className = "copy-source-btn";
    button.textContent = "Copy";
    button.onclick = function () {
      navigator.clipboard.writeText(block.textContent);
      button.textContent = "Copied!";
      setTimeout(() => (button.textContent = "Copy"), 2000);
    };
    block.appendChild(button);
  });

  // Toggle source code visibility
  document.querySelectorAll(".source-toggle").forEach(function (toggle) {
    toggle.onclick = function () {
      const content = this.nextElementSibling;
      content.classList.toggle("hidden");
      this.textContent = content.classList.contains("hidden")
        ? "Show Source"
        : "Hide Source";
    };
  });
});
```

## Integration with Issue #6

For AutoAPI template customization (Issue #6), viewcode provides:

1. **Source Access**: Direct access to source code for template rendering
2. **Line Information**: Precise line numbers for accurate source linking
3. **File Paths**: Source file locations for GitHub integration
4. **Interactive Elements**: Foundation for enhanced source code presentation

Viewcode enables AutoAPI templates to create rich, interactive documentation that seamlessly connects API reference with implementation details.
