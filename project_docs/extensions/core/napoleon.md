# sphinx.ext.napoleon - Google & NumPy Docstring Support

**Extension**: `sphinx.ext.napoleon`  
**Priority**: Core Foundation (Position 2 in extensions list)  
**Official Documentation**: [sphinx.ext.napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)  
**Status in PyDevelop-Docs**: ✅ Implemented with comprehensive Google/NumPy style configuration

## Overview

`sphinx.ext.napoleon` extends autodoc to parse and format Google-style and NumPy-style docstrings, converting them into reStructuredText format that Sphinx can process. This extension is essential for modern Python documentation, as it allows developers to write more readable docstrings while maintaining full Sphinx compatibility.

## Core Capabilities

### 1. Docstring Style Support

- **Google Style**: Clean, readable format used by Google and many modern Python projects
- **NumPy Style**: Scientific computing style with section-based organization
- **Mixed Support**: Can handle both styles within the same project
- **RST Integration**: Converts both styles to proper reStructuredText

### 2. Section Processing

- **Args/Parameters**: Automatic parameter documentation with types
- **Returns/Yields**: Return value documentation with type information
- **Raises/Except**: Exception documentation with descriptions
- **Note/Warning**: Admonition creation from docstring sections
- **Examples**: Code block formatting for usage examples

### 3. Type Annotation Integration

- **Type Hints**: Seamless integration with Python type annotations
- **Cross-References**: Automatic linking to documented types
- **Generic Support**: Proper handling of generic types and unions

## Configuration in PyDevelop-Docs

### Current Implementation

```python
# In config.py - comprehensive Napoleon configuration
"napoleon_google_docstring": True,    # Enable Google-style parsing
"napoleon_numpy_docstring": True,     # Enable NumPy-style parsing
"napoleon_include_init_with_doc": False,  # Don't duplicate __init__ docs
"napoleon_include_private_with_doc": False,  # Skip private member docs
```

### Enhanced Configuration Options

```python
# Advanced Napoleon configuration for PyDevelop-Docs
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True  # Include special methods
napoleon_use_admonition_for_examples = True  # Format examples as admonitions
napoleon_use_admonition_for_notes = True    # Format notes as admonitions
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False  # Don't use :ivar: for instance variables
napoleon_use_param = True  # Use :param: for parameters
napoleon_use_rtype = True  # Use :rtype: for return types
napoleon_use_keyword = True  # Use :keyword: for keyword arguments
napoleon_preprocess_types = True  # Preprocess type annotations
napoleon_type_aliases = {  # Custom type aliases
    'array_like': ':class:`numpy.ndarray`',
    'callable': ':py:class:`collections.abc.Callable`',
}
napoleon_custom_sections = [  # Additional custom sections
    'Technical Details',
    'Implementation Notes',
    'Memory Considerations',
    'Performance',
]
```

## Docstring Style Examples

### 1. Google Style (Recommended)

```python
def process_agent_workflow(
    agent_config: AgentConfig,
    input_data: Dict[str, Any],
    timeout: float = 30.0
) -> WorkflowResult:
    """Process an agent workflow with comprehensive validation.

    This function demonstrates the Google docstring style that Napoleon
    processes into beautiful Sphinx documentation. The format is clean,
    readable, and integrates perfectly with type hints.

    Args:
        agent_config: Configuration object containing agent parameters.
            Must include valid model settings and tool configurations.
        input_data: Dictionary containing workflow input data.
            Expected keys: 'messages', 'context', 'metadata'.
        timeout: Maximum execution time in seconds. Defaults to 30.0.
            Set to 0 for unlimited execution time.

    Returns:
        WorkflowResult: Complete workflow execution result containing:
            - status: Execution status ('success', 'error', 'timeout')
            - output: Agent response data
            - metadata: Execution metrics and timing information
            - error: Error details if execution failed

    Raises:
        ConfigurationError: If agent_config is invalid or incomplete.
        ValidationError: If input_data fails validation checks.
        TimeoutError: If execution exceeds the specified timeout.
        AgentExecutionError: If agent encounters runtime errors.

    Example:
        Basic workflow execution:

        >>> config = AgentConfig(model="gpt-4", temperature=0.7)
        >>> data = {"messages": [{"role": "user", "content": "Hello"}]}
        >>> result = process_agent_workflow(config, data)
        >>> print(result.status)
        'success'

        With custom timeout:

        >>> result = process_agent_workflow(config, data, timeout=60.0)
        >>> result.metadata['execution_time'] < 60.0
        True

    Note:
        This function is thread-safe and can be called concurrently.
        For production use, consider implementing retry logic for
        transient failures.

    Warning:
        Large input datasets may cause memory issues. Consider
        chunking data for inputs larger than 1MB.

    See Also:
        :class:`AgentConfig`: Configuration object documentation
        :func:`validate_workflow_input`: Input validation function
        :doc:`/guides/workflow-patterns`: Workflow pattern guide
    """
```

### 2. NumPy Style (Scientific Computing)

```python
def calculate_similarity_matrix(
    embeddings: np.ndarray,
    metric: str = 'cosine'
) -> np.ndarray:
    """Calculate similarity matrix between embeddings.

    Parameters
    ----------
    embeddings : np.ndarray, shape (n_samples, n_features)
        Input embeddings matrix where each row represents an embedding vector.
        Must be 2-dimensional with consistent feature dimensions.
    metric : {'cosine', 'euclidean', 'manhattan'}, default='cosine'
        Distance metric to use for similarity calculation.

    Returns
    -------
    np.ndarray, shape (n_samples, n_samples)
        Symmetric similarity matrix with values in [0, 1] for cosine similarity
        or distance values for other metrics.

    Raises
    ------
    ValueError
        If embeddings is not 2-dimensional or contains invalid values.
    NotImplementedError
        If specified metric is not supported.

    Examples
    --------
    >>> embeddings = np.random.rand(5, 10)
    >>> similarity = calculate_similarity_matrix(embeddings)
    >>> similarity.shape
    (5, 5)
    >>> np.allclose(similarity, similarity.T)  # Check symmetry
    True

    For different metrics:

    >>> cosine_sim = calculate_similarity_matrix(embeddings, 'cosine')
    >>> euclidean_sim = calculate_similarity_matrix(embeddings, 'euclidean')

    Notes
    -----
    The cosine similarity is calculated as:

    .. math::
        sim(A, B) = \\frac{A \\cdot B}{||A|| ||B||}

    For performance considerations with large matrices, consider using
    batch processing or approximate methods.
    """
```

## Template Integration Opportunities

### 1. Enhanced AutoAPI Templates

```jinja2
{# _autoapi_templates/python/function.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% endif %}

.. py:function:: {{ obj.id }}{{ obj.args }}

   {% if obj.docstring %}
   {{ obj.docstring|prepare_docstring|indent(3) }}
   {% endif %}

   {% if obj.parameters %}
   **Parameters:**

   {% for param in obj.parameters %}
   * **{{ param.name }}** ({{ param.type }}) -- {{ param.description }}
   {% endfor %}
   {% endif %}
```

### 2. Class Method Templates

```jinja2
{# Enhanced class method documentation #}
{% for method in obj.methods %}
{% if method.docstring %}

{{ method.name }}
{{ "-" * method.name|length }}

{{ method.docstring|prepare_docstring|indent(0) }}

{% endif %}
{% endfor %}
```

### 3. Custom Section Processing

```jinja2
{# Process custom Napoleon sections #}
{% if obj.technical_details %}
**Technical Details:**

{{ obj.technical_details|prepare_docstring|indent(0) }}
{% endif %}

{% if obj.performance %}
**Performance Considerations:**

{{ obj.performance|prepare_docstring|indent(0) }}
{% endif %}
```

## Best Practices for PyDevelop-Docs

### 1. Consistent Style Choice

```python
# Choose Google style for readability and modern Python conventions
class AgentBase:
    """Base class for all Haive agents.

    This class provides the foundation for agent implementations with
    consistent interface patterns and configuration management.

    Args:
        name: Unique identifier for the agent instance.
        config: Agent configuration object with model and tool settings.

    Attributes:
        name: The agent's unique identifier.
        config: Current agent configuration.
        state: Current execution state of the agent.

    Example:
        Create a basic agent:

        >>> config = AgentConfig(model="gpt-4")
        >>> agent = AgentBase("my-agent", config)
        >>> agent.name
        'my-agent'
    """
```

### 2. Type Information Integration

```python
def create_multi_agent(
    agents: List[Union[SimpleAgent, ReactAgent]],
    coordination_mode: Literal["sequential", "parallel"] = "sequential"
) -> MultiAgent:
    """Create a multi-agent system from individual agents.

    Args:
        agents: List of agent instances to coordinate. All agents must
            have unique names and compatible configurations.
        coordination_mode: How agents should be coordinated:
            * "sequential": Execute agents one after another
            * "parallel": Execute agents concurrently

    Returns:
        MultiAgent: Configured multi-agent system ready for execution.

    Raises:
        ValueError: If agents list is empty or contains duplicate names.
        ConfigurationError: If agent configurations are incompatible.
    """
```

### 3. Rich Example Documentation

```python
class ReactAgent:
    """React-style reasoning agent with tool integration.

    Example:
        Basic agent with calculator tool:

        >>> from haive.tools import Calculator
        >>> agent = ReactAgent(
        ...     name="math-assistant",
        ...     model="gpt-4",
        ...     tools=[Calculator()]
        ... )
        >>> result = agent.run("What is 15 * 23?")
        >>> "345" in result.response
        True

        Multi-step reasoning:

        >>> agent = ReactAgent(
        ...     name="researcher",
        ...     model="gpt-4",
        ...     tools=[WebSearch(), Calculator(), FileReader()]
        ... )
        >>> result = agent.run("Research Python trends and calculate growth rate")
        >>> result.tool_calls_made > 1  # Used multiple tools
        True

    Note:
        React agents work best with clear, specific instructions and
        access to relevant tools for the task domain.
    """
```

## Enhancement Opportunities

### 1. Custom Section Handlers

```python
def napoleon_process_custom_section(lines):
    """Process custom docstring sections for PyDevelop-Docs."""
    # Implementation Notes section
    if lines[0].strip() == 'Implementation Notes:':
        return _format_implementation_notes(lines[1:])

    # Performance section
    if lines[0].strip() == 'Performance:':
        return _format_performance_section(lines[1:])

    return lines

# Register custom section processor
def setup(app):
    app.connect('napoleon-process-docstring', napoleon_process_custom_section)
```

### 2. Type Alias Expansion

```python
# Enhanced type aliases for common Haive types
napoleon_type_aliases = {
    'AgentConfig': ':class:`~haive.core.config.AgentConfig`',
    'StateSchema': ':class:`~haive.core.schema.StateSchema`',
    'ToolResult': ':class:`~haive.core.tools.ToolResult`',
    'MessageList': ':class:`List[BaseMessage] <typing.List>`',
    'ToolList': ':class:`List[Tool] <typing.List>`',
    'ConfigDict': ':class:`Dict[str, Any] <typing.Dict>`',
}
```

### 3. Enhanced Example Processing

```python
def process_examples_with_execution(app, what, name, obj, options, lines):
    """Enhanced example processing with execution validation."""
    in_example = False
    example_lines = []

    for i, line in enumerate(lines):
        if line.strip() in ['Example:', 'Examples:']:
            in_example = True
            continue

        if in_example:
            if line and not line[0].isspace():
                # Process accumulated example
                if example_lines:
                    processed = _validate_example_code(example_lines)
                    lines[i-len(example_lines):i] = processed
                in_example = False
                example_lines = []
            else:
                example_lines.append(line)
```

## Current Implementation Status

### ✅ Working Features

- [x] **Google docstring parsing** - Fully functional
- [x] **NumPy docstring parsing** - Fully functional
- [x] **Type annotation integration** - Works with autodoc
- [x] **Custom sections** - Basic support implemented
- [x] **Example formatting** - Code blocks properly formatted
- [x] **Cross-references** - Automatic linking works

### 🔄 Enhancement Opportunities

- [ ] **Custom section handlers** - More sophisticated section processing
- [ ] **Enhanced type aliases** - Better type linking for Haive components
- [ ] **Example validation** - Runtime validation of example code
- [ ] **Documentation metrics** - Track docstring quality and coverage
- [ ] **Interactive examples** - Integration with execution extensions

### 📋 Template Integration Tasks

1. **Enhance AutoAPI templates** to better leverage Napoleon's parsed structure
2. **Create custom section processors** for Haive-specific documentation patterns
3. **Improve type linking** with comprehensive type aliases
4. **Add example validation** to ensure code examples remain functional

## Integration with AutoAPI

### Parsed Structure Access

```jinja2
{# Access Napoleon's parsed docstring structure in templates #}
{% if obj.napoleon_parsed %}
   {% if obj.napoleon_parsed.args %}
   **Parameters:**

   {% for arg in obj.napoleon_parsed.args %}
   * **{{ arg.name }}** ({{ arg.type }}) -- {{ arg.description }}
   {% endfor %}
   {% endif %}

   {% if obj.napoleon_parsed.returns %}
   **Returns:**
   {{ obj.napoleon_parsed.returns.description }}
   {% endif %}
{% endif %}
```

### Enhanced Rendering

```jinja2
{# Custom rendering for Napoleon sections #}
{% macro render_google_docstring(obj) %}
   {% if obj.docstring %}
   {{ obj.short_description }}

   {% if obj.long_description %}
   {{ obj.long_description }}
   {% endif %}

   {% if obj.parameters %}
   Args:
   {% for param in obj.parameters %}
       {{ param.name }} ({{ param.type }}): {{ param.description }}
   {% endfor %}
   {% endif %}

   {% if obj.returns %}
   Returns:
       {{ obj.returns.type }}: {{ obj.returns.description }}
   {% endif %}
   {% endif %}
{% endmacro %}
```

## Performance Considerations

### Build Time Optimization

```python
# Optimize Napoleon for faster builds
napoleon_preprocess_types = False  # Disable type preprocessing for speed
napoleon_use_admonition_for_examples = False  # Simpler example formatting
```

### Memory Usage

```python
# Reduce memory usage for large codebases
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
```

## Troubleshooting

### Common Issues

1. **Malformed Docstrings**: Napoleon is strict about section formatting
2. **Type Reference Failures**: Ensure proper imports and type aliases
3. **Section Recognition**: Custom sections need proper registration
4. **Cross-Reference Issues**: Check intersphinx mapping for external types

### Debug Configuration

```python
# Debug Napoleon processing
napoleon_debug_sections = True  # Enable section debugging
napoleon_custom_sections = []   # Clear custom sections if causing issues
```

## Integration with Issue #6

For AutoAPI template customization (Issue #6), Napoleon provides:

1. **Structured Docstring Data**: Access to parsed sections and parameters
2. **Type Information**: Rich type data for template rendering
3. **Section Processing**: Custom section handling for domain-specific documentation
4. **Cross-Reference Support**: Automatic linking and type resolution

Napoleon transforms raw docstrings into structured data that AutoAPI templates can leverage for sophisticated, consistent documentation generation.
