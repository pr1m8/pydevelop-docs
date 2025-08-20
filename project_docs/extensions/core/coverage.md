# sphinx.ext.coverage - Documentation Coverage Analysis

**Extension**: `sphinx.ext.coverage`  
**Priority**: Core Foundation (Position 6 in extensions list)  
**Official Documentation**: [sphinx.ext.coverage](https://www.sphinx-doc.org/en/master/usage/extensions/coverage.html)  
**Status in PyDevelop-Docs**: ✅ Implemented for documentation quality assurance

## Overview

`sphinx.ext.coverage` analyzes documentation coverage by comparing documented objects with actual Python code objects. It identifies undocumented modules, classes, functions, and methods, providing detailed reports to help maintain comprehensive documentation. This extension is essential for ensuring documentation quality and completeness in large codebases.

## Core Capabilities

### 1. Coverage Analysis

- **Module Coverage**: Identifies undocumented modules and packages
- **Class Coverage**: Tracks documented vs undocumented classes
- **Function Coverage**: Analyzes function and method documentation
- **Attribute Coverage**: Checks documentation for class and module attributes

### 2. Detailed Reporting

- **Coverage Statistics**: Percentage coverage by type and module
- **Undocumented Items**: Lists all undocumented objects
- **Coverage Trends**: Track documentation progress over time
- **Quality Metrics**: Comprehensive documentation health assessment

### 3. Filtering and Control

- **Selective Analysis**: Choose which modules to analyze
- **Pattern Matching**: Include/exclude objects based on patterns
- **Inheritance Handling**: Control how inherited documentation is counted
- **Private Member Control**: Configure analysis of private objects

## Configuration in PyDevelop-Docs

### Current Implementation

```python
# In config.py - coverage extension included in core
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",  # Documentation coverage analysis
    # ... other extensions
]

# Basic coverage configuration (uses defaults)
# Standard coverage analysis enabled
```

### Enhanced Configuration Options

```python
# Advanced coverage configuration for PyDevelop-Docs
coverage_modules = [
    'haive.core',
    'haive.agents',
    'haive.tools',
    'haive.games',
    'haive.dataflow',
    'haive.mcp',
    'haive.prebuilt'
]

# Coverage analysis settings
coverage_ignore_modules = [
    '*.tests.*',
    '*.test_*',
    '*.__pycache__.*',
    '*.migrations.*',
    '*.vendored.*'
]

coverage_ignore_functions = [
    '__repr__',
    '__str__',
    '__unicode__',
    '__init__',  # Often inherit docstring from class
]

coverage_ignore_classes = [
    '*.Meta',
    '*.Config',
    '*Test*',
    '*Mock*'
]

# Coverage reporting options
coverage_show_missing_items = True
coverage_write_headline = True
coverage_include_undoc_from_autodoc = True

# Advanced coverage options
coverage_report_functions = True
coverage_report_classes = True
coverage_report_constants = True
coverage_report_methods = True
coverage_report_properties = True

# Coverage thresholds for CI/CD
coverage_minimum_percentage = 80.0
coverage_fail_under = 75.0  # Fail build if below this threshold

# Coverage statistics collection
coverage_statistics_to_stdout = True
coverage_statistics_to_file = 'coverage-stats.json'

# Inheritance handling
coverage_count_inherited_members = False  # Don't count inherited docs as coverage
coverage_ignore_inherited_private = True
```

### CI/CD Integration

```python
# Different coverage configurations for different environments
import os

if os.environ.get('CI'):
    # Strict coverage for CI builds
    coverage_fail_under = 80.0
    coverage_show_missing_items = True
    coverage_statistics_to_stdout = True
else:
    # Relaxed coverage for development
    coverage_fail_under = 60.0
    coverage_show_missing_items = False
```

## Template Integration Opportunities

### 1. Coverage-Aware AutoAPI Templates

```jinja2
{# _autoapi_templates/python/module.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{# Coverage statistics for this module #}
{% set coverage_stats = obj.get_coverage_statistics() %}
.. admonition:: Documentation Coverage
   :class: coverage-stats

   **Overall:** {{ coverage_stats.percentage }}% ({{ coverage_stats.documented }}/{{ coverage_stats.total }} objects)

   * Classes: {{ coverage_stats.classes.percentage }}%
   * Functions: {{ coverage_stats.functions.percentage }}%
   * Methods: {{ coverage_stats.methods.percentage }}%

   {% if coverage_stats.percentage < 80 %}
   .. warning:: This module needs more documentation coverage.
   {% endif %}

{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% else %}
.. warning:: **Missing Module Documentation**

   This module lacks a comprehensive docstring. Add module-level
   documentation to improve coverage score.
{% endif %}

{# Undocumented items section #}
{% set undocumented = obj.get_undocumented_items() %}
{% if undocumented %}
.. admonition:: Undocumented Items
   :class: coverage-missing

   The following items need documentation:

   {% for item in undocumented %}
   * ``{{ item.name }}`` ({{ item.type }}) - Missing {{ item.missing_elements|join(", ") }}
   {% endfor %}

   Use the :ref:`documentation-guidelines` to add proper documentation.
{% endif %}
```

### 2. Class Coverage Templates

```jinja2
{# _autoapi_templates/python/class.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{# Class coverage analysis #}
{% set class_coverage = obj.analyze_documentation_coverage() %}
.. container:: coverage-indicator

   .. admonition:: Documentation Status
      :class: coverage-{{ class_coverage.status }}

      **Coverage:** {{ class_coverage.percentage }}%
      **Status:** {{ class_coverage.status|title }}

      {% if class_coverage.missing_elements %}
      **Missing:**
      {% for element in class_coverage.missing_elements %}
      * {{ element }}
      {% endfor %}
      {% endif %}

{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% else %}
.. error:: **Missing Class Documentation**

   This class requires comprehensive documentation including:

   * Purpose and functionality description
   * Constructor parameter documentation
   * Usage examples
   * Related classes and inheritance information

   **Impact on Coverage:** -30 points
{% endif %}

{# Method coverage section #}
{% if obj.methods %}
Methods
-------

{% for method in obj.methods %}
{% set method_coverage = method.get_coverage_score() %}
{% if method_coverage.percentage < 50 %}
.. admonition:: Low Documentation Coverage
   :class: coverage-warning

   Method ``{{ method.name }}`` has {{ method_coverage.percentage }}% coverage.
   Missing: {{ method_coverage.missing_elements|join(", ") }}
{% endif %}

{{ method.render()|indent(0) }}
{% endfor %}
{% endif %}
```

### 3. Function Coverage Templates

```jinja2
{# Enhanced function documentation with coverage analysis #}
{% macro render_function_with_coverage(func) %}
{% set coverage = func.analyze_coverage() %}

.. py:function:: {{ func.signature }}

   {% if func.docstring %}
   {{ func.docstring|prepare_docstring|indent(3) }}
   {% else %}
   .. error:: **Undocumented Function**

      This function needs documentation including:

      * Purpose and behavior description
      * Parameter types and descriptions
      * Return value documentation
      * Usage examples

      **Coverage Impact:** This reduces module coverage by {{ coverage.penalty }}%
   {% endif %}

   {% if coverage.completeness < 80 %}
   .. admonition:: Coverage Analysis
      :class: coverage-analysis

      **Completeness:** {{ coverage.completeness }}%

      {% if not coverage.has_param_docs %}
      * ❌ Parameter documentation missing
      {% endif %}
      {% if not coverage.has_return_docs %}
      * ❌ Return value documentation missing
      {% endif %}
      {% if not coverage.has_examples %}
      * ❌ Usage examples missing
      {% endif %}
      {% if not coverage.has_exception_docs %}
      * ⚠️ Exception documentation recommended
      {% endif %}
   {% endif %}
{% endmacro %}
```

## Best Practices for PyDevelop-Docs

### 1. Comprehensive Module Documentation

```python
"""Agent configuration management module.

This module provides comprehensive configuration management for Haive agents,
including validation, serialization, and environment-specific settings.

The module supports various configuration sources:
* Environment variables
* Configuration files (YAML, JSON, TOML)
* Direct programmatic configuration
* Runtime configuration updates

Example:
    Basic agent configuration:

    >>> from haive.config import AgentConfig
    >>> config = AgentConfig.from_file("agent.yaml")
    >>> config.validate()
    True

    Environment-based configuration:

    >>> config = AgentConfig.from_env()
    >>> config.model_name
    'gpt-4'

Note:
    This module requires proper environment setup. See the
    :doc:`/guides/configuration` guide for details.

Coverage Target: 95% (critical infrastructure module)
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import os

class AgentConfig:
    """Agent configuration with comprehensive validation.

    This class manages all aspects of agent configuration, from basic
    model selection to advanced tool integration settings.

    Args:
        model_name: Name of the language model to use.
            Must be one of the supported models listed in :data:`SUPPORTED_MODELS`.
        temperature: Sampling temperature for model responses.
            Range: 0.0 (deterministic) to 2.0 (highly creative).
        tools: List of tool names to make available to the agent.
            See :mod:`haive.tools` for available tools.
        max_tokens: Maximum tokens for model responses.
            Set to None for model defaults.

    Attributes:
        model_name: The configured language model name.
        temperature: Current temperature setting.
        tools: List of available tool configurations.
        validation_errors: List of configuration validation errors.

    Example:
        Create and validate a configuration:

        >>> config = AgentConfig(
        ...     model_name="gpt-4",
        ...     temperature=0.7,
        ...     tools=["calculator", "web_search"]
        ... )
        >>> config.validate()
        True
        >>> config.is_valid
        True

        Load from file:

        >>> config = AgentConfig.from_file("config.yaml")
        >>> config.model_name
        'gpt-4'

    Note:
        Configuration validation is performed automatically during
        initialization and can be re-run with :meth:`validate`.

    See Also:
        :class:`ToolConfig`: Individual tool configuration
        :func:`load_default_config`: Load system default configuration
        :doc:`/guides/configuration`: Complete configuration guide
    """

    def __init__(
        self,
        model_name: str,
        temperature: float = 0.7,
        tools: Optional[List[str]] = None,
        max_tokens: Optional[int] = None
    ) -> None:
        """Initialize agent configuration with validation."""
        self.model_name = model_name
        self.temperature = temperature
        self.tools = tools or []
        self.max_tokens = max_tokens
        self.validation_errors: List[str] = []

        # Automatic validation
        self.validate()

    def validate(self) -> bool:
        """Validate configuration parameters.

        Performs comprehensive validation of all configuration parameters
        including model availability, parameter ranges, and tool compatibility.

        Returns:
            bool: True if configuration is valid, False otherwise.

        Note:
            Validation errors are stored in :attr:`validation_errors` and
            can be inspected for detailed error information.

        Example:
            Validate and handle errors:

            >>> config = AgentConfig("invalid-model")
            >>> if not config.validate():
            ...     for error in config.validation_errors:
            ...         print(f"Error: {error}")
            Error: Unknown model: invalid-model
        """
        self.validation_errors.clear()

        # Model validation
        if self.model_name not in SUPPORTED_MODELS:
            self.validation_errors.append(f"Unknown model: {self.model_name}")

        # Temperature validation
        if not 0.0 <= self.temperature <= 2.0:
            self.validation_errors.append(f"Temperature must be 0.0-2.0, got {self.temperature}")

        # Tool validation
        for tool in self.tools:
            if not self._is_tool_available(tool):
                self.validation_errors.append(f"Tool not available: {tool}")

        return len(self.validation_errors) == 0

    @property
    def is_valid(self) -> bool:
        """Check if configuration is currently valid.

        Returns:
            bool: True if configuration has no validation errors.
        """
        return len(self.validation_errors) == 0
```

### 2. Progressive Documentation Enhancement

```python
class MultiAgentCoordinator:
    """Multi-agent coordination system.

    .. note:: Documentation Coverage: 75%
       This class needs additional examples and method documentation
       to reach the 90% target for core components.
    """

    def __init__(self, agents: List[Agent]) -> None:
        """Initialize coordinator with agent list.

        Args:
            agents: List of agent instances to coordinate.
        """
        self.agents = agents

    def coordinate_sequential(self, input_data: Any) -> CoordinationResult:
        """Execute agents in sequential order.

        .. todo:: Add comprehensive documentation
           :category: api
           :priority: high

           Missing documentation elements:
           * Detailed parameter description
           * Return value structure
           * Error handling behavior
           * Usage examples

           Current coverage: 40% (needs +50% to meet target)
        """
        # Implementation here
        pass

    def coordinate_parallel(self, input_data: Any) -> CoordinationResult:
        """Execute agents in parallel with synchronization.

        Executes all registered agents concurrently and synchronizes
        their results according to the configured coordination strategy.

        Args:
            input_data: Input data to distribute to all agents.
                Can be any JSON-serializable object.

        Returns:
            CoordinationResult: Aggregated results from all agents including:
                * individual_results: List of results from each agent
                * aggregated_result: Combined/merged result
                * execution_metadata: Timing and coordination statistics
                * errors: Any errors encountered during execution

        Raises:
            CoordinationError: If agent coordination fails.
            TimeoutError: If any agent exceeds the configured timeout.

        Example:
            Basic parallel coordination:

            >>> coordinator = MultiAgentCoordinator([agent1, agent2, agent3])
            >>> result = coordinator.coordinate_parallel({"task": "analyze"})
            >>> len(result.individual_results)
            3
            >>> result.aggregated_result is not None
            True

        Note:
            Parallel execution uses asyncio for concurrency. Ensure all
            agents support async execution or use the sync wrapper.

        Coverage: 95% (meets target for core coordination methods)
        """
        # Comprehensive implementation here
        pass
```

## Enhancement Opportunities

### 1. Advanced Coverage Metrics

```python
def setup_advanced_coverage_analysis(app):
    """Setup enhanced coverage analysis with custom metrics."""

    class DocumentationQualityAnalyzer:
        """Analyze documentation quality beyond basic coverage."""

        def __init__(self, app):
            self.app = app
            self.quality_metrics = {}

        def analyze_module_quality(self, module_name):
            """Analyze comprehensive documentation quality for a module."""
            metrics = {
                'basic_coverage': self.calculate_basic_coverage(module_name),
                'docstring_quality': self.analyze_docstring_quality(module_name),
                'example_coverage': self.analyze_example_coverage(module_name),
                'type_annotation_coverage': self.analyze_type_coverage(module_name),
                'cross_reference_density': self.analyze_cross_references(module_name),
                'external_link_coverage': self.analyze_external_links(module_name)
            }

            # Calculate composite quality score
            weights = {
                'basic_coverage': 0.3,
                'docstring_quality': 0.25,
                'example_coverage': 0.20,
                'type_annotation_coverage': 0.15,
                'cross_reference_density': 0.05,
                'external_link_coverage': 0.05
            }

            quality_score = sum(
                metrics[key] * weights[key]
                for key in weights
            )

            metrics['overall_quality'] = quality_score
            return metrics

        def generate_quality_report(self):
            """Generate comprehensive quality report."""
            report = {
                'modules': {},
                'summary': {
                    'total_modules': 0,
                    'average_quality': 0,
                    'modules_above_80': 0,
                    'modules_below_60': 0
                }
            }

            for module in self.app.config.coverage_modules:
                quality = self.analyze_module_quality(module)
                report['modules'][module] = quality

                if quality['overall_quality'] >= 80:
                    report['summary']['modules_above_80'] += 1
                elif quality['overall_quality'] < 60:
                    report['summary']['modules_below_60'] += 1

            return report

    def analyze_coverage_quality(app, exception):
        """Perform advanced coverage quality analysis."""
        if exception:
            return

        analyzer = DocumentationQualityAnalyzer(app)
        quality_report = analyzer.generate_quality_report()

        # Write detailed quality report
        import json
        report_path = Path(app.outdir) / 'documentation-quality-report.json'
        with open(report_path, 'w') as f:
            json.dump(quality_report, f, indent=2)

        app.info(f"Documentation quality report: {report_path}")

    app.connect('build-finished', analyze_coverage_quality)

def setup(app):
    setup_advanced_coverage_analysis(app)
```

### 2. Coverage-Driven Documentation Generation

```python
def add_coverage_driven_todo_generation(app):
    """Generate TODOs based on coverage analysis."""

    def generate_coverage_todos(app, exception):
        """Generate TODO items for low coverage areas."""
        if exception:
            return

        # Analyze coverage data
        coverage_data = app.env.coverage_data
        low_coverage_items = []

        for module, data in coverage_data.items():
            if data['coverage_percentage'] < 75:
                low_coverage_items.append({
                    'module': module,
                    'coverage': data['coverage_percentage'],
                    'missing_items': data['undocumented_items']
                })

        # Generate TODO RST file
        todo_content = generate_coverage_todo_rst(low_coverage_items)
        todo_path = Path(app.srcdir) / 'auto-generated-coverage-todos.rst'

        with open(todo_path, 'w') as f:
            f.write(todo_content)

        app.info(f"Generated coverage TODOs: {todo_path}")

    app.connect('build-finished', generate_coverage_todos)

def generate_coverage_todo_rst(low_coverage_items):
    """Generate RST content for coverage-based TODOs."""
    content = """
Coverage-Based Documentation TODOs
==================================

This file is automatically generated based on documentation coverage analysis.

"""

    for item in low_coverage_items:
        content += f"""
{item['module']} ({item['coverage']:.1f}% coverage)
{'-' * (len(item['module']) + 20)}

.. todo:: Improve documentation coverage for {item['module']}
   :category: api
   :priority: {'high' if item['coverage'] < 50 else 'medium'}
   :assigned: documentation

   Current coverage: {item['coverage']:.1f}%
   Target coverage: 80%

   Undocumented items:

"""
        for missing in item['missing_items']:
            content += f"   * ``{missing['name']}`` ({missing['type']})\n"

        content += "\n"

    return content
```

### 3. Coverage Trend Tracking

```python
def setup_coverage_trend_tracking(app):
    """Setup coverage trend tracking across builds."""

    def track_coverage_trends(app, exception):
        """Track coverage trends over time."""
        if exception:
            return

        import json
        from datetime import datetime

        # Current coverage data
        current_coverage = app.env.coverage_statistics

        # Load historical data
        trend_file = Path(app.outdir) / 'coverage-trends.json'
        trends = []
        if trend_file.exists():
            with open(trend_file, 'r') as f:
                trends = json.load(f)

        # Add current data point
        trends.append({
            'timestamp': datetime.now().isoformat(),
            'overall_coverage': current_coverage['overall_percentage'],
            'module_coverage': current_coverage['by_module'],
            'total_objects': current_coverage['total_objects'],
            'documented_objects': current_coverage['documented_objects']
        })

        # Keep only last 100 data points
        trends = trends[-100:]

        # Save trends
        with open(trend_file, 'w') as f:
            json.dump(trends, f, indent=2)

        # Generate trend visualization
        generate_coverage_trend_chart(trends, app.outdir)

    app.connect('build-finished', track_coverage_trends)

def generate_coverage_trend_chart(trends, output_dir):
    """Generate coverage trend visualization."""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime

        # Extract data
        dates = [datetime.fromisoformat(t['timestamp']) for t in trends]
        coverage = [t['overall_coverage'] for t in trends]

        # Create chart
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, coverage, marker='o', linewidth=2, markersize=4)
        ax.set_xlabel('Date')
        ax.set_ylabel('Coverage Percentage')
        ax.set_title('Documentation Coverage Trend')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)

        # Format dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.xticks(rotation=45)

        # Add target line
        ax.axhline(y=80, color='r', linestyle='--', alpha=0.7, label='Target (80%)')
        ax.legend()

        plt.tight_layout()
        plt.savefig(Path(output_dir) / 'coverage-trend.png', dpi=150, bbox_inches='tight')
        plt.close()

    except ImportError:
        pass  # matplotlib not available
```

## Current Implementation Status

### ✅ Working Features

- [x] **Basic coverage analysis** - Standard object coverage tracking
- [x] **Coverage reporting** - Undocumented items identification
- [x] **Module filtering** - Selective coverage analysis
- [x] **Statistics generation** - Coverage percentage calculations
- [x] **Build integration** - Coverage runs with standard builds

### 🔄 Enhancement Opportunities

- [ ] **Advanced quality metrics** - Beyond basic coverage analysis
- [ ] **Coverage-driven TODOs** - Automatic TODO generation for low coverage
- [ ] **Trend tracking** - Historical coverage analysis
- [ ] **Template integration** - Coverage-aware AutoAPI templates
- [ ] **CI/CD integration** - Coverage gates and reporting

### 📋 Template Integration Tasks

1. **Coverage-aware AutoAPI templates** with quality indicators
2. **Automatic TODO generation** based on coverage analysis
3. **Quality metrics dashboard** for documentation health
4. **Trend tracking system** for coverage monitoring

## Integration with AutoAPI

### Coverage-Aware Object Rendering

```jinja2
{# Render objects with coverage awareness #}
{% set coverage = obj.get_coverage_analysis() %}

<div class="api-object coverage-{{ coverage.grade }}">
   <h2>{{ obj.name }}
      <span class="coverage-badge {{ coverage.grade }}">
         {{ coverage.percentage }}%
      </span>
   </h2>

   {% if coverage.percentage < 70 %}
   <div class="coverage-warning">
      ⚠️ Low documentation coverage. Missing: {{ coverage.missing_elements|join(", ") }}
   </div>
   {% endif %}

   {{ obj.render_documentation() }}
</div>
```

### Module Quality Indicators

```jinja2
{# Module-level coverage indicators #}
{% if module.coverage_stats %}
<div class="module-coverage-stats">
   <h3>Documentation Quality</h3>

   <div class="coverage-grid">
      <div class="coverage-metric">
         <span class="metric-value">{{ module.coverage_stats.overall }}%</span>
         <span class="metric-label">Overall Coverage</span>
      </div>

      <div class="coverage-metric">
         <span class="metric-value">{{ module.coverage_stats.classes }}%</span>
         <span class="metric-label">Classes</span>
      </div>

      <div class="coverage-metric">
         <span class="metric-value">{{ module.coverage_stats.functions }}%</span>
         <span class="metric-label">Functions</span>
      </div>
   </div>

   {% if module.coverage_stats.overall < 80 %}
   <div class="improvement-suggestions">
      <h4>Improvement Suggestions:</h4>
      <ul>
         {% for suggestion in module.coverage_stats.suggestions %}
         <li>{{ suggestion }}</li>
         {% endfor %}
      </ul>
   </div>
   {% endif %}
</div>
{% endif %}
```

## Performance Considerations

### Build Time Optimization

```python
# Optimize coverage analysis for large codebases
coverage_analysis_cache_enabled = True
coverage_analysis_parallel = True  # Analyze modules in parallel

# Skip coverage for development builds
if os.environ.get('SKIP_COVERAGE'):
    extensions.remove('sphinx.ext.coverage')
```

### Memory Usage

```python
# Limit memory usage for coverage analysis
coverage_max_modules_per_batch = 10
coverage_enable_garbage_collection = True
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Modules that can't be imported won't be analyzed
2. **Performance Issues**: Large codebases may require optimization
3. **False Positives**: Inherited documentation may not be detected
4. **Reporting Failures**: Output directory permissions or disk space

### Debug Configuration

```python
# Debug coverage analysis
coverage_debug = True
coverage_verbose = True  # Detailed coverage analysis output
```

## Integration with Issue #6

For AutoAPI template customization (Issue #6), the coverage extension provides:

1. **Quality Indicators**: Visual coverage indicators in templates
2. **Automatic Improvement Tracking**: TODO generation for low coverage areas
3. **Quality Metrics**: Comprehensive documentation health assessment
4. **Progressive Enhancement**: Systematic approach to documentation improvement

The coverage extension enables data-driven improvements to AutoAPI templates by providing detailed insights into documentation quality and specific areas needing attention.
