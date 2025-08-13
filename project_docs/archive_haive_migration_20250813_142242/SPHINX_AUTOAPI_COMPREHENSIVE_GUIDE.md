# Sphinx AutoAPI Comprehensive Guide

**Version**: 1.0  
**Purpose**: Complete technical guide to sphinx-autoapi implementation  
**Last Updated**: 2025-08-05

## Table of Contents

1. [Overview & Core Concepts](#overview--core-concepts)
2. [Installation & Basic Setup](#installation--basic-setup)
3. [Configuration Options Reference](#configuration-options-reference)
4. [Directory Structure & File Generation](#directory-structure--file-generation)
5. [Template System & Customization](#template-system--customization)
6. [Complex Project Structures](#complex-project-structures)
7. [Integration with Other Extensions](#integration-with-other-extensions)
8. [Performance Optimization](#performance-optimization)
9. [Troubleshooting Common Issues](#troubleshooting-common-issues)
10. [Advanced Patterns & Best Practices](#advanced-patterns--best-practices)
11. [Real-World Examples](#real-world-examples)

## Overview & Core Concepts

### What is Sphinx AutoAPI?

Sphinx AutoAPI is a Sphinx extension that automatically generates API documentation by **parsing source code** without requiring code imports or execution. This fundamental difference from traditional `sphinx.ext.autodoc` makes it safer and more efficient for complex projects.

### Key Characteristics

- **Parse-only approach**: Analyzes source code statically without importing modules
- **Zero configuration**: Works out-of-the-box with minimal setup
- **Multi-language support**: Python, .NET, Go, JavaScript
- **Template-based**: Uses Jinja2 templates for customizable output
- **TOC integration**: Automatically creates table of contents entries

### AutoAPI vs Autodoc Comparison

| Feature          | sphinx-autoapi       | sphinx.ext.autodoc             |
| ---------------- | -------------------- | ------------------------------ |
| **Approach**     | Parse source code    | Import and introspect          |
| **Setup**        | Automatic discovery  | Manual sphinx-apidoc required  |
| **Safety**       | No code execution    | Executes import statements     |
| **Performance**  | Static analysis      | Runtime introspection          |
| **Dependencies** | Parse-time only      | Runtime dependencies required  |
| **TOC entries**  | Automatic generation | Manual or autosummary required |
| **Memory usage** | Lower                | Higher (loads all modules)     |

## Installation & Basic Setup

### Installation

```bash
pip install sphinx-autoapi
```

### Minimal Configuration

Add to your `conf.py`:

```python
extensions = ['autoapi.extension']
autoapi_dirs = ['../src']  # Path to your source code
```

### Basic Project Structure

```
myproject/
├── docs/
│   ├── conf.py
│   ├── index.rst
│   └── _build/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── module1.py
│       └── subpackage/
│           ├── __init__.py
│           └── module2.py
└── setup.py
```

### Build Documentation

```bash
cd docs/
sphinx-build -b html . _build/html
```

## Configuration Options Reference

### Required Configuration

```python
# Minimum required configuration
extensions = ['autoapi.extension']
autoapi_dirs = ['../src', '../lib']  # List of source directories
```

### Core Options

```python
# Output control
autoapi_root = 'api'  # Default: 'autoapi' - Output directory name
autoapi_add_toctree_entry = True  # Default: True - Add to TOC

# File processing
autoapi_file_patterns = ['*.py', '*.pyi']  # File patterns to process
autoapi_ignore = ['*migrations*', '*tests*']  # Patterns to ignore

# Content control
autoapi_options = [
    'members',           # Show module/class members
    'undoc-members',     # Include undocumented members
    'private-members',   # Include private members (_private)
    'show-inheritance',  # Show class inheritance
    'show-module-summary',  # Show module summary tables
    'special-members',   # Include special methods (__init__, etc.)
    'imported-members',  # Show imported objects
]

# Documentation behavior
autoapi_python_class_content = 'class'  # 'class', 'both', or 'init'
autoapi_member_order = 'alphabetical'  # 'alphabetical', 'bysource', 'groupwise'
autoapi_keep_files = False  # Keep generated .rst files for debugging
```

### Advanced Configuration

```python
# Language-specific settings
autoapi_type = 'python'  # 'python', 'dotnet', 'go', 'javascript'
autoapi_python_use_implicit_namespaces = False  # PEP 420 namespace support

# Template customization
autoapi_template_dir = '_autoapi_templates'
autoapi_include_summaries = True

# Warning suppression
suppress_warnings = [
    'autoapi.python_import_resolution',
    'autoapi.not_readable',
    'autoapi.nothing_rendered'
]

# Custom Jinja2 environment
def autoapi_prepare_jinja_env(jinja_env):
    """Customize Jinja2 environment for templates."""
    jinja_env.filters['my_filter'] = lambda x: x.upper()
    jinja_env.tests['my_test'] = lambda x: x.startswith('_')
    jinja_env.globals['my_global'] = 'Custom Value'

# Event handlers
def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_member_handler)
```

### Configuration Validation

```python
# Validate your configuration
def validate_autoapi_config():
    import os
    for dir_path in autoapi_dirs:
        if not os.path.exists(dir_path):
            raise ValueError(f"autoapi_dirs path does not exist: {dir_path}")
    print("✅ AutoAPI configuration validated")
```

## Directory Structure & File Generation

### Generated File Structure

AutoAPI generates files following this pattern:

```
docs/_build/html/autoapi/
├── index.html                    # Main API index
├── mypackage/
│   ├── index.html               # Package overview
│   ├── module1.html             # Module documentation
│   └── subpackage/
│       ├── index.html           # Subpackage overview
│       └── module2.html         # Submodule documentation
```

### Source Code Mapping

```python
# Source structure maps to documentation structure
src/mypackage/
├── __init__.py              → autoapi/mypackage/index.rst
├── core.py                  → autoapi/mypackage/core.rst
├── utils/
│   ├── __init__.py          → autoapi/mypackage/utils/index.rst
│   └── helpers.py           → autoapi/mypackage/utils/helpers.rst
```

### Custom Output Location

```python
# Change output directory
autoapi_root = 'reference'  # Creates docs/reference/ instead of docs/autoapi/

# Disable automatic TOC entry
autoapi_add_toctree_entry = False

# Manually add to your main TOC
# In index.rst:
.. toctree::
   :maxdepth: 2

   reference/index
```

### File Pattern Matching

```python
# Control which files are processed
autoapi_file_patterns = [
    '*.py',      # Python files
    '*.pyi',     # Stub files (processed first if both exist)
    '*.pyx',     # Cython files
]

# Ignore patterns (glob-style)
autoapi_ignore = [
    '*migrations*',
    '*test*',
    '*_deprecated.py',
    '*/vendor/*',
]
```

## Template System & Customization

### Template Architecture

AutoAPI uses Jinja2 templates with this structure:

```
_autoapi_templates/
└── python/
    ├── class.rst           # Class documentation template
    ├── module.rst          # Module documentation template
    ├── package.rst         # Package documentation template
    ├── function.rst        # Function documentation template
    ├── method.rst          # Method documentation template
    ├── attribute.rst       # Attribute documentation template
    ├── property.rst        # Property documentation template
    ├── data.rst            # Module-level variable template
    ├── exception.rst       # Exception class template
    └── index.rst           # Main index template
```

### Template Context Variables

Every template receives these context variables:

```python
# Available in all templates
{
    'autoapi_options': ['members', 'undoc-members', ...],
    'include_summaries': True,
    'obj': PythonPythonMapper,  # The object being documented
    'own_page_types': {'class', 'exception', 'function'},
    'sphinx_version': (4, 5, 0),
}
```

### Custom Template Example

Create `_autoapi_templates/python/class.rst`:

```rst
{%- if obj.docstring %}
{{ obj.docstring|indent(0, True) }}
{% endif %}

{%- if obj.bases %}

**Inheritance:**
{% for base in obj.bases %}
- :py:class:`{{ base }}`
{% endfor %}
{% endif %}

{%- if obj.children %}

**Members:**

{%- for child in obj.children if child.short_name in obj.all %}
{{ child.render()|indent(0, True) }}
{% endfor %}
{% endif %}

{%- if obj.example %}

**Example:**

.. code-block:: python

{{ obj.example|indent(4, True) }}
{% endif %}
```

### Jinja2 Environment Customization

```python
def autoapi_prepare_jinja_env(jinja_env):
    """Add custom filters, tests, and globals."""

    # Custom filters
    def format_signature(obj):
        """Format function/method signature."""
        if hasattr(obj, 'args'):
            args = ', '.join([arg.name for arg in obj.args])
            return f"{obj.name}({args})"
        return obj.name

    def is_public(name):
        """Test if a name is public (doesn't start with _)."""
        return not name.startswith('_')

    def group_by_type(children):
        """Group children by their type."""
        groups = {}
        for child in children:
            child_type = child.__class__.__name__.replace('Python', '').lower()
            groups.setdefault(child_type, []).append(child)
        return groups

    # Register custom functions
    jinja_env.filters['format_signature'] = format_signature
    jinja_env.filters['group_by_type'] = group_by_type
    jinja_env.tests['public'] = is_public

    # Global variables
    jinja_env.globals['project_name'] = 'My Awesome Project'
    jinja_env.globals['version'] = '1.0.0'
```

### Template with Custom Logic

```rst
{# Custom class template with grouping #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{% if obj.docstring %}
{{ obj.docstring|indent(0, True) }}
{% endif %}

{%- set grouped = obj.children|group_by_type %}

{%- if grouped.method %}
Methods
-------
{% for method in grouped.method if method.name is public %}
.. automethod:: {{ method.name }}
{% endfor %}
{% endif %}

{%- if grouped.attribute %}
Attributes
----------
{% for attr in grouped.attribute if attr.name is public %}
.. autoattribute:: {{ attr.name }}
{% endfor %}
{% endif %}
```

## Complex Project Structures

### Namespace Packages (PEP 420)

For implicit namespace packages without `__init__.py`:

```python
# Enable namespace package support
autoapi_python_use_implicit_namespaces = True

# Project structure:
src/
├── namespace/
│   └── package1/
│       └── module.py
└── namespace/
    └── package2/
        └── module.py
```

### Multi-Package Projects

```python
# Document multiple separate packages
autoapi_dirs = [
    '../src/core_package',
    '../src/utils_package',
    '../src/plugins',
    '../vendor/third_party'
]

# Use different ignore patterns per directory
autoapi_ignore = [
    '*/tests/*',
    '*/vendor/*/test*',
    '*_internal.py'
]
```

### Monorepo Structure

```python
# Large monorepo with selective documentation
project_root/
├── services/
│   ├── api/
│   ├── worker/
│   └── scheduler/
├── libs/
│   ├── common/
│   └── database/
└── docs/

# Configuration for monorepo
autoapi_dirs = [
    '../services/api/src',
    '../services/worker/src',
    '../libs/common',
    '../libs/database'
]

# Organize by service
autoapi_template_dir = '_templates/autoapi'
# Custom index template to group by service
```

### Complex Inheritance Hierarchies

```python
# Handle complex inheritance with better display
autoapi_options = [
    'members',
    'show-inheritance',
    'show-inheritance-diagram',  # If sphinx.ext.inheritance_diagram enabled
]

# Custom template for inheritance
# _autoapi_templates/python/class.rst
```

### Package with C Extensions

```python
# Mix of Python and C extension modules
autoapi_dirs = ['../src']
autoapi_file_patterns = [
    '*.py',      # Pure Python
    '*.pyi',     # Type stubs for C extensions
    '*.pyx',     # Cython
]

# Skip C extension files that can't be parsed
autoapi_ignore = [
    '*.so',
    '*.dll',
    '*.dylib'
]
```

## Integration with Other Extensions

### Napoleon (Google/NumPy Docstrings)

```python
extensions = [
    'sphinx.ext.napoleon',
    'autoapi.extension'
]

# Napoleon configuration
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = ['Returns', 'Yields']
```

### Type Hints Integration

```python
extensions = [
    'sphinx.ext.autodoc',
    'autoapi.extension'
]

# Enhanced type hint display
autodoc_typehints = 'description'  # 'signature', 'description', 'both'
autodoc_typehints_description_target = 'documented'
autodoc_type_aliases = {
    'MyCustomType': 'mypackage.types.MyCustomType'
}

# Python 3.10+ union syntax support
python_use_unqualified_type_names = True
```

### MyST Parser (Markdown Support)

```python
extensions = [
    'myst_parser',
    'autoapi.extension'
]

# MyST configuration
myst_enable_extensions = [
    'deflist',
    'fieldlist',
    'substitution',
    'colon_fence'
]

# Use Markdown in docstrings
myst_fence_as_directive = ['note', 'warning']
```

### Intersphinx (Cross-Project References)

```python
extensions = [
    'sphinx.ext.intersphinx',
    'autoapi.extension'
]

# Link to external documentation
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'requests': ('https://requests.readthedocs.io/en/stable/', None),
}

# AutoAPI will automatically use intersphinx for cross-references
```

### Custom CSS and Theming

```python
# Integrate with Furo theme
html_theme = 'furo'
html_theme_options = {
    'sidebar_hide_name': True,
    'navigation_with_keys': True,
}

# Custom CSS for AutoAPI elements
html_static_path = ['_static']
html_css_files = [
    'css/autoapi-custom.css',
]
```

Custom CSS (`_static/css/autoapi-custom.css`):

```css
/* Style AutoAPI elements */
.autoapi-section {
  margin-bottom: 2rem;
}

.autoapi-object-signature {
  background-color: #f8f9fa;
  padding: 0.5rem;
  border-radius: 4px;
  font-family: "Consolas", "Monaco", monospace;
}

.autoapi-inheritance {
  font-style: italic;
  color: #6c757d;
}

/* Group sections */
.autoapi-methods,
.autoapi-attributes {
  border-left: 3px solid #007bff;
  padding-left: 1rem;
  margin: 1rem 0;
}
```

### ReadTheDocs Configuration

`.readthedocs.yaml`:

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

sphinx:
  configuration: docs/conf.py
  fail_on_warning: true

python:
  install:
    - requirements: docs/requirements.txt
    - method: pip
      path: .
      extra_requirements:
        - docs
```

`docs/requirements.txt`:

```txt
sphinx>=4.0.0
sphinx-autoapi>=2.0.0
furo>=2022.6.21
myst-parser>=0.18.0
```

## Performance Optimization

### Build Time Optimization

```python
# Reduce parsing overhead
autoapi_keep_files = False  # Don't keep intermediate files
autoapi_include_summaries = False  # Disable summary tables if not needed

# Limit documentation scope
autoapi_options = [
    'members',           # Essential
    'show-inheritance',  # Usually needed
    # Remove expensive options:
    # 'undoc-members',   # Skip undocumented items
    # 'private-members', # Skip private members
    # 'imported-members' # Skip imported objects
]

# Optimize file patterns
autoapi_file_patterns = ['*.py']  # Skip .pyi files if not needed
autoapi_ignore = [
    '*test*',
    '*example*',
    '*demo*',
    '*benchmark*'
]
```

### Memory Usage Optimization

```python
# For large codebases
import sys

def optimize_autoapi_memory():
    """Configure AutoAPI for memory efficiency."""
    # Limit recursion depth
    sys.setrecursionlimit(1500)

    # Process in smaller chunks
    return {
        'autoapi_keep_files': False,
        'autoapi_include_summaries': False,
        'autoapi_options': ['members', 'show-inheritance']
    }

# Apply optimization
locals().update(optimize_autoapi_memory())
```

### Parallel Processing

```python
# Enable Sphinx parallel processing
# Command line: sphinx-build -j auto -b html docs/ docs/_build/html

# Configure for parallel builds
def setup(app):
    """Configure app for parallel processing."""
    app.setup_extension('autoapi.extension')

    # AutoAPI is parallel-safe by design (no shared state)
    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

### Incremental Builds

```python
# Keep generated files for incremental builds in development
if os.getenv('SPHINX_AUTOAPI_KEEP_FILES'):
    autoapi_keep_files = True
    print("🔧 AutoAPI: Keeping files for incremental builds")

# Build script for development
# docs/build_dev.sh:
#!/bin/bash
export SPHINX_AUTOAPI_KEEP_FILES=1
sphinx-build -b html -E . _build/html  # -E forces rebuild
```

### Profiling and Monitoring

```python
import time
import logging

# Profile AutoAPI performance
class AutoAPIProfiler:
    def __init__(self):
        self.start_time = None

    def profile_autoapi_build(self, app, config):
        """Profile AutoAPI build time."""
        self.start_time = time.time()
        logging.info("🔍 AutoAPI: Starting documentation generation")

    def profile_autoapi_complete(self, app, exception):
        """Log completion time."""
        if self.start_time:
            duration = time.time() - self.start_time
            logging.info(f"✅ AutoAPI: Completed in {duration:.2f}s")

# Enable profiling
profiler = AutoAPIProfiler()

def setup(app):
    app.connect('builder-inited', profiler.profile_autoapi_build)
    app.connect('build-finished', profiler.profile_autoapi_complete)
```

## Troubleshooting Common Issues

### Import Resolution Errors

**Problem**: `python_import_resolution` warnings

**Solution**:

```python
# 1. Suppress warnings temporarily
suppress_warnings = ['autoapi.python_import_resolution']

# 2. Fix underlying issues
# Check for circular imports in your code
# Ensure all parent modules have __init__.py files

# 3. Debug import issues
def debug_import_resolution():
    import ast
    import os

    for dir_path in autoapi_dirs:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            ast.parse(f.read())
                        print(f"✅ {file_path}")
                    except SyntaxError as e:
                        print(f"❌ {file_path}: {e}")
```

### Empty API Documentation

**Problem**: AutoAPI generates empty documentation

**Solutions**:

```python
# 1. Check autoapi_dirs paths
import os
for path in autoapi_dirs:
    abs_path = os.path.abspath(path)
    print(f"Checking: {abs_path}")
    print(f"Exists: {os.path.exists(abs_path)}")
    if os.path.exists(abs_path):
        files = [f for f in os.listdir(abs_path) if f.endswith('.py')]
        print(f"Python files: {files}")

# 2. Check autoapi_options
autoapi_options = [
    'members',          # Essential for content
    'undoc-members',    # Include items without docstrings
]

# 3. Debug with verbose output
autoapi_keep_files = True  # Inspect generated .rst files

# 4. Check __all__ declarations
# In your Python modules, ensure __all__ includes items to document
__all__ = ['MyClass', 'my_function', 'CONSTANT']
```

### Template Errors

**Problem**: Custom templates not working

**Solutions**:

```python
# 1. Verify template directory structure
import os

def validate_template_structure():
    template_dir = '_autoapi_templates'
    required_templates = [
        'python/class.rst',
        'python/module.rst',
        'python/index.rst'
    ]

    for template in required_templates:
        path = os.path.join(template_dir, template)
        if os.path.exists(path):
            print(f"✅ {template}")
        else:
            print(f"❌ Missing: {template}")

# 2. Test Jinja2 syntax
def test_jinja_template():
    from jinja2 import Template, Environment

    template_content = """
{{ obj.name }}
{{ "=" * obj.name|length }}
{% if obj.docstring %}
{{ obj.docstring }}
{% endif %}
    """

    try:
        template = Template(template_content)
        print("✅ Template syntax valid")
    except Exception as e:
        print(f"❌ Template error: {e}")

# 3. Debug template context
def autoapi_prepare_jinja_env(jinja_env):
    def debug_context(template_name):
        print(f"🔍 Rendering template: {template_name}")

    jinja_env.globals['debug'] = debug_context
```

### Performance Issues

**Problem**: Slow documentation builds

**Solutions**:

```python
# 1. Profile build time
import cProfile
import pstats

def profile_sphinx_build():
    """Profile Sphinx build to identify bottlenecks."""
    profiler = cProfile.Profile()
    profiler.enable()

    # Run sphinx-build here

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 slowest functions

# 2. Optimize autoapi_options
autoapi_options = [
    'members',
    'show-inheritance',
    # Remove expensive options:
    # 'undoc-members',    # Can be slow for large codebases
    # 'private-members',  # Often not needed
    # 'imported-members', # Can cause performance issues
]

# 3. Use selective documentation
autoapi_ignore = [
    '*test*',      # Skip test files
    '*migration*', # Skip migration files
    '*__pycache__*',
    '*.pyc',
]

# 4. Enable parallel processing
# sphinx-build -j auto -b html docs/ docs/_build/html
```

### Module Not Found Errors

**Problem**: Modules can't be found during documentation

**Solutions**:

```python
# 1. Fix Python path in conf.py
import sys
import os

# Add source directories to Python path
sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, os.path.abspath('../'))

# 2. Check relative paths
current_dir = os.path.dirname(__file__)
autoapi_dirs = [
    os.path.join(current_dir, '..', 'src'),
    os.path.join(current_dir, '..', 'lib'),
]

# 3. Use absolute paths for clarity
autoapi_dirs = [
    '/absolute/path/to/src',
    '/absolute/path/to/lib',
]

# 4. Debug module discovery
def debug_module_discovery():
    import importlib.util

    for dir_path in autoapi_dirs:
        print(f"Checking directory: {dir_path}")
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.py') and not file.startswith('_'):
                    module_path = os.path.join(root, file)
                    spec = importlib.util.spec_from_file_location("test", module_path)
                    if spec:
                        print(f"  ✅ Can load: {file}")
                    else:
                        print(f"  ❌ Cannot load: {file}")
```

## Advanced Patterns & Best Practices

### Event-Driven Customization

```python
def setup(sphinx):
    """Advanced AutoAPI event handling."""

    def skip_test_modules(app, what, name, obj, skip, options):
        """Skip test modules and private members."""
        if what == "module" and "test" in name:
            return True
        if what == "method" and name.startswith("test_"):
            return True
        return skip

    def modify_docstring(app, what, name, obj, options, lines):
        """Modify docstrings during processing."""
        if lines and "TODO" in lines[0]:
            lines.insert(0, ".. warning:: This is a work in progress")

    def add_custom_sections(app, what, name, obj, options, signature, return_annotation):
        """Add custom sections to documentation."""
        if hasattr(obj, '_custom_metadata'):
            return f"{signature} -> {return_annotation}"
        return None

    # Connect event handlers
    sphinx.connect("autoapi-skip-member", skip_test_modules)
    sphinx.connect("autodoc-process-docstring", modify_docstring)
    sphinx.connect("autodoc-process-signature", add_custom_sections)
```

### Dynamic Configuration

```python
def configure_autoapi_for_environment():
    """Configure AutoAPI based on environment."""
    import os

    is_rtd = os.environ.get('READTHEDOCS') == 'True'
    is_ci = os.environ.get('CI') == 'true'
    is_dev = os.environ.get('SPHINX_DEV') == '1'

    if is_rtd:
        # ReadTheDocs: Minimal config for faster builds
        return {
            'autoapi_options': ['members', 'show-inheritance'],
            'autoapi_keep_files': False,
            'autoapi_include_summaries': False,
        }
    elif is_ci:
        # CI: Include warnings as errors
        return {
            'autoapi_options': ['members', 'undoc-members', 'show-inheritance'],
            'autoapi_keep_files': True,  # For debugging CI failures
        }
    elif is_dev:
        # Development: Full documentation with debugging
        return {
            'autoapi_options': [
                'members', 'undoc-members', 'private-members',
                'show-inheritance', 'show-module-summary'
            ],
            'autoapi_keep_files': True,
            'autoapi_include_summaries': True,
        }
    else:
        # Production: Comprehensive documentation
        return {
            'autoapi_options': [
                'members', 'undoc-members', 'show-inheritance',
                'show-module-summary', 'imported-members'
            ],
            'autoapi_keep_files': False,
        }

# Apply environment-based configuration
locals().update(configure_autoapi_for_environment())
```

### Multi-Version Documentation

```python
# Support for multiple versions/branches
import os

def setup_multiversion_autoapi():
    """Configure AutoAPI for multi-version docs."""
    version = os.environ.get('SPHINX_VERSION', 'latest')

    # Version-specific source paths
    version_map = {
        'latest': '../src',
        'v2.0': '../branches/v2.0/src',
        'v1.0': '../branches/v1.0/src',
    }

    return {
        'autoapi_dirs': [version_map.get(version, '../src')],
        'autoapi_root': f'api/{version}',
        'version': version,
    }

# Configure for current version
config = setup_multiversion_autoapi()
autoapi_dirs = config['autoapi_dirs']
autoapi_root = config['autoapi_root']
```

### Custom Object Processing

```python
class AutoAPIProcessor:
    """Advanced AutoAPI object processing."""

    def __init__(self):
        self.processed_objects = {}
        self.custom_metadata = {}

    def process_class(self, obj):
        """Add custom processing for classes."""
        # Extract design patterns
        if 'Singleton' in obj.bases:
            obj.custom_tags = ['singleton']

        # Add complexity metrics
        method_count = len([child for child in obj.children
                          if child.type == 'method'])
        obj.complexity_score = method_count

        return obj

    def process_function(self, obj):
        """Add custom processing for functions."""
        # Detect decorators
        if hasattr(obj, 'decorators'):
            if 'property' in obj.decorators:
                obj.custom_type = 'property'

        return obj

    def generate_metrics(self):
        """Generate code metrics."""
        return {
            'total_classes': len([o for o in self.processed_objects.values()
                                if o.type == 'class']),
            'total_functions': len([o for o in self.processed_objects.values()
                                  if o.type == 'function']),
        }

# Integrate processor
processor = AutoAPIProcessor()

def autoapi_prepare_jinja_env(jinja_env):
    jinja_env.globals['processor'] = processor
    jinja_env.filters['process_class'] = processor.process_class
    jinja_env.filters['process_function'] = processor.process_function
```

### API Stability Checking

```python
def setup_api_stability_check():
    """Check API stability between versions."""

    def check_api_changes(app, env, updated, added, removed):
        """Monitor API changes."""
        if removed:
            app.warn(f"API elements removed: {removed}")
        if added:
            app.info(f"API elements added: {added}")

    def validate_public_api(app, what, name, obj, skip, options):
        """Validate public API consistency."""
        if what == "class" and not name.startswith('_'):
            # Check for required docstring
            if not getattr(obj, 'docstring', None):
                app.warn(f"Public class {name} missing docstring")

            # Check for version info
            if not hasattr(obj, '__version__'):
                app.info(f"Class {name} missing version info")

        return skip

    return {
        'api_change_handler': check_api_changes,
        'api_validator': validate_public_api,
    }
```

## Real-World Examples

### Large Open Source Project Configuration

```python
# Example: numpy-style scientific library
project = 'SciPyLib'
copyright = '2024, SciPy Team'
author = 'SciPy Team'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'autoapi.extension',
    'numpydoc',
]

# AutoAPI configuration
autoapi_dirs = ['../scipylib']
autoapi_root = 'api'
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
]

# Skip internal modules
autoapi_ignore = [
    '*/_internal/*',
    '*/tests/*',
    '*/_version.py',
    '*/conftest.py',
]

# NumPy-style docstrings
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_special_with_doc = True

# Scientific computing cross-references
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
}

# Math rendering
mathjax3_config = {
    'tex': {'packages': {'[+]': ['amsmath', 'amsfonts']}},
}

# Custom template for scientific functions
autoapi_template_dir = '_templates/autoapi'
```

### Enterprise Django Project

```python
# Example: Large Django application
project = 'Enterprise App'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'autoapi.extension',
    'sphinx_django',
]

# Document Django apps selectively
autoapi_dirs = [
    '../myproject/apps/core',
    '../myproject/apps/users',
    '../myproject/apps/api',
    '../myproject/libs',
]

# Skip Django-specific files
autoapi_ignore = [
    '*/migrations/*',
    '*/tests/*',
    '*/settings/*',
    '**/management/**',
    'manage.py',
    'wsgi.py',
    'asgi.py',
]

# Django-specific options
autoapi_options = [
    'members',
    'show-inheritance',
    'show-module-summary',
]

# Group documentation by Django app
autoapi_member_order = 'groupwise'

# Custom Django template
def autoapi_prepare_jinja_env(jinja_env):
    def is_django_model(obj):
        return 'django.db.models' in str(getattr(obj, 'bases', []))

    def is_django_view(obj):
        bases_str = str(getattr(obj, 'bases', []))
        return any(view_type in bases_str for view_type in
                  ['View', 'APIView', 'ViewSet'])

    jinja_env.tests['django_model'] = is_django_model
    jinja_env.tests['django_view'] = is_django_view
```

### Microservices Architecture

```python
# Example: Multiple microservices in monorepo
services = [
    'user_service',
    'auth_service',
    'payment_service',
    'notification_service',
]

# Document all services
autoapi_dirs = [f'../services/{service}/src' for service in services]

# Organize by service
autoapi_root = 'services'

# Service-specific ignore patterns
service_ignores = []
for service in services:
    service_ignores.extend([
        f'*/{service}/tests/*',
        f'*/{service}/migrations/*',
        f'*/{service}/__pycache__/*',
    ])

autoapi_ignore = service_ignores + [
    '*/proto/*',  # Protocol buffer files
    '*/vendor/*', # Vendored dependencies
]

# Custom service index template
autoapi_template_dir = '_templates/microservices'

def autoapi_prepare_jinja_env(jinja_env):
    def group_by_service(modules):
        groups = {}
        for module in modules:
            service = module.name.split('.')[0]
            groups.setdefault(service, []).append(module)
        return groups

    jinja_env.filters['group_by_service'] = group_by_service
    jinja_env.globals['services'] = services
```

### API Client Library

```python
# Example: REST API client library
project = 'MyAPI Client'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.example',
    'autoapi.extension',
    'sphinx_rtd_theme',
]

# Document client modules
autoapi_dirs = ['../myapi_client']

# Focus on public API
autoapi_options = [
    'members',
    'show-inheritance',
    'show-module-summary',
]

# Skip private implementation details
autoapi_ignore = [
    '*/_internal/*',
    '*/tests/*',
    '*/_vendor/*',
]

# API client specific grouping
autoapi_member_order = 'groupwise'

# Custom templates for API methods
def autoapi_prepare_jinja_env(jinja_env):
    def format_http_method(obj):
        """Format HTTP method documentation."""
        if hasattr(obj, 'http_method'):
            return f"**{obj.http_method.upper()}** {obj.endpoint}"
        return ""

    def is_api_method(obj):
        """Check if object is an API method."""
        return hasattr(obj, 'http_method')

    jinja_env.filters['format_http_method'] = format_http_method
    jinja_env.tests['api_method'] = is_api_method

# Example usage in template:
# {% if obj is api_method %}
# {{ obj|format_http_method }}
# {% endif %}
```

---

## Conclusion

Sphinx AutoAPI provides a powerful, flexible solution for automatic API documentation generation. Its parse-only approach offers significant advantages over traditional autodoc, especially for complex projects, while its template system allows for extensive customization.

Key takeaways:

1. **Start simple** with minimal configuration and expand as needed
2. **Use templates** for custom documentation layouts
3. **Integrate with other extensions** for enhanced functionality
4. **Optimize for performance** in large codebases
5. **Monitor and troubleshoot** common issues proactively

The comprehensive configuration options and extensibility make AutoAPI suitable for projects ranging from small libraries to large enterprise applications.

For the most up-to-date information, always refer to the [official documentation](https://sphinx-autoapi.readthedocs.io/).
