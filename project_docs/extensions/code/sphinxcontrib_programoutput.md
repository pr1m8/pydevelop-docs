# sphinxcontrib.programoutput - Include Program Output

**Extension**: `sphinxcontrib.programoutput`
**Package**: `sphinxcontrib-programoutput`
**Purpose**: Execute external programs and include their output in documentation
**Version**: 0.18+
**Priority**: High (Execution category in PyDevelop-Docs)

## Overview

`sphinxcontrib.programoutput` enables execution of external programs, shell commands, and scripts during documentation build, capturing and formatting their output. This extension is essential for creating documentation that includes real command-line examples, CLI tool demonstrations, and system integration examples, particularly valuable for showing actual usage of PyDevelop-Docs itself.

## Core Capabilities

### Command Execution

Execute any command and include output:

```rst
.. program-output:: python --version

.. program-output:: ls -la /path/to/project

.. program-output:: poetry run pydvlp-docs --help
```

### Script Execution

Run Python scripts and capture output:

```rst
.. program-output:: python -c "
    from haive.agents.simple import SimpleAgent
    print('SimpleAgent available')
    print(f'Module: {SimpleAgent.__module__}')
    "
```

### Enhanced Output Formatting

Format output with syntax highlighting:

```rst
.. program-output:: python -c "import json; print(json.dumps({'status': 'success', 'agents': ['simple', 'react']}, indent=2))"
    :language: json
    :linenos:
```

## Configuration in PyDevelop-Docs

### Current Settings

```python
# In config.py
"programoutput_use_ansi": True,              # Enable ANSI color support
```

### Comprehensive Configuration

```python
# Complete programoutput settings
programoutput_use_ansi = True                # ANSI escape sequence support
programoutput_prompt_template = "$ {command}"  # Command prompt format
programoutput_include_stderr = False         # Include stderr in output
programoutput_cache_timeout = 3600           # Cache results for 1 hour
programoutput_working_directory = None       # Use current directory
programoutput_env = None                     # Environment variables
```

## Security Considerations

### Command Restrictions

```python
# Security configuration
programoutput_allowed_commands = [
    "python",
    "poetry",
    "pip",
    "ls",
    "cat",
    "head",
    "tail",
    "grep",
    "find"
]

programoutput_forbidden_commands = [
    "rm",
    "rmdir",
    "del",
    "format",
    "sudo",
    "su",
    "chmod",
    "chown",
    "wget",
    "curl"
]
```

### Safe Environment

```python
# Isolated execution environment
programoutput_working_dir = "_program_temp"   # Isolated directory
programoutput_timeout = 30                   # Execution timeout
programoutput_env_whitelist = [              # Environment variable whitelist
    "PATH",
    "PYTHONPATH",
    "HOME",
    "USER"
]
```

## AutoAPI Template Integration

### CLI Tool Documentation

```jinja2
{# _autoapi_templates/python/module.rst #}
{% if obj.name == "cli" %}
Command Line Usage
-----------------

.. program-output:: python -m {{ obj.id }} --help
    :caption: CLI Help Output

{% if obj.has_main_function %}
Example Commands
~~~~~~~~~~~~~~~

.. program-output:: python -m {{ obj.id }} init --help
    :caption: Init Command Help

.. program-output:: python -m {{ obj.id }} build --help
    :caption: Build Command Help
{% endif %}
{% endif %}
```

### Live Tool Demonstrations

```jinja2
{# Show actual tool usage #}
{% if obj.is_executable_module %}
Basic Usage
----------

.. program-output:: python -c "
    import sys
    sys.path.insert(0, '.')
    from {{ obj.id }} import main

    # Show help
    try:
        main(['--help'])
    except SystemExit:
        pass
    "
    :caption: {{ obj.name }} Help Output

Example Execution
~~~~~~~~~~~~~~~~

.. program-output:: python -c "
    from {{ obj.id }} import {{ obj.main_function }}

    # Run with example parameters
    result = {{ obj.main_function }}({{ obj.example_args }})
    print(f'Result: {result}')
    "
    :caption: Example Execution
{% endif %}
```

### Package Information Display

```jinja2
{# Show package metadata and structure #}
Package Information
------------------

.. program-output:: python -c "
    import {{ obj.id }}
    import pkg_resources

    try:
        dist = pkg_resources.get_distribution('{{ obj.package_name }}')
        print(f'Version: {dist.version}')
        print(f'Location: {dist.location}')
    except:
        print('Package not installed via pip')

    # Show module info
    print(f'Module file: {{{ obj.id }}.__file__}')
    if hasattr({{ obj.id }}, '__version__'):
        print(f'Module version: {{{ obj.id }}.__version__}')
    "
    :caption: Package Metadata
```

## Advanced Usage Patterns

### Multi-Command Workflows

```rst
.. program-output:: bash -c "
    # Initialize documentation
    cd /tmp/test-project
    poetry run pydvlp-docs init --force

    # Build documentation
    poetry run pydvlp-docs build

    # Show results
    ls -la docs/build/
    "
    :caption: Complete Documentation Workflow
```

### Environment Testing

```rst
.. program-output:: python -c "
    import sys
    import os

    print('Python Environment:')
    print(f'  Version: {sys.version}')
    print(f'  Path: {sys.executable}')
    print(f'  Platform: {sys.platform}')

    print('\\nKey Packages:')
    try:
        import sphinx
        print(f'  Sphinx: {sphinx.__version__}')
    except ImportError:
        print('  Sphinx: Not available')

    try:
        import pydantic
        print(f'  Pydantic: {pydantic.VERSION}')
    except ImportError:
        print('  Pydantic: Not available')
    "
    :caption: Environment Check
```

### Live Testing Examples

```rst
.. program-output:: python -c "
    # Test PyDevelop-Docs functionality
    from pydevelop_docs.cli import main
    from pydevelop_docs.config import get_haive_config

    # Test configuration generation
    config = get_haive_config('test-package')
    print('Configuration keys:')
    for key in sorted(config.keys())[:10]:
        print(f'  {key}')

    print(f'\\nTotal configuration items: {len(config)}')
    "
    :caption: Live Configuration Test
```

## Error Handling and Debugging

### Error Display Options

```rst
.. program-output:: python -c "raise ValueError('Example error')"
    :stderr:          # Include stderr output
    :ignore-errors:   # Don't fail build on error
    :return-code:     # Show return code
```

### Debug Output

```rst
.. program-output:: python -c "
    import sys
    print('Debug info:', file=sys.stderr)
    print('Standard output')
    exit(42)
    "
    :stderr:
    :return-code:
    :caption: Debug Output Example
```

### Conditional Execution

```rst
.. program-output:: python -c "
    import os
    if os.getenv('CI'):
        print('Running in CI environment')
        print('Skipping interactive tests')
    else:
        print('Local development environment')
        print('Running full test suite')
    "
    :caption: Environment-Specific Output
```

## Performance Optimization

### Output Caching

```python
# Cache command results
programoutput_cache_enabled = True          # Enable caching
programoutput_cache_dir = "_programoutput_cache"  # Cache directory
programoutput_cache_key_includes = [        # Cache key components
    "command",
    "working_dir",
    "env_vars",
    "file_mtime"
]
```

### Execution Limits

```python
# Performance limits
programoutput_timeout = 30                  # Command timeout
programoutput_output_limit = 100000         # Max output size
programoutput_concurrent_limit = 3          # Max concurrent executions
programoutput_memory_limit = "256MB"        # Memory limit per command
```

## Integration with PyDevelop-Docs

### Self-Documentation

```rst
Show PyDevelop-Docs in Action
----------------------------

.. program-output:: poetry run pydvlp-docs --version
    :caption: Version Information

.. program-output:: poetry run pydvlp-docs init --help
    :caption: Initialization Options

.. program-output:: poetry run pydvlp-docs init --dry-run --use-shared-config
    :caption: Dry Run Example
```

### Extension Testing

```rst
Extension Verification
---------------------

.. program-output:: python -c "
    import pkg_resources

    extensions = [
        'sphinx-autoapi',
        'furo',
        'sphinx-copybutton',
        'sphinx-design',
        'myst-parser'
    ]

    print('Extension Status:')
    for ext in extensions:
        try:
            dist = pkg_resources.get_distribution(ext)
            print(f'  ✓ {ext}: {dist.version}')
        except pkg_resources.DistributionNotFound:
            print(f'  ✗ {ext}: Not found')
    "
    :caption: Extension Status Check
```

### Build Process Documentation

```rst
Documentation Build Process
--------------------------

.. program-output:: bash -c "
    echo 'Step 1: Clean previous build'
    rm -rf docs/build

    echo 'Step 2: Generate configuration'
    poetry run pydvlp-docs init --force

    echo 'Step 3: Build documentation'
    cd docs && poetry run sphinx-build -b html source build

    echo 'Step 4: Verify build'
    ls -la docs/build/
    echo 'Build complete!'
    "
    :caption: Complete Build Process
```

## Testing and Validation

### Command Testing

```rst
.. program-output:: python -c "
    import subprocess
    import sys

    # Test that PyDevelop-Docs CLI works
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pydevelop_docs.cli', '--version'
        ], capture_output=True, text=True, timeout=10)

        print(f'Return code: {result.returncode}')
        print(f'Output: {result.stdout.strip()}')

        if result.returncode == 0:
            print('✓ CLI test passed')
        else:
            print('✗ CLI test failed')
            print(f'Error: {result.stderr}')

    except Exception as e:
        print(f'✗ CLI test error: {e}')
    "
    :test: true
    :caption: CLI Functionality Test
```

### Environment Validation

```rst
.. program-output:: python -c "
    # Validate documentation build environment
    import sys
    import subprocess

    required_commands = ['poetry', 'git', 'python']

    print('Environment Validation:')
    for cmd in required_commands:
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.split('\\n')[0]
                print(f'  ✓ {cmd}: {version}')
            else:
                print(f'  ✗ {cmd}: Command failed')
        except FileNotFoundError:
            print(f'  ✗ {cmd}: Not found')
        except Exception as e:
            print(f'  ✗ {cmd}: Error - {e}')
    "
    :test: true
    :caption: Environment Validation
```

## Implementation Status in PyDevelop-Docs

### Current State

- ✅ **Enabled**: Active in main configuration
- ✅ **Configured**: ANSI color support enabled
- ✅ **Working**: Basic program output inclusion functional
- 📋 **TODO**: Security hardening and AutoAPI integration

### Integration Roadmap

1. **Phase 1**: Security configuration and command restrictions
2. **Phase 2**: AutoAPI template integration for CLI documentation
3. **Phase 3**: Advanced output formatting and caching
4. **Phase 4**: Comprehensive testing and validation examples

## Best Practices

### Security First

```python
# Always configure security restrictions
programoutput_allowed_commands = ["python", "poetry", "pip"]
programoutput_timeout = 30
programoutput_working_dir = "_temp"
```

### Performance Optimization

```python
# Cache results for faster builds
programoutput_cache_enabled = True
programoutput_output_limit = 50000
programoutput_concurrent_limit = 2
```

### Content Guidelines

```rst
# Write command examples that:
# 1. Are deterministic and repeatable
# 2. Don't require external network access
# 3. Use relative paths when possible
# 4. Include proper error handling
# 5. Show realistic, practical usage
```

This extension bridges the gap between documentation and reality by showing actual program execution, making it invaluable for CLI tools, installation guides, and any documentation that needs to demonstrate real-world usage patterns.
