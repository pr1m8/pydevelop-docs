# sphinx.ext.todo - Task and TODO Management

**Extension**: `sphinx.ext.todo`  
**Priority**: Core Foundation (Position 5 in extensions list)  
**Official Documentation**: [sphinx.ext.todo](https://www.sphinx-doc.org/en/master/usage/extensions/todo.html)  
**Status in PyDevelop-Docs**: ✅ Implemented for development workflow management

## Overview

`sphinx.ext.todo` adds support for TODO items in documentation, providing a systematic way to track incomplete documentation, planned features, and development tasks. This extension is particularly valuable during active development, allowing teams to maintain documentation quality while tracking what needs attention.

## Core Capabilities

### 1. TODO Item Creation

- **Directive Support**: `.. todo::` directive for marking incomplete sections
- **Inline TODOs**: Support for inline TODO markers in documentation
- **Structured Format**: Consistent formatting for all TODO items
- **Rich Content**: TODOs can contain formatted text, code, and other directives

### 2. TODO Collection and Management

- **Central TODO List**: Automatic generation of all TODO items
- **Categorization**: Group TODOs by type, priority, or location
- **Status Tracking**: Mark TODOs as resolved or in progress
- **Cross-References**: Link to specific TODO items from other documentation

### 3. Development Workflow Integration

- **Build Warnings**: Optional warnings for unresolved TODOs
- **Conditional Display**: Show/hide TODOs based on build configuration
- **Team Coordination**: Assign TODOs to specific team members or components

## Configuration in PyDevelop-Docs

### Current Implementation

```python
# In config.py - todo extension included in core
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",  # TODO management for development
    # ... other extensions
]

# Basic todo configuration (uses defaults)
# Inherits standard todo behavior
```

### Enhanced Configuration Options

```python
# Advanced todo configuration for PyDevelop-Docs
todo_include_todos = True  # Show TODOs in documentation
todo_emit_warnings = False  # Don't warn on TODOs (development-friendly)
todo_link_only = False  # Include full TODO content, not just links

# Custom TODO styling
todo_header_format = "TODO ({author}): {title}"
todo_footer_format = "Added: {date} | Priority: {priority}"

# TODO categorization
todo_categories = {
    'api': {
        'title': 'API Documentation',
        'color': '#007acc',
        'priority': 'high'
    },
    'examples': {
        'title': 'Code Examples',
        'color': '#28a745',
        'priority': 'medium'
    },
    'guides': {
        'title': 'User Guides',
        'color': '#ffc107',
        'priority': 'medium'
    },
    'templates': {
        'title': 'Template Enhancements',
        'color': '#6f42c1',
        'priority': 'low'
    },
    'performance': {
        'title': 'Performance Optimization',
        'color': '#dc3545',
        'priority': 'high'
    }
}

# TODO assignment and tracking
todo_assignments = {
    'development': ['api', 'performance'],
    'documentation': ['examples', 'guides'],
    'design': ['templates']
}
```

### Production Build Configuration

```python
# Different configurations for development vs production
import os

# Production builds hide TODOs
if os.environ.get('SPHINX_BUILD_MODE') == 'production':
    todo_include_todos = False
    todo_emit_warnings = True  # Warn about unresolved TODOs in production
else:
    # Development builds show TODOs
    todo_include_todos = True
    todo_emit_warnings = False
```

## Template Integration Opportunities

### 1. Enhanced TODO Templates

```jinja2
{# _autoapi_templates/python/todo_enhanced.rst #}
{% if obj.todos %}
.. container:: todo-section

   .. admonition:: Documentation TODOs
      :class: todo-list

      {% for todo in obj.todos %}
      .. todo:: {{ todo.title }}
         :category: {{ todo.category }}
         :priority: {{ todo.priority }}
         :assigned: {{ todo.assigned_to }}

         {{ todo.description }}

         **Context:** {{ obj.name }} ({{ obj.type }})
         **File:** ``{{ obj.source_file }}:{{ obj.line_number }}``
      {% endfor %}
{% endif %}
```

### 2. AutoAPI Integration Templates

```jinja2
{# _autoapi_templates/python/class.rst #}
{{ obj.name }}
{{ "=" * obj.name|length }}

{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% else %}
.. todo:: Add comprehensive docstring for {{ obj.name }}
   :category: api
   :priority: high
   :assigned: documentation

   This class needs a complete docstring including:

   * Purpose and functionality description
   * Parameter documentation for __init__
   * Usage examples
   * Related classes and methods

   **Class:** ``{{ obj.id }}``
   **Module:** ``{{ obj.module }}``
{% endif %}

{% if obj.methods %}
Methods
-------

{% for method in obj.methods %}
{% if not method.docstring %}
.. todo:: Document {{ method.name }} method
   :category: api
   :priority: medium
   :assigned: development

   Add docstring for ``{{ obj.name }}.{{ method.name }}()`` including:

   * Method purpose and behavior
   * Parameter types and descriptions
   * Return value documentation
   * Usage examples

{% endif %}
{{ method.render()|indent(0) }}
{% endfor %}
{% endif %}
```

### 3. Module-Level TODO Management

```jinja2
{# _autoapi_templates/python/module.rst #}
{% if obj.docstring %}
{{ obj.docstring|prepare_docstring|indent(0) }}
{% else %}
.. todo:: Add module documentation for {{ obj.name }}
   :category: api
   :priority: high
   :assigned: documentation

   This module needs comprehensive documentation including:

   * Module purpose and overview
   * Key classes and functions summary
   * Usage patterns and examples
   * Integration points with other modules

   **Module:** ``{{ obj.name }}``
   **Package:** ``{{ obj.package }}``
{% endif %}

{# Check for undocumented functions and classes #}
{% set undocumented_items = [] %}
{% for item in obj.children %}
{% if not item.docstring %}
{% set _ = undocumented_items.append(item) %}
{% endif %}
{% endfor %}

{% if undocumented_items %}
.. todo:: Document undocumented items in {{ obj.name }}
   :category: api
   :priority: medium
   :assigned: development

   The following items need documentation:

   {% for item in undocumented_items %}
   * ``{{ item.name }}`` ({{ item.type }})
   {% endfor %}

   Focus on public APIs and commonly used functionality.
{% endif %}
```

## Best Practices for PyDevelop-Docs

### 1. Structured TODO Documentation

```python
class AgentConfiguration:
    """Agent configuration management.

    .. todo:: Enhance configuration validation
       :category: api
       :priority: high
       :assigned: development

       Add comprehensive validation for:

       * Model parameter ranges and types
       * Tool compatibility checking
       * Configuration schema validation
       * Performance impact assessment

       See: :issue:`123` for requirements
    """

    def __init__(self, model: str, tools: List[str]):
        """Initialize agent configuration.

        .. todo:: Add configuration examples
           :category: examples
           :priority: medium
           :assigned: documentation

           Include examples for:

           * Basic agent configuration
           * Advanced tool integration
           * Performance optimization settings
           * Multi-agent coordination
        """
        self.model = model
        self.tools = tools
```

### 2. Development Workflow TODOs

```rst
Agent Creation Guide
===================

This guide explains how to create custom agents in the Haive framework.

.. todo:: Complete agent creation tutorial
   :category: guides
   :priority: high
   :assigned: documentation

   Sections to add:

   * Step-by-step agent creation process
   * Configuration best practices
   * Testing and validation approaches
   * Deployment considerations

   Target audience: Python developers new to Haive

Basic Agent Setup
-----------------

.. todo:: Add code examples for basic setup
   :category: examples
   :priority: medium
   :assigned: development

   Include working examples for:

   * SimpleAgent configuration
   * ReactAgent with tools
   * Multi-agent coordination

   All examples should be runnable and tested.

Advanced Features
-----------------

.. todo:: Document advanced agent features
   :category: api
   :priority: low
   :assigned: documentation

   Cover advanced topics:

   * Custom tool development
   * State management patterns
   * Performance optimization
   * Error handling strategies
```

### 3. Template Enhancement TODOs

```rst
AutoAPI Template Improvements
============================

.. todo:: Implement custom AutoAPI templates
   :category: templates
   :priority: high
   :assigned: design

   **Objective:** Create custom Jinja2 templates for better API documentation

   **Requirements:**

   * Enhanced class documentation with examples
   * Better parameter formatting
   * Integration with external type links
   * Consistent styling across all objects

   **Files to create:**

   * ``_autoapi_templates/python/class.rst``
   * ``_autoapi_templates/python/function.rst``
   * ``_autoapi_templates/python/module.rst``

   **Reference:** Issue #6 - AutoAPI Jinja2 Templates

.. todo:: Add interactive examples to templates
   :category: templates
   :priority: medium
   :assigned: development

   Integrate with sphinx_exec_code for:

   * Runnable code examples in API docs
   * Real-time validation of examples
   * Interactive parameter exploration

   **Dependencies:** sphinx_exec_code configuration
```

## Enhancement Opportunities

### 1. TODO Analytics and Reporting

```python
def generate_todo_report(app, exception):
    """Generate comprehensive TODO analytics report."""
    if exception:
        return

    # Collect all TODOs
    todos = []
    for docname in app.env.all_docs:
        doc = app.env.get_doctree(docname)
        for todo_node in doc.traverse(todo_list):
            todos.append({
                'content': todo_node.astext(),
                'docname': docname,
                'category': todo_node.get('category', 'uncategorized'),
                'priority': todo_node.get('priority', 'medium'),
                'assigned': todo_node.get('assigned', 'unassigned'),
            })

    # Generate statistics
    total_todos = len(todos)
    by_category = {}
    by_priority = {}
    by_assignment = {}

    for todo in todos:
        category = todo['category']
        priority = todo['priority']
        assigned = todo['assigned']

        by_category[category] = by_category.get(category, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1
        by_assignment[assigned] = by_assignment.get(assigned, 0) + 1

    # Write report
    report_path = Path(app.outdir) / 'todo-report.html'
    with open(report_path, 'w') as f:
        f.write(generate_todo_html_report(total_todos, by_category, by_priority, by_assignment))

    app.info(f"TODO report generated: {report_path}")
    app.info(f"Total TODOs: {total_todos}")

def setup(app):
    app.connect('build-finished', generate_todo_report)
```

### 2. TODO Assignment and Tracking

```python
def add_todo_metadata_support(app):
    """Add enhanced metadata support for TODO items."""

    class EnhancedTodoDirective(SphinxDirective):
        """Enhanced TODO directive with metadata."""

        has_content = True
        option_spec = {
            'category': directives.unchanged,
            'priority': directives.unchanged,
            'assigned': directives.unchanged,
            'due': directives.unchanged,
            'issue': directives.unchanged,
            'milestone': directives.unchanged,
        }

        def run(self):
            # Enhanced TODO processing with metadata
            env = self.state.document.settings.env
            node = todo_node()
            node.line = self.lineno

            # Add metadata
            for key, value in self.options.items():
                node[key] = value

            # Process content
            self.state.nested_parse(self.content, self.content_offset, node)

            # Add to environment tracking
            if not hasattr(env, 'todo_all_todos'):
                env.todo_all_todos = []

            env.todo_all_todos.append({
                'docname': env.docname,
                'lineno': self.lineno,
                'todo': node.deepcopy(),
                'metadata': self.options
            })

            return [node]

    app.add_directive('todo', EnhancedTodoDirective, override=True)

def setup(app):
    add_todo_metadata_support(app)
```

### 3. Integration with Issue Tracking

```python
def integrate_with_github_issues(app):
    """Integrate TODOs with GitHub issue tracking."""

    def process_issue_references(app, doctree, docname):
        """Process issue references in TODO items."""
        for todo_node in doctree.traverse(todo_list):
            issue_ref = todo_node.get('issue')
            if issue_ref:
                # Create link to GitHub issue
                issue_url = f"https://github.com/haive-ai/haive/issues/{issue_ref}"
                reference = reference_node(
                    rawtext=f"Issue #{issue_ref}",
                    text=f"Issue #{issue_ref}",
                    refuri=issue_url
                )

                # Add issue link to TODO
                issue_para = paragraph()
                issue_para += strong(text="Related Issue: ")
                issue_para += reference
                todo_node.append(issue_para)

    app.connect('doctree-resolved', process_issue_references)

def setup(app):
    integrate_with_github_issues(app)
```

## Current Implementation Status

### ✅ Working Features

- [x] **Basic TODO directive** - Standard TODO creation working
- [x] **TODO list generation** - Central TODO collection functional
- [x] **Conditional display** - TODOs can be hidden in production builds
- [x] **Rich content support** - TODOs can contain formatted content
- [x] **Cross-references** - TODOs can link to other documentation

### 🔄 Enhancement Opportunities

- [ ] **Enhanced metadata support** - Categories, priorities, assignments
- [ ] **TODO analytics** - Comprehensive reporting and tracking
- [ ] **GitHub integration** - Link TODOs to GitHub issues
- [ ] **Template integration** - Automatic TODO generation for undocumented code
- [ ] **Team workflow** - Assignment and progress tracking features

### 📋 Template Integration Tasks

1. **AutoAPI TODO templates** for automatic documentation TODO generation
2. **Metadata enhancement** with categories, priorities, and assignments
3. **Reporting system** for TODO analytics and tracking
4. **Issue tracking integration** for workflow management

## Integration with AutoAPI

### Automatic TODO Generation

```jinja2
{# Generate TODOs for undocumented code #}
{% if not obj.docstring %}
.. todo:: Add documentation for {{ obj.name }}
   :category: api
   :priority: {% if obj.is_public %}high{% else %}medium{% endif %}
   :assigned: {% if obj.type == 'class' %}development{% else %}documentation{% endif %}

   This {{ obj.type }} needs comprehensive documentation.

   **Location:** ``{{ obj.id }}``
   **File:** ``{{ obj.source_file }}:{{ obj.line_number }}``

   {% if obj.type == 'function' %}
   Required sections:
   * Purpose and behavior
   * Parameter documentation
   * Return value description
   * Usage examples
   {% elif obj.type == 'class' %}
   Required sections:
   * Class purpose and functionality
   * Constructor parameters
   * Key methods overview
   * Usage patterns and examples
   {% endif %}
{% endif %}
```

### Documentation Quality Tracking

```jinja2
{# Track documentation completeness #}
{% set completion_score = obj.calculate_documentation_score() %}
{% if completion_score < 80 %}
.. todo:: Improve documentation quality for {{ obj.name }}
   :category: api
   :priority: {% if completion_score < 50 %}high{% else %}medium{% endif %}
   :assigned: documentation

   **Current Score:** {{ completion_score }}%

   **Missing Elements:**
   {% if not obj.docstring %}
   * Main docstring (30 points)
   {% endif %}
   {% if not obj.examples %}
   * Usage examples (20 points)
   {% endif %}
   {% if not obj.type_annotations %}
   * Type annotations (15 points)
   {% endif %}
   {% if not obj.cross_references %}
   * Cross-references (10 points)
   {% endif %}

   **Target:** 80%+ documentation completeness
{% endif %}
```

## Performance Considerations

### Build Time Optimization

```python
# Optimize TODO processing for large codebases
todo_include_todos = False if os.environ.get('FAST_BUILD') else True

# Cache TODO processing results
todo_cache_enabled = True
todo_cache_expiry = 3600  # 1 hour cache
```

### Memory Usage

```python
# Limit TODO content size for performance
todo_max_content_length = 1000  # Characters
todo_truncate_long_content = True
```

## Troubleshooting

### Common Issues

1. **Missing TODOs**: Check `todo_include_todos` configuration
2. **TODO Formatting**: Ensure proper directive syntax
3. **Cross-Reference Failures**: Verify TODO link targets exist
4. **Performance Issues**: Large numbers of TODOs may slow builds

### Debug Configuration

```python
# Debug TODO processing
todo_debug = True
todo_emit_warnings = True  # Show all TODO-related warnings
```

## CSS Styling for TODOs

### Enhanced TODO Presentation

```css
/* Enhanced TODO styling */
.admonition.todo {
  border-left: 4px solid #ffc107;
  background-color: #fff3cd;
  border-color: #ffeaa7;
}

.todo-list {
  margin: 1em 0;
}

.todo-metadata {
  font-size: 0.9em;
  color: #6c757d;
  margin-top: 0.5em;
}

.todo-category-api {
  border-left-color: #007acc;
}

.todo-category-examples {
  border-left-color: #28a745;
}

.todo-priority-high {
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

.todo-priority-medium {
  background-color: #fff3cd;
  border-color: #ffeaa7;
}

.todo-priority-low {
  background-color: #d1ecf1;
  border-color: #bee5eb;
}
```

## Integration with Issue #6

For AutoAPI template customization (Issue #6), the TODO extension provides:

1. **Documentation Quality Tracking**: Automatic TODO generation for undocumented code
2. **Template Enhancement TODOs**: Systematic tracking of template improvement needs
3. **Development Workflow**: Coordinated approach to documentation improvements
4. **Quality Metrics**: Measurable progress tracking for documentation completeness

The TODO extension enables a structured approach to improving AutoAPI templates by providing clear, trackable tasks for enhancement work.
