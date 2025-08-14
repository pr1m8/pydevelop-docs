# sphinxcontrib.blockdiag - Block and Network Diagram Creation

**Extension**: `sphinxcontrib.blockdiag`  
**Purpose**: Simple block diagrams and network topology visualization  
**Status**: ✅ Active in PyDevelop-Docs  
**Priority**: Medium - Specialized network and system diagrams  
**Issue #6 Relevance**: Useful for system architecture and data flow diagrams

## Overview

The `sphinxcontrib.blockdiag` extension provides a simple yet powerful way to create block diagrams, network topologies, and system architecture diagrams. It's particularly effective for showing data flow, system components, and network structures in a clean, minimalist style.

### Visual Capabilities

- **Clean Block Diagrams**: Simple, professional-looking block structures
- **Network Topologies**: Network architecture and connection diagrams
- **Data Flow Visualization**: Process flow and data movement diagrams
- **System Architecture**: High-level system component relationships
- **Minimal Syntax**: Easy-to-write textual descriptions
- **Customizable Styling**: Colors, shapes, and layout options

## Diagram Types and Use Cases

### 1. System Architecture Diagrams

```rst
.. blockdiag::
   :caption: PyDevelop-Docs System Architecture
   :align: center

   blockdiag {
       // System components
       User [color = "#dbeafe"];
       CLI [color = "#bfdbfe"];
       Config [color = "#93c5fd"];
       Template [color = "#60a5fa"];
       Builder [color = "#3b82f6"];
       Output [color = "#1d4ed8"];

       // Data flow
       User -> CLI -> Config -> Template -> Builder -> Output;

       // Extension system
       group {
           label = "Sphinx Extensions";
           color = "#f0fdf4";
           AutoAPI [color = "#dcfce7"];
           Mermaid [color = "#bbf7d0"];
           PlantUML [color = "#86efac"];
           BlockDiag [color = "#4ade80"];
       }

       Builder -> AutoAPI;
       Builder -> Mermaid;
       Builder -> PlantUML;
       Builder -> BlockDiag;

       // Output formats
       group {
           label = "Output Formats";
           color = "#fef3c7";
           HTML [color = "#fde68a"];
           PDF [color = "#fcd34d"];
           CSS [color = "#fbbf24"];
           JS [color = "#f59e0b"];
       }

       Output -> HTML;
       Output -> PDF;
       Output -> CSS;
       Output -> JS;
   }
```

### 2. Agent Data Flow Diagrams

```rst
.. blockdiag::
   :caption: Haive Agent Data Flow
   :scale: 90%

   blockdiag {
       // Input processing
       UserInput [label = "User\nInput", color = "#dbeafe"];
       Validation [label = "Input\nValidation", color = "#bfdbfe"];
       Preprocessing [label = "Text\nPreprocessing", color = "#93c5fd"];

       // Agent processing
       AgentRouter [label = "Agent\nRouter", color = "#fef3c7"];
       SimpleAgent [label = "Simple\nAgent", color = "#fde68a"];
       ReactAgent [label = "React\nAgent", color = "#fcd34d"];
       MultiAgent [label = "Multi\nAgent", color = "#fbbf24"];

       // Tool system
       ToolRegistry [label = "Tool\nRegistry", color = "#f0fdf4"];
       Calculator [label = "Calculator\nTool", color = "#dcfce7"];
       WebSearch [label = "Web Search\nTool", color = "#bbf7d0"];
       FileSystem [label = "File System\nTool", color = "#86efac"];

       // Output processing
       ResponseGen [label = "Response\nGeneration", color = "#fef2f2"];
       Formatting [label = "Output\nFormatting", color = "#fecaca"];
       FinalOutput [label = "Final\nOutput", color = "#fca5a5"];

       // Main flow
       UserInput -> Validation -> Preprocessing -> AgentRouter;

       // Agent selection
       AgentRouter -> SimpleAgent;
       AgentRouter -> ReactAgent;
       AgentRouter -> MultiAgent;

       // Tool integration
       SimpleAgent -> ToolRegistry;
       ReactAgent -> ToolRegistry;
       MultiAgent -> ToolRegistry;

       ToolRegistry -> Calculator;
       ToolRegistry -> WebSearch;
       ToolRegistry -> FileSystem;

       // Output flow
       SimpleAgent -> ResponseGen;
       ReactAgent -> ResponseGen;
       MultiAgent -> ResponseGen;

       ResponseGen -> Formatting -> FinalOutput;

       // Groups for organization
       group {
           label = "Input Processing";
           color = "#f8fafc";
           UserInput; Validation; Preprocessing;
       }

       group {
           label = "Agent Layer";
           color = "#fffbeb";
           AgentRouter; SimpleAgent; ReactAgent; MultiAgent;
       }

       group {
           label = "Tool Ecosystem";
           color = "#f0fdf4";
           ToolRegistry; Calculator; WebSearch; FileSystem;
       }

       group {
           label = "Output Pipeline";
           color = "#fef2f2";
           ResponseGen; Formatting; FinalOutput;
       }
   }
```

### 3. Network Topology Diagrams

```rst
.. blockdiag::
   :caption: Haive Deployment Architecture
   :align: center

   blockdiag {
       // Client tier
       WebBrowser [label = "Web\nBrowser", color = "#dbeafe"];
       MobileApp [label = "Mobile\nApp", color = "#bfdbfe"];
       CLI [label = "CLI\nInterface", color = "#93c5fd"];

       // Load balancer
       LoadBalancer [label = "Load\nBalancer", color = "#fef3c7"];

       // Application tier
       AppServer1 [label = "App Server\n1", color = "#f0fdf4"];
       AppServer2 [label = "App Server\n2", color = "#dcfce7"];
       AppServer3 [label = "App Server\n3", color = "#bbf7d0"];

       // Service tier
       AgentService [label = "Agent\nService", color = "#fef2f2"];
       ToolService [label = "Tool\nService", color = "#fecaca"];
       StateService [label = "State\nService", color = "#fca5a5"];

       // Data tier
       PostgreSQL [label = "PostgreSQL\nDatabase", color = "#f3e8ff"];
       Redis [label = "Redis\nCache", color = "#e9d5ff"];
       VectorDB [label = "Vector\nDatabase", color = "#ddd6fe"];

       // External services
       OpenAI [label = "OpenAI\nAPI", color = "#fff7ed"];
       AWS [label = "AWS\nServices", color = "#fed7aa"];

       // Connections
       WebBrowser -> LoadBalancer;
       MobileApp -> LoadBalancer;
       CLI -> LoadBalancer;

       LoadBalancer -> AppServer1;
       LoadBalancer -> AppServer2;
       LoadBalancer -> AppServer3;

       AppServer1 -> AgentService;
       AppServer2 -> ToolService;
       AppServer3 -> StateService;

       AgentService -> OpenAI;
       ToolService -> AWS;
       StateService -> PostgreSQL;
       StateService -> Redis;
       StateService -> VectorDB;

       // Network groups
       group {
           label = "Client Tier";
           color = "#f8fafc";
           WebBrowser; MobileApp; CLI;
       }

       group {
           label = "Application Tier";
           color = "#f0fdf4";
           AppServer1; AppServer2; AppServer3;
       }

       group {
           label = "Service Tier";
           color = "#fef2f2";
           AgentService; ToolService; StateService;
       }

       group {
           label = "Data Tier";
           color = "#f3e8ff";
           PostgreSQL; Redis; VectorDB;
       }

       group {
           label = "External Services";
           color = "#fff7ed";
           OpenAI; AWS;
       }
   }
```

### 4. Documentation Build Pipeline

```rst
.. blockdiag::
   :caption: Documentation Build Process
   :scale: 80%

   blockdiag {
       // Source inputs
       PythonCode [label = "Python\nSource Code", color = "#dbeafe"];
       Docstrings [label = "Function\nDocstrings", color = "#bfdbfe"];
       MarkdownFiles [label = "Markdown\nFiles", color = "#93c5fd"];
       ConfigFiles [label = "Config\nFiles", color = "#60a5fa"];

       // Processing stages
       Scanner [label = "Code\nScanner", color = "#fef3c7"];
       Parser [label = "AST\nParser", color = "#fde68a"];
       Extractor [label = "Docstring\nExtractor", color = "#fcd34d"];

       // Documentation generation
       AutoAPI [label = "AutoAPI\nProcessor", color = "#f0fdf4"];
       TemplateEngine [label = "Template\nEngine", color = "#dcfce7"];
       DiagramGen [label = "Diagram\nGenerator", color = "#bbf7d0"];

       // Output processing
       HTMLGen [label = "HTML\nGenerator", color = "#fef2f2"];
       CSSProcessor [label = "CSS\nProcessor", color = "#fecaca"];
       JSBundler [label = "JS\nBundler", color = "#fca5a5"];

       // Final outputs
       StaticSite [label = "Static\nWebsite", color = "#f3e8ff"];
       SearchIndex [label = "Search\nIndex", color = "#e9d5ff"];
       Sitemap [label = "XML\nSitemap", color = "#ddd6fe"];

       // Processing flow
       PythonCode -> Scanner;
       Docstrings -> Parser;
       MarkdownFiles -> Extractor;
       ConfigFiles -> Scanner;

       Scanner -> AutoAPI;
       Parser -> TemplateEngine;
       Extractor -> DiagramGen;

       AutoAPI -> HTMLGen;
       TemplateEngine -> CSSProcessor;
       DiagramGen -> JSBundler;

       HTMLGen -> StaticSite;
       CSSProcessor -> SearchIndex;
       JSBundler -> Sitemap;

       // Processing groups
       group {
           label = "Source Materials";
           color = "#f8fafc";
           PythonCode; Docstrings; MarkdownFiles; ConfigFiles;
       }

       group {
           label = "Analysis Phase";
           color = "#fffbeb";
           Scanner; Parser; Extractor;
       }

       group {
           label = "Generation Phase";
           color = "#f0fdf4";
           AutoAPI; TemplateEngine; DiagramGen;
       }

       group {
           label = "Output Phase";
           color = "#fef2f2";
           HTMLGen; CSSProcessor; JSBundler;
       }

       group {
           label = "Final Deliverables";
           color = "#f3e8ff";
           StaticSite; SearchIndex; Sitemap;
       }
   }
```

## Configuration Options

### Current PyDevelop-Docs Configuration

```python
# In config.py - Line 473
extensions = [
    "sphinxcontrib.blockdiag",   # Block diagram support
    # ... other extensions
]

# Basic blockdiag configuration (implicit defaults)
blockdiag_output_format = "svg"  # Vector output for web
blockdiag_fontpath = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
```

### Enhanced Configuration for Issue #6

```python
# Advanced blockdiag configuration
blockdiag_output_format = "svg"             # SVG for scalability
blockdiag_html_image_format = "svg"         # HTML image format
blockdiag_latex_image_format = "pdf"        # LaTeX image format
blockdiag_pdf_image_format = "pdf"          # PDF image format

# Font configuration for better typography
blockdiag_fontpath = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",          # Primary
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Fallback
    "/System/Library/Fonts/Helvetica.ttc",                      # macOS
]

# Enhanced styling configuration
blockdiag_default_node_color = "#f8fafc"    # Light gray
blockdiag_default_edge_color = "#64748b"    # Slate gray
blockdiag_default_text_color = "#1e293b"    # Dark slate
blockdiag_default_fontsize = 11             # Readable font size

# Responsive design settings
blockdiag_max_width = 1000                  # Maximum diagram width
blockdiag_mobile_scale = 0.8                # Mobile scaling factor
blockdiag_dpi = 150                         # High DPI for crisp rendering

# Performance settings
blockdiag_cache_enabled = True              # Enable diagram caching
blockdiag_parallel_processing = True        # Parallel rendering
blockdiag_timeout = 30                      # Rendering timeout (seconds)
```

## Template Integration for Issue #6

### 1. Module Architecture Templates

```jinja2
{# In _autoapi_templates/python/module.rst #}

{% if obj.children|length > 4 %}
**Module Architecture:**

.. blockdiag::
   :caption: {{ obj.name }} - Component Structure
   :align: center

   blockdiag {
       // Module components
       {% for child in obj.children %}
       {% if child.type == "class" %}
       {{ child.name }} [label = "{{ child.name }}\nClass", color = "#dbeafe"];
       {% elif child.type == "function" %}
       {{ child.name }} [label = "{{ child.name }}\nFunction", color = "#f0fdf4"];
       {% endif %}
       {% endfor %}

       // Relationships (simplified)
       {% set classes = obj.children|selectattr("type", "equalto", "class")|list %}
       {% set functions = obj.children|selectattr("type", "equalto", "function")|list %}

       {% for func in functions[:3] %}
       {% for cls in classes[:3] %}
       {% if cls.name.lower() in func.docstring.lower() %}
       {{ func.name }} -> {{ cls.name }};
       {% endif %}
       {% endfor %}
       {% endfor %}

       // Groups
       group {
           label = "Classes";
           color = "#f8fafc";
           {% for cls in classes %}
           {{ cls.name }};
           {% endfor %}
       }

       group {
           label = "Functions";
           color = "#f0fdf4";
           {% for func in functions %}
           {{ func.name }};
           {% endfor %}
       }
   }

{% endif %}
```

### 2. Package Component Diagrams

```jinja2
{# In _autoapi_templates/python/package.rst #}

**Package Component Overview:**

.. blockdiag::
   :caption: {{ obj.name }} - Package Structure
   :scale: 90%

   blockdiag {
       // Package entry point
       PackageInit [label = "{{ obj.name }}\n__init__.py", color = "#2563eb", textcolor = "#ffffff"];

       // Submodules
       {% for module in obj.children %}
       {% if module.type == "module" %}
       {{ module.name.replace('.', '_') }} [label = "{{ module.name.split('.')[-1] }}\nModule", color = "#dbeafe"];
       PackageInit -> {{ module.name.replace('.', '_') }};

       {% if module.children %}
       // Module contents
       {% for child in module.children[:3] %}
       {% if child.type == "class" %}
       {{ child.name.replace('.', '_') }} [label = "{{ child.name }}\nClass", color = "#f0fdf4"];
       {{ module.name.replace('.', '_') }} -> {{ child.name.replace('.', '_') }};
       {% endif %}
       {% endfor %}
       {% endif %}

       {% endif %}
       {% endfor %}

       // External dependencies (if any)
       {% if obj.imports %}
       group {
           label = "Dependencies";
           color = "#fef3c7";
           {% for imp in obj.imports[:3] %}
           {{ imp.replace('.', '_') }} [label = "{{ imp }}", color = "#fde68a"];
           PackageInit -> {{ imp.replace('.', '_') }};
           {% endfor %}
       }
       {% endif %}
   }
```

### 3. Data Flow Templates

```jinja2
{# For agent workflow documentation #}

.. blockdiag::
   :caption: Agent Processing Pipeline
   :align: center

   blockdiag {
       // Input stage
       UserInput [label = "User\nInput", color = "#dbeafe"];
       InputValidator [label = "Input\nValidator", color = "#bfdbfe"];

       // Processing stage
       AgentSelector [label = "Agent\nSelector", color = "#fef3c7"];
       {% if "simple" in agents %}
       SimpleAgent [label = "Simple\nAgent", color = "#f0fdf4"];
       {% endif %}
       {% if "react" in agents %}
       ReactAgent [label = "React\nAgent", color = "#dcfce7"];
       {% endif %}
       {% if "multi" in agents %}
       MultiAgent [label = "Multi\nAgent", color = "#bbf7d0"];
       {% endif %}

       // Tool integration
       ToolRegistry [label = "Tool\nRegistry", color = "#fef2f2"];

       // Output stage
       ResponseFormatter [label = "Response\nFormatter", color = "#f3e8ff"];
       FinalOutput [label = "Final\nOutput", color = "#e9d5ff"];

       // Flow connections
       UserInput -> InputValidator -> AgentSelector;

       {% if "simple" in agents %}
       AgentSelector -> SimpleAgent -> ToolRegistry;
       {% endif %}
       {% if "react" in agents %}
       AgentSelector -> ReactAgent -> ToolRegistry;
       {% endif %}
       {% if "multi" in agents %}
       AgentSelector -> MultiAgent -> ToolRegistry;
       {% endif %}

       ToolRegistry -> ResponseFormatter -> FinalOutput;

       // Processing groups
       group {
           label = "Input Processing";
           color = "#f8fafc";
           UserInput; InputValidator;
       }

       group {
           label = "Agent Processing";
           color = "#fffbeb";
           AgentSelector;
           {% if "simple" in agents %}SimpleAgent;{% endif %}
           {% if "react" in agents %}ReactAgent;{% endif %}
           {% if "multi" in agents %}MultiAgent;{% endif %}
       }

       group {
           label = "Output Processing";
           color = "#f3e8ff";
           ResponseFormatter; FinalOutput;
       }
   }
```

## Responsive Design and Mobile Optimization

### Mobile-Optimized CSS

```css
/* Blockdiag responsive design */
.blockdiag-container {
  max-width: 100%;
  overflow-x: auto;
  margin: 1rem 0;
  border-radius: 8px;
  background: var(--color-background-secondary);
  border: 1px solid var(--color-background-border);
  padding: 1rem;
}

.blockdiag-container svg {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}

/* Mobile-specific optimizations */
@media (max-width: 768px) {
  .blockdiag-container {
    padding: 0.5rem;
    overflow-x: scroll;
    -webkit-overflow-scrolling: touch;
  }

  .blockdiag-container svg {
    min-width: 500px; /* Maintain readability */
    max-width: none;
  }

  /* Touch-friendly zoom indicator */
  .blockdiag-container::before {
    content: "📱 Swipe to explore diagram";
    display: block;
    text-align: center;
    font-size: 0.75rem;
    color: var(--color-foreground-secondary);
    margin-bottom: 0.5rem;
    padding: 0.25rem;
    background: var(--color-background-primary);
    border-radius: 4px;
    border: 1px solid var(--color-background-border);
  }
}

/* High-DPI optimization */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .blockdiag-container svg {
    image-rendering: -webkit-optimize-contrast;
    image-rendering: crisp-edges;
  }
}

/* Dark theme adjustments */
@media (prefers-color-scheme: dark) {
  .blockdiag-container {
    background: var(--color-background-secondary);
    border-color: var(--color-background-border);
  }
}
```

### Responsive Blockdiag Configuration

```python
# Mobile-responsive blockdiag settings
def get_responsive_blockdiag_config():
    """Get blockdiag configuration optimized for different screen sizes."""

    base_config = {
        "node_width": 120,
        "node_height": 60,
        "span_width": 64,
        "span_height": 40,
        "fontsize": 11,
    }

    mobile_config = {
        "node_width": 100,      # Smaller nodes
        "node_height": 50,
        "span_width": 50,       # Tighter spacing
        "span_height": 30,
        "fontsize": 10,         # Smaller fonts
    }

    return base_config, mobile_config
```

## Performance Considerations

### Build-Time Optimization

```python
# Blockdiag performance optimization
blockdiag_cache_dir = "_blockdiag_cache"    # Cache directory
blockdiag_cache_expiry = 86400               # 24 hours cache
blockdiag_parallel_workers = 2              # Parallel processing workers
blockdiag_memory_limit = "512m"             # Memory limit per process

# Conditional diagram generation
def should_generate_blockdiag(obj):
    """Determine if a block diagram adds value."""
    if obj.type == "module":
        # Generate for modules with multiple components
        return len(obj.children) >= 4
    elif obj.type == "package":
        # Generate for packages with multiple modules
        return len([child for child in obj.children if child.type == "module"]) >= 3
    elif obj.type == "function" and "flow" in obj.name.lower():
        # Generate for functions that represent workflows
        return True
    return False
```

### Memory Management

```python
# Memory-efficient blockdiag processing
blockdiag_cleanup_temp_files = True         # Clean temporary files
blockdiag_max_nodes = 50                    # Limit diagram complexity
blockdiag_max_edges = 100                   # Limit edge count
blockdiag_warn_large_diagrams = True        # Warn about complex diagrams
```

## Integration with Other Extensions

### AutoAPI Integration

```python
# Enhanced AutoAPI with blockdiag diagrams
autoapi_blockdiag_enabled = True
autoapi_blockdiag_module_diagrams = True    # Generate module diagrams
autoapi_blockdiag_package_diagrams = True   # Generate package diagrams
autoapi_blockdiag_min_components = 4        # Minimum components for diagrams
```

### Theme Integration

```python
# Furo theme color integration
blockdiag_furo_colors = {
    "primary": "#2563eb",      # Furo brand blue
    "secondary": "#64748b",    # Slate gray
    "success": "#10b981",      # Emerald
    "warning": "#f59e0b",      # Amber
    "danger": "#ef4444",       # Red
    "info": "#3b82f6",         # Blue
    "light": "#f8fafc",        # Very light gray
    "dark": "#1e293b",         # Dark slate
}
```

## Current Implementation Status

### ✅ Production Ready Features

- **Block Diagram Support**: Full blockdiag integration with SVG output
- **Network Diagrams**: System topology and architecture diagrams
- **Clean Syntax**: Simple, readable diagram descriptions
- **Basic Styling**: Color and layout customization

### 🚀 Issue #6 Enhancement Opportunities

1. **AutoAPI Templates**: Automated module and package diagrams
2. **Responsive Design**: Mobile-optimized diagram layouts
3. **Theme Integration**: Deep Furo theme color matching
4. **Performance Optimization**: Caching and parallel processing
5. **Interactive Elements**: Click-to-zoom and navigation features

### 📋 Implementation Roadmap

1. **Phase 1**: AutoAPI template integration for system diagrams
2. **Phase 2**: Mobile-responsive design implementation
3. **Phase 3**: Performance optimization and caching
4. **Phase 4**: Interactive features and enhanced styling

## Best Practices

### 1. Diagram Simplicity

```blockdiag
// Keep diagrams focused and readable
blockdiag {
    // Maximum 15-20 nodes for readability
    // Use groups to organize components
    // Clear, descriptive labels
}
```

### 2. Color Consistency

```python
# Use consistent color scheme across diagrams
BLOCKDIAG_COLORS = {
    "input": "#dbeafe",        # Light blue
    "process": "#f0fdf4",      # Light green
    "output": "#fef3c7",       # Light yellow
    "external": "#f3e8ff",     # Light purple
    "error": "#fef2f2",        # Light red
}
```

### 3. Mobile-First Design

- **Minimum Node Size**: 80x40px for touch interfaces
- **Font Size**: Minimum 10pt for mobile readability
- **Spacing**: Adequate spacing for touch navigation
- **Scrollable**: Allow horizontal scrolling for large diagrams

### 4. Performance Guidelines

- **Node Limit**: Maximum 20 nodes per diagram
- **Complexity**: Keep relationships simple and clear
- **Caching**: Use diagram caching for repeated builds
- **Conditional**: Only generate diagrams when beneficial

---

**Status**: Specialized extension for system architecture diagrams  
**Next Extension**: [sphinxcontrib.seqdiag](sphinxcontrib_seqdiag.md) - Sequence diagram specialization  
**Related**: [System Architecture Patterns](../../architecture/)
