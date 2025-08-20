# sphinx.ext.intersphinx - Cross-Documentation Linking

**Extension**: `sphinx.ext.intersphinx`  
**Priority**: Core Foundation (Position 4 in extensions list)  
**Official Documentation**: [sphinx.ext.intersphinx](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html)  
**Status in PyDevelop-Docs**: ✅ Implemented with comprehensive external linking

## Overview

`sphinx.ext.intersphinx` enables cross-documentation linking between different Sphinx projects. It allows documentation to reference external libraries (Python, NumPy, Pandas, etc.) with automatic link resolution, creating a connected ecosystem of documentation that enhances user experience and reduces documentation maintenance overhead.

## Core Capabilities

### 1. External Documentation Linking

- **Automatic Resolution**: Converts `:py:class:`dict`` to links to Python's documentation
- **Multi-Project Support**: Link to multiple external documentation sites
- **Role Integration**: Works with all Sphinx cross-reference roles
- **Fallback Handling**: Graceful degradation when external docs are unavailable

### 2. Inventory Management

- **Object Inventory**: Downloads and caches external documentation inventories
- **Smart Caching**: Efficient caching system for inventory files
- **Version Detection**: Handles different versions of external documentation
- **Custom Mappings**: Support for non-standard documentation URLs

### 3. Link Quality Assurance

- **Link Validation**: Verifies external links during build
- **Warning System**: Reports broken or missing external references
- **Fallback Strategies**: Configurable behavior for unresolved links

## Configuration in PyDevelop-Docs

### Current Implementation

```python
# In config.py - comprehensive intersphinx mapping
"intersphinx_mapping": _get_complete_intersphinx_mapping(),

def _get_complete_intersphinx_mapping() -> Dict[str, tuple]:
    """Get complete intersphinx mapping for cross-references."""
    return {
        "python": ("https://docs.python.org/3", None),
        "sphinx": ("https://www.sphinx-doc.org/en/master", None),
        "pydantic": ("https://docs.pydantic.dev/latest", None),
        "langchain": ("https://python.langchain.com/", None),
        "fastapi": ("https://fastapi.tiangolo.com/", None),
        # Add other Haive packages as they become available
        # "haive-core": ("https://docs.haive.ai/packages/haive-core/", None),
        # "haive-agents": ("https://docs.haive.ai/packages/haive-agents/", None),
    }
```

### Enhanced Configuration Options

```python
# Advanced intersphinx configuration for PyDevelop-Docs
intersphinx_mapping = {
    # Core Python ecosystem
    'python': ('https://docs.python.org/3', None),
    'typing': ('https://docs.python.org/3', None),

    # Documentation tools
    'sphinx': ('https://www.sphinx-doc.org/en/master', None),
    'docutils': ('https://docutils.sourceforge.io/docs/', None),

    # AI/ML Libraries
    'pydantic': ('https://docs.pydantic.dev/latest', None),
    'langchain': ('https://python.langchain.com/', None),
    'openai': ('https://platform.openai.com/docs/', None),
    'anthropic': ('https://docs.anthropic.com/', None),

    # Web frameworks
    'fastapi': ('https://fastapi.tiangolo.com/', None),
    'starlette': ('https://www.starlette.io/', None),
    'uvicorn': ('https://www.uvicorn.org/', None),

    # Data processing
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'polars': ('https://pola-rs.github.io/polars/', None),

    # Database
    'sqlalchemy': ('https://docs.sqlalchemy.org/en/20/', None),
    'asyncpg': ('https://magicstack.github.io/asyncpg/', None),
    'psycopg': ('https://www.psycopg.org/psycopg3/docs/', None),

    # Testing
    'pytest': ('https://docs.pytest.org/en/stable/', None),
    'hypothesis': ('https://hypothesis.readthedocs.io/en/latest/', None),

    # Utilities
    'click': ('https://click.palletsprojects.com/', None),
    'rich': ('https://rich.readthedocs.io/en/stable/', None),
    'typer': ('https://typer.tiangolo.com/', None),

    # Future Haive packages (when published)
    # 'haive-core': ('https://docs.haive.ai/packages/haive-core/', None),
    # 'haive-agents': ('https://docs.haive.ai/packages/haive-agents/', None),
    # 'haive-tools': ('https://docs.haive.ai/packages/haive-tools/', None),
}

# Advanced intersphinx options
intersphinx_disabled_reftypes = []  # Don't disable any reference types
intersphinx_timeout = 30  # Timeout for inventory downloads
intersphinx_cache_limit = 5  # Days to cache inventory files
intersphinx_debug = False  # Enable for debugging link resolution
```

### Dynamic Inventory Discovery

```python
# Auto-populate intersphinx from pyproject.toml dependencies
def auto_populate_intersphinx_mapping(app):
    """Automatically add intersphinx mappings from project dependencies."""
    try:
        import tomli
        from pathlib import Path

        pyproject_path = Path(app.srcdir).parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                pyproject = tomli.load(f)

            # Extract dependencies
            deps = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})

            # Known documentation URLs for common packages
            known_docs = {
                'fastapi': 'https://fastapi.tiangolo.com/',
                'pydantic': 'https://docs.pydantic.dev/latest/',
                'langchain': 'https://python.langchain.com/',
                'numpy': 'https://numpy.org/doc/stable/',
                'pandas': 'https://pandas.pydata.org/docs/',
                'pytest': 'https://docs.pytest.org/en/stable/',
                'click': 'https://click.palletsprojects.com/',
                'rich': 'https://rich.readthedocs.io/en/stable/',
            }

            # Add mappings for found dependencies
            for dep in deps:
                if dep in known_docs:
                    app.config.intersphinx_mapping[dep] = (known_docs[dep], None)

    except ImportError:
        pass  # tomli not available

def setup(app):
    app.connect('config-inited', auto_populate_intersphinx_mapping)
```

## Template Integration Opportunities

### 1. Enhanced Cross-Reference Templates

```jinja2
{# _autoapi_templates/python/class.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% endif %}

{% if obj.inheritance %}
**Inheritance:**

{% for base in obj.inheritance %}
* :py:class:`{{ base.full_name }}`
{% endfor %}

.. inheritance-diagram:: {{ obj.id }}
   :parts: 1
{% endif %}

{% if obj.related_types %}
**Related Types:**

{% for type_ref in obj.related_types %}
* :py:class:`{{ type_ref }}`
{% endfor %}
{% endif %}
```

### 2. Smart Type Linking

```jinja2
{# Enhanced type reference handling #}
{% macro format_type_annotation(type_str) %}
{% set known_types = {
    'dict': ':py:class:`dict`',
    'list': ':py:class:`list`',
    'str': ':py:class:`str`',
    'int': ':py:class:`int`',
    'float': ':py:class:`float`',
    'bool': ':py:class:`bool`',
    'BaseModel': ':py:class:`pydantic.BaseModel`',
    'Dict': ':py:class:`typing.Dict`',
    'List': ':py:class:`typing.List`',
    'Optional': ':py:class:`typing.Optional`',
    'Union': ':py:class:`typing.Union`',
    'Callable': ':py:class:`typing.Callable`',
} %}

{% if type_str in known_types %}
{{ known_types[type_str] }}
{% else %}
``{{ type_str }}``
{% endif %}
{% endmacro %}
```

### 3. Related Documentation Links

```jinja2
{# Automatic related documentation discovery #}
{% if obj.external_references %}
**See Also:**

{% for ref in obj.external_references %}
* {{ ref.formatted_link }} - {{ ref.description }}
{% endfor %}
{% endif %}

{# Common patterns section #}
{% if obj.common_usage_patterns %}
**Common Usage Patterns:**

{% for pattern in obj.common_usage_patterns %}
* :doc:`{{ pattern.doc_link }}` - {{ pattern.description }}
{% endfor %}
{% endif %}
```

## Best Practices for PyDevelop-Docs

### 1. Rich Type Documentation

```python
from typing import Dict, List, Optional, Union
from pydantic import BaseModel
import pandas as pd

class AgentConfig(BaseModel):
    """Agent configuration with comprehensive external type linking.

    This class demonstrates how intersphinx automatically creates links
    to external documentation for better user experience.

    Attributes:
        name: Agent identifier string.
        model_params: Configuration dictionary for the language model.
            See :py:class:`dict` for basic dictionary operations.
        tools: List of available tool names.
            See :py:class:`list` for list manipulation methods.
        metadata: Optional metadata for the agent.
            See :py:class:`typing.Optional` for optional type handling.
        data_frame: Optional pandas DataFrame for agent data.
            See :py:class:`pandas.DataFrame` for data manipulation methods.
    """

    name: str
    model_params: Dict[str, Union[str, int, float]]
    tools: List[str] = []
    metadata: Optional[Dict[str, Any]] = None
    data_frame: Optional[pd.DataFrame] = None

    class Config:
        """Pydantic configuration.

        See :py:class:`pydantic.BaseConfig` for all available options.
        """
        arbitrary_types_allowed = True
```

### 2. Cross-Framework Integration

```python
from fastapi import FastAPI, HTTPException
from langchain.llms import OpenAI
from pydantic import ValidationError

async def create_agent_endpoint(
    app: FastAPI,
    agent_config: AgentConfig
) -> Dict[str, Any]:
    """Create agent endpoint for FastAPI application.

    This function demonstrates cross-framework documentation linking
    where intersphinx automatically resolves references to external
    frameworks and libraries.

    Args:
        app: FastAPI application instance.
            See :py:class:`fastapi.FastAPI` for application configuration.
        agent_config: Agent configuration object.
            See :py:class:`pydantic.BaseModel` for validation features.

    Returns:
        Dictionary containing endpoint creation status.
        See :py:class:`dict` for dictionary operations.

    Raises:
        ValidationError: If agent configuration is invalid.
            See :py:exc:`pydantic.ValidationError` for error handling.
        HTTPException: If endpoint creation fails.
            See :py:exc:`fastapi.HTTPException` for HTTP error responses.

    Example:
        Create an agent endpoint:

        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> config = AgentConfig(name="test-agent")
        >>> result = await create_agent_endpoint(app, config)
        >>> result['status']
        'created'

    Note:
        This endpoint integrates with :py:class:`langchain.llms.OpenAI`
        for language model functionality.
    """
    try:
        # Implementation with automatic type linking
        llm = OpenAI(temperature=agent_config.temperature)
        # FastAPI and LangChain references automatically linked
        return {"status": "created", "agent_id": agent_config.name}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
```

### 3. Advanced Cross-Reference Usage

```python
def process_with_external_libraries(
    data: pd.DataFrame,
    config: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Process data using external libraries with full documentation links.

    Args:
        data: Input pandas DataFrame.
            See :py:class:`pandas.DataFrame` for data manipulation methods.
            Common operations: :py:meth:`pandas.DataFrame.groupby`,
            :py:meth:`pandas.DataFrame.merge`, :py:meth:`pandas.DataFrame.apply`.
        config: Configuration dictionary.
            See :py:class:`dict` for dictionary operations.
            Use :py:meth:`dict.get` for safe key access.

    Returns:
        List of processing results.
        See :py:class:`list` for list operations and
        :py:meth:`list.append` for adding results.

    Example:
        Process agent conversation data:

        >>> import pandas as pd
        >>> data = pd.DataFrame({'messages': ['hello', 'world']})
        >>> config = {'model': 'gpt-4', 'temperature': 0.7}
        >>> results = process_with_external_libraries(data, config)
        >>> len(results) > 0
        True

    See Also:
        :py:mod:`pandas` - Data manipulation library
        :py:mod:`typing` - Type hint utilities
        :doc:`guides/data-processing` - Data processing guide
    """
```

## Enhancement Opportunities

### 1. Intelligent Link Resolution

```python
def enhanced_link_resolver(app, env, node, contnode):
    """Enhanced intersphinx link resolution with fallbacks."""

    # Try standard intersphinx resolution first
    result = standard_resolve(app, env, node, contnode)
    if result:
        return result

    # Custom fallback strategies
    target = node.get('reftarget', '')

    # Try common documentation patterns
    fallback_urls = {
        'numpy': 'https://numpy.org/doc/stable/reference/generated/',
        'pandas': 'https://pandas.pydata.org/docs/reference/api/',
        'sklearn': 'https://scikit-learn.org/stable/modules/generated/',
    }

    for lib, base_url in fallback_urls.items():
        if target.startswith(lib):
            return create_fallback_link(base_url, target)

    return None

def setup(app):
    app.connect('missing-reference', enhanced_link_resolver)
```

### 2. Documentation Quality Metrics

```python
def analyze_external_links(app, exception):
    """Analyze external link usage and quality."""
    if exception:
        return

    # Count external references by library
    external_refs = {}
    total_refs = 0

    for docname in app.env.all_docs:
        doc = app.env.get_doctree(docname)
        for ref_node in doc.traverse(addnodes.pending_xref):
            if ref_node.get('refdomain') == 'py':
                target = ref_node.get('reftarget', '')
                if '.' in target:
                    lib = target.split('.')[0]
                    external_refs[lib] = external_refs.get(lib, 0) + 1
                    total_refs += 1

    # Report statistics
    app.info(f"External references: {total_refs}")
    for lib, count in sorted(external_refs.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_refs) * 100
        app.info(f"  {lib}: {count} ({percentage:.1f}%)")

def setup(app):
    app.connect('build-finished', analyze_external_links)
```

### 3. Custom Documentation Patterns

```python
def add_haive_specific_references(app):
    """Add Haive-specific intersphinx patterns."""

    # Custom reference resolver for Haive components
    def resolve_haive_reference(app, env, node, contnode):
        target = node.get('reftarget', '')

        if target.startswith('haive.'):
            # Map to appropriate Haive package documentation
            package_map = {
                'haive.core': 'haive-core',
                'haive.agents': 'haive-agents',
                'haive.tools': 'haive-tools',
                'haive.games': 'haive-games',
            }

            for prefix, package in package_map.items():
                if target.startswith(prefix):
                    base_url = f"https://docs.haive.ai/packages/{package}/"
                    return create_package_link(base_url, target)

        return None

    app.connect('missing-reference', resolve_haive_reference)

def setup(app):
    add_haive_specific_references(app)
```

## Current Implementation Status

### ✅ Working Features

- [x] **Core library linking** - Python, Sphinx, Pydantic working
- [x] **AI/ML library support** - LangChain, FastAPI, OpenAI references
- [x] **Automatic inventory downloads** - External doc inventories cached
- [x] **Cross-reference validation** - Broken links detected during build
- [x] **Type annotation linking** - Rich type references with links

### 🔄 Enhancement Opportunities

- [ ] **Dynamic inventory discovery** - Auto-detect dependencies for linking
- [ ] **Haive inter-package linking** - Link between Haive package docs
- [ ] **Link quality metrics** - Track external reference usage
- [ ] **Fallback strategies** - Better handling of missing external docs
- [ ] **Performance optimization** - Faster inventory processing

### 📋 Template Integration Tasks

1. **Enhanced AutoAPI templates** with rich external type linking
2. **Haive package cross-references** for inter-package documentation
3. **Link quality analysis** for documentation health monitoring
4. **Custom reference patterns** for domain-specific linking

## Integration with AutoAPI

### External Type Linking

```jinja2
{# Automatic external type linking in templates #}
{% for param in obj.parameters %}
**{{ param.name }}** ({{ param.type|auto_link_types }}) -- {{ param.description }}

{% if param.type_info.external_docs %}
See :py:class:`{{ param.type_info.external_reference }}` for details.
{% endif %}
{% endfor %}
```

### Related Documentation Discovery

```jinja2
{# Discover and link related external documentation #}
{% if obj.uses_external_libraries %}
**External Dependencies:**

{% for lib in obj.external_libraries %}
* :py:mod:`{{ lib.name }}` - {{ lib.description }}

  Common classes: {% for cls in lib.common_classes %}:py:class:`{{ cls }}` {% endfor %}
{% endfor %}
{% endif %}
```

## Performance Considerations

### Build Time Optimization

```python
# Optimize intersphinx for faster builds
intersphinx_cache_limit = 1  # Cache inventories for 1 day
intersphinx_timeout = 10     # Shorter timeout for faster builds

# Disable during development
intersphinx_disabled_reftypes = ['py:class', 'py:func'] if app.debug else []
```

### Memory Usage

```python
# Reduce memory usage for large external inventories
def filter_inventory_objects(inventory):
    """Filter inventory to only include commonly used objects."""
    common_objects = {
        'python': ['dict', 'list', 'str', 'int', 'float', 'bool'],
        'pydantic': ['BaseModel', 'Field', 'validator'],
        'fastapi': ['FastAPI', 'APIRouter', 'HTTPException'],
    }

    filtered = {}
    for domain, objects in inventory.items():
        if domain in common_objects:
            filtered[domain] = {
                k: v for k, v in objects.items()
                if k in common_objects[domain]
            }

    return filtered
```

## Troubleshooting

### Common Issues

1. **Inventory Download Failures**: Network issues or incorrect URLs
2. **Broken Cross-References**: Missing objects in external documentation
3. **Version Mismatches**: External docs version incompatibility
4. **Performance Issues**: Large inventories slowing builds

### Debug Configuration

```python
# Debug intersphinx processing
intersphinx_debug = True
intersphinx_timeout = 60  # Longer timeout for debugging

# Log inventory contents
import logging
logging.getLogger('sphinx.ext.intersphinx').setLevel(logging.DEBUG)
```

## Integration with Issue #6

For AutoAPI template customization (Issue #6), intersphinx provides:

1. **Rich Type Linking**: Automatic external documentation links in templates
2. **Cross-Reference Data**: Access to resolved reference information
3. **Library Integration**: Seamless linking to external library documentation
4. **Documentation Quality**: Enhanced user experience through connected documentation

Intersphinx enables AutoAPI templates to create documentation that feels like part of a larger, interconnected ecosystem rather than isolated API reference.
