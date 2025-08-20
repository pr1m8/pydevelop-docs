# sphinxcontrib.mermaid - Modern Mermaid.js Diagrams

**Extension**: `sphinxcontrib.mermaid`  
**Purpose**: Modern, interactive Mermaid.js diagram integration  
**Status**: ✅ Active in PyDevelop-Docs with extensive customization  
**Priority**: Very High - Primary diagramming solution  
**Issue #6 Relevance**: Essential for beautiful, interactive API diagrams

## Overview

The `sphinxcontrib.mermaid` extension brings modern Mermaid.js diagrams to Sphinx documentation. Unlike traditional static diagrams, Mermaid provides interactive, responsive, and beautifully styled diagrams that integrate seamlessly with modern documentation themes.

### Visual Capabilities

- **Live Rendering**: Client-side JavaScript rendering for fast loading
- **Interactive Elements**: Clickable nodes, zoom, and pan functionality
- **Modern Styling**: Beautiful default themes with full customization
- **Responsive Design**: Perfect scaling across all device sizes
- **Multiple Diagram Types**: 12+ diagram types for comprehensive visualization
- **Theme Integration**: Deep integration with Furo dark/light modes

## Diagram Types and Use Cases

### 1. Flowcharts - Perfect for API Process Flow

```rst
.. mermaid::
   :caption: Agent Processing Pipeline
   :align: center

   flowchart TD
       A[User Input] --> B{Input Validation}
       B -->|Valid| C[Agent Selection]
       B -->|Invalid| D[Error Response]
       C --> E[Tool Loading]
       E --> F[Execution]
       F --> G[Response Generation]
       G --> H[Output Formatting]
       H --> I[User Response]

       classDef inputNode fill:#dbeafe,stroke:#2563eb,stroke-width:2px
       classDef processNode fill:#f0fdf4,stroke:#10b981,stroke-width:2px
       classDef outputNode fill:#fef3c7,stroke:#f59e0b,stroke-width:2px

       class A,I outputNode
       class C,E,F,G,H processNode
       class B inputNode
```

### 2. Class Diagrams - Enhanced OOP Visualization

```rst
.. mermaid::
   :caption: Haive Agent Architecture

   classDiagram
       class Agent {
           +name: str
           +engine: AugLLMConfig
           +state: StateSchema
           +run(input: str) str
           +arun(input: str) str
       }

       class SimpleAgent {
           +prompt_template: ChatPromptTemplate
           +tools: List[Tool]
           +execute() Response
       }

       class ReactAgent {
           +reasoning_loop() Decision
           +tool_selection() Tool
           +reflection() Evaluation
       }

       class MultiAgent {
           +agents: Dict[str, Agent]
           +execution_mode: str
           +coordinate() Result
       }

       Agent <|-- SimpleAgent : inherits
       Agent <|-- ReactAgent : inherits
       Agent <|-- MultiAgent : inherits

       SimpleAgent --> Tool : uses
       ReactAgent --> Tool : uses
       MultiAgent --> Agent : orchestrates
```

### 3. Sequence Diagrams - API Interaction Flow

```rst
.. mermaid::
   :caption: Multi-Agent Interaction Sequence

   sequenceDiagram
       participant U as User
       participant M as MultiAgent
       participant R as ReactAgent
       participant S as SimpleAgent
       participant T as Tool

       U->>M: Execute Task
       M->>R: Analyze & Plan
       R->>T: Use Research Tool
       T-->>R: Research Results
       R-->>M: Analysis Complete
       M->>S: Generate Response
       S->>T: Use Format Tool
       T-->>S: Formatted Output
       S-->>M: Response Ready
       M-->>U: Final Result

       note over R,T: Reasoning phase with tools
       note over S,T: Execution phase with formatting
```

### 4. State Diagrams - Agent Lifecycle

```rst
.. mermaid::
   :caption: Agent State Management

   stateDiagram-v2
       [*] --> Initializing
       Initializing --> Ready : Configuration Complete
       Ready --> Processing : Input Received
       Processing --> ToolSelection : Need Tools
       Processing --> Generating : Direct Response
       ToolSelection --> ToolExecution : Tool Selected
       ToolExecution --> Processing : Tool Result
       Generating --> Complete : Response Ready
       Complete --> Ready : Reset for Next Input
       Complete --> [*] : Session End

       Processing --> Error : Validation Failed
       ToolExecution --> Error : Tool Failed
       Error --> Ready : Error Handled
```

### 5. Git Graphs - Development Workflow

```rst
.. mermaid::
   :caption: PyDevelop-Docs Development Flow

   gitgraph
       commit id: "Initial Setup"
       branch feature/autoapi-fix
       checkout feature/autoapi-fix
       commit id: "Add hierarchical config"
       commit id: "Fix template issues"
       checkout main
       merge feature/autoapi-fix
       commit id: "Release v1.1.0"
       branch feature/mermaid-enhancement
       checkout feature/mermaid-enhancement
       commit id: "Enhanced Mermaid integration"
       commit id: "Mobile responsive"
       checkout main
       merge feature/mermaid-enhancement
```

## Configuration Options

### Current PyDevelop-Docs Configuration

```python
# In config.py - Lines 471, 187-196
extensions = [
    "sphinxcontrib.mermaid",     # Modern Mermaid.js diagrams
    # ... other extensions
]

# Mermaid configuration with custom theming
"myst_fence_as_directive": ["mermaid", "note", "warning"],  # Enable in MyST
"mermaid_params": [
    "--theme", "neutral",        # Base theme
    "--width", "800",           # Default width
    "--backgroundColor", "transparent",  # Transparent background
],
"mermaid_verbose": True,        # Debug output
```

### Enhanced Configuration for Issue #6

```python
# Advanced Mermaid configuration for AutoAPI integration
mermaid_version = "10.6.1"     # Latest version
mermaid_init_js = """
{
    "theme": "base",
    "themeVariables": {
        "primaryColor": "#2563eb",
        "primaryTextColor": "#ffffff",
        "primaryBorderColor": "#1d4ed8",
        "lineColor": "#cbd5e1",
        "sectionBkgColor": "#f8fafc",
        "altSectionBkgColor": "#e2e8f0",
        "gridColor": "#e5e7eb",
        "c0": "#2563eb", "c1": "#10b981", "c2": "#f59e0b", "c3": "#ef4444"
    },
    "flowchart": {
        "nodeSpacing": 50,
        "rankSpacing": 50,
        "curve": "basis",
        "useMaxWidth": true,
        "htmlLabels": true
    },
    "sequence": {
        "actorMargin": 50,
        "width": 150,
        "height": 65,
        "boxMargin": 10,
        "messageMargin": 35,
        "mirrorActors": false,
        "showSequenceNumbers": true,
        "useMaxWidth": true
    },
    "class": {
        "titleTopMargin": 25,
        "arrowMarkerAbsolute": false,
        "dividerMargin": 10,
        "padding": 5,
        "textHeight": 10,
        "useMaxWidth": true
    },
    "state": {
        "dividerMargin": 10,
        "sizeUnit": 5,
        "padding": 8,
        "textHeight": 10,
        "titleShift": -15,
        "noteMargin": 10,
        "forkWidth": 70,
        "forkHeight": 7
    },
    "gitGraph": {
        "diagramPadding": 8,
        "nodeLabel": {"width": 75, "height": 100},
        "mainBranchName": "main",
        "theme": "base"
    }
}
"""

# Custom CSS integration
html_css_files = [
    "mermaid-custom.css",       # Custom Mermaid styling
    # ... other CSS files
]

html_js_files = [
    "mermaid-config.js",        # Enhanced Mermaid configuration
    # ... other JS files
]
```

## Template Integration for Issue #6

### 1. Enhanced AutoAPI Class Templates

```jinja2
{# In _autoapi_templates/python/class.rst #}

{# Class relationship diagram #}
{% if obj.bases or obj.subclasses %}
**Class Relationships:**

.. mermaid::
   :caption: {{ obj.name }} - Inheritance & Composition

   classDiagram
       {%- for base in obj.bases %}
       class {{ base.split('.')[-1] }} {
           <<abstract>>
       }
       {{ base.split('.')[-1] }} <|-- {{ obj.name }}
       {%- endfor %}

       class {{ obj.name }} {
           {%- for attr in obj.attributes[:5] %}
           +{{ attr.name }}: {{ attr.annotation or 'Any' }}
           {%- endfor %}
           {%- for method in obj.methods[:8] %}
           +{{ method.name }}({{ method.args|join(', ') }})
           {%- endfor %}
       }

       {%- for subclass in obj.subclasses[:5] %}
       class {{ subclass.split('.')[-1] }}
       {{ obj.name }} <|-- {{ subclass.split('.')[-1] }}
       {%- endfor %}

       {%- if obj.used_by %}
       {%- for user in obj.used_by[:3] %}
       class {{ user.split('.')[-1] }}
       {{ obj.name }} --> {{ user.split('.')[-1] }} : used by
       {%- endfor %}
       {%- endif %}

{% endif %}
```

### 2. Module Architecture Diagrams

```jinja2
{# In _autoapi_templates/python/module.rst #}

{# Module component flowchart #}
{% if obj.children|length > 2 %}
**Module Architecture:**

.. mermaid::
   :caption: {{ obj.name }} - Component Flow
   :align: center

   flowchart TB
       subgraph "{{ obj.name|upper }}"
           direction TB

           {%- for child in obj.children %}
           {%- if child.type == "class" %}
           {{ child.name }}[{{ child.name }}]
           {%- elif child.type == "function" %}
           {{ child.name }}({{ child.name }}())
           {%- endif %}
           {%- endfor %}
       end

       {%- set class_nodes = obj.children|selectattr("type", "equalto", "class")|list %}
       {%- set func_nodes = obj.children|selectattr("type", "equalto", "function")|list %}

       {%- for func in func_nodes %}
       {%- for cls in class_nodes %}
       {%- if cls.name in func.source %}
       {{ func.name }} --> {{ cls.name }}
       {%- endif %}
       {%- endfor %}
       {%- endfor %}

       classDef classNode fill:#dbeafe,stroke:#2563eb,stroke-width:2px
       classDef funcNode fill:#f0fdf4,stroke:#10b981,stroke-width:2px

       {%- for cls in class_nodes %}
       class {{ cls.name }} classNode
       {%- endfor %}
       {%- for func in func_nodes %}
       class {{ func.name }} funcNode
       {%- endfor %}

{% endif %}
```

### 3. Package Overview Diagrams

```jinja2
{# In _autoapi_templates/python/package.rst #}

**Package Structure:**

.. mermaid::
   :caption: {{ obj.name }} - Package Overview

   graph TB
       subgraph "{{ obj.name }}"
           direction TB

           {%- for module in obj.children %}
           {%- if module.type == "module" %}
           {{ module.name|replace(".", "_") }}["📄 {{ module.name }}"]

           {%- if module.children %}
           subgraph "{{ module.name|replace(".", "_") }}_content" ["{{ module.name }} Contents"]
               {%- for child in module.children[:5] %}
               {%- if child.type == "class" %}
               {{ child.name|replace(".", "_") }}["🏛️ {{ child.name }}"]
               {%- elif child.type == "function" %}
               {{ child.name|replace(".", "_") }}["⚙️ {{ child.name }}()"]
               {%- endif %}
               {%- endfor %}
           end
           {{ module.name|replace(".", "_") }} --- {{ module.name|replace(".", "_") }}_content
           {%- endif %}

           {%- endif %}
           {%- endfor %}
       end

       classDef moduleNode fill:#e2e8f0,stroke:#64748b,stroke-width:2px
       classDef classNode fill:#dbeafe,stroke:#2563eb,stroke-width:2px
       classDef funcNode fill:#f0fdf4,stroke:#10b981,stroke-width:2px
```

## Responsive Design and Mobile Optimization

### Current Mobile CSS (from mermaid-custom.css)

The current implementation already includes comprehensive mobile optimization:

```css
/* Responsive design */
@media (max-width: 768px) {
  .mermaid-container {
    padding: 1rem;
    margin: 1rem 0;
  }

  .mermaid svg {
    min-height: 200px;
  }

  .mermaid .node .label {
    font-size: 0.875rem;
  }

  .mermaid .edgeLabel {
    font-size: 0.75rem;
    padding: 0.125rem 0.25rem;
  }
}
```

### Enhanced Mobile Features

```javascript
// In mermaid-config.js - Enhanced mobile detection
function isMobileDevice() {
  return (
    window.innerWidth <= 768 ||
    /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent,
    )
  );
}

// Mobile-optimized configuration
if (isMobileDevice()) {
  mermaidConfig.flowchart.nodeSpacing = 30;
  mermaidConfig.flowchart.rankSpacing = 30;
  mermaidConfig.sequence.actorMargin = 30;
  mermaidConfig.sequence.messageMargin = 25;
  mermaidConfig.class.padding = 3;
}
```

## Performance Considerations

### Lazy Loading for Large Diagrams

```javascript
// Intersection Observer for lazy loading
const mermaidObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const mermaidElement = entry.target;
        if (!mermaidElement.classList.contains("mermaid-rendered")) {
          mermaid.init(undefined, mermaidElement);
          mermaidElement.classList.add("mermaid-rendered");
        }
        mermaidObserver.unobserve(mermaidElement);
      }
    });
  },
  { threshold: 0.1 },
);

// Apply to all Mermaid diagrams
document.querySelectorAll(".mermaid").forEach((el) => {
  mermaidObserver.observe(el);
});
```

### Build-Time Optimization

```python
# Conditional Mermaid generation based on complexity
def should_generate_mermaid_diagram(obj):
    """Determine if a Mermaid diagram would be beneficial."""
    if obj.type == "class":
        # Generate for classes with inheritance or many methods
        return len(obj.bases) > 0 or len(obj.subclasses) > 0 or len(obj.methods) > 5
    elif obj.type == "module":
        # Generate for modules with multiple related components
        return len(obj.children) > 3
    return False
```

## Interactive Features Enhancement

### Clickable Elements with Cross-References

```rst
.. mermaid::
   :caption: Interactive Agent Architecture

   classDiagram
       class Agent {
           +name: str
           +run(input: str) str
       }

       class SimpleAgent {
           +execute() Response
       }

       Agent <|-- SimpleAgent : inherits

       click Agent "agent.html" "Go to Agent documentation"
       click SimpleAgent "simple-agent.html" "Go to SimpleAgent documentation"
```

### Zoom and Pan Controls

```javascript
// Enhanced interaction controls
mermaidConfig.zoom = true;
mermaidConfig.pan = true;
mermaidConfig.controls = true;

// Add zoom controls to container
function addZoomControls(container) {
  const controls = document.createElement("div");
  controls.className = "mermaid-controls";
  controls.innerHTML = `
        <button onclick="zoomIn(this)">🔍+</button>
        <button onclick="zoomOut(this)">🔍-</button>
        <button onclick="resetZoom(this)">↻</button>
    `;
  container.appendChild(controls);
}
```

## CSS Styling and Theming Options

### Current Theme Integration

The extension already includes comprehensive Furo theme integration:

```css
/* Override Mermaid default colors to match Furo theme */
.mermaid .node rect,
.mermaid .node circle {
  fill: var(--color-api-background);
  stroke: var(--color-brand-primary);
  stroke-width: 2px;
}

/* Dark theme overrides */
@media (prefers-color-scheme: dark) {
  .mermaid .node rect {
    fill: var(--color-background-secondary);
    stroke: var(--color-brand-primary);
  }
}
```

### Custom Styling Classes

```css
/* Enhanced styling for different diagram types */
.mermaid-architecture {
  border: 3px solid var(--color-brand-primary);
  border-radius: 15px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.mermaid-sequence {
  box-shadow: 0 8px 25px rgba(37, 99, 235, 0.15);
  transform: perspective(1000px) rotateX(2deg);
}

.mermaid-class-diagram {
  position: relative;
  overflow: hidden;
}

.mermaid-class-diagram::after {
  content: "🏛️ Class Structure";
  position: absolute;
  top: 10px;
  left: 10px;
  background: var(--color-brand-primary);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}
```

## Current Implementation Status

### ✅ Production Ready Features

- **Complete Mermaid.js Integration**: Version 10.6.1+ with all diagram types
- **Furo Theme Integration**: Perfect color matching and dark mode support
- **Mobile Responsive**: Comprehensive mobile optimization
- **Interactive Elements**: Zoom, pan, and click functionality
- **Performance Optimized**: Lazy loading and efficient rendering

### 🚀 Issue #6 Enhancement Opportunities

1. **AutoAPI Template Integration**: Custom inheritance and architecture diagrams
2. **Interactive Cross-References**: Clickable nodes linking to documentation
3. **Dynamic Diagram Generation**: Conditional diagrams based on complexity
4. **Enhanced Mobile UX**: Touch gestures and mobile-first controls
5. **Animation Effects**: Smooth transitions and loading states

### 📋 Implementation Roadmap

1. **Phase 1**: Enhanced AutoAPI templates with Mermaid diagrams
2. **Phase 2**: Interactive cross-reference system
3. **Phase 3**: Performance optimization for large monorepos
4. **Phase 4**: Advanced mobile UX features

## Best Practices for AutoAPI Integration

### 1. Conditional Diagram Generation

```jinja2
{# Only generate diagrams when they add value #}
{% if (obj.type == "class" and (obj.bases|length > 0 or obj.subclasses|length > 0))
   or (obj.type == "module" and obj.children|length > 3) %}
{# Generate Mermaid diagram #}
{% endif %}
```

### 2. Responsive Design Patterns

```css
/* Container queries for adaptive layouts */
@container (max-width: 600px) {
  .mermaid-container {
    padding: 0.5rem;
    font-size: 0.875rem;
  }
}
```

### 3. Performance Guidelines

- **Limit Complexity**: Maximum 20 nodes per diagram
- **Use Subgraphs**: Group related components
- **Lazy Loading**: Only render visible diagrams
- **Caching**: Leverage browser and Sphinx caching

---

**Status**: Production-ready with extensive customization  
**Next Extension**: [sphinxcontrib.plantuml](sphinxcontrib_plantuml.md) - Enterprise diagram support  
**Related**: [Custom CSS Integration](../../css_files_comparison_20250813.md)
