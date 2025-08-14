# sphinx.ext.graphviz - Core Graphviz Diagram Support

**Extension**: `sphinx.ext.graphviz`  
**Purpose**: Core Sphinx extension for rendering Graphviz diagrams  
**Status**: ✅ Active in PyDevelop-Docs  
**Priority**: High - Foundation for inheritance diagrams  
**Issue #6 Relevance**: Critical for custom inheritance diagram templates

## Overview

The `sphinx.ext.graphviz` extension provides native Sphinx support for embedding Graphviz diagrams directly in documentation. It's the foundation extension that enables inheritance diagrams and custom graph visualizations essential for API documentation.

### Visual Capabilities

- **DOT Language Support**: Full Graphviz DOT syntax for precise control
- **Inheritance Diagrams**: Native support for class inheritance visualization
- **Directed Graphs**: Complex relationships and flow diagrams
- **Undirected Graphs**: Network topology and connection diagrams
- **Multiple Output Formats**: SVG, PNG, PDF support
- **Interactive Elements**: Clickable nodes with cross-references

## Diagram Types and Use Cases

### 1. Class Inheritance Diagrams

Perfect for showing object-oriented relationships in API documentation:

```rst
.. inheritance-diagram:: haive.agents.simple.SimpleAgent haive.agents.react.ReactAgent
   :parts: 2
   :private-bases:
   :caption: Agent Inheritance Hierarchy
```

**Generated Output**: Interactive inheritance tree with clickable classes

### 2. Architecture Flow Diagrams

```rst
.. graphviz::
   :caption: Haive Agent Processing Flow

   digraph AgentFlow {
       rankdir=LR;
       node [shape=box, style="rounded,filled", fillcolor="#dbeafe"];

       Input -> Preprocessing;
       Preprocessing -> "Tool Selection";
       "Tool Selection" -> Execution;
       Execution -> "Response Generation";
       "Response Generation" -> Output;

       {rank=same; Input, Output}
   }
```

### 3. Module Dependency Graphs

```rst
.. graphviz::
   :align: center

   digraph ModuleDeps {
       node [shape=ellipse, style=filled, fillcolor="#f8fafc"];
       edge [color="#2563eb"];

       "haive.core" -> "haive.agents";
       "haive.core" -> "haive.tools";
       "haive.agents" -> "haive.games";
       "haive.tools" -> "haive.dataflow";
   }
```

## Configuration Options

### Current PyDevelop-Docs Configuration

```python
# In config.py - Line 470
extensions = [
    "sphinx.ext.graphviz",  # Core Graphviz support
    # ... other extensions
]

# Graphviz configuration (implicit defaults)
graphviz_output_format = "svg"  # Better for web, scalable
graphviz_dot_args = ["-Gfontname=ui-sans-serif", "-Nfontname=ui-sans-serif"]
```

### Enhanced Configuration Options

```python
# Advanced Graphviz configuration for better AutoAPI integration
graphviz_output_format = "svg"  # SVG for crisp scaling
graphviz_dot_args = [
    "-Gfontname=ui-sans-serif",  # Match Furo theme font
    "-Nfontname=ui-sans-serif",
    "-Gfontsize=11",
    "-Nfontsize=10",
    "-Grankdir=TB",              # Top-to-bottom layout
    "-Gsplines=true",            # Curved edges
    "-Goverlap=false",           # Prevent node overlap
]

# Inheritance diagram configuration
inheritance_graph_attrs = {
    "rankdir": "TB",             # Top-to-bottom
    "size": '"8.0, 12.0"',       # Size limit
    "concentrate": "true",       # Merge edges
}

inheritance_node_attrs = {
    "shape": "box",
    "fontsize": 10,
    "height": 0.25,
    "fontname": "ui-sans-serif",
    "style": '"rounded,filled"',
    "fillcolor": '"#dbeafe"',    # Light blue matching Furo
}

inheritance_edge_attrs = {
    "arrowsize": 0.5,
    "style": "solid",
    "color": '"#2563eb"',        # Furo brand color
}
```

## Template Integration for Issue #6

### Custom Inheritance Templates

Replace default ugly inheritance diagrams with beautiful custom ones:

```jinja2
{# In _autoapi_templates/python/class.rst #}
{% if obj.bases %}
**Inheritance Hierarchy:**

.. inheritance-diagram:: {{ obj.id }}
   :parts: 2
   :private-bases:
   :top-classes: {{ obj.bases | join(", ") }}
   :caption: {{ obj.name }} inheritance structure

{% endif %}
```

### Custom Graphviz Directive Templates

```jinja2
{# Architecture diagrams in module templates #}
{% if obj.children %}
**Module Architecture:**

.. graphviz::
   :caption: {{ obj.name }} Component Relationships

   digraph ModuleArch {
       node [fontname="ui-sans-serif", style="rounded,filled"];

       {% for child in obj.children %}
       "{{ child.name }}" [fillcolor="#dbeafe"];
       {% endfor %}

       {% for child in obj.children %}
       {% if child.inherited_members %}
       {% for parent in child.inherited_members %}
       "{{ parent }}" -> "{{ child.name }}";
       {% endfor %}
       {% endif %}
       {% endfor %}
   }
{% endif %}
```

## Rendering Quality and Performance

### SVG Advantages for Documentation

- **Scalable Vector Graphics**: Perfect for high-DPI displays
- **Interactive Elements**: Clickable nodes with Sphinx cross-references
- **Small File Sizes**: Efficient for web delivery
- **Theme Integration**: CSS styling matches Furo theme

### Performance Optimizations

```python
# Optimized settings for large inheritance hierarchies
graphviz_dot_args = [
    "-Gnslimit=2.0",            # Layout time limit
    "-Gnslimit1=2.0",           # First phase limit
    "-Gmaxiter=1000",           # Maximum iterations
    "-Gconcentrate=true",       # Merge parallel edges
]
```

## Responsive Design and Mobile Optimization

### CSS Enhancements for Mobile

```css
/* In _static/graphviz-responsive.css */
.graphviz {
  max-width: 100%;
  height: auto;
  overflow-x: auto;
  margin: 1rem 0;
}

.graphviz svg {
  max-width: 100%;
  height: auto;
  min-height: 200px;
}

/* Mobile-specific optimizations */
@media (max-width: 768px) {
  .graphviz {
    overflow-x: scroll;
    -webkit-overflow-scrolling: touch;
  }

  .graphviz svg {
    min-width: 600px; /* Maintain readability */
  }
}
```

### Responsive Graphviz Attributes

```python
# Mobile-optimized graph attributes
graphviz_mobile_attrs = {
    "dpi": 150,                 # Higher DPI for mobile
    "fontsize": 12,             # Larger fonts for mobile
    "mindist": 1.5,             # More spacing
    "nodesep": 0.8,             # Node separation
}
```

## Code Examples for AutoAPI Templates

### 1. Enhanced Class Inheritance Diagram

```jinja2
{# Enhanced inheritance with styling #}
{% if obj.bases or obj.subclasses %}
<div class="inheritance-section">
    <h3>🏗️ Class Hierarchy</h3>

    .. graphviz::
       :caption: {{ obj.name }} - Complete Inheritance Tree

       digraph Inheritance {
           rankdir=TB;
           node [
               shape=box,
               style="rounded,filled",
               fontname="ui-sans-serif",
               fontsize=10,
               height=0.4,
               width=1.2
           ];

           // Current class (highlighted)
           "{{ obj.name }}" [
               fillcolor="#2563eb",
               fontcolor="white",
               style="rounded,filled,bold"
           ];

           {% for base in obj.bases %}
           "{{ base }}" [fillcolor="#dbeafe"];
           "{{ base }}" -> "{{ obj.name }}";
           {% endfor %}

           {% for subclass in obj.subclasses %}
           "{{ subclass }}" [fillcolor="#f0fdf4"];
           "{{ obj.name }}" -> "{{ subclass }}";
           {% endfor %}
       }
</div>
{% endif %}
```

### 2. Module Component Diagram

```jinja2
{# Module overview with component relationships #}
{% if obj.children|length > 3 %}
.. graphviz::
   :caption: {{ obj.name }} - Module Components
   :align: center

   digraph Components {
       // Layout configuration
       rankdir=LR;
       compound=true;
       concentrate=true;

       // Styling
       node [
           fontname="ui-sans-serif",
           fontsize=9,
           style="rounded,filled"
       ];

       // Group by type
       subgraph cluster_classes {
           label="Classes";
           style=filled;
           fillcolor="#f8fafc";

           {% for child in obj.children %}
           {% if child.type == "class" %}
           "{{ child.name }}" [fillcolor="#dbeafe"];
           {% endif %}
           {% endfor %}
       }

       subgraph cluster_functions {
           label="Functions";
           style=filled;
           fillcolor="#f0fdf4";

           {% for child in obj.children %}
           {% if child.type == "function" %}
           "{{ child.name }}" [fillcolor="#dcfce7"];
           {% endif %}
           {% endfor %}
       }
   }
{% endif %}
```

## Performance Considerations

### Build Time Optimization

- **Conditional Generation**: Only generate diagrams for complex hierarchies
- **Caching**: Leverage Sphinx's build cache for unchanged diagrams
- **Size Limits**: Set reasonable node/edge limits for large projects

### Memory Usage

```python
# Memory-efficient settings for large monorepos
graphviz_dot_args = [
    "-Gmaxiter=100",            # Limit iterations
    "-Gnslimit=1.0",            # Time limit per graph
    "-Gpack=true",              # Pack connected components
]
```

## Integration with Other Extensions

### AutoAPI Integration

Works seamlessly with AutoAPI for automatic inheritance diagrams:

```python
# Automatic inheritance diagrams for classes with many subclasses
autoapi_python_class_content = "both"
autoapi_add_class_diagram = True        # Enable inheritance diagrams
autoapi_class_diagram_depth = 3         # Maximum depth
```

### Intersphinx Cross-References

```rst
.. graphviz::

   digraph CrossRefs {
       "MyClass" [URL="../api/myclass.html"];
       "BaseClass" [URL="https://docs.python.org/3/library/abc.html#abc.ABC"];
       "BaseClass" -> "MyClass";
   }
```

## Current Implementation Status

### ✅ Active Features

- Core Graphviz rendering with SVG output
- Basic inheritance diagram support
- Furo theme color integration
- Responsive CSS for mobile devices

### 🔄 Issue #6 Enhancements Needed

- Custom inheritance diagram templates
- Enhanced AutoAPI integration
- Interactive diagram elements
- Mobile-optimized layouts
- Performance optimizations for large hierarchies

### 📋 Next Steps

1. **Template Enhancement**: Create custom Jinja2 templates for inheritance diagrams
2. **CSS Integration**: Develop Graphviz-specific responsive styles
3. **Performance Tuning**: Optimize for large monorepo documentation
4. **Interactive Features**: Add clickable elements and cross-references

## Best Practices

### 1. Diagram Complexity Management

- **Limit Depth**: Maximum 3-4 inheritance levels
- **Focus Scope**: Show relevant relationships only
- **Use Clustering**: Group related components

### 2. Responsive Design

- **Mobile-First**: Design for smallest screens first
- **Scalable Fonts**: Use relative font sizes
- **Touch-Friendly**: Ensure interactive elements are accessible

### 3. Performance Optimization

- **Conditional Generation**: Only create diagrams when beneficial
- **Size Constraints**: Set reasonable limits on diagram complexity
- **Caching Strategy**: Leverage Sphinx's incremental build system

---

**Status**: Foundation extension - critical for Issue #6 visual enhancements  
**Next Extension**: [sphinxcontrib.mermaid](sphinxcontrib_mermaid.md) - Modern diagram integration  
**Related**: [AutoAPI Template Integration](../api/autoapi_extension.md)
