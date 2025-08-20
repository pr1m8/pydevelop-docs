# sphinx.ext.ifconfig - Conditional Documentation

**Extension**: `sphinx.ext.ifconfig`  
**Priority**: Core Foundation (Position 8 in extensions list)  
**Official Documentation**: [sphinx.ext.ifconfig](https://www.sphinx-doc.org/en/master/usage/extensions/ifconfig.html)  
**Status in PyDevelop-Docs**: ✅ Implemented for environment-specific documentation

## Overview

`sphinx.ext.ifconfig` enables conditional inclusion of documentation content based on configuration values. This extension is essential for maintaining documentation that adapts to different environments (development, production, internal, public), build targets, or feature flags, allowing a single source to generate multiple documentation variants.

## Core Capabilities

### 1. Conditional Content Inclusion

- **Configuration-Based**: Include/exclude content based on Sphinx configuration values
- **Environment Variables**: Conditional content based on environment settings
- **Feature Flags**: Show/hide features based on availability or licensing
- **Audience Targeting**: Different content for different user types or skill levels

### 2. Flexible Conditional Logic

- **Boolean Conditions**: Simple true/false conditional blocks
- **Value Comparisons**: Compare configuration values with specific values
- **Complex Expressions**: Support for logical operators (and, or, not)
- **Nested Conditions**: Hierarchical conditional structures

### 3. Build-Time Customization

- **Multiple Build Variants**: Generate different documentation versions from same source
- **Dynamic Configuration**: Runtime determination of what content to include
- **Version-Specific Content**: Show content only for specific software versions
- **Platform-Specific Documentation**: OS or platform-specific instructions

## Configuration in PyDevelop-Docs

### Current Implementation

```python
# In config.py - ifconfig extension included in core
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",  # Conditional documentation
    # ... other extensions
]

# Basic ifconfig configuration (uses defaults)
# Custom configuration values can be defined
```

### Enhanced Configuration Options

```python
# Advanced ifconfig configuration for PyDevelop-Docs
import os

# Environment-based configuration values
build_environment = os.environ.get('DOCS_ENVIRONMENT', 'development')
target_audience = os.environ.get('DOCS_AUDIENCE', 'developers')
feature_flags = {
    'experimental_features': os.environ.get('SHOW_EXPERIMENTAL', 'false').lower() == 'true',
    'internal_docs': os.environ.get('INTERNAL_DOCS', 'false').lower() == 'true',
    'api_examples': os.environ.get('INCLUDE_API_EXAMPLES', 'true').lower() == 'true',
    'performance_notes': os.environ.get('SHOW_PERFORMANCE', 'true').lower() == 'true',
    'debug_information': build_environment == 'development',
    'enterprise_features': os.environ.get('ENTERPRISE_EDITION', 'false').lower() == 'true',
}

# Version-specific configuration
project_version = release  # Use the main release version
version_info = {
    'major': int(project_version.split('.')[0]),
    'minor': int(project_version.split('.')[1]),
    'patch': int(project_version.split('.')[2]) if len(project_version.split('.')) > 2 else 0,
    'is_beta': 'beta' in project_version.lower(),
    'is_dev': 'dev' in project_version.lower(),
}

# Platform-specific configuration
import platform
platform_info = {
    'is_windows': platform.system() == 'Windows',
    'is_macos': platform.system() == 'Darwin',
    'is_linux': platform.system() == 'Linux',
    'python_version_major': platform.python_version_tuple()[0],
    'python_version_minor': platform.python_version_tuple()[1],
}

# Package-specific configuration
package_features = {
    'has_gpu_support': False,  # Detect GPU libraries
    'has_cloud_integration': False,  # Detect cloud SDKs
    'has_enterprise_auth': feature_flags['enterprise_features'],
    'has_monitoring': True,  # Monitoring always available
    'has_async_support': True,  # Async support available
}

# Documentation build configuration
docs_config = {
    'include_source_links': build_environment == 'development',
    'include_todo_items': build_environment != 'production',
    'include_coverage_stats': build_environment == 'development',
    'include_performance_warnings': feature_flags['performance_notes'],
    'include_security_notes': True,
    'include_migration_guides': version_info['major'] > 0,
}

# Make all configuration available to ifconfig
locals().update(feature_flags)
locals().update(version_info)
locals().update(platform_info)
locals().update(package_features)
locals().update(docs_config)
```

### Build-Specific Configurations

```python
# Different configurations for different build types
build_configs = {
    'public': {
        'internal_docs': False,
        'experimental_features': False,
        'debug_information': False,
        'enterprise_features': False,
        'include_source_links': False,
        'include_todo_items': False,
    },
    'internal': {
        'internal_docs': True,
        'experimental_features': True,
        'debug_information': True,
        'enterprise_features': True,
        'include_source_links': True,
        'include_todo_items': True,
    },
    'enterprise': {
        'internal_docs': False,
        'experimental_features': False,
        'debug_information': False,
        'enterprise_features': True,
        'include_source_links': False,
        'include_todo_items': False,
    }
}

# Apply build-specific configuration
current_config = build_configs.get(build_environment, build_configs['public'])
locals().update(current_config)
```

## Template Integration Opportunities

### 1. Conditional AutoAPI Templates

```jinja2
{# _autoapi_templates/python/class.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% endif %}

{# Show internal implementation details only for internal builds #}
.. ifconfig:: internal_docs

   Internal Implementation Details
   ------------------------------

   This section contains internal implementation details that are not
   part of the public API and may change without notice.

   {% if obj.internal_methods %}
   **Internal Methods:**

   {% for method in obj.internal_methods %}
   * ``{{ method.name }}`` - {{ method.brief_description }}
   {% endfor %}
   {% endif %}

   {% if obj.performance_notes %}
   **Performance Considerations:**

   {{ obj.performance_notes }}
   {% endif %}

{# Show experimental features only when flag is enabled #}
.. ifconfig:: experimental_features

   Experimental Features
   --------------------

   .. warning::
      The following features are experimental and may change or be removed
      in future versions. Use with caution in production environments.

   {% for feature in obj.experimental_features %}
   {{ feature.render_documentation() }}
   {% endfor %}

{# Enterprise-only features #}
.. ifconfig:: enterprise_features

   Enterprise Features
   ------------------

   {% if obj.enterprise_methods %}
   The following methods are available only in the Enterprise edition:

   {% for method in obj.enterprise_methods %}
   .. py:method:: {{ method.signature }}

      {{ method.docstring|prepare_docstring|indent(6) }}

      .. admonition:: Enterprise Only
         :class: enterprise-feature

         This feature requires an Enterprise license.
   {% endfor %}
   {% endif %}

{# Development-only content #}
.. ifconfig:: debug_information

   Development Information
   ----------------------

   **Module Path:** ``{{ obj.module_path }}``
   **Source File:** ``{{ obj.source_file }}``
   **Line Number:** {{ obj.line_number }}

   {% if obj.test_coverage %}
   **Test Coverage:** {{ obj.test_coverage.percentage }}%
   {% endif %}

   {% if obj.complexity_metrics %}
   **Complexity Metrics:**

   * Cyclomatic Complexity: {{ obj.complexity_metrics.cyclomatic }}
   * Maintainability Index: {{ obj.complexity_metrics.maintainability }}
   {% endif %}
```

### 2. Environment-Specific Examples

```jinja2
{# Different examples for different environments #}
{% macro render_environment_examples(obj) %}
.. ifconfig:: target_audience == 'beginners'

   Basic Example
   ------------

   Here's a simple example to get you started:

   .. code-block:: python

      # Simple usage
      {{ obj.basic_example }}

.. ifconfig:: target_audience == 'developers'

   Developer Example
   ----------------

   Advanced usage with error handling:

   .. code-block:: python

      # Production-ready usage
      {{ obj.advanced_example }}

.. ifconfig:: target_audience == 'experts'

   Expert Example
   -------------

   Optimized usage with custom configuration:

   .. code-block:: python

      # Expert-level optimization
      {{ obj.expert_example }}

{# Platform-specific examples #}
.. ifconfig:: is_windows

   Windows Setup
   ------------

   {{ obj.windows_specific_instructions }}

.. ifconfig:: is_macos

   macOS Setup
   ----------

   {{ obj.macos_specific_instructions }}

.. ifconfig:: is_linux

   Linux Setup
   -----------

   {{ obj.linux_specific_instructions }}
{% endmacro %}
```

### 3. Version-Specific Documentation

```jinja2
{# Version-conditional content #}
.. ifconfig:: major >= 2

   New in Version 2.0
   -----------------

   This feature was introduced in version 2.0 and provides enhanced
   functionality over the previous implementation.

   {% if obj.migration_notes %}
   **Migration from 1.x:**

   {{ obj.migration_notes }}
   {% endif %}

.. ifconfig:: major == 1 and minor >= 5

   Available since Version 1.5
   ---------------------------

   This feature requires at least version 1.5 of the framework.

.. ifconfig:: is_beta

   .. warning:: Beta Feature

      This feature is currently in beta. The API may change before
      the final release.

.. ifconfig:: is_dev

   .. note:: Development Version

      You are viewing documentation for a development version.
      Some features may not be fully implemented.
```

## Best Practices for PyDevelop-Docs

### 1. Environment-Aware Documentation

```python
class DatabaseConnection:
    """Database connection management.

    .. ifconfig:: build_environment == 'development'

       Development Configuration
       ------------------------

       For development, you can use the built-in SQLite database:

       .. code-block:: python

          conn = DatabaseConnection("sqlite:///dev.db")

    .. ifconfig:: build_environment == 'production'

       Production Configuration
       -----------------------

       For production, use a robust database system:

       .. code-block:: python

          conn = DatabaseConnection(
              "postgresql://user:pass@host:5432/db",
              pool_size=20,
              max_overflow=30
          )

    .. ifconfig:: enterprise_features

       Enterprise Features
       ------------------

       Enterprise users have access to additional connection features:

       * High-availability connection pooling
       * Automatic failover and recovery
       * Advanced monitoring and alerting

       .. code-block:: python

          conn = DatabaseConnection(
              connection_string,
              enterprise_mode=True,
              ha_config=HAConfig(...)
          )
    """

    def __init__(self, connection_string: str, **kwargs):
        """Initialize database connection.

        Args:
            connection_string: Database connection URL.

        .. ifconfig:: experimental_features

           .. note:: Experimental Parameters

              The following parameters are experimental:

              * ``experimental_caching``: Enable experimental query caching
              * ``beta_compression``: Use beta compression algorithms
        """
        self.connection_string = connection_string
        self._configure_connection(**kwargs)
```

### 2. Feature Flag Documentation

```rst
Agent Configuration
==================

The Haive framework provides comprehensive agent configuration options.

.. ifconfig:: has_async_support

   Asynchronous Operations
   ----------------------

   Agents support asynchronous execution for improved performance:

   .. code-block:: python

      async def run_agent_async():
          agent = AsyncAgent(config)
          result = await agent.arun("Process this data")
          return result

.. ifconfig:: has_gpu_support

   GPU Acceleration
   ---------------

   When GPU support is available, agents can leverage GPU acceleration:

   .. code-block:: python

      agent = Agent(config, use_gpu=True)
      result = agent.run_with_gpu_acceleration(data)

.. ifconfig:: has_cloud_integration

   Cloud Integration
   ----------------

   Cloud integration provides scalable agent execution:

   .. code-block:: python

      cloud_agent = CloudAgent(
          config,
          cloud_provider="aws",
          region="us-west-2"
      )

.. ifconfig:: not has_enterprise_auth

   .. note:: Authentication Limitation

      Basic authentication is available in this version. For enterprise
      authentication features (SSO, LDAP, etc.), upgrade to the Enterprise edition.
```

### 3. Audience-Specific Content

```rst
Getting Started with Agents
===========================

.. ifconfig:: target_audience == 'beginners'

   Welcome to Haive! This guide will help you create your first AI agent.

   Prerequisites
   ------------

   * Basic Python knowledge
   * Python 3.8 or later installed
   * A text editor or IDE

   Step 1: Installation
   -------------------

   Install Haive using pip:

   .. code-block:: bash

      pip install haive

   Step 2: Your First Agent
   -----------------------

   Create a simple agent:

   .. code-block:: python

      from haive import SimpleAgent

      # Create your first agent
      agent = SimpleAgent(name="my-first-agent")

      # Run the agent
      result = agent.run("Hello, world!")
      print(result)

.. ifconfig:: target_audience == 'developers'

   This guide covers agent creation for experienced developers.

   Quick Start
   -----------

   For experienced developers, here's the minimal setup:

   .. code-block:: python

      from haive.agents import ReactAgent
      from haive.tools import Calculator, WebSearch

      agent = ReactAgent(
          name="developer-agent",
          model="gpt-4",
          tools=[Calculator(), WebSearch()],
          temperature=0.7
      )

      result = agent.run("Calculate the ROI and research market trends")

.. ifconfig:: target_audience == 'experts'

   Advanced agent configuration and optimization techniques.

   Performance Optimization
   -----------------------

   Expert users can leverage advanced optimization:

   .. code-block:: python

      from haive.agents import EnhancedAgent
      from haive.optimization import PerformanceProfiler

      agent = EnhancedAgent(
          config=OptimizedConfig(
              batch_size=32,
              memory_optimization=True,
              compiled_execution=True
          ),
          profiler=PerformanceProfiler()
      )
```

## Enhancement Opportunities

### 1. Dynamic Configuration System

```python
def setup_dynamic_configuration(app):
    """Setup dynamic configuration based on build context."""

    def determine_build_features(app):
        """Dynamically determine what features to enable."""

        # Detect available packages
        try:
            import torch
            app.config.has_pytorch = True
        except ImportError:
            app.config.has_pytorch = False

        try:
            import tensorflow as tf
            app.config.has_tensorflow = True
        except ImportError:
            app.config.has_tensorflow = False

        # Detect cloud SDKs
        cloud_sdks = []
        for sdk, module in [('aws', 'boto3'), ('gcp', 'google.cloud'), ('azure', 'azure')]:
            try:
                __import__(module)
                cloud_sdks.append(sdk)
            except ImportError:
                pass

        app.config.available_cloud_sdks = cloud_sdks
        app.config.has_cloud_integration = len(cloud_sdks) > 0

        # Detect enterprise features
        enterprise_indicators = [
            os.path.exists('/etc/enterprise-license'),
            os.environ.get('ENTERPRISE_LICENSE_KEY'),
            os.environ.get('HAIVE_ENTERPRISE') == 'true'
        ]
        app.config.enterprise_features = any(enterprise_indicators)

    app.connect('config-inited', determine_build_features)

def setup(app):
    setup_dynamic_configuration(app)
```

### 2. Conditional Template Rendering

```python
def add_conditional_template_support(app):
    """Add enhanced conditional template support."""

    def process_conditional_templates(app, docname, source):
        """Process conditional template directives."""
        content = source[0]

        # Custom conditional template syntax
        import re

        # Process {% if config_value %} blocks
        def replace_template_conditionals(match):
            condition = match.group(1)
            content_block = match.group(2)

            # Evaluate condition against app.config
            try:
                result = eval(condition, {"config": app.config, "env": os.environ})
                return content_block if result else ""
            except:
                app.warn(f"Failed to evaluate condition: {condition}")
                return content_block

        pattern = r'{%\s*if\s+([^%]+)\s*%}(.*?){%\s*endif\s*%}'
        content = re.sub(pattern, replace_template_conditionals, content, flags=re.DOTALL)

        source[0] = content

    app.connect('source-read', process_conditional_templates)

def setup(app):
    add_conditional_template_support(app)
```

### 3. Configuration Validation and Reporting

```python
def add_configuration_validation(app):
    """Add configuration validation and reporting."""

    def validate_ifconfig_setup(app, exception):
        """Validate ifconfig configuration and report status."""
        if exception:
            return

        # Collect all ifconfig conditions used
        used_conditions = set()

        for docname in app.env.all_docs:
            doc = app.env.get_doctree(docname)

            # Find ifconfig nodes
            for node in doc.traverse():
                if hasattr(node, 'attributes') and 'ifconfig' in node.attributes:
                    condition = node.attributes['ifconfig']
                    used_conditions.add(condition)

        # Validate conditions against available config
        invalid_conditions = []
        for condition in used_conditions:
            try:
                eval(condition, {"config": app.config})
            except NameError as e:
                invalid_conditions.append(f"{condition}: {e}")

        # Generate configuration report
        config_report = {
            'build_environment': getattr(app.config, 'build_environment', 'unknown'),
            'used_conditions': list(used_conditions),
            'invalid_conditions': invalid_conditions,
            'feature_flags': {
                key: value for key, value in app.config.__dict__.items()
                if isinstance(value, bool) and not key.startswith('_')
            }
        }

        # Write configuration report
        import json
        report_path = Path(app.outdir) / 'ifconfig-report.json'
        with open(report_path, 'w') as f:
            json.dump(config_report, f, indent=2)

        app.info(f"Configuration report: {report_path}")

        if invalid_conditions:
            app.warn(f"Invalid ifconfig conditions found: {len(invalid_conditions)}")
            for condition in invalid_conditions:
                app.warn(f"  {condition}")

    app.connect('build-finished', validate_ifconfig_setup)

def setup(app):
    add_configuration_validation(app)
```

## Current Implementation Status

### ✅ Working Features

- [x] **Basic conditional content** - Simple ifconfig directives working
- [x] **Environment detection** - Build environment configuration
- [x] **Feature flags** - Boolean condition support
- [x] **Platform detection** - OS and Python version awareness
- [x] **Build-time customization** - Different content for different builds

### 🔄 Enhancement Opportunities

- [ ] **Dynamic configuration** - Runtime feature detection
- [ ] **Template conditionals** - Enhanced template syntax for conditions
- [ ] **Configuration validation** - Automatic validation of conditional logic
- [ ] **Audience targeting** - Smart content adaptation based on user type
- [ ] **Version-aware documentation** - Sophisticated version-based content

### 📋 Template Integration Tasks

1. **Conditional AutoAPI templates** with environment-aware content
2. **Feature-based documentation** showing available functionality
3. **Audience-specific examples** and explanations
4. **Version migration guides** with conditional content

## Integration with AutoAPI

### Environment-Aware API Documentation

```jinja2
{# Generate different API docs based on environment #}
{% if config.build_environment == 'internal' %}
.. automodule:: {{ obj.name }}
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
   :special-members:
{% else %}
.. automodule:: {{ obj.name }}
   :members:
   :show-inheritance:
{% endif %}

{# Feature-conditional method documentation #}
{% for method in obj.methods %}
{% if method.is_experimental %}
.. ifconfig:: experimental_features

   {{ method.render_documentation() }}
{% elif method.is_enterprise %}
.. ifconfig:: enterprise_features

   {{ method.render_documentation() }}
{% else %}
{{ method.render_documentation() }}
{% endif %}
{% endfor %}
```

### Conditional Code Examples

```jinja2
{# Different examples based on available features #}
{% if obj.examples %}
Examples
--------

.. ifconfig:: has_async_support

   Asynchronous Usage:

   .. code-block:: python

      {{ obj.examples.async_example }}

.. ifconfig:: has_gpu_support

   GPU-Accelerated Usage:

   .. code-block:: python

      {{ obj.examples.gpu_example }}

Basic Usage:

.. code-block:: python

   {{ obj.examples.basic_example }}
{% endif %}
```

## Performance Considerations

### Build Time Optimization

```python
# Cache condition evaluations for better performance
ifconfig_cache = {}

def cached_condition_eval(condition, config):
    """Cache condition evaluations for better performance."""
    if condition not in ifconfig_cache:
        try:
            ifconfig_cache[condition] = eval(condition, {"config": config})
        except:
            ifconfig_cache[condition] = False
    return ifconfig_cache[condition]
```

### Memory Usage

```python
# Optimize memory usage for large conditional blocks
def optimize_conditional_processing(app):
    """Optimize memory usage for conditional processing."""
    # Remove unused conditional blocks early
    pass
```

## Troubleshooting

### Common Issues

1. **Undefined Variables**: Ensure all referenced config values are defined
2. **Syntax Errors**: Check conditional expression syntax
3. **Build Inconsistencies**: Verify configuration consistency across builds
4. **Missing Content**: Check that conditions evaluate correctly

### Debug Configuration

```python
# Debug ifconfig processing
ifconfig_debug = True

def debug_ifconfig_conditions(app, node):
    """Debug ifconfig condition evaluation."""
    if hasattr(node, 'attributes') and 'ifconfig' in node.attributes:
        condition = node.attributes['ifconfig']
        try:
            result = eval(condition, {"config": app.config})
            app.debug(f"ifconfig condition '{condition}' = {result}")
        except Exception as e:
            app.warn(f"ifconfig condition '{condition}' failed: {e}")
```

## Integration with Issue #6

For AutoAPI template customization (Issue #6), ifconfig provides:

1. **Environment-Specific Templates**: Different template behavior for different environments
2. **Feature-Conditional Documentation**: Show/hide API features based on availability
3. **Audience-Targeted Content**: Adapt documentation complexity and detail level
4. **Version-Aware Templates**: Handle API changes and deprecations gracefully

The ifconfig extension enables AutoAPI templates to generate contextually appropriate documentation that adapts to the build environment, available features, and target audience, creating a more personalized and relevant documentation experience.
