# sphinxcontrib.plantuml - Enterprise PlantUML Diagram Support

**Extension**: `sphinxcontrib.plantuml`  
**Purpose**: Professional UML diagrams with PlantUML integration  
**Status**: ✅ Active in PyDevelop-Docs  
**Priority**: High - Enterprise-grade diagram generation  
**Issue #6 Relevance**: Essential for complex architectural diagrams

## Overview

The `sphinxcontrib.plantuml` extension integrates PlantUML, the industry-standard tool for creating UML diagrams from simple textual descriptions. PlantUML excels at complex architectural diagrams, detailed class relationships, and enterprise-level system documentation.

### Visual Capabilities

- **Professional UML**: All standard UML diagram types with precise formatting
- **Complex Architectures**: Multi-level system diagrams with detailed relationships
- **Enterprise Standards**: Industry-standard notation and symbols
- **High-Quality Output**: Vector-based SVG/PNG with crisp rendering
- **Extensive Customization**: Themes, colors, and styling options
- **Large-Scale Diagrams**: Handles complex systems with hundreds of components

## Diagram Types and Use Cases

### 1. Detailed Class Diagrams - Perfect for Complex OOP

```rst
.. uml::
   :caption: Haive Agent Framework - Complete Class Architecture
   :align: center

   @startuml
   !theme vibrant

   abstract class Agent {
       +name: str
       +engine: AugLLMConfig
       +state: StateSchema
       +conversation_history: List[BaseMessage]
       --
       +run(input: str): str
       +arun(input: str): Awaitable[str]
       +add_tool(tool: Tool): void
       +get_state(): StateSchema
       #_validate_input(input: str): bool
       #_process_response(response: str): str
   }

   class SimpleAgent {
       +prompt_template: ChatPromptTemplate
       +tools: List[Tool]
       +recompile_needed: bool
       --
       +execute(): Response
       +recompile(): void
       #_build_prompt(input: str): str
   }

   class ReactAgent {
       +reasoning_steps: List[ReasoningStep]
       +max_iterations: int
       +reflection_enabled: bool
       --
       +reasoning_loop(): Decision
       +tool_selection(): Tool
       +reflection(): Evaluation
       #_analyze_context(): Context
       #_plan_execution(): Plan
   }

   class MultiAgent {
       +agents: Dict[str, Agent]
       +execution_mode: ExecutionMode
       +coordination_strategy: Strategy
       --
       +coordinate(): Result
       +add_agent(name: str, agent: Agent): void
       +remove_agent(name: str): void
       #_route_to_agent(input: str): Agent
       #_merge_responses(responses: List[str]): str
   }

   enum ExecutionMode {
       SEQUENTIAL
       PARALLEL
       CONDITIONAL
       HIERARCHICAL
   }

   class AugLLMConfig {
       +model: str
       +temperature: float
       +max_tokens: int
       +tools: List[Tool]
       +structured_output_model: BaseModel
       --
       +with_structured_output(model: BaseModel): AugLLMConfig
       +add_tool(tool: Tool): AugLLMConfig
   }

   interface Tool {
       +name: str
       +description: str
       --
       +execute(input: str): str
   }

   class StateSchema {
       +messages: List[BaseMessage]
       +metadata: Dict[str, Any]
       +created_at: datetime
       --
       +add_message(message: BaseMessage): void
       +get_context(): Dict[str, Any]
       +serialize(): Dict[str, Any]
   }

   Agent <|-- SimpleAgent
   Agent <|-- ReactAgent
   Agent <|-- MultiAgent
   Agent --> AugLLMConfig : uses
   Agent --> StateSchema : manages
   Agent --> Tool : utilizes
   MultiAgent --> ExecutionMode : configured_with
   MultiAgent o-- Agent : contains

   note right of Agent : "Base agent with core\nfunctionality and state\nmanagement"

   note bottom of MultiAgent : "Orchestrates multiple agents\nwith different execution modes\nand coordination strategies"

   @enduml
```

### 2. Complex Sequence Diagrams - Multi-Agent Interactions

```rst
.. uml::
   :caption: Multi-Agent Processing Sequence
   :scale: 80%

   @startuml
   !theme amiga

   actor User as U
   participant "MultiAgent\nCoordinator" as MA
   participant "ReactAgent\n(Planner)" as RA
   participant "Tool\nRegistry" as TR
   participant "SimpleAgent\n(Executor)" as SA
   participant "StateSchema\nManager" as SM
   database "Vector\nStore" as VS

   U -> MA: execute_task("Analyze competitor data")
   activate MA

   MA -> SM: get_current_state()
   activate SM
   SM --> MA: StateSchema{messages, metadata}
   deactivate SM

   MA -> RA: plan_analysis(task, state)
   activate RA

   RA -> TR: get_available_tools()
   activate TR
   TR --> RA: [WebSearchTool, DataAnalysisTool, VisualizationTool]
   deactivate TR

   RA -> RA: reasoning_loop()
   note right: Internal reasoning:\n1. Break down task\n2. Select tools\n3. Plan sequence

   RA --> MA: AnalysisPlan{steps, tools, expected_output}
   deactivate RA

   loop for each step in plan
       MA -> SA: execute_step(step, tools)
       activate SA

       SA -> TR: load_tool(tool_name)
       activate TR
       TR --> SA: ToolInstance
       deactivate TR

       SA -> VS: search_relevant_data(query)
       activate VS
       VS --> SA: RelevantDocuments
       deactivate VS

       SA -> SA: process_with_tool()
       SA --> MA: StepResult{data, status}
       deactivate SA

       MA -> SM: update_state(step_result)
       activate SM
       SM --> MA: Updated StateSchema
       deactivate SM
   end

   MA -> SA: synthesize_results(all_results)
   activate SA
   SA --> MA: FinalAnalysis{insights, recommendations}
   deactivate SA

   MA -> SM: finalize_state(final_result)
   activate SM
   SM --> MA: Complete StateSchema
   deactivate SM

   MA --> U: AnalysisReport{insights, visualizations, next_steps}
   deactivate MA

   note over U, VS: Complete multi-agent workflow\nwith state management and\ntool coordination

   @enduml
```

### 3. Component Diagrams - System Architecture

```rst
.. uml::
   :caption: PyDevelop-Docs Extension Architecture

   @startuml
   !theme blueprint

   package "PyDevelop-Docs Core" {
       component [CLI Interface] as CLI
       component [Configuration Manager] as Config
       component [Template Engine] as Template
       component [Builder System] as Builder
   }

   package "Sphinx Extensions" {
       component [AutoAPI] as API
       component [Mermaid] as Mermaid
       component [PlantUML] as PlantUML
       component [Graphviz] as Graphviz
       component [Block Diagrams] as Block
   }

   package "Documentation Output" {
       component [HTML Generator] as HTML
       component [PDF Generator] as PDF
       component [CSS Processor] as CSS
       component [JS Bundler] as JS
   }

   package "External Tools" {
       component [PlantUML Server] as PlantUMLServer
       component [Graphviz Engine] as GraphvizEngine
       component [Mermaid Renderer] as MermaidRenderer
   }

   CLI --> Config : configures
   Config --> Template : provides settings
   Template --> Builder : generates content

   Builder --> API : processes Python code
   Builder --> Mermaid : renders diagrams
   Builder --> PlantUML : generates UML
   Builder --> Graphviz : creates graphs
   Builder --> Block : builds block diagrams

   API --> HTML : API documentation
   Mermaid --> HTML : interactive diagrams
   PlantUML --> HTML : UML diagrams
   Graphviz --> HTML : inheritance graphs
   Block --> HTML : network diagrams

   HTML --> CSS : styled output
   HTML --> JS : interactive features

   PlantUML --> PlantUMLServer : remote rendering
   Graphviz --> GraphvizEngine : local processing
   Mermaid --> MermaidRenderer : client-side rendering

   note top of "External Tools" : Optional external\nrendering services\nfor better performance

   @enduml
```

### 4. Activity Diagrams - Documentation Build Process

```rst
.. uml::
   :caption: PyDevelop-Docs Build Workflow

   @startuml
   !theme carbon

   start

   :User runs pydvlp-docs init;

   if (Project type?) then (Single Package)
       :Configure single package settings;
       :Set autoapi_dirs to package path;
   else (Monorepo)
       :Configure central hub settings;
       :Enable sphinx-collections;
       :Set up package aggregation;
   endif

   :Generate conf.py from template;
   :Apply hierarchical AutoAPI settings;

   partition "Extension Processing" {
       :Load Sphinx extensions;
       :Configure AutoAPI;
       :Setup Mermaid rendering;
       :Initialize PlantUML;
       :Configure Graphviz;
       :Setup block diagrams;
   }

   partition "Content Generation" {
       :Scan Python source code;
       :Generate API documentation;
       :Process custom templates;
       :Render diagrams;
       :Apply CSS theming;
   }

   if (Build successful?) then (yes)
       :Generate HTML output;
       :Apply responsive CSS;
       :Bundle JavaScript;
       :Optimize images;
       :Create sitemap;
       stop
   else (no)
       :Log build errors;
       :Suggest fixes;
       :Exit with error code;
       stop
   endif

   @enduml
```

### 5. State Diagrams - Agent Lifecycle Management

```rst
.. uml::
   :caption: Agent State Management

   @startuml
   !theme superhero-outline

   state "Agent Lifecycle" as Lifecycle {
       [*] --> Initializing

       state Initializing {
           [*] --> LoadingConfig
           LoadingConfig --> ValidatingConfig
           ValidatingConfig --> SetupTools
           SetupTools --> Ready
           ValidatingConfig --> ConfigError : validation fails
           ConfigError --> [*]
       }

       Ready --> Processing : input received

       state Processing {
           [*] --> InputValidation
           InputValidation --> ToolSelection : valid input
           InputValidation --> InputError : invalid input

           state ToolSelection {
               [*] --> AnalyzeRequest
               AnalyzeRequest --> SelectTools
               SelectTools --> LoadTools
               LoadTools --> ToolsReady
           }

           ToolsReady --> Execution

           state Execution {
               [*] --> PreProcessing
               PreProcessing --> ToolExecution
               ToolExecution --> PostProcessing
               PostProcessing --> ResponseGeneration
               ResponseGeneration --> ValidationOutput
               ValidationOutput --> Complete

               ToolExecution --> ToolError : tool fails
               ToolError --> RetryTool : retries < max
               ToolError --> ExecutionFailed : retries >= max
               RetryTool --> ToolExecution
           }

           Complete --> [*]
           ExecutionFailed --> [*]
           InputError --> [*]
       }

       Processing --> Ready : task complete
       Processing --> Error : processing fails
       Processing --> Shutdown : shutdown requested

       Ready --> Maintenance : maintenance mode
       Maintenance --> Ready : maintenance complete

       Error --> Recovery : auto recovery
       Error --> Shutdown : critical error
       Recovery --> Ready : recovery successful
       Recovery --> Shutdown : recovery failed

       Shutdown --> [*]
   }

   note right of Initializing : Agent startup and\nconfiguration phase
   note bottom of Processing : Main processing loop\nwith tool integration
   note left of Error : Error handling and\nrecovery mechanisms

   @enduml
```

## Configuration Options

### Current PyDevelop-Docs Configuration

```python
# In config.py - Lines 472, 198-199
extensions = [
    "sphinxcontrib.plantuml",    # PlantUML diagram support
    # ... other extensions
]

# PlantUML configuration
"plantuml_output_format": "svg",  # Vector output for crisp rendering
"plantuml": "plantuml",          # Command or server URL
```

### Enhanced Configuration for Issue #6

```python
# Advanced PlantUML configuration for better integration
plantuml_output_format = "svg"           # SVG for scalability
plantuml_latex_output_format = "pdf"     # PDF for LaTeX output
plantuml_epstopdf = "epstopdf"           # EPS to PDF conversion

# PlantUML server configuration (optional, for better performance)
plantuml_server_url = "http://www.plantuml.com/plantuml"
plantuml_server_type = "server"          # "server" or "local"

# Enhanced PlantUML jar configuration
plantuml_jar_path = "/usr/share/plantuml/plantuml.jar"
plantuml_java_args = [
    "-Djava.awt.headless=true",          # Headless mode
    "-Duser.timezone=UTC",               # Consistent timezone
    "-Xmx1024m",                         # Memory limit
]

# Custom PlantUML configuration
plantuml_config = {
    "!theme": "vibrant",                 # Modern theme
    "skinparam": {
        "backgroundColor": "transparent",
        "classAttributeIconSize": 0,
        "classFontColor": "#1e293b",
        "classFontName": "ui-sans-serif",
        "classFontSize": 11,
        "classHeaderBackgroundColor": "#2563eb",
        "classHeaderFontColor": "#ffffff",
        "classBorderColor": "#1d4ed8",
        "packageBorderColor": "#64748b",
        "packageFontColor": "#374151",
        "arrowColor": "#2563eb",
        "arrowFontColor": "#1e293b",
        "noteBackgroundColor": "#fef3c7",
        "noteBorderColor": "#f59e0b",
        "noteFontColor": "#92400e",
    }
}

# Responsive design settings
plantuml_responsive = True               # Enable responsive images
plantuml_max_width = 1200               # Maximum diagram width
plantuml_mobile_scale = 0.8             # Mobile scaling factor
```

## Template Integration for Issue #6

### 1. Enhanced Class Documentation with UML

```jinja2
{# In _autoapi_templates/python/class.rst #}

{% if obj.bases or obj.subclasses or obj.methods|length > 5 %}
**Detailed Class Architecture:**

.. uml::
   :caption: {{ obj.name }} - Complete UML Class Diagram
   :scale: 90%

   @startuml
   !theme vibrant

   {% if obj.bases %}
   {# Base classes #}
   {% for base in obj.bases %}
   class {{ base.split('.')[-1] }} {
       <<abstract>>
   }
   {% endfor %}
   {% endif %}

   {# Current class with full details #}
   class {{ obj.name }} {
       {% for attr in obj.attributes %}
       {% if not attr.name.startswith('_') %}
       +{{ attr.name }}: {{ attr.annotation or 'Any' }}
       {% endif %}
       {% endfor %}
       --
       {% for method in obj.methods %}
       {% if not method.name.startswith('_') or method.name in ['__init__', '__call__'] %}
       {% if method.name.startswith('_') %}#{% else %}+{% endif %}{{ method.name }}({% for arg in method.args %}{{ arg }}{% if not loop.last %}, {% endif %}{% endfor %}): {{ method.return_annotation or 'Any' }}
       {% endif %}
       {% endfor %}
   }

   {% if obj.subclasses %}
   {# Subclasses #}
   {% for subclass in obj.subclasses %}
   class {{ subclass.split('.')[-1] }} {
   }
   {% endfor %}
   {% endif %}

   {# Relationships #}
   {% for base in obj.bases %}
   {{ base.split('.')[-1] }} <|-- {{ obj.name }} : inherits
   {% endfor %}

   {% for subclass in obj.subclasses %}
   {{ obj.name }} <|-- {{ subclass.split('.')[-1] }} : extends
   {% endfor %}

   {# Usage relationships #}
   {% if obj.used_by %}
   {% for user in obj.used_by[:3] %}
   {{ obj.name }} <-- {{ user.split('.')[-1] }} : uses
   {% endfor %}
   {% endif %}

   note right of {{ obj.name }} : {{ obj.docstring.split('\n')[0] or 'Main class implementation' }}

   @enduml

{% endif %}
```

### 2. Package Architecture Overview

```jinja2
{# In _autoapi_templates/python/package.rst #}

**Package Architecture:**

.. uml::
   :caption: {{ obj.name }} - Complete Package Structure
   :align: center

   @startuml
   !theme blueprint

   package "{{ obj.name }}" as MainPackage {
       {% for module in obj.children %}
       {% if module.type == "module" %}

       package "{{ module.name.split('.')[-1] }}" as {{ module.name.replace('.', '_') }} {
           {% for child in module.children %}
           {% if child.type == "class" %}
           class {{ child.name }} {
               {% for method in child.methods[:3] %}
               +{{ method.name }}()
               {% endfor %}
           }
           {% elif child.type == "function" %}
           interface {{ child.name }} {
               {{ child.signature or '+execute()' }}
           }
           {% endif %}
           {% endfor %}
       }

       {% endif %}
       {% endfor %}
   }

   {# Show relationships between modules #}
   {% for module in obj.children %}
   {% for other_module in obj.children %}
   {% if module != other_module and other_module.name in module.imports %}
   {{ module.name.replace('.', '_') }} --> {{ other_module.name.replace('.', '_') }} : imports
   {% endif %}
   {% endfor %}
   {% endfor %}

   note top of MainPackage : {{ obj.docstring.split('\n')[0] if obj.docstring else 'Package overview' }}

   @enduml
```

### 3. Multi-Agent System Architecture

```jinja2
{# For multi-agent systems documentation #}

.. uml::
   :caption: Multi-Agent System Architecture
   :scale: 75%

   @startuml
   !theme carbon

   actor User as U

   package "Haive Framework" {
       component "MultiAgent Coordinator" as MAC {
           port "Input Processing" as IP
           port "Output Aggregation" as OA
           port "Agent Management" as AM
       }

       component "ReactAgent" as RA {
           port "Reasoning Engine" as RE
           port "Tool Interface" as TI
       }

       component "SimpleAgent" as SA {
           port "Direct Execution" as DE
           port "Response Generation" as RG
       }

       component "Tool Registry" as TR {
           port "Tool Discovery" as TD
           port "Tool Execution" as TE
       }

       component "State Manager" as SM {
           port "State Persistence" as SP
           port "Context Management" as CM
       }
   }

   database "Vector Store" as VS
   cloud "External APIs" as APIs

   U --> IP : task request
   OA --> U : final result

   IP --> AM : route to agents
   AM --> RE : planning tasks
   AM --> DE : execution tasks

   RE --> TI : tool selection
   DE --> RG : response creation

   TI --> TD : discover tools
   TD --> TE : execute tools

   TE --> APIs : external calls
   TE --> VS : data retrieval

   AM --> SP : save state
   SP --> CM : manage context
   CM --> RE : provide context
   CM --> DE : provide context

   @enduml
```

## Responsive Design and Mobile Optimization

### Mobile-Optimized PlantUML CSS

```css
/* PlantUML responsive design */
.plantuml-container {
  max-width: 100%;
  overflow-x: auto;
  margin: 1rem 0;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.plantuml-container img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}

/* Mobile optimizations */
@media (max-width: 768px) {
  .plantuml-container {
    margin: 0.5rem 0;
    overflow-x: scroll;
    -webkit-overflow-scrolling: touch;
  }

  .plantuml-container img {
    min-width: 600px; /* Maintain diagram readability */
    max-width: none;
  }

  /* Zoom controls for mobile */
  .plantuml-container::after {
    content: "📱 Tap and drag to explore";
    display: block;
    text-align: center;
    font-size: 0.75rem;
    color: #6b7280;
    padding: 0.5rem;
    background: #f9fafb;
    border-top: 1px solid #e5e7eb;
  }
}

/* High-DPI display optimization */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .plantuml-container img[src$=".svg"] {
    image-rendering: auto;
    image-rendering: crisp-edges;
    image-rendering: pixelated;
  }
}
```

### PlantUML Responsive Configuration

```python
# Responsive PlantUML generation
def configure_plantuml_responsive():
    """Configure PlantUML for responsive output."""
    base_config = {
        "scale": "0.8",                  # Default scale
        "dpi": "150",                    # High DPI
        "format": "svg",                 # Vector format
    }

    mobile_config = {
        "scale": "0.6",                  # Smaller for mobile
        "dpi": "200",                    # Higher DPI for mobile
        "max_width": "800",              # Limit width
    }

    return base_config, mobile_config
```

## Performance Considerations

### Build-Time Optimization

```python
# PlantUML caching and optimization
plantuml_cache_enabled = True           # Enable diagram caching
plantuml_cache_dir = "_plantuml_cache"  # Cache directory
plantuml_parallel_processing = True     # Parallel rendering
plantuml_max_concurrent = 4             # Concurrent diagram limit

# Conditional diagram generation
def should_generate_plantuml_diagram(obj):
    """Determine if a PlantUML diagram adds value."""
    complexity_score = 0

    if obj.type == "class":
        complexity_score += len(obj.methods) * 1
        complexity_score += len(obj.attributes) * 0.5
        complexity_score += len(obj.bases) * 2
        complexity_score += len(obj.subclasses) * 1.5
    elif obj.type == "module":
        complexity_score += len(obj.children) * 1
        complexity_score += len(obj.imports) * 0.5

    return complexity_score > 5  # Only generate for complex objects
```

### Memory Management

```python
# Memory-efficient PlantUML processing
plantuml_memory_limit = "1024m"         # JVM memory limit
plantuml_timeout = 30                   # Rendering timeout (seconds)
plantuml_cleanup_temp = True            # Clean temporary files
plantuml_batch_size = 10                # Process diagrams in batches
```

## Integration with Other Extensions

### AutoAPI Integration

```python
# Enhanced AutoAPI with PlantUML diagrams
autoapi_plantuml_enabled = True
autoapi_plantuml_inheritance = True      # Generate inheritance diagrams
autoapi_plantuml_composition = True      # Show composition relationships
autoapi_plantuml_min_complexity = 3     # Minimum complexity for diagrams
```

### Cross-Reference Support

```rst
.. uml::
   :caption: Cross-Referenced Architecture

   @startuml
   class Agent {
       +run()
   }
   class SimpleAgent {
       +execute()
   }

   Agent <|-- SimpleAgent

   note right of Agent : See :class:`haive.core.Agent`
   note right of SimpleAgent : See :class:`haive.agents.SimpleAgent`
   @enduml
```

## Current Implementation Status

### ✅ Production Ready Features

- **PlantUML Integration**: Full PlantUML support with SVG output
- **UML Diagram Types**: All standard UML diagrams supported
- **Theme Integration**: Configurable themes matching Furo
- **Performance Optimized**: Caching and parallel processing ready

### 🚀 Issue #6 Enhancement Opportunities

1. **Advanced AutoAPI Templates**: Complex class and package diagrams
2. **Interactive Elements**: Clickable UML elements with cross-references
3. **Mobile Optimization**: Touch-friendly diagram exploration
4. **Performance Scaling**: Optimized for large monorepo documentation
5. **Theme Customization**: Deep Furo theme integration

### 📋 Implementation Roadmap

1. **Phase 1**: Enhanced AutoAPI templates with detailed UML diagrams
2. **Phase 2**: Mobile-optimized responsive design
3. **Phase 3**: Performance optimization and caching
4. **Phase 4**: Interactive features and cross-references

## Best Practices

### 1. Diagram Complexity Management

```plantuml
!define MAX_METHODS 8
!define MAX_ATTRIBUTES 6
!define MAX_INHERITANCE_DEPTH 3

' Use these limits to keep diagrams readable
```

### 2. Responsive Design Guidelines

- **Minimum Width**: 600px for mobile readability
- **SVG Output**: Always use SVG for scalability
- **Font Sizes**: Minimum 10pt for mobile devices
- **Color Contrast**: Ensure accessibility compliance

### 3. Performance Best Practices

- **Conditional Generation**: Only create diagrams for complex structures
- **Caching Strategy**: Cache rendered diagrams between builds
- **Batch Processing**: Process multiple diagrams concurrently
- **Memory Limits**: Set appropriate JVM memory limits

---

**Status**: Production-ready with enterprise-grade capabilities  
**Next Extension**: [sphinxcontrib.blockdiag](sphinxcontrib_blockdiag.md) - Network and block diagrams  
**Related**: [Template Customization Guide](../../issues/jinja2_research_comprehensive.md)
