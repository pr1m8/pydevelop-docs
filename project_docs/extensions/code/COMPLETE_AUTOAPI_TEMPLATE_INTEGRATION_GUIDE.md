# Complete AutoAPI Template Integration Guide

**Document**: Master Implementation Guide for Issue #6
**Purpose**: End-to-end guide for building perfect AutoAPI templates with code execution, CSS integration, and Jinja2 templating
**Version**: 1.0
**Date**: 2025-08-13

## Table of Contents

1. [Project Overview](#project-overview)
2. [Code Execution Extensions](#code-execution-extensions)
3. [Template Architecture](#template-architecture)
4. [CSS Integration Strategy](#css-integration-strategy)
5. [Jinja2 Template Development](#jinja2-template-development)
6. [Security and Performance](#security-and-performance)
7. [Complete Implementation](#complete-implementation)
8. [Testing and Validation](#testing-and-validation)
9. [Deployment Guide](#deployment-guide)

## Project Overview

### Current Status

Pydvlppy provides 40+ Sphinx extensions with advanced AutoAPI configuration, but Issue #6 requires custom Jinja2 templates for AutoAPI with integrated code execution extensions. This creates dynamic, live documentation where examples are always current and tested.

### Architecture Vision

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTOAPI TEMPLATE SYSTEM                  │
├─────────────────────┬─────────────────────┬─────────────────┤
│   JINJA2 TEMPLATES  │   CODE EXECUTION    │   CSS STYLING   │
│                     │                     │                 │
│ • class.rst         │ • sphinx_exec_code  │ • api-docs.css  │
│ • module.rst        │ • sphinx_runpython  │ • furo-int.css  │
│ • index.rst         │ • programoutput     │ • custom.css    │
│ • function.rst      │ • codeautolink      │ • theme.css     │
├─────────────────────┼─────────────────────┼─────────────────┤
│   DYNAMIC CONTENT   │   LIVE EXAMPLES     │   RESPONSIVE    │
│                     │                     │                 │
│ • Auto-generated    │ • Real execution    │ • Dark/Light    │
│ • Type-aware        │ • Error handling    │ • Mobile ready  │
│ • Cross-linked      │ • Performance opt   │ • Print styles  │
└─────────────────────┴─────────────────────┴─────────────────┘
```

### Key Goals

1. **Live Documentation**: Examples that execute during build and stay current
2. **Perfect Integration**: Seamless blend of templates, execution, and styling
3. **Developer Experience**: Intuitive navigation and comprehensive examples
4. **Performance**: Fast builds even with live code execution
5. **Security**: Safe code execution in documentation builds

## Code Execution Extensions

### Extension Matrix

| Extension          | Purpose             | Security Level         | Performance | AutoAPI Integration |
| ------------------ | ------------------- | ---------------------- | ----------- | ------------------- |
| `sphinx_exec_code` | Live code execution | High restrictions      | Medium      | ⭐⭐⭐ Excellent    |
| `sphinx_runpython` | Enhanced execution  | Medium restrictions    | Low         | ⭐⭐⭐ Excellent    |
| `programoutput`    | CLI/System commands | Very high restrictions | High        | ⭐⭐ Good           |
| `codeautolink`     | Automatic linking   | No restrictions        | High        | ⭐⭐⭐ Excellent    |

### Configuration Strategy

```python
# config.py - Complete code execution setup
EXECUTION_CONFIG = {
    # sphinx_exec_code - Primary live examples
    "exec_code_working_dir": "_exec_code_temp",
    "exec_code_timeout": 15,
    "exec_code_allowed_modules": [
        "haive.*", "pydantic", "typing", "datetime", "json", "re"
    ],
    "exec_code_forbidden_imports": [
        "os", "sys.exit", "subprocess", "socket", "urllib"
    ],
    "exec_code_cache_enabled": True,
    "exec_code_parallel": True,

    # sphinx_runpython - Enhanced examples
    "runpython_context_persist": True,
    "runpython_output_limit": 50000,
    "runpython_memory_limit": "128MB",
    "runpython_show_plots": True,
    "runpython_format_stdout": True,

    # programoutput - CLI demonstrations
    "programoutput_use_ansi": True,
    "programoutput_timeout": 30,
    "programoutput_allowed_commands": [
        "python", "poetry", "pip", "ls", "cat", "head"
    ],
    "programoutput_cache_timeout": 3600,

    # codeautolink - Automatic linking
    "codeautolink_autodoc_inject": True,
    "codeautolink_concat_default": True,
    "codeautolink_debug": False,
    "codeautolink_warn_on_missing": True
}
```

### Security Model

```python
# Comprehensive security configuration
SECURITY_CONFIG = {
    # Global restrictions
    "execution_timeout": 15,                    # Max execution time
    "memory_limit": "256MB",                    # Memory per execution
    "network_access": False,                    # No network access
    "file_access": "read_only",                 # Read-only file access

    # Module whitelist
    "allowed_modules": [
        "haive.*",           # Our code
        "pydantic",          # Safe data validation
        "typing",            # Type annotations
        "datetime",          # Date/time utilities
        "json",              # JSON handling
        "re",                # Regular expressions
        "math",              # Mathematical operations
        "statistics",        # Statistical functions
    ],

    # Forbidden operations
    "forbidden_imports": [
        "os",                # Operating system interface
        "sys.exit",          # System exit
        "subprocess",        # Process execution
        "socket",            # Network operations
        "urllib",            # URL operations
        "requests",          # HTTP requests
        "shutil",            # File operations
        "__import__",        # Dynamic imports
        "eval",              # Code evaluation
        "exec",              # Code execution
    ],

    # Resource limits
    "max_output_lines": 1000,
    "max_execution_count": 100,
    "cleanup_on_exit": True
}
```

## Template Architecture

### Directory Structure

```
src/pydevelop_docs/templates/_autoapi_templates/
├── python/
│   ├── index.rst                   # Main API index
│   ├── module.rst                  # Module documentation
│   ├── class.rst                   # Class documentation
│   ├── function.rst                # Function documentation
│   ├── method.rst                  # Method documentation
│   ├── attribute.rst               # Attribute documentation
│   └── exception.rst               # Exception documentation
├── includes/
│   ├── live_examples.rst           # Live example templates
│   ├── code_execution.rst          # Code execution blocks
│   ├── performance_tips.rst        # Performance examples
│   └── security_examples.rst       # Security demonstrations
├── macros/
│   ├── code_generation.rst         # Code generation macros
│   ├── example_builders.rst        # Example builder macros
│   └── type_detection.rst          # Type detection utilities
└── static/
    ├── css/
    │   ├── autoapi-live.css        # Live execution styling
    │   ├── code-examples.css       # Code example styling
    │   └── responsive-api.css      # Responsive API styling
    └── js/
        ├── live-examples.js        # Interactive example features
        └── code-execution.js       # Code execution utilities
```

### Template Hierarchy

```jinja2
{# Base template pattern #}
{% extends "base_api.rst" %}

{# Common includes #}
{% include "includes/live_examples.rst" %}
{% include "includes/code_execution.rst" %}

{# Macro imports #}
{% from "macros/code_generation.rst" import generate_example, safe_execution %}
{% from "macros/example_builders.rst" import build_class_example, build_method_example %}
```

## CSS Integration Strategy

### Current CSS Architecture

Pydvlppy consolidates CSS from 17+ files to 6 optimized files:

```
docs/source/_static/css/
├── api-docs.css           # 🎯 API documentation styling
├── custom.css             # 🎨 General customizations
├── furo-intense.css       # 🌙 Dark mode fixes
├── mermaid-custom.css     # 📊 Diagram styling
├── tippy-enhancements.css # 💬 Tooltip improvements
└── toc-enhancements.css   # 📑 Table of contents
```

### AutoAPI-Specific CSS

```css
/* api-docs.css - Core API documentation styling */

/* Live code execution blocks */
.exec-code-block {
  background: var(--color-code-background);
  border-left: 4px solid var(--color-brand-primary);
  margin: 1.5rem 0;
  border-radius: 0.375rem;
}

.exec-code-block .highlight {
  margin: 0;
  border-radius: 0;
}

.exec-code-output {
  background: var(--color-background-secondary);
  border-top: 1px solid var(--color-border);
  padding: 1rem;
  font-family: var(--font-stack-monospace);
  font-size: 0.875rem;
  overflow-x: auto;
}

/* AutoAPI class documentation */
.autoapi-class {
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  margin: 2rem 0;
  overflow: hidden;
}

.autoapi-class-header {
  background: var(--color-background-primary);
  padding: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.autoapi-class-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-heading);
  margin: 0;
}

.autoapi-class-signature {
  font-family: var(--font-stack-monospace);
  background: var(--color-code-background);
  padding: 0.5rem;
  border-radius: 0.25rem;
  margin-top: 0.5rem;
  overflow-x: auto;
}

/* Method documentation */
.autoapi-method {
  margin: 1.5rem 0;
  padding: 1rem;
  border: 1px solid var(--color-border-light);
  border-radius: 0.375rem;
}

.autoapi-method-name {
  font-family: var(--font-stack-monospace);
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-link);
  margin-bottom: 0.5rem;
}

.autoapi-method-signature {
  font-family: var(--font-stack-monospace);
  font-size: 0.875rem;
  background: var(--color-code-background);
  padding: 0.5rem;
  border-radius: 0.25rem;
  margin-bottom: 1rem;
  overflow-x: auto;
}

/* Live examples */
.live-example {
  background: linear-gradient(
    135deg,
    var(--color-background-secondary) 0%,
    var(--color-background-primary) 100%
  );
  border: 1px solid var(--color-brand-primary);
  border-radius: 0.5rem;
  margin: 1.5rem 0;
  overflow: hidden;
}

.live-example-header {
  background: var(--color-brand-primary);
  color: white;
  padding: 0.75rem 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.live-example-header::before {
  content: "▶";
  font-size: 0.875rem;
}

.live-example-content {
  padding: 1rem;
}

/* Code execution status */
.execution-status {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-weight: 500;
}

.execution-status.success {
  background: rgba(34, 197, 94, 0.1);
  color: rgb(34, 197, 94);
}

.execution-status.error {
  background: rgba(239, 68, 68, 0.1);
  color: rgb(239, 68, 68);
}

.execution-status.timeout {
  background: rgba(245, 158, 11, 0.1);
  color: rgb(245, 158, 11);
}

/* Responsive design */
@media (max-width: 768px) {
  .autoapi-class-signature,
  .autoapi-method-signature,
  .exec-code-output {
    font-size: 0.75rem;
    padding: 0.75rem;
  }

  .live-example-header {
    padding: 0.5rem;
    font-size: 0.875rem;
  }
}

/* Dark mode optimizations */
[data-theme="dark"] .exec-code-block {
  border-left-color: var(--color-brand-primary-light);
}

[data-theme="dark"] .live-example {
  border-color: var(--color-brand-primary-light);
}

[data-theme="dark"] .live-example-header {
  background: var(--color-brand-primary-dark);
}

/* Print styles */
@media print {
  .exec-code-output,
  .live-example {
    break-inside: avoid;
    border: 1px solid #ccc;
    background: white !important;
  }

  .live-example-header {
    background: #f5f5f5 !important;
    color: #333 !important;
  }
}
```

### Furo Theme Integration

```css
/* furo-intense.css - Enhanced dark mode */

/* Fix white-on-white text issues */
.furo-content pre {
  background: var(--color-background-secondary) !important;
  color: var(--color-foreground-primary) !important;
}

.furo-content code {
  background: var(--color-background-secondary) !important;
  color: var(--color-foreground-primary) !important;
  padding: 0.125rem 0.25rem;
  border-radius: 0.125rem;
}

/* AutoAPI integration with Furo */
.furo-sidebar .autoapi-toc {
  margin: 1rem 0;
}

.furo-sidebar .autoapi-toc a {
  color: var(--color-sidebar-link-text);
  text-decoration: none;
  display: block;
  padding: 0.25rem 0;
  border-left: 2px solid transparent;
  padding-left: 0.5rem;
}

.furo-sidebar .autoapi-toc a:hover {
  border-left-color: var(--color-brand-primary);
  background: var(--color-sidebar-item-background--hover);
}

.furo-sidebar .autoapi-toc .current {
  border-left-color: var(--color-brand-primary);
  background: var(--color-sidebar-item-background--current);
  font-weight: 600;
}
```

## Jinja2 Template Development

### Master Class Template

```jinja2
{# _autoapi_templates/python/class.rst #}
{%- set class_name = obj.name -%}
{%- set module_name = obj.module.id -%}
{%- set full_name = obj.id -%}

{{ class_name }}
{{ "=" * class_name|length }}

.. currentmodule:: {{ module_name }}

.. autoclass:: {{ class_name }}
   :members:
   :undoc-members:
   :show-inheritance:

{% if obj.docstring %}
Overview
--------

{{ obj.docstring }}
{% endif %}

{% if obj.constructor_args %}
Initialization
--------------

.. exec-code:: python
   :caption: {{ class_name }} Creation

   from {{ module_name }} import {{ class_name }}

   # Create instance with example parameters
   {% if obj.has_simple_constructor %}
   instance = {{ class_name }}()
   print(f"Created {instance.__class__.__name__} instance")
   {% else %}
   # Complex constructor - show signature
   import inspect
   print(f"Constructor signature:")
   print(f"  {inspect.signature({{ class_name }})}")
   {% endif %}

{% endif %}

{% if obj.attributes %}
Attributes
----------

{% for attr in obj.attributes %}
{% if not attr.name.startswith('_') %}
.. runpython::
   :context: {{ class_name|lower }}_attrs

   {% if loop.first %}
   from {{ module_name }} import {{ class_name }}
   instance = {{ class_name }}() if hasattr({{ class_name }}, '__init__') else None
   {% endif %}

   # {{ attr.name }} attribute
   if instance and hasattr(instance, '{{ attr.name }}'):
       try:
           value = getattr(instance, '{{ attr.name }}')
           print(f"{{ attr.name }}: {value} (type: {type(value).__name__})")
       except Exception as e:
           print(f"{{ attr.name }}: <property - {e}>")
   else:
       print(f"{{ attr.name }}: <class attribute>")

{% endif %}
{% endfor %}
{% endif %}

{% if obj.methods %}
Methods
-------

{% for method in obj.methods %}
{% if not method.name.startswith('_') or method.name in ['__init__', '__call__', '__str__', '__repr__'] %}

{{ method.name }}
{{ "~" * method.name|length }}

.. automethod:: {{ method.name }}

{% if method.has_safe_example %}
.. exec-code:: python
   :caption: {{ method.name }} Example
   :linenos:

   from {{ module_name }} import {{ class_name }}

   {% if method.name == '__init__' %}
   # Constructor example
   instance = {{ class_name }}({{ method.example_args or '' }})
   print(f"Instance created: {instance}")

   {% elif method.name == '__call__' %}
   # Callable example
   instance = {{ class_name }}()
   result = instance({{ method.example_args or "'example_input'" }})
   print(f"Call result: {result}")

   {% elif method.name in ['__str__', '__repr__'] %}
   # String representation
   instance = {{ class_name }}()
   print(f"String representation: {instance}")

   {% else %}
   # Regular method example
   instance = {{ class_name }}()
   try:
       {% if method.example_args %}
       result = instance.{{ method.name }}({{ method.example_args }})
       {% else %}
       result = instance.{{ method.name }}()
       {% endif %}
       print(f"Method result: {result}")
       print(f"Return type: {type(result).__name__}")
   except Exception as e:
       print(f"Example execution note: {e}")
   {% endif %}

{% endif %}
{% endif %}
{% endfor %}
{% endif %}

{% if obj.example_usage %}
Complete Example
---------------

.. runpython::
   :context: {{ class_name|lower }}_complete
   :show-plots:

   from {{ module_name }} import {{ class_name }}

   # Complete usage example
   {{ obj.example_usage }}

{% endif %}

{% if obj.related_classes %}
Related Classes
--------------

{% for related in obj.related_classes %}
* :class:`{{ related.id }}`{% if related.relationship %} - {{ related.relationship }}{% endif %}
{% endfor %}
{% endif %}

{% if obj.performance_notes %}
Performance Notes
----------------

.. program-output:: python -c "
   from {{ module_name }} import {{ class_name }}
   import time
   import sys

   # Performance timing example
   start_time = time.time()

   # Create and use instance
   instance = {{ class_name }}()
   # Add performance test here

   end_time = time.time()
   execution_time = end_time - start_time

   print(f'Execution time: {execution_time:.4f} seconds')
   print(f'Memory usage: {sys.getsizeof(instance)} bytes')
   "
   :caption: Performance Metrics

{{ obj.performance_notes }}
{% endif %}

See Also
--------

* :doc:`{{ module_name.replace('.', '/') }}/index` - Module documentation
* :doc:`/api/index` - Full API reference
{% if obj.source_file %}
* `Source code <{{ obj.source_file }}>`_ - View on GitHub
{% endif %}
```

### Master Module Template

```jinja2
{# _autoapi_templates/python/module.rst #}
{%- set module_name = obj.name -%}
{%- set module_id = obj.id -%}

{{ module_name }}
{{ "=" * module_name|length }}

.. automodule:: {{ module_id }}

{% if obj.docstring %}
{{ obj.docstring }}
{% endif %}

{% if obj.all %}
Public API
----------

.. program-output:: python -c "
   import {{ module_id }}

   # Show public API
   if hasattr({{ module_id }}, '__all__'):
       print('Exported items:')
       for item in {{ module_id }}.__all__:
           print(f'  - {item}')
   else:
       print('All public items available for import')
   "
   :caption: Module Exports

{% endif %}

{% if obj.functions %}
Functions
---------

{% for function in obj.functions %}
{{ function.name }}
{{ "~" * function.name|length }}

.. autofunction:: {{ function.name }}

{% if function.has_example %}
.. exec-code:: python
   :caption: {{ function.name }} Example

   from {{ module_id }} import {{ function.name }}

   # Function example
   {% if function.example_args %}
   result = {{ function.name }}({{ function.example_args }})
   {% else %}
   result = {{ function.name }}()
   {% endif %}
   print(f"Function result: {result}")
   print(f"Return type: {type(result).__name__}")

{% endif %}
{% endfor %}
{% endif %}

{% if obj.classes %}
Classes
-------

{% for class in obj.classes %}
{{ class.name }}
{{ "~" * class.name|length }}

.. autoclass:: {{ class.name }}
   :members:
   :noindex:

{% if class.has_quick_example %}
.. exec-code:: python
   :caption: Quick {{ class.name }} Example

   from {{ module_id }} import {{ class.name }}

   # Quick class example
   instance = {{ class.name }}()
   print(f"Created: {instance.__class__.__name__}")

   # Show key methods
   methods = [m for m in dir(instance) if not m.startswith('_')][:3]
   print(f"Key methods: {', '.join(methods)}")

{% endif %}

* :doc:`{{ class.name|lower }}` - Detailed documentation

{% endfor %}
{% endif %}

{% if obj.submodules %}
Submodules
----------

.. toctree::
   :maxdepth: 1

{% for submodule in obj.submodules %}
   {{ submodule.name }}
{% endfor %}

{% endif %}

{% if obj.exceptions %}
Exceptions
----------

{% for exception in obj.exceptions %}
.. autoexception:: {{ exception.name }}

{% endfor %}
{% endif %}

Quick Start
-----------

.. runpython::
   :context: {{ module_id.replace('.', '_') }}_quickstart

   # Quick start example for {{ module_name }}
   import {{ module_id }}

   {% if obj.quick_start_example %}
   {{ obj.quick_start_example }}
   {% else %}
   # Basic import test
   print(f"Module loaded: {{ module_id }}")
   print(f"Location: {{{ module_id }}.__file__}")

   # Show available items
   items = [item for item in dir({{ module_id }}) if not item.startswith('_')]
   print(f"Available items: {len(items)}")
   for item in items[:5]:  # Show first 5
       print(f"  - {item}")
   {% endif %}

Integration Examples
-------------------

.. exec-code:: python
   :caption: Integration with Other Modules

   # Show how this module integrates with others
   import {{ module_id }}
   {% for related in obj.related_modules %}
   try:
       import {{ related }}
       print(f"✓ Compatible with {{ related }}")
   except ImportError:
       print(f"- {{ related }} not available")
   {% endfor %}

Testing
-------

.. program-output:: python -c "
   import {{ module_id }}
   import doctest

   # Run doctests if available
   try:
       result = doctest.testmod({{ module_id }}, verbose=True)
       print(f'Doctests: {result.attempted} attempted, {result.failed} failed')
   except Exception as e:
       print(f'Doctest execution: {e}')
   "
   :caption: Module Testing

See Also
--------

* :doc:`/api/index` - Full API reference
* :doc:`/examples/{{ module_name|lower }}` - Extended examples
{% if obj.source_file %}
* `Source code <{{ obj.source_file }}>`_ - View on GitHub
{% endif %}
```

### Example Builder Macros

```jinja2
{# macros/example_builders.rst #}

{%- macro generate_safe_example(obj, example_type="basic") -%}
{% set timeout = 10 if example_type == "quick" else 30 %}
.. exec-code:: python
   :timeout: {{ timeout }}
   :caption: {{ obj.name }} {{ example_type|title }} Example

   {% if example_type == "basic" %}
   from {{ obj.module.id }} import {{ obj.name }}

   # Basic usage
   {% if obj.has_simple_constructor %}
   instance = {{ obj.name }}()
   {% else %}
   # Complex constructor - show signature
   import inspect
   print(f"Signature: {inspect.signature({{ obj.name }})}")
   {% endif %}

   {% elif example_type == "advanced" %}
   from {{ obj.module.id }} import {{ obj.name }}

   # Advanced usage with error handling
   try:
       instance = {{ obj.name }}({{ obj.advanced_example_args or '' }})

       {% if obj.chainable_methods %}
       # Method chaining example
       result = instance{% for method in obj.chainable_methods[:3] %}.{{ method.name }}(){% endfor %}
       print(f"Chained result: {result}")
       {% endif %}

   except Exception as e:
       print(f"Advanced example note: {e}")

   {% elif example_type == "performance" %}
   from {{ obj.module.id }} import {{ obj.name }}
   import time

   # Performance example
   start_time = time.time()

   {% if obj.performance_test %}
   {{ obj.performance_test }}
   {% else %}
   # Basic performance test
   instances = [{{ obj.name }}() for _ in range(100)]
   print(f"Created {len(instances)} instances")
   {% endif %}

   execution_time = time.time() - start_time
   print(f"Execution time: {execution_time:.4f}s")
   {% endif %}

{%- endmacro -%}

{%- macro generate_method_example(method, class_obj) -%}
.. exec-code:: python
   :caption: {{ method.name }} Method Example

   from {{ class_obj.module.id }} import {{ class_obj.name }}

   # Method-specific example
   instance = {{ class_obj.name }}()

   {% if method.name == '__init__' %}
   # Constructor already called above
   print(f"Instance type: {type(instance).__name__}")

   {% elif method.is_property %}
   # Property access
   try:
       value = instance.{{ method.name }}
       print(f"Property value: {value}")
   except Exception as e:
       print(f"Property access: {e}")

   {% elif method.is_classmethod %}
   # Class method
   result = {{ class_obj.name }}.{{ method.name }}({{ method.example_args or '' }})
   print(f"Class method result: {result}")

   {% elif method.is_staticmethod %}
   # Static method
   result = {{ class_obj.name }}.{{ method.name }}({{ method.example_args or '' }})
   print(f"Static method result: {result}")

   {% else %}
   # Instance method
   try:
       {% if method.example_args %}
       result = instance.{{ method.name }}({{ method.example_args }})
       {% else %}
       result = instance.{{ method.name }}()
       {% endif %}
       print(f"Method result: {result}")
   except Exception as e:
       print(f"Method example: {e}")
   {% endif %}

{%- endmacro -%}

{%- macro generate_integration_test(obj) -%}
.. program-output:: python -c "
   # Integration test for {{ obj.name }}
   from {{ obj.module.id }} import {{ obj.name }}
   import sys
   import traceback

   try:
       # Basic instantiation test
       instance = {{ obj.name }}()
       print('✓ Instantiation successful')

       # Method availability test
       expected_methods = {{ obj.expected_methods or '[]' }}
       for method_name in expected_methods:
           if hasattr(instance, method_name):
               print(f'✓ Method {method_name} available')
           else:
               print(f'✗ Method {method_name} missing')

       # Type validation
       print(f'Instance type: {type(instance).__name__}')
       print(f'Module: {instance.__class__.__module__}')

   except Exception as e:
       print(f'✗ Integration test failed: {e}')
       traceback.print_exc()
   "
   :caption: {{ obj.name }} Integration Test

{%- endmacro -%}
```

## Security and Performance

### Security Implementation

```python
# security_manager.py
class ExecutionSecurityManager:
    """Manage security for code execution in templates."""

    ALLOWED_MODULES = {
        "haive.*",
        "pydantic",
        "typing",
        "datetime",
        "json",
        "re",
        "math",
        "statistics",
        "collections",
        "itertools",
        "functools"
    }

    FORBIDDEN_OPERATIONS = {
        "__import__", "eval", "exec", "compile",
        "open", "file", "input", "raw_input",
        "exit", "quit", "reload", "execfile"
    }

    SAFE_BUILTINS = {
        "abs", "all", "any", "bin", "bool", "chr", "dict",
        "dir", "divmod", "enumerate", "filter", "float",
        "format", "frozenset", "getattr", "hasattr", "hash",
        "hex", "id", "int", "isinstance", "issubclass", "iter",
        "len", "list", "map", "max", "min", "next", "oct",
        "ord", "pow", "print", "range", "repr", "reversed",
        "round", "set", "slice", "sorted", "str", "sum", "tuple",
        "type", "vars", "zip"
    }

    @classmethod
    def create_safe_globals(cls, module_whitelist=None):
        """Create safe globals dict for code execution."""
        safe_globals = {
            "__builtins__": {name: getattr(__builtins__, name)
                           for name in cls.SAFE_BUILTINS
                           if hasattr(__builtins__, name)}
        }

        # Add whitelisted modules
        if module_whitelist:
            for module_pattern in module_whitelist:
                try:
                    if module_pattern.endswith(".*"):
                        # Handle wildcard imports
                        base_module = module_pattern[:-2]
                        module = __import__(base_module)
                        safe_globals[base_module] = module
                    else:
                        module = __import__(module_pattern)
                        safe_globals[module_pattern] = module
                except ImportError:
                    pass  # Module not available

        return safe_globals

    @classmethod
    def validate_code(cls, code_string):
        """Validate code string for security issues."""
        # Check for forbidden operations
        for forbidden in cls.FORBIDDEN_OPERATIONS:
            if forbidden in code_string:
                raise SecurityError(f"Forbidden operation: {forbidden}")

        # Check for dangerous imports
        import ast
        try:
            tree = ast.parse(code_string)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if not cls._is_module_allowed(alias.name):
                            raise SecurityError(f"Forbidden import: {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module and not cls._is_module_allowed(node.module):
                        raise SecurityError(f"Forbidden import: {node.module}")
        except SyntaxError:
            raise SecurityError("Invalid Python syntax")

        return True

    @classmethod
    def _is_module_allowed(cls, module_name):
        """Check if module is in allowed list."""
        for pattern in cls.ALLOWED_MODULES:
            if pattern.endswith(".*"):
                if module_name.startswith(pattern[:-2]):
                    return True
            elif pattern == module_name:
                return True
        return False

class SecurityError(Exception):
    """Security validation error."""
    pass
```

### Performance Optimization

```python
# performance_manager.py
import time
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from functools import lru_cache
import hashlib

class ExecutionPerformanceManager:
    """Manage performance for code execution."""

    def __init__(self):
        self.execution_cache = {}
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.execution_times = {}
        self.lock = threading.Lock()

    @lru_cache(maxsize=1000)
    def get_cached_result(self, code_hash, context_hash):
        """Get cached execution result."""
        cache_key = f"{code_hash}:{context_hash}"
        return self.execution_cache.get(cache_key)

    def cache_result(self, code_hash, context_hash, result):
        """Cache execution result."""
        cache_key = f"{code_hash}:{context_hash}"
        with self.lock:
            self.execution_cache[cache_key] = result

    def execute_with_timeout(self, code_string, globals_dict, timeout=15):
        """Execute code with timeout and performance monitoring."""
        start_time = time.time()

        # Check cache first
        code_hash = hashlib.md5(code_string.encode()).hexdigest()
        context_hash = hashlib.md5(str(sorted(globals_dict.keys())).encode()).hexdigest()

        cached_result = self.get_cached_result(code_hash, context_hash)
        if cached_result:
            return cached_result

        # Execute with timeout
        future = self.executor.submit(self._execute_code, code_string, globals_dict)

        try:
            result = future.result(timeout=timeout)
            execution_time = time.time() - start_time

            # Cache successful results
            self.cache_result(code_hash, context_hash, result)

            # Track performance
            with self.lock:
                self.execution_times[code_hash] = execution_time

            return result

        except TimeoutError:
            future.cancel()
            raise ExecutionTimeoutError(f"Code execution timeout after {timeout}s")
        except Exception as e:
            raise ExecutionError(f"Code execution failed: {e}")

    def _execute_code(self, code_string, globals_dict):
        """Internal code execution."""
        locals_dict = {}
        exec(code_string, globals_dict, locals_dict)
        return locals_dict

    def get_performance_stats(self):
        """Get execution performance statistics."""
        with self.lock:
            if not self.execution_times:
                return {"count": 0, "avg_time": 0, "max_time": 0}

            times = list(self.execution_times.values())
            return {
                "count": len(times),
                "avg_time": sum(times) / len(times),
                "max_time": max(times),
                "min_time": min(times),
                "cache_hits": len(self.execution_cache)
            }

class ExecutionTimeoutError(Exception):
    """Code execution timeout error."""
    pass

class ExecutionError(Exception):
    """Code execution error."""
    pass
```

## Complete Implementation

### Template Integration Service

```python
# template_integration.py
from pathlib import Path
import shutil
from jinja2 import Environment, FileSystemLoader
from .security_manager import ExecutionSecurityManager
from .performance_manager import ExecutionPerformanceManager

class AutoAPITemplateIntegrator:
    """Complete AutoAPI template integration service."""

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.template_dir = self.project_root / "src/pydevelop_docs/templates"
        self.security_manager = ExecutionSecurityManager()
        self.performance_manager = ExecutionPerformanceManager()

        # Setup Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Add custom filters and functions
        self._setup_jinja_environment()

    def _setup_jinja_environment(self):
        """Setup Jinja2 environment with custom filters."""

        def safe_execution_filter(code_string, timeout=15):
            """Jinja2 filter for safe code execution."""
            try:
                self.security_manager.validate_code(code_string)
                safe_globals = self.security_manager.create_safe_globals([
                    "haive.*", "pydantic", "typing"
                ])
                return self.performance_manager.execute_with_timeout(
                    code_string, safe_globals, timeout
                )
            except Exception as e:
                return {"error": str(e)}

        def format_code_block(code, language="python", caption=None):
            """Format code block with proper styling."""
            lines = [f".. code-block:: {language}"]
            if caption:
                lines.append(f"   :caption: {caption}")
            lines.append("   :linenos:")
            lines.append("")
            for line in code.split('\n'):
                lines.append(f"   {line}")
            return '\n'.join(lines)

        def generate_example_args(obj):
            """Generate safe example arguments for objects."""
            if hasattr(obj, 'constructor_args'):
                args = []
                for arg in obj.constructor_args:
                    if arg.type == 'str':
                        args.append(f'"{arg.example_value or "example"}"')
                    elif arg.type == 'int':
                        args.append(str(arg.example_value or 42))
                    elif arg.type == 'float':
                        args.append(str(arg.example_value or 3.14))
                    elif arg.type == 'bool':
                        args.append(str(arg.example_value or True))
                    else:
                        args.append(f'None  # {arg.type}')
                return ', '.join(args)
            return ''

        # Register filters
        self.jinja_env.filters['safe_execution'] = safe_execution_filter
        self.jinja_env.filters['format_code'] = format_code_block
        self.jinja_env.filters['example_args'] = generate_example_args

        # Register global functions
        self.jinja_env.globals['performance_stats'] = self.performance_manager.get_performance_stats

    def install_templates(self, target_dir):
        """Install AutoAPI templates to target directory."""
        target_path = Path(target_dir) / "_autoapi_templates"

        # Create target directory
        target_path.mkdir(parents=True, exist_ok=True)

        # Copy template files
        template_source = self.template_dir / "_autoapi_templates"
        if template_source.exists():
            shutil.copytree(template_source, target_path, dirs_exist_ok=True)
        else:
            # Generate templates if they don't exist
            self._generate_templates(target_path)

        # Install CSS files
        self._install_css_files(target_dir)

        return target_path

    def _generate_templates(self, target_path):
        """Generate AutoAPI templates programmatically."""
        templates = {
            "python/class.rst": self._get_class_template(),
            "python/module.rst": self._get_module_template(),
            "python/index.rst": self._get_index_template(),
            "python/function.rst": self._get_function_template(),
            "includes/live_examples.rst": self._get_live_examples_include(),
            "macros/example_builders.rst": self._get_example_builders_macro()
        }

        for template_path, content in templates.items():
            full_path = target_path / template_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

    def _install_css_files(self, target_dir):
        """Install CSS files for AutoAPI integration."""
        css_source = self.template_dir / "static/css"
        css_target = Path(target_dir) / "_static/css"

        css_target.mkdir(parents=True, exist_ok=True)

        # Copy CSS files
        if css_source.exists():
            for css_file in css_source.glob("*.css"):
                shutil.copy2(css_file, css_target)

    def render_template(self, template_name, context):
        """Render template with given context."""
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)

    def validate_installation(self, target_dir):
        """Validate template installation."""
        target_path = Path(target_dir) / "_autoapi_templates"

        required_templates = [
            "python/class.rst",
            "python/module.rst",
            "python/index.rst"
        ]

        missing_templates = []
        for template in required_templates:
            if not (target_path / template).exists():
                missing_templates.append(template)

        if missing_templates:
            raise ValidationError(f"Missing templates: {missing_templates}")

        return True

    def _get_class_template(self):
        """Get the complete class template content."""
        return '''
{# Complete class template with live examples #}
{%- set class_name = obj.name -%}
{%- set module_name = obj.module.id -%}

{{ class_name }}
{{ "=" * class_name|length }}

.. currentmodule:: {{ module_name }}
.. autoclass:: {{ class_name }}
   :members:
   :undoc-members:
   :show-inheritance:

{% include "includes/live_examples.rst" %}

{# Rest of template content from earlier examples #}
        '''.strip()

# Continue with other template methods...
```

### Configuration Integration

```python
# Update config.py with template integration
def get_complete_autoapi_config(package_name, is_central_hub=False):
    """Get complete AutoAPI configuration with template integration."""

    base_config = get_haive_config(package_name, is_central_hub)

    # Add template-specific configuration
    template_config = {
        # AutoAPI with custom templates
        "autoapi_template_dir": "_autoapi_templates",
        "autoapi_own_page_level": "module",
        "autoapi_options": [
            "members",
            "undoc-members",
            "show-inheritance",
            "show-module-summary",
            "special-members",
            "private-members",
        ],

        # Code execution security
        "exec_code_working_dir": "_exec_code_temp",
        "exec_code_timeout": 15,
        "exec_code_allowed_modules": [
            "haive.*", "pydantic", "typing", "datetime", "json", "re"
        ],
        "exec_code_cache_enabled": True,

        # Performance optimization
        "runpython_cache_enabled": True,
        "runpython_parallel_contexts": True,
        "programoutput_cache_timeout": 3600,

        # Enhanced linking
        "codeautolink_autodoc_inject": True,
        "codeautolink_concat_default": True,

        # Template-specific CSS
        "html_css_files": [
            "css/api-docs.css",
            "css/custom.css",
            "css/furo-intense.css",
            "css/live-examples.css"
        ]
    }

    # Merge configurations
    base_config.update(template_config)
    return base_config
```

## Testing and Validation

### Comprehensive Test Suite

```python
# test_template_integration.py
import pytest
import tempfile
from pathlib import Path
from .template_integration import AutoAPITemplateIntegrator

class TestAutoAPIIntegration:
    """Test suite for AutoAPI template integration."""

    @pytest.fixture
    def integrator(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield AutoAPITemplateIntegrator(tmp_dir)

    @pytest.fixture
    def mock_class_obj(self):
        """Mock class object for testing."""
        class MockClass:
            def __init__(self):
                self.name = "TestClass"
                self.module = MockModule()
                self.id = "test.module.TestClass"
                self.docstring = "Test class docstring"
                self.methods = [MockMethod()]
                self.attributes = [MockAttribute()]
                self.has_simple_constructor = True

        return MockClass()

    def test_template_installation(self, integrator):
        """Test template installation."""
        with tempfile.TemporaryDirectory() as target_dir:
            result = integrator.install_templates(target_dir)

            assert result.exists()
            assert (result / "python/class.rst").exists()
            assert (result / "python/module.rst").exists()

    def test_security_validation(self, integrator):
        """Test security validation."""
        # Safe code should pass
        safe_code = "from haive.agents import SimpleAgent\nprint('test')"
        assert integrator.security_manager.validate_code(safe_code)

        # Dangerous code should fail
        with pytest.raises(SecurityError):
            dangerous_code = "import os\nos.system('rm -rf /')"
            integrator.security_manager.validate_code(dangerous_code)

    def test_template_rendering(self, integrator, mock_class_obj):
        """Test template rendering."""
        context = {"obj": mock_class_obj}

        # This would use the actual template
        result = integrator.render_template("python/class.rst", context)

        assert "TestClass" in result
        assert "exec-code::" in result
        assert "autoclass::" in result

    def test_performance_optimization(self, integrator):
        """Test performance optimization."""
        # Test caching
        code = "x = 1 + 1\nprint(x)"
        globals_dict = {"print": print}

        # First execution
        start_time = time.time()
        result1 = integrator.performance_manager.execute_with_timeout(
            code, globals_dict
        )
        first_time = time.time() - start_time

        # Second execution (should be cached)
        start_time = time.time()
        result2 = integrator.performance_manager.execute_with_timeout(
            code, globals_dict
        )
        second_time = time.time() - start_time

        # Cached execution should be faster
        assert second_time < first_time
        assert result1 == result2

    def test_css_integration(self, integrator):
        """Test CSS file integration."""
        with tempfile.TemporaryDirectory() as target_dir:
            integrator.install_templates(target_dir)

            css_dir = Path(target_dir) / "_static/css"
            assert css_dir.exists()
            assert (css_dir / "api-docs.css").exists()

class MockModule:
    def __init__(self):
        self.id = "test.module"

class MockMethod:
    def __init__(self):
        self.name = "test_method"
        self.has_safe_example = True
        self.example_args = '"test_arg"'

class MockAttribute:
    def __init__(self):
        self.name = "test_attr"
```

### End-to-End Validation

```bash
#!/bin/bash
# validate_complete_integration.sh

echo "🚀 Starting complete AutoAPI template integration validation"

# Setup test environment
TEST_DIR="/tmp/pydevelop_docs_test"
rm -rf $TEST_DIR
mkdir -p $TEST_DIR
cd $TEST_DIR

# Create test project structure
mkdir -p test_package
cat > test_package/__init__.py << 'EOF'
"""Test package for AutoAPI template validation."""

__version__ = "1.0.0"
__all__ = ["TestClass", "test_function"]

class TestClass:
    """A test class for AutoAPI template testing."""

    def __init__(self, name: str = "default"):
        """Initialize test class."""
        self.name = name

    def test_method(self, value: int) -> str:
        """Test method with example."""
        return f"Result: {self.name} - {value}"

def test_function(arg: str) -> str:
    """Test function with example."""
    return f"Function result: {arg}"
EOF

# Initialize with Pydvlppy
echo "📝 Initializing documentation with custom templates"
poetry run pydvlppy init --force --use-shared-config

# Verify template installation
echo "🔍 Verifying template installation"
if [ -d "docs/source/_autoapi_templates" ]; then
    echo "✅ AutoAPI templates installed"
    ls -la docs/source/_autoapi_templates/python/
else
    echo "❌ AutoAPI templates missing"
    exit 1
fi

# Build documentation with live examples
echo "🏗️ Building documentation with live examples"
cd docs
poetry run sphinx-build -b html source build -v

# Validate build results
echo "🧪 Validating build results"
if [ -f "build/index.html" ]; then
    echo "✅ Documentation built successfully"
else
    echo "❌ Documentation build failed"
    exit 1
fi

# Check for live example execution
if grep -q "exec-code" build/autoapi/test_package/index.html; then
    echo "✅ Live examples included"
else
    echo "❌ Live examples missing"
fi

# Verify CSS integration
if [ -f "build/_static/css/api-docs.css" ]; then
    echo "✅ Custom CSS integrated"
else
    echo "❌ Custom CSS missing"
fi

# Performance test
echo "⚡ Running performance test"
start_time=$(date +%s)
poetry run sphinx-build -b html source build_perf
end_time=$(date +%s)
build_time=$((end_time - start_time))

echo "📊 Build time: ${build_time}s"
if [ $build_time -lt 30 ]; then
    echo "✅ Performance acceptable"
else
    echo "⚠️ Performance needs optimization"
fi

echo "🎉 Complete integration validation finished"
```

## Deployment Guide

### Production Deployment

1. **Update Pydvlppy Configuration**

```python
# In src/pydevelop_docs/config.py - Add template integration
def get_haive_config(package_name, is_central_hub=False):
    config = {
        # ... existing config ...

        # Enable AutoAPI templates
        "autoapi_template_dir": "_autoapi_templates",
        "autoapi_own_page_level": "module",

        # Code execution extensions
        "extensions": [
            # ... existing extensions ...
            "sphinx_exec_code",
            "sphinx_runpython",
            "sphinxcontrib.programoutput",
            "sphinx_codeautolink",
        ],

        # Security configuration
        "exec_code_allowed_modules": ["haive.*", "pydantic", "typing"],
        "exec_code_timeout": 15,
        "runpython_memory_limit": "128MB",
        "programoutput_use_ansi": True,

        # CSS integration
        "html_css_files": [
            "css/api-docs.css",
            "css/custom.css",
            "css/furo-intense.css",
            "css/live-examples.css"
        ]
    }
    return config
```

2. **Install Template Files**

```bash
# Copy templates to Pydvlppy
cp -r project_docs/extensions/code/templates/* src/pydevelop_docs/templates/

# Copy CSS files
cp -r project_docs/extensions/code/static/* docs/source/_static/
```

3. **Update CLI Integration**

```python
# In src/pydevelop_docs/cli.py - Add template installation
def initialize_project(args):
    # ... existing initialization ...

    # Install AutoAPI templates if requested
    if args.with_live_examples:
        integrator = AutoAPITemplateIntegrator(Path.cwd())
        integrator.install_templates("docs/source")
        print("✅ AutoAPI templates with live examples installed")
```

4. **Testing Integration**

```bash
# Run comprehensive tests
poetry run pytest project_docs/extensions/code/test_template_integration.py

# Validate with test project
cd test-projects/test-haive-template
poetry run pydvlppy init --force --with-live-examples
poetry run pydvlppy build
```

### Documentation Update

Update project documentation to reflect new capabilities:

````markdown
# Pydvlppy v2.0 - Live Documentation

## New Features

- **🔥 Live Code Examples**: AutoAPI templates with executable code
- **🎯 Dynamic Content**: Examples that stay current with your code
- **🛡️ Secure Execution**: Safe code execution with comprehensive restrictions
- **⚡ Performance Optimized**: Caching and parallel execution
- **🎨 Enhanced Styling**: Beautiful CSS integration with Furo theme

## Usage

```bash
# Initialize with live examples
pydvlppy init --with-live-examples

# Build with dynamic content
pydvlppy build
```
````

## Configuration

```python
# Enable all code execution features
exec_code_enabled = True
runpython_enabled = True
programoutput_enabled = True
codeautolink_enabled = True
```

```

This complete implementation transforms Pydvlppy from a static documentation generator into a dynamic, live documentation system where examples are always current, tested, and beautifully presented. The integration of code execution extensions with custom AutoAPI templates creates documentation that developers can trust and rely on for accurate, up-to-date examples.
```
