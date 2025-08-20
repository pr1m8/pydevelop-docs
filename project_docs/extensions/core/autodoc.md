# sphinx.ext.autodoc - Automatic Documentation Generation

**Extension**: `sphinx.ext.autodoc`  
**Priority**: Core Foundation (Position 1 in extensions list)  
**Official Documentation**: [sphinx.ext.autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)  
**Status in PyDevelop-Docs**: ✅ Implemented with comprehensive configuration

## Overview

`sphinx.ext.autodoc` is the cornerstone of automatic Python documentation generation in Sphinx. It automatically extracts docstrings from Python modules, classes, functions, and methods, converting them into beautiful documentation pages. This extension forms the foundation upon which all other API documentation tools build.

## Core Capabilities

### 1. Automatic Code Extraction

- **Module Documentation**: Extracts module-level docstrings and structure
- **Class Documentation**: Documents classes with inheritance, methods, and attributes
- **Function Documentation**: Captures function signatures, parameters, and return values
- **Method Documentation**: Handles instance and class methods with proper context
- **Attribute Documentation**: Documents class and module attributes with type hints

### 2. Intelligent Filtering

- **Member Selection**: Choose which members to document (public, private, special)
- **Inheritance Handling**: Control how inherited members are displayed
- **Import Filtering**: Decide whether to include imported members
- **Signature Processing**: Enhanced signature display with type hints

### 3. Docstring Processing

- **Multiple Formats**: Supports reStructuredText, Google, and NumPy docstring styles
- **Cross-References**: Automatic linking between documented elements
- **Type Annotation**: Integration with type hints for enhanced documentation

## Configuration in PyDevelop-Docs

### Current Implementation

```python
# In config.py - autodoc is the first core extension
extensions = [
    "sphinx.ext.autodoc",  # Foundation for all automatic documentation
    "sphinx.ext.napoleon", # Extends autodoc with Google/NumPy style support
    # ... other extensions
]

# Autodoc-specific configuration
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
```

### Enhanced Configuration Options

```python
# Advanced autodoc configuration for PyDevelop-Docs
autodoc_typehints = "description"  # Show type hints in descriptions
autodoc_typehints_description_target = "documented"
autodoc_typehints_format = "short"
autodoc_preserve_defaults = True  # Keep default parameter values
autodoc_class_signature = "separated"  # Separate class and __init__ signatures
autodoc_inherit_docstrings = True  # Inherit docstrings from parent classes
autodoc_mock_imports = []  # Mock imports for modules that can't be imported
```

## Directives and Usage

### Basic Directives

```rst
.. automodule:: mymodule
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: MyClass
   :members:
   :inherited-members:
   :special-members: __init__

.. autofunction:: my_function

.. automethod:: MyClass.my_method

.. autoattribute:: MyClass.my_attribute
```

### Advanced Usage Patterns

```rst
.. automodule:: haive.core.engine
   :members:
   :undoc-members:
   :show-inheritance:
   :synopsis: Core engine components for agent execution
   :platform: Any

.. autoclass:: haive.core.engine.AugLLMConfig
   :members:
   :inherited-members:
   :special-members: __init__, __call__
   :exclude-members: __weakref__
```

## Template Integration Opportunities

### 1. Custom Object Templates

Create enhanced templates for different object types:

```jinja2
{# _autoapi_templates/python/class.rst #}
{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% endif %}

{% if obj.inheritance %}
**Inheritance Hierarchy:**

.. inheritance-diagram:: {{ obj.name }}
   :parts: 1
{% endif %}

{% for item in obj.children %}
{% if item.type == "method" %}
{{ item.render()|indent(0) }}
{% endif %}
{% endfor %}
```

### 2. Enhanced Module Templates

```jinja2
{# _autoapi_templates/python/module.rst #}
{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% endif %}

{% if obj.classes %}
Classes
-------

{% for class in obj.classes %}
.. autoclass:: {{ class.id }}
   :members:
   :show-inheritance:
{% endfor %}
{% endif %}

{% if obj.functions %}
Functions
---------

{% for function in obj.functions %}
.. autofunction:: {{ function.id }}
{% endfor %}
{% endif %}
```

### 3. AutoAPI Integration

Autodoc works seamlessly with AutoAPI through the hierarchical configuration:

```python
# AutoAPI configuration that leverages autodoc
autoapi_options = [
    'members',        # Use autodoc to document all members
    'undoc-members',  # Include undocumented members
    'show-inheritance', # Show class inheritance
    'special-members', # Include special methods like __init__
]
```

## Best Practices for PyDevelop-Docs

### 1. Docstring Standards

```python
def process_agent_response(
    agent_response: str,
    validation_config: ValidationConfig
) -> ProcessedResponse:
    """Process agent response with comprehensive validation.

    This function demonstrates proper docstring format that autodoc
    will extract and format beautifully.

    Args:
        agent_response: Raw response from the agent execution
        validation_config: Configuration object for validation rules

    Returns:
        ProcessedResponse: Validated and processed response object

    Raises:
        ValidationError: If response fails validation checks
        ProcessingError: If processing encounters errors

    Example:
        >>> config = ValidationConfig(strict=True)
        >>> response = process_agent_response("Hello", config)
        >>> response.validated
        True
    """
```

### 2. Type Annotation Support

```python
from typing import List, Dict, Optional, Union

class AgentConfig:
    """Agent configuration with full type annotation support.

    Autodoc will automatically extract and display type information
    from annotations, creating rich API documentation.
    """

    def __init__(
        self,
        name: str,
        tools: List[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize agent configuration."""
```

### 3. Cross-Reference Integration

```python
class ReactAgent:
    """React-style agent for reasoning workflows.

    See Also:
        :class:`~haive.core.engine.AugLLMConfig`: Engine configuration
        :func:`~haive.tools.calculator`: Built-in calculator tool
        :doc:`/guides/agent-creation`: Agent creation guide
    """
```

## Enhancement Opportunities

### 1. Custom Member Filters

```python
def autodoc_skip_member(app, what, name, obj, skip, options):
    """Custom filtering for autodoc member inclusion."""
    # Skip test methods
    if name.startswith('test_'):
        return True

    # Skip private attributes but keep special methods
    if name.startswith('_') and not name.startswith('__'):
        return True

    return skip

def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip_member)
```

### 2. Enhanced Signature Processing

```python
def autodoc_process_signature(app, what, name, obj, options, signature, return_annotation):
    """Enhance signature display with custom formatting."""
    if signature:
        # Clean up long signatures
        if len(signature) > 80:
            signature = signature.replace(', ', ',\n    ')

    return signature, return_annotation
```

### 3. Documentation Templates

```python
# Custom autodoc templates for consistent formatting
autodoc_default_options = {
    'members': True,
    'member-order': 'groupwise',  # Group by type (methods, attributes, etc.)
    'special-members': '__init__, __call__, __enter__, __exit__',
    'undoc-members': True,
    'show-inheritance': True,
    'inherited-members': True,
    'exclude-members': '__weakref__, __dict__, __module__'
}
```

## Current Implementation Status

### ✅ Working Features

- [x] **Basic autodoc extraction** - Fully functional
- [x] **Type hint integration** - Works with `sphinx_autodoc_typehints`
- [x] **Napoleon compatibility** - Google/NumPy docstrings supported
- [x] **AutoAPI integration** - Seamless cooperation
- [x] **Cross-references** - Links work between documented elements

### 🔄 Enhancement Opportunities

- [ ] **Custom member filters** - Better control over what gets documented
- [ ] **Enhanced templates** - More sophisticated formatting
- [ ] **Improved signature display** - Better handling of complex signatures
- [ ] **Documentation quality metrics** - Track documentation coverage
- [ ] **Interactive examples** - Integration with execution extensions

### 📋 Template Integration Tasks

1. **Create custom autodoc templates** for consistent object documentation
2. **Enhance AutoAPI templates** to better leverage autodoc capabilities
3. **Add documentation quality filters** to improve output
4. **Implement signature enhancement** for better readability

## Code Examples

### Basic Usage in RST

```rst
API Reference
=============

Core Engine
-----------

.. automodule:: haive.core.engine
   :members:
   :undoc-members:
   :show-inheritance:

Agent Types
-----------

.. autoclass:: haive.agents.SimpleAgent
   :members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: haive.agents.ReactAgent
   :members:
   :inherited-members:
   :show-inheritance:
```

### Integration with AutoAPI

```python
# In autoapi template
{% for class in obj.classes %}
.. autoclass:: {{ class.id }}
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   {% if class.docstring %}
   {{ class.docstring|prepare_docstring|indent(3) }}
   {% endif %}
{% endfor %}
```

## Performance Considerations

### Import Time Optimization

```python
# Optimize imports for faster documentation builds
autodoc_mock_imports = [
    'expensive_module',
    'optional_dependency'
]

# Use type checking imports
autodoc_typehints_format = "short"
autodoc_preserve_defaults = False  # For faster builds
```

### Build Time Improvements

```python
# Skip expensive inheritance diagrams during development
autodoc_inherit_docstrings = False  # Set to True for production
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Use `autodoc_mock_imports` for problematic modules
2. **Missing Docstrings**: Enable `undoc-members` but filter appropriately
3. **Long Signatures**: Implement custom signature processing
4. **Cross-Reference Failures**: Ensure proper `intersphinx_mapping`

### Debug Configuration

```python
# Enable autodoc debugging
autodoc_warningiserror = False  # Don't fail on warnings during development
keep_warnings = True  # Show all warnings for debugging
```

## Integration with Issue #6

For AutoAPI template customization (Issue #6), autodoc provides the foundation:

1. **Template Variables**: Access to all autodoc-extracted information
2. **Formatting Control**: Custom rendering of docstrings and signatures
3. **Member Selection**: Fine-grained control over what gets documented
4. **Cross-Reference Support**: Rich linking between documentation elements

The key is leveraging autodoc's extracted data within AutoAPI templates for consistent, beautiful documentation output.
