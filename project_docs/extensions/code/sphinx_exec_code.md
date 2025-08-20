# sphinx_exec_code - Execute Code in Documentation

**Extension**: `sphinx_exec_code`
**Purpose**: Execute Python code blocks during documentation build and include output
**Version**: 0.5.0+
**Priority**: High (Execution category in PyDevelop-Docs)

## Overview

`sphinx_exec_code` enables live code execution within Sphinx documentation, allowing for dynamic examples that are always up-to-date. This extension is crucial for AutoAPI integration as it can generate real-time examples from actual API objects, ensuring documentation examples never become stale or outdated.

## Core Capabilities

### Live Code Execution

Execute Python code during documentation build:

```rst
.. exec-code:: python

    from haive.agents.simple import SimpleAgent
    from haive.core.engine.aug_llm import AugLLMConfig

    # This code runs during documentation build
    config = AugLLMConfig(temperature=0.7)
    agent = SimpleAgent(name="demo", engine=config)

    print(f"Agent created: {agent.name}")
    print(f"Engine type: {type(agent.engine).__name__}")
```

### Dynamic Output Inclusion

Capture and display execution results:

```rst
.. exec-code:: python
    :hide-code:      # Hide the code, show only output

    import sys
    print(f"Python version: {sys.version}")
    print(f"Available classes: {[cls.__name__ for cls in [SimpleAgent, ReactAgent]]}")
```

## Security Architecture

### Sandboxed Execution

```python
# Safe execution environment
exec_code_working_dir = "docs/_exec_temp"     # Isolated working directory
exec_code_stdout_limit = 1000000             # Limit output size
exec_code_timeout = 30                       # Execution timeout in seconds
exec_code_allowed_modules = [                # Whitelist modules
    "haive.*",
    "pydantic",
    "typing",
    "datetime"
]
```

### Security Restrictions

```python
# Prevent dangerous operations
exec_code_forbidden_imports = [
    "os",                    # System operations
    "subprocess",           # Process execution
    "shutil",              # File operations
    "socket",              # Network access
    "__import__",          # Dynamic imports
    "eval",                # Code evaluation
    "exec"                 # Code execution
]

# Restricted built-ins
exec_code_safe_builtins = [
    "print", "len", "str", "int", "float", "bool", "list", "dict", "tuple", "set"
]
```

## Configuration Options

### Basic Settings

```python
# Core execution settings
exec_code_working_dir = "_exec_code_temp"     # Temporary directory
exec_code_output_limit = 50000               # Maximum output characters
exec_code_linenos = True                     # Show line numbers
exec_code_show_source = True                 # Show source code by default
```

### Advanced Configuration

```python
# Performance and safety
exec_code_timeout = 15                       # Execution timeout (seconds)
exec_code_memory_limit = "128MB"             # Memory limit per execution
exec_code_max_processes = 1                  # Concurrent execution limit
exec_code_cleanup_on_exit = True             # Clean temp files

# Error handling
exec_code_ignore_errors = False              # Stop build on code errors
exec_code_error_format = "short"             # Error display format
exec_code_show_traceback = True              # Include full tracebacks
```

## AutoAPI Template Integration

### Dynamic API Examples

Generate live examples from API objects:

```jinja2
{# _autoapi_templates/python/class.rst #}
{% if obj.methods %}
Examples
--------

{% for method in obj.public_methods[:3] %}
.. exec-code:: python
    :caption: {{ method.name }} Example

    from {{ obj.module.id }} import {{ obj.name }}

    # Create instance with safe defaults
    instance = {{ obj.name }}()

    # Execute method and show result
    try:
        result = instance.{{ method.name }}({{ method.safe_example_args }})
        print(f"Result: {result}")
        print(f"Type: {type(result).__name__}")
    except Exception as e:
        print(f"Example error: {e}")

{% endfor %}
{% endif %}
```

### Live Property Demonstration

```jinja2
{# Show class properties and attributes dynamically #}
{% if obj.attributes %}
.. exec-code:: python
    :caption: {{ obj.name }} Properties

    from {{ obj.module.id }} import {{ obj.name }}

    # Inspect class attributes
    instance = {{ obj.name }}()

    {% for attr in obj.attributes %}
    {% if not attr.name.startswith('_') %}
    try:
        value = getattr(instance, '{{ attr.name }}')
        print(f"{{ attr.name }}: {value} (type: {type(value).__name__})")
    except:
        print(f"{{ attr.name }}: <property>")
    {% endif %}
    {% endfor %}
{% endif %}
```

## Performance Optimization

### Build Time Management

```python
# Cache execution results
exec_code_cache_enabled = True               # Enable result caching
exec_code_cache_dir = "_exec_cache"          # Cache directory
exec_code_cache_timeout = 3600               # Cache validity (seconds)

# Parallel execution
exec_code_parallel = True                    # Execute blocks in parallel
exec_code_worker_count = 2                   # Number of worker processes
```

### Selective Execution

```python
# Skip execution in specific conditions
exec_code_skip_on_ci = True                  # Skip in CI environments
exec_code_skip_patterns = [                  # Skip blocks matching patterns
    "slow_operation",
    "network_request",
    "file_system_access"
]
```

## Error Handling Strategies

### Graceful Degradation

```rst
.. exec-code:: python
    :ignore-errors:    # Continue build even if this fails
    :fallback-text: "Example execution failed - see manual examples below"

    # This might fail in some environments
    from optional_dependency import special_feature
    result = special_feature.complex_operation()
```

### Error Recovery

```python
# Error handling configuration
exec_code_error_fallback = "hide"            # hide|show|replace
exec_code_default_error_text = "Code execution failed"
exec_code_log_errors = True                  # Log errors for debugging

# Custom error handling
def exec_code_error_handler(error, code_block):
    """Custom error handling function."""
    if "ImportError" in str(error):
        return "Optional dependency not available"
    return f"Execution failed: {error}"
```

## AutoAPI Live Documentation Pattern

### Complete Integration Example

```jinja2
{# _autoapi_templates/python/module.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{{ obj.docstring }}

{% if obj.classes %}
Live Examples
-------------

{% for cls in obj.classes %}
{{ cls.name }} Usage
{{ "~" * (cls.name|length + 6) }}

.. exec-code:: python
    :linenos:
    :caption: Interactive {{ cls.name }} Example

    from {{ obj.id }} import {{ cls.name }}
    import inspect

    # Create instance
    {% if cls.constructor_args %}
    instance = {{ cls.name }}(
        {% for arg in cls.safe_constructor_args %}
        {{ arg.name }}={{ arg.example_value }},
        {% endfor %}
    )
    {% else %}
    instance = {{ cls.name }}()
    {% endif %}

    # Show class information
    print(f"Class: {instance.__class__.__name__}")
    print(f"Module: {instance.__class__.__module__}")

    # Show available methods
    methods = [m for m in dir(instance) if not m.startswith('_')]
    print(f"Public methods: {methods[:5]}...")  # Limit output

    {% if cls.public_methods %}
    # Demonstrate key methods
    {% for method in cls.public_methods[:2] %}
    print(f"\\n{{ method.name }} method:")
    try:
        {% if method.safe_example_call %}
        result = instance.{{ method.safe_example_call }}
        print(f"  Result: {result}")
        {% else %}
        print(f"  Signature: {inspect.signature(instance.{{ method.name }})}")
        {% endif %}
    except Exception as e:
        print(f"  Example error: {e}")
    {% endfor %}
    {% endif %}

{% endfor %}
{% endif %}
```

## Testing and Validation

### Code Example Testing

```rst
.. exec-code:: python
    :test: true       # Mark as test - fail build if error
    :timeout: 5       # Quick timeout for tests

    # Validate that examples work
    from haive.agents.simple import SimpleAgent
    from haive.core.engine.aug_llm import AugLLMConfig

    # Test basic instantiation
    config = AugLLMConfig()
    agent = SimpleAgent(name="test", engine=config)

    assert agent.name == "test"
    assert agent.engine is not None
    print("✓ Basic instantiation test passed")
```

### Integration Testing

```python
# In sphinx configuration
exec_code_test_examples = True               # Test all examples during build
exec_code_test_timeout = 10                  # Test timeout
exec_code_fail_on_test_error = True          # Fail build on test errors
```

## Advanced Features

### Code Block Variants

```rst
.. exec-code:: python
    :hide-output:     # Show code, hide output
    :hide-code:       # Show output, hide code
    :linenos:         # Show line numbers
    :emphasize-lines: 2,3  # Highlight specific lines
    :filename: example.py  # Show as file
```

### Variable Persistence

```rst
.. exec-code:: python
    :context: shared   # Share variables between blocks

    # This variable persists to next block
    shared_config = AugLLMConfig(temperature=0.5)

.. exec-code:: python
    :context: shared

    # Can use shared_config from previous block
    agent = SimpleAgent(engine=shared_config)
    print(f"Agent with shared config: {agent.name}")
```

## Implementation Status in PyDevelop-Docs

### Current State

- ✅ **Available**: Listed in extensions but testing focus
- ⚠️ **Disabled**: Currently commented out in conf.py for testing
- 📋 **TODO**: Security configuration and AutoAPI integration
- 🔄 **Priority**: High for Issue #6 (AutoAPI templates)

### Integration Roadmap

1. **Phase 1**: Enable with security restrictions
2. **Phase 2**: Create AutoAPI template examples
3. **Phase 3**: Add comprehensive error handling
4. **Phase 4**: Performance optimization and caching

## Best Practices

### Security First

```python
# Always configure security restrictions
exec_code_allowed_modules = ["haive.*", "pydantic", "typing"]
exec_code_timeout = 15
exec_code_memory_limit = "64MB"
```

### Performance Considerations

```python
# Optimize for build speed
exec_code_cache_enabled = True
exec_code_parallel = True
exec_code_skip_on_ci = False  # Run in CI for validation
```

### Example Quality

```rst
# Write examples that:
# 1. Are fast to execute (<1 second)
# 2. Don't require external resources
# 3. Show realistic usage patterns
# 4. Include error handling where appropriate
```

This extension enables truly live documentation where examples are always current and tested, making it invaluable for maintaining high-quality API documentation that developers can trust.
