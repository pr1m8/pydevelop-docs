# sphinx_runpython - Run Python Code Blocks

**Extension**: `sphinx_runpython`
**Purpose**: Execute Python code blocks with enhanced output formatting and variable persistence
**Version**: 1.4.0+
**Priority**: High (Execution category in PyDevelop-Docs)

## Overview

`sphinx_runpython` provides advanced Python code execution capabilities within Sphinx documentation, with sophisticated output formatting, variable persistence across code blocks, and integration with plotting libraries. Unlike `sphinx_exec_code`, it focuses on enhanced output presentation and cross-block state management, making it ideal for tutorial-style documentation and complex AutoAPI examples.

## Core Capabilities

### Enhanced Code Execution

Execute Python with rich output formatting:

```rst
.. runpython::

    from haive.agents.simple import SimpleAgent
    from haive.core.engine.aug_llm import AugLLMConfig

    # Create configuration
    config = AugLLMConfig(
        temperature=0.7,
        model="gpt-4",
        max_tokens=1000
    )

    # Display configuration details
    print("Configuration created:")
    for key, value in config.__dict__.items():
        if not key.startswith('_'):
            print(f"  {key}: {value}")
```

### Persistent Variable Context

Maintain state across multiple code blocks:

```rst
.. runpython::
    :context:

    # First block - create shared objects
    from haive.agents.simple import SimpleAgent
    shared_config = AugLLMConfig()
    agents = []

.. runpython::
    :context:

    # Second block - use shared objects
    for i in range(3):
        agent = SimpleAgent(name=f"agent_{i}", engine=shared_config)
        agents.append(agent)

    print(f"Created {len(agents)} agents")
    for agent in agents:
        print(f"  - {agent.name}")
```

## Advanced Configuration

### Execution Environment

```python
# Core settings
runpython_working_dir = "_runpython_temp"     # Working directory
runpython_timeout = 30                       # Execution timeout
runpython_linenos = True                     # Show line numbers
runpython_output_encoding = "utf-8"          # Output encoding
```

### Output Formatting

```python
# Enhanced output control
runpython_output_limit = 100000              # Max output characters
runpython_stderr_limit = 10000               # Max error output
runpython_format_stdout = True               # Format standard output
runpython_format_stderr = True               # Format error output
runpython_show_return_value = True           # Show return values
```

### Context Management

```python
# Variable persistence
runpython_context_persist = True             # Persist variables
runpython_context_timeout = 3600             # Context lifetime (seconds)
runpython_context_cleanup = True             # Clean up on build end
runpython_context_name = "default"           # Context namespace
```

## Security and Safety

### Execution Sandboxing

```python
# Security restrictions
runpython_allowed_modules = [
    "haive.*",
    "pydantic",
    "typing",
    "datetime",
    "json",
    "re",
    "math",
    "statistics"
]

runpython_forbidden_imports = [
    "os",
    "sys.exit",
    "subprocess",
    "shutil",
    "socket",
    "urllib",
    "requests"
]
```

### Resource Limits

```python
# Performance and safety limits
runpython_memory_limit = "256MB"             # Memory limit per execution
runpython_cpu_limit = 10                     # CPU time limit (seconds)
runpython_max_open_files = 10                # File handle limit
runpython_network_access = False             # Disable network access
```

## AutoAPI Template Integration

### Dynamic Class Exploration

```jinja2
{# _autoapi_templates/python/class.rst #}
{% if obj.methods %}
Interactive Examples
-------------------

.. runpython::
    :context: {{ obj.name|lower }}

    from {{ obj.module.id }} import {{ obj.name }}
    import inspect

    # Create instance for exploration
    {% if obj.has_simple_constructor %}
    instance = {{ obj.name }}()
    {% else %}
    # Complex constructor - show signature instead
    print("Constructor signature:")
    print(f"  {inspect.signature({{ obj.name }})}")
    instance = None
    {% endif %}

    if instance:
        print(f"Created {instance.__class__.__name__} instance")

        # Show instance attributes
        attrs = [attr for attr in dir(instance) if not attr.startswith('_')]
        print(f"Public attributes: {len(attrs)}")
        for attr in attrs[:5]:  # Show first 5
            try:
                value = getattr(instance, attr)
                print(f"  {attr}: {type(value).__name__}")
            except:
                print(f"  {attr}: <property>")

{% for method in obj.public_methods[:3] %}
{{ method.name }} Method
{{ "~" * (method.name|length + 7) }}

.. runpython::
    :context: {{ obj.name|lower }}

    {% if method.has_safe_example %}
    # Execute {{ method.name }} with example parameters
    if instance:
        try:
            {% if method.example_args %}
            result = instance.{{ method.name }}({{ method.example_args }})
            {% else %}
            result = instance.{{ method.name }}()
            {% endif %}

            print(f"Method: {{ method.name }}")
            print(f"Result: {result}")
            print(f"Return type: {type(result).__name__}")

            {% if method.returns_self %}
            print("Method returns self - supports chaining")
            {% endif %}

        except Exception as e:
            print(f"Example execution failed: {e}")
    {% else %}
    # {{ method.name }} - complex method, show signature
    if instance:
        print(f"Method signature: {inspect.signature(instance.{{ method.name }})}")
        print("{{ method.short_description }}")
    {% endif %}

{% endfor %}
{% endif %}
```

### Module-Level Examples

```jinja2
{# _autoapi_templates/python/module.rst #}
{% if obj.functions %}
Function Demonstrations
----------------------

.. runpython::
    :context: {{ obj.name.replace('.', '_') }}

    from {{ obj.id }} import *
    import inspect

    # Available functions
    functions = [{{ obj.functions|map(attribute='name')|join(', ') }}]
    print(f"Module {{ obj.name }} provides {len(functions)} functions:")

    {% for func in obj.functions[:5] %}
    # {{ func.name }} function
    print(f"\\n{{ func.name }}:")
    print(f"  Signature: {inspect.signature({{ func.name }})}")
    {% if func.has_example %}
    try:
        result = {{ func.name }}({{ func.example_call }})
        print(f"  Example result: {result}")
    except Exception as e:
        print(f"  Example error: {e}")
    {% endif %}
    {% endfor %}
{% endif %}
```

## Error Handling and Debugging

### Comprehensive Error Display

```rst
.. runpython::
    :show-traceback:      # Show full traceback on errors
    :ignore-errors:       # Continue build even if this fails

    # Code that might fail
    from optional_module import missing_function
    result = missing_function()
```

### Debug Mode

```python
# Enhanced debugging
runpython_debug = True                       # Enable debug output
runpython_show_execution_time = True         # Show execution timing
runpython_log_context_changes = True        # Log variable changes
runpython_trace_imports = True              # Trace import statements
```

### Error Recovery

```python
# Error handling strategies
runpython_error_format = "detailed"          # Error display format
runpython_continue_on_error = False          # Stop vs continue on errors
runpython_error_context_lines = 3           # Lines around error
runpython_collect_errors = True             # Collect all errors for summary
```

## Performance Optimization

### Execution Caching

```python
# Cache execution results
runpython_cache_enabled = True              # Enable result caching
runpython_cache_dir = "_runpython_cache"    # Cache directory
runpython_cache_key_includes = [            # Cache key components
    "source_hash",
    "python_version",
    "dependencies"
]
```

### Parallel Processing

```python
# Concurrent execution
runpython_parallel_contexts = True          # Parallel context execution
runpython_max_workers = 2                   # Worker process limit
runpython_shared_context_limit = 5          # Max shared contexts
```

## Advanced Features

### Plot Integration

```rst
.. runpython::
    :show-plots:      # Display matplotlib/plotly plots

    import matplotlib.pyplot as plt
    import numpy as np

    # Generate sample data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Create plot
    plt.figure(figsize=(8, 4))
    plt.plot(x, y, label='sin(x)')
    plt.title('Example Plot')
    plt.legend()
    plt.grid(True)

    # Plot will be automatically included in documentation
```

### Rich Output Formatting

```rst
.. runpython::
    :output-format: rich    # Use rich library for formatting

    from rich.console import Console
    from rich.table import Table

    console = Console()

    # Create formatted table
    table = Table(title="Agent Comparison")
    table.add_column("Agent Type", style="cyan")
    table.add_column("Features", style="green")
    table.add_column("Use Case", style="yellow")

    table.add_row("SimpleAgent", "Basic LLM", "Simple tasks")
    table.add_row("ReactAgent", "Tool usage", "Complex reasoning")
    table.add_row("MultiAgent", "Coordination", "Workflows")

    console.print(table)
```

## Testing Integration

### Example Validation

```rst
.. runpython::
    :test: true           # Mark as test - fail build if error
    :test-timeout: 10     # Test-specific timeout

    # Validate all examples work
    from haive.agents.simple import SimpleAgent
    from haive.core.engine.aug_llm import AugLLMConfig

    # Test configuration creation
    config = AugLLMConfig()
    assert config is not None

    # Test agent creation
    agent = SimpleAgent(name="test", engine=config)
    assert agent.name == "test"
    assert agent.engine is config

    print("✓ All validation tests passed")
```

### Continuous Integration

```python
# CI/CD configuration
runpython_ci_mode = True                     # Enable CI-specific behavior
runpython_ci_timeout = 5                     # Shorter timeout in CI
runpython_ci_skip_slow = True                # Skip slow examples in CI
runpython_ci_error_summary = True           # Collect error summary
```

## Integration with Other Extensions

### Combined with AutoAPI

```rst
.. runpython::
    :autoapi-inject:     # Inject into AutoAPI templates

    # This code runs when AutoAPI processes classes
    current_class = autoapi_current_object
    print(f"Processing: {current_class.name}")
```

### With Code Linking

```rst
.. runpython::
    :codeautolink:       # Enable automatic code linking

    from haive.agents.simple import SimpleAgent  # Will be linked
    agent = SimpleAgent()  # Links to SimpleAgent docs
```

## Implementation Status in PyDevelop-Docs

### Current State

- ✅ **Available**: Listed in extensions configuration
- ⚠️ **Testing**: Currently in testing focus phase
- 📋 **TODO**: Security hardening and AutoAPI integration
- 🔄 **Priority**: High for Issue #6 implementation

### Integration Plan

1. **Phase 1**: Basic configuration with security restrictions
2. **Phase 2**: AutoAPI template integration for live examples
3. **Phase 3**: Advanced output formatting (plots, tables)
4. **Phase 4**: Performance optimization and caching

## Best Practices

### Security Configuration

```python
# Always configure security first
runpython_allowed_modules = ["haive.*", "pydantic", "typing"]
runpython_memory_limit = "128MB"
runpython_timeout = 15
runpython_network_access = False
```

### Performance Guidelines

```python
# Optimize for documentation builds
runpython_cache_enabled = True
runpython_parallel_contexts = True
runpython_output_limit = 50000  # Prevent excessive output
```

### Content Strategy

```rst
# Write examples that:
# 1. Build on each other using :context:
# 2. Show progressive complexity
# 3. Include error handling demonstrations
# 4. Validate key functionality
```

This extension provides the most sophisticated Python execution environment for documentation, with advanced features like variable persistence, rich output formatting, and comprehensive error handling that make it ideal for creating tutorial-style documentation and interactive API examples.
