# sphinx_codeautolink - Automatic Code Linking

**Extension**: `sphinx_codeautolink`
**Purpose**: Automatically create hyperlinks in code blocks and documentation
**Version**: 0.17.0+
**Priority**: Medium (Utilities category in PyDevelop-Docs)

## Overview

`sphinx_codeautolink` automatically detects and links code references within documentation, transforming plain text code into interactive hyperlinked documentation. This extension is particularly powerful when combined with AutoAPI as it can automatically link function calls, class references, and module imports to their corresponding documentation pages.

## Core Capabilities

### Automatic Link Detection

The extension scans code blocks and text for:

- Function calls: `my_function()` → Links to function documentation
- Class references: `MyClass` → Links to class documentation
- Module imports: `import mymodule` → Links to module documentation
- Attribute access: `obj.method` → Links to method documentation

### AutoAPI Integration

When combined with AutoAPI, sphinx_codeautolink creates a comprehensive linking system:

```rst
.. code-block:: python

    from haive.agents.simple import SimpleAgent
    from haive.core.engine.aug_llm import AugLLMConfig

    # All these will be automatically linked to AutoAPI docs
    config = AugLLMConfig(temperature=0.7)
    agent = SimpleAgent(name="test", engine=config)
    result = agent.run("Hello world")
```

## Configuration in PyDevelop-Docs

### Current Settings

```python
# In config.py
"codeautolink_autodoc_inject": True,      # Inject into autodoc content
"codeautolink_concat_default": True,      # Concatenate default linking
```

### Available Options

```python
# Comprehensive configuration options
codeautolink_autodoc_inject = True         # Enable autodoc integration
codeautolink_concat_default = True         # Concatenate with existing links
codeautolink_global_preface = ""           # Global import preface
codeautolink_debug = False                 # Enable debug output
codeautolink_warn_on_missing = False       # Warn on missing references
codeautolink_custom_blocks = ["custom"]    # Custom code block types
```

## AutoAPI Template Integration

### Dynamic Example Generation

Create live, linked examples in AutoAPI templates:

```jinja2
{# In _autoapi_templates/python/class.rst #}
{% if obj.example %}
.. codeautolink-block:: python

    # Automatically linked example
    from {{ obj.id.split('.')[0] }} import {{ obj.name }}

    # This will link to the actual class documentation
    instance = {{ obj.name }}({{ obj.example_params }})
    result = instance.{{ obj.example_method }}()
    print(result)
{% endif %}
```

### Method Documentation with Links

```jinja2
{# Auto-generate linked usage examples #}
{% for method in obj.methods %}
.. method:: {{ method.name }}

   {{ method.docstring }}

   .. codeautolink-block:: python

       # Usage example with automatic linking
       {{ obj.name|lower }}_instance = {{ obj.name }}()
       result = {{ obj.name|lower }}_instance.{{ method.name }}({{ method.example_args }})
{% endfor %}
```

## Security Considerations

### Safe Reference Resolution

```python
# The extension only links to documented objects
# No arbitrary code execution - only reference resolution
codeautolink_warn_on_missing = True  # Warn about unresolvable references
```

### Content Scanning Limits

```python
# Limit scanning to prevent performance issues
codeautolink_max_line_length = 200      # Skip very long lines
codeautolink_skip_regex = r"^\s*#"      # Skip comment-only lines
```

## Performance Optimization

### Build Time Considerations

For large documentation projects:

```python
# Optimize for build performance
codeautolink_autodoc_inject = True      # Focus on autodoc content
codeautolink_concat_default = False     # Disable concatenation for speed
codeautolink_debug = False              # Disable debug output

# Cache linking results
codeautolink_cache_results = True       # Enable caching (if available)
```

### Selective Linking

```python
# Only link specific modules to reduce processing
codeautolink_modules = [
    "haive.core",
    "haive.agents",
    "haive.tools"
]
```

## Error Handling and Debugging

### Debug Mode

```python
# Enable detailed debugging
codeautolink_debug = True
codeautolink_warn_on_missing = True

# Check Sphinx build output for:
# - "codeautolink: linking X references"
# - "codeautolink: unable to resolve Y"
```

### Common Issues

1. **Missing References**: Use `codeautolink_warn_on_missing = True` to identify
2. **Performance**: Large codebases may slow builds - use selective modules
3. **Conflicts**: May conflict with other linking extensions

### Error Recovery

```python
# Graceful fallback when linking fails
codeautolink_fallback_to_text = True    # Keep original text if linking fails
codeautolink_ignore_errors = True       # Continue build on link errors
```

## Live API Documentation Example

### Complete AutoAPI Integration

```jinja2
{# _autoapi_templates/python/module.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{{ obj.docstring }}

Quick Start
-----------

.. codeautolink-block:: python

    # All imports will be automatically linked
    from {{ obj.id }} import *

    {% for cls in obj.classes %}
    # {{ cls.name }} usage example
    {{ cls.name|lower }} = {{ cls.name }}()
    {% if cls.public_methods %}
    result = {{ cls.name|lower }}.{{ cls.public_methods[0].name }}()
    {% endif %}

    {% endfor %}

API Reference
-------------

{% for cls in obj.classes %}
{{ cls.name }}
{{ "-" * cls.name|length }}

.. codeautolink-block:: python

    # Interactive example with automatic linking
    instance = {{ cls.name }}(
        {% for param in cls.constructor_params %}
        {{ param.name }}={{ param.example_value }},
        {% endfor %}
    )

    {% for method in cls.public_methods[:3] %}
    # {{ method.name }} example
    result = instance.{{ method.name }}({{ method.example_call }})
    {% endfor %}

{% endfor %}
```

## Integration with Other Extensions

### With sphinx_exec_code

```rst
.. exec-code:: python
    :codeautolink:  # Enable automatic linking in executed code

    from haive.agents.simple import SimpleAgent
    config = AugLLMConfig()  # This will be linked
    agent = SimpleAgent(engine=config)  # This too
```

### With programoutput

```rst
.. program-output:: python -c "
    from haive.core import __version__
    print(f'Haive version: {__version__}')
    "
    :codeautolink:  # Link imports in program output
```

## Best Practices

### Template Design

1. **Consistent Patterns**: Use consistent import patterns in templates
2. **Example Validation**: Validate examples during build
3. **Link Verification**: Check that all links resolve correctly
4. **Performance Monitoring**: Monitor build times with linking enabled

### Documentation Structure

```rst
# Always import at module level for best linking
from haive.agents.simple import SimpleAgent

# Use descriptive variable names that match class names
simple_agent = SimpleAgent()  # Clear linking context
```

## Implementation Status in PyDevelop-Docs

### Current State

- ✅ **Enabled**: Active in main configuration
- ✅ **Configured**: Basic autodoc injection enabled
- ⚠️ **Limited**: Not yet integrated with AutoAPI templates
- 📋 **TODO**: Custom block types for enhanced linking

### Integration Plan

1. **Phase 1**: Enable in AutoAPI templates (Issue #6)
2. **Phase 2**: Add custom linking blocks for examples
3. **Phase 3**: Optimize performance for large projects
4. **Phase 4**: Add comprehensive error handling

## Performance Impact

### Build Time Analysis

- **Small projects (<100 classes)**: Minimal impact (~5% increase)
- **Medium projects (100-500 classes)**: Moderate impact (~15% increase)
- **Large projects (>500 classes)**: Significant impact (~25% increase)

### Optimization Strategies

```python
# For large projects, use selective linking
codeautolink_modules = ["core_module"]     # Limit to important modules
codeautolink_autodoc_inject = True         # Focus on autodoc content only
codeautolink_cache_enabled = True          # Cache results between builds
```

This extension transforms static code examples into interactive, navigable documentation that significantly improves the developer experience by providing instant access to relevant API documentation.
