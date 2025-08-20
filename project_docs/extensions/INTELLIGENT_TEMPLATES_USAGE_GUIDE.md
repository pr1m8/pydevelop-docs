# Intelligent Templates Usage Guide

**Created**: 2025-08-13
**Purpose**: Complete guide for using the intelligent AutoAPI template system
**Status**: Implementation Complete

## Overview

The intelligent template system transforms AutoAPI documentation from flat, generic output into rich, type-aware, and extension-enhanced documentation. It leverages all 45+ Sphinx extensions to create beautiful, interactive API documentation.

## Quick Start

### 1. Enable Intelligent Templates

Add to your `conf.py`:

```python
# At the end of conf.py
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

try:
    from pydevelop_docs.templates._autoapi_templates.config_update import setup_intelligent_templates

    # Apply intelligent template configuration
    setup_intelligent_templates(globals())

    print("✅ Intelligent AutoAPI templates enabled!")

except ImportError:
    print("⚠️  Intelligent templates not available, using defaults")
```

### 2. Build Documentation

```bash
# Clean build
poetry run pydevelop-docs clean
poetry run pydevelop-docs build

# Or directly with Sphinx
poetry run sphinx-build -b html docs/source docs/build -E
```

### 3. View Results

```bash
python -m http.server 8003 --directory docs/build
# Open http://localhost:8003
```

## Template Features

### 1. Progressive Disclosure

The templates automatically determine what content to show expanded vs collapsed based on:

- **Complexity score** - Complex items start collapsed
- **Object type** - Core modules expanded, utilities collapsed
- **Content length** - Long content auto-collapsed

### 2. Type-Specific Rendering

Different object types get specialized rendering:

#### Pydantic Models

```python
class UserModel(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(gt=0, le=150)
```

Renders with:

- Interactive field table with types, defaults, and validation
- Constraint visualization
- JSON schema display
- Example usage with validation

#### Agent Classes

```python
class ResearchAgent(BaseAgent):
    tools = ["web_search", "calculator"]
    workflow = ["analyze", "research", "summarize"]
```

Renders with:

- Tool cards showing available tools
- Workflow diagram (Mermaid)
- Configuration examples
- Integration patterns

#### Tool Classes

```python
class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web"
```

Renders with:

- Parameter schema table
- Return type documentation
- Tool schema JSON
- Usage examples with copy button

#### Enum Classes

```python
class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
```

Renders with:

- Value table with descriptions
- Usage examples
- Auto-generated code samples

### 3. Extension Integration

#### Mermaid Diagrams

- Class hierarchies
- State machines
- Workflow diagrams
- Dependency graphs

#### Sphinx Design

- Info cards for statistics
- Grid layouts for modules
- Collapsible sections
- Interactive navigation

#### Code Features

- Copy button on all code blocks
- Syntax highlighting
- Line numbers with emphasis
- Executable code blocks (sphinx_exec_code)

#### Enhanced UI

- Tabbed content for organization
- Tooltips with sphinx_tippy
- Mobile-responsive design
- Dark mode support

## Template Structure

```
_autoapi_templates/
├── python/
│   ├── _base/
│   │   ├── foundation.j2      # Base template with extension detection
│   │   └── progressive.j2     # Progressive disclosure patterns
│   ├── _components/
│   │   ├── diagrams.j2       # Diagram rendering macros
│   │   ├── code_blocks.j2    # Enhanced code rendering
│   │   └── navigation.j2     # Navigation components
│   ├── _macros/
│   │   └── type_specific.j2  # Type-specific rendering macros
│   ├── _filters/
│   │   └── type_filters.py   # Custom Jinja2 filters
│   ├── class.rst             # Class documentation template
│   ├── module.rst            # Module documentation template
│   ├── function.rst          # Function documentation template
│   ├── method.rst            # Method documentation template
│   ├── attribute.rst         # Attribute documentation template
│   └── index.rst             # API index template
└── config_update.py          # Configuration integration
```

## Customization

### 1. Override Specific Templates

Create your own template to override defaults:

```python
# In your docs/source/_templates/autoapi/python/class.rst
{%- extends "autoapi/python/class.rst" -%}

{%- block content -%}
{# Your custom content #}
{{ super() }}
{# Additional custom content #}
{%- endblock -%}
```

### 2. Add Custom Filters

```python
# In conf.py
def setup(app):
    def my_custom_filter(value):
        return value.upper()

    app.add_jinja_filter('my_filter', my_custom_filter)
```

### 3. Configure Display Options

```python
# In conf.py
# Control progressive disclosure thresholds
autoapi_python_class_content_types = ["class", "exception"]
autoapi_keep_files = True  # Keep generated RST for debugging
```

## Examples

### Example 1: API Index Page

The index template creates:

```
API Reference
=============

┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 📦 Modules  │ 🏗️ Classes │ ⚡ Functions │ 📊 Coverage │
│     25      │    150      │     300     │    85%      │
└─────────────┴─────────────┴─────────────┴─────────────┘

🔍 Quick Search: Use Ctrl+K to search the API

📂 Package Structure
[Interactive Mermaid diagram showing package hierarchy]

🏛️ Core Modules
┌─────────────────────────┐ ┌─────────────────────────┐
│ haive.core.engine      │ │ haive.core.schema      │
│ Engine implementations  │ │ Schema definitions      │
│ 15 classes • 45 funcs  │ │ 20 classes • 30 funcs  │
└─────────────────────────┘ └─────────────────────────┘
```

### Example 2: Class Documentation

```python
class Agent(BaseModel):
    """AI agent with tools and memory."""

    name: str = Field(..., description="Agent identifier")
    tools: List[str] = Field(default_factory=list)
    memory: Optional[Memory] = None
```

Renders as:

```
Agent
=====

AI agent with tools and memory.

┌─────────────┬─────────────┬─────────────┐
│ Inheritance │ Subclasses  │ Used By     │
│ BaseModel   │ ReactAgent  │ Coordinator │
│             │ SimpleAgent │ Workflow    │
└─────────────┴─────────────┴─────────────┘

▼ Model Fields [click to expand]
┌────────┬──────────────┬──────────┬─────────────────────┐
│ Field  │ Type         │ Required │ Description         │
├────────┼──────────────┼──────────┼─────────────────────┤
│ name   │ str          │ ✓        │ Agent identifier    │
│ tools  │ List[str]    │ ✗        │ Available tools     │
│ memory │ Memory|None  │ ✗        │ Agent memory        │
└────────┴──────────────┴──────────┴─────────────────────┘

▼ Available Tools [click to expand]
┌─────────────────┐ ┌─────────────────┐
│ web_search      │ │ calculator      │
│ Search the web  │ │ Math operations │
└─────────────────┘ └─────────────────┘
```

### Example 3: Module Documentation

```
haive.agents.react
==================

ReAct (Reasoning and Acting) agent implementation.

📊 Module Statistics
• 5 classes • 12 functions • 3 exceptions

▼ Module Contents [click to expand]

Classes
-------
┌─────────────────────────────────────────┐
│ ReactAgent                              │
│ Main ReAct agent with reasoning loop    │
│                                         │
│ ReactConfig                             │
│ Configuration for ReAct agents          │
│                                         │
│ ThoughtProcess                          │
│ Reasoning chain representation          │
└─────────────────────────────────────────┘

Functions
---------
• create_react_agent() - Factory function
• parse_thoughts() - Parse reasoning output
• execute_action() - Execute selected action
```

## Troubleshooting

### Templates Not Loading

1. Check template path in conf.py:

```python
autoapi_template_dir = 'pydevelop_docs/templates/_autoapi_templates'
```

2. Verify templates exist:

```bash
ls src/pydevelop_docs/templates/_autoapi_templates/python/
```

3. Clear build cache:

```bash
rm -rf docs/build docs/source/autoapi
```

### Extension Features Not Working

1. Verify extension is installed:

```bash
poetry show | grep sphinx
```

2. Check extension is in conf.py:

```python
extensions = [
    'autoapi.extension',
    'sphinx_design',
    'sphinxcontrib.mermaid',
    # ... other extensions
]
```

3. Check console for errors during build

### Custom Filters Not Available

1. Ensure config_update.py is imported
2. Check for Python path issues
3. Verify filter function signatures

## Performance Tips

1. **Use module-level pages**:

   ```python
   autoapi_own_page_level = 'module'
   ```

2. **Cache builds when testing**:

   ```bash
   sphinx-build -b html -d build/doctrees source build/html
   ```

3. **Exclude large generated files**:
   ```python
   autoapi_ignore = ['*/migrations/*', '*/tests/*']
   ```

## Next Steps

1. **Test with your project**: Apply templates to see results
2. **Customize for your needs**: Override specific templates
3. **Add project-specific filters**: Enhance for your use case
4. **Share feedback**: Report issues or improvements

## Related Documentation

- [Template Architecture](INTELLIGENT_TEMPLATE_SYSTEM_ARCHITECTURE.md)
- [Implementation Plan](IMPLEMENTATION_PLAN_INTELLIGENT_TEMPLATES.md)
- [Extension Research](../research/)
- [AutoAPI Jinja2 Research](../issues/jinja2_research_comprehensive.md)
