# sphinxcontrib.seqdiag - Sequence Diagram Generation

**Extension**: `sphinxcontrib.seqdiag`  
**Purpose**: Specialized sequence diagram creation for API interaction flows  
**Status**: ✅ Active in PyDevelop-Docs  
**Priority**: High - Essential for API documentation interaction flows  
**Issue #6 Relevance**: Critical for documenting method calls and agent interactions

## Overview

The `sphinxcontrib.seqdiag` extension specializes in creating sequence diagrams that show the order of interactions between different components, methods, or systems over time. It's particularly valuable for documenting API calls, agent interactions, and complex workflow sequences in the Haive framework.

### Visual Capabilities

- **Time-Based Flow**: Clear chronological representation of interactions
- **Actor/Object Interaction**: Multi-participant communication flows
- **Method Call Sequences**: API method invocation documentation
- **Async/Await Patterns**: Modern asynchronous programming flows
- **Condition Branching**: Conditional logic and error handling
- **Loop Structures**: Iterative processes and batch operations

## Diagram Types and Use Cases

### 1. Agent Interaction Sequences

```rst
.. seqdiag::
   :caption: Multi-Agent Conversation Flow
   :align: center

   seqdiag {
       // Participants
       User; MultiAgent; ReactAgent; SimpleAgent; ToolRegistry; VectorStore;

       activation = none;
       edge_length = 200;
       span_height = 40;

       // Main interaction flow
       User -> MultiAgent [label = "execute_task('Research AI trends')"];
       MultiAgent -> MultiAgent [label = "select_agent_strategy()"];

       // React agent for research
       MultiAgent -> ReactAgent [label = "arun(research_query)"];
       activate ReactAgent;

       ReactAgent -> ToolRegistry [label = "get_tool('web_search')"];
       ToolRegistry --> ReactAgent [label = "WebSearchTool"];

       ReactAgent -> ReactAgent [label = "reasoning_loop()"];
       note right of ReactAgent {
           Internal reasoning:
           1. Analyze query
           2. Plan search strategy
           3. Execute searches
           4. Evaluate results
       }

       // Tool execution
       ReactAgent -> ToolRegistry [label = "execute('web_search', query)"];
       activate ToolRegistry;
       ToolRegistry --> ReactAgent [label = "search_results"];
       deactivate ToolRegistry;

       // Vector storage
       ReactAgent -> VectorStore [label = "store_context(results)"];
       VectorStore --> ReactAgent [label = "context_id"];

       ReactAgent --> MultiAgent [label = "research_summary"];
       deactivate ReactAgent;

       // Simple agent for formatting
       MultiAgent -> SimpleAgent [label = "arun(format_request)"];
       activate SimpleAgent;

       SimpleAgent -> VectorStore [label = "retrieve_context(context_id)"];
       VectorStore --> SimpleAgent [label = "research_data"];

       SimpleAgent -> SimpleAgent [label = "format_response()"];
       SimpleAgent --> MultiAgent [label = "formatted_report"];
       deactivate SimpleAgent;

       // Final response
       MultiAgent --> User [label = "comprehensive_ai_trends_report"];

       // Error handling example
       === Error Scenario ===
       User -> MultiAgent [label = "execute_task('Invalid request')"];
       MultiAgent -> MultiAgent [label = "validate_input()"];
       MultiAgent --> User [label = "ValidationError", color = red];
   }
```

### 2. Tool Execution Sequences

```rst
.. seqdiag::
   :caption: Tool Execution and State Management
   :scale: 90%

   seqdiag {
       // Participants
       Agent; ToolEngine; Calculator; FileSystem; WebAPI; StateManager;

       activation = none;
       edge_length = 180;

       // Tool registration phase
       Agent -> ToolEngine [label = "add_tool(Calculator)"];
       ToolEngine -> Calculator [label = "register()"];
       Calculator --> ToolEngine [label = "tool_metadata"];
       ToolEngine --> Agent [label = "tool_registered"];

       Agent -> ToolEngine [label = "add_tool(FileSystem)"];
       ToolEngine -> FileSystem [label = "register()"];
       FileSystem --> ToolEngine [label = "tool_metadata"];
       ToolEngine --> Agent [label = "tool_registered"];

       // Execution phase
       Agent -> ToolEngine [label = "execute_tool('calculator', '15 * 23')"];
       activate ToolEngine;

       ToolEngine -> StateManager [label = "get_current_state()"];
       StateManager --> ToolEngine [label = "agent_state"];

       ToolEngine -> Calculator [label = "execute('15 * 23')"];
       activate Calculator;
       Calculator -> Calculator [label = "validate_expression()"];
       Calculator -> Calculator [label = "compute_result()"];
       Calculator --> ToolEngine [label = "result: 345"];
       deactivate Calculator;

       ToolEngine -> StateManager [label = "update_state(tool_result)"];
       StateManager --> ToolEngine [label = "state_updated"];

       ToolEngine --> Agent [label = "execution_result"];
       deactivate ToolEngine;

       // Chained tool execution
       Agent -> ToolEngine [label = "execute_tool('filesystem', 'save_result')"];
       activate ToolEngine;

       ToolEngine -> FileSystem [label = "save_file(result)"];
       activate FileSystem;
       FileSystem -> FileSystem [label = "validate_path()"];
       FileSystem -> FileSystem [label = "write_file()"];
       FileSystem --> ToolEngine [label = "file_saved"];
       deactivate FileSystem;

       ToolEngine --> Agent [label = "file_operation_complete"];
       deactivate ToolEngine;

       // Error handling in tool execution
       === Error Scenario ===
       Agent -> ToolEngine [label = "execute_tool('web_api', 'invalid_endpoint')"];
       ToolEngine -> WebAPI [label = "call_endpoint('invalid')"];
       WebAPI --> ToolEngine [label = "HTTP 404 Error", color = red];
       ToolEngine -> ToolEngine [label = "handle_error()"];
       ToolEngine --> Agent [label = "ToolExecutionError", color = red];
   }
```

### 3. Async/Await Pattern Documentation

```rst
.. seqdiag::
   :caption: Asynchronous Agent Processing
   :align: center

   seqdiag {
       // Async participants
       Client; AsyncCoordinator; Agent1; Agent2; Agent3; Database; ExternalAPI;

       activation = none;
       edge_length = 160;
       span_height = 35;

       // Async task initiation
       Client -> AsyncCoordinator [label = "await process_batch(tasks)"];
       activate AsyncCoordinator;

       AsyncCoordinator -> AsyncCoordinator [label = "create_task_group()"];

       // Parallel agent execution
       AsyncCoordinator -> Agent1 [label = "asyncio.create_task(arun(task1))", color = blue];
       AsyncCoordinator -> Agent2 [label = "asyncio.create_task(arun(task2))", color = green];
       AsyncCoordinator -> Agent3 [label = "asyncio.create_task(arun(task3))", color = orange];

       activate Agent1;
       activate Agent2;
       activate Agent3;

       // Concurrent operations
       Agent1 -> Database [label = "await query_data()", color = blue];
       Agent2 -> ExternalAPI [label = "await fetch_external()", color = green];
       Agent3 -> Database [label = "await update_records()", color = orange];

       // Wait for responses
       Database --> Agent1 [label = "query_results", color = blue];
       ExternalAPI --> Agent2 [label = "api_response", color = green];
       Database --> Agent3 [label = "update_confirmation", color = orange];

       // Processing
       Agent1 -> Agent1 [label = "process_data()", color = blue];
       Agent2 -> Agent2 [label = "parse_response()", color = green];
       Agent3 -> Agent3 [label = "validate_update()", color = orange];

       // Return results
       Agent1 --> AsyncCoordinator [label = "result1", color = blue];
       Agent2 --> AsyncCoordinator [label = "result2", color = green];
       Agent3 --> AsyncCoordinator [label = "result3", color = orange];

       deactivate Agent1;
       deactivate Agent2;
       deactivate Agent3;

       // Aggregate results
       AsyncCoordinator -> AsyncCoordinator [label = "await gather_results()"];
       AsyncCoordinator -> AsyncCoordinator [label = "merge_outputs()"];

       AsyncCoordinator --> Client [label = "batch_results"];
       deactivate AsyncCoordinator;

       // Error handling with async
       === Async Error Handling ===
       Client -> AsyncCoordinator [label = "await process_with_timeout()"];
       AsyncCoordinator -> Agent1 [label = "asyncio.wait_for(arun(), timeout=30)"];
       Agent1 --> AsyncCoordinator [label = "asyncio.TimeoutError", color = red];
       AsyncCoordinator --> Client [label = "TimeoutError: Operation timed out", color = red];
   }
```

### 4. State Management Sequences

```rst
.. seqdiag::
   :caption: Agent State Lifecycle Management
   :scale: 85%

   seqdiag {
       // State management participants
       User; Agent; StateSchema; MetaState; StateManager; Persistence;

       activation = none;
       edge_length = 200;

       // State initialization
       User -> Agent [label = "initialize_agent(config)"];
       activate Agent;

       Agent -> StateSchema [label = "create_initial_state()"];
       activate StateSchema;
       StateSchema -> StateSchema [label = "validate_schema()"];
       StateSchema --> Agent [label = "initial_state"];
       deactivate StateSchema;

       Agent -> MetaState [label = "wrap_in_meta_state(state)"];
       activate MetaState;
       MetaState -> MetaState [label = "setup_projections()"];
       MetaState --> Agent [label = "meta_state_wrapper"];
       deactivate MetaState;

       Agent -> StateManager [label = "register_state(meta_state)"];
       StateManager --> Agent [label = "state_id"];

       Agent --> User [label = "agent_ready"];
       deactivate Agent;

       // State updates during execution
       User -> Agent [label = "execute(input_data)"];
       activate Agent;

       Agent -> StateManager [label = "get_current_state(state_id)"];
       StateManager --> Agent [label = "current_state"];

       Agent -> Agent [label = "process_input()"];
       Agent -> Agent [label = "update_conversation_history()"];

       Agent -> StateSchema [label = "add_message(user_message)"];
       StateSchema -> StateSchema [label = "validate_message()"];
       StateSchema --> Agent [label = "state_updated"];

       // Processing and tool usage
       Agent -> Agent [label = "select_tools()"];
       Agent -> Agent [label = "execute_tools()"];

       Agent -> StateSchema [label = "add_message(assistant_message)"];
       StateSchema --> Agent [label = "final_state"];

       // State persistence
       Agent -> StateManager [label = "save_state(final_state)"];
       activate StateManager;
       StateManager -> Persistence [label = "persist_to_storage()"];
       Persistence --> StateManager [label = "saved_successfully"];
       StateManager --> Agent [label = "state_persisted"];
       deactivate StateManager;

       Agent --> User [label = "execution_result"];
       deactivate Agent;

       // State recovery scenario
       === State Recovery ===
       User -> Agent [label = "recover_from_checkpoint()"];
       Agent -> StateManager [label = "load_state(state_id)"];
       StateManager -> Persistence [label = "retrieve_from_storage()"];
       Persistence --> StateManager [label = "stored_state"];
       StateManager --> Agent [label = "recovered_state"];
       Agent --> User [label = "state_recovered"];
   }
```

### 5. Configuration and Recompilation Sequences

```rst
.. seqdiag::
   :caption: Agent Recompilation and Configuration Updates
   :align: center

   seqdiag {
       // Configuration participants
       Developer; ConfigManager; Agent; ToolRegistry; GraphBuilder; ValidationEngine;

       activation = none;
       edge_length = 180;
       span_height = 38;

       // Configuration update trigger
       Developer -> ConfigManager [label = "update_config(new_tools)"];
       activate ConfigManager;

       ConfigManager -> ConfigManager [label = "validate_configuration()"];
       ConfigManager -> Agent [label = "notify_config_change()"];

       activate Agent;
       Agent -> Agent [label = "mark_for_recompilation()"];
       Agent -> Agent [label = "set_recompile_reason('config_update')"];

       // Recompilation process
       Agent -> ToolRegistry [label = "update_tool_list(new_tools)"];
       activate ToolRegistry;
       ToolRegistry -> ToolRegistry [label = "validate_tools()"];
       ToolRegistry -> ToolRegistry [label = "register_new_tools()"];
       ToolRegistry --> Agent [label = "tools_updated"];
       deactivate ToolRegistry;

       Agent -> GraphBuilder [label = "rebuild_execution_graph()"];
       activate GraphBuilder;
       GraphBuilder -> GraphBuilder [label = "analyze_dependencies()"];
       GraphBuilder -> GraphBuilder [label = "create_new_nodes()"];
       GraphBuilder -> GraphBuilder [label = "wire_connections()"];
       GraphBuilder --> Agent [label = "new_graph"];
       deactivate GraphBuilder;

       // Validation phase
       Agent -> ValidationEngine [label = "validate_new_configuration()"];
       activate ValidationEngine;
       ValidationEngine -> ValidationEngine [label = "check_tool_compatibility()"];
       ValidationEngine -> ValidationEngine [label = "verify_graph_integrity()"];
       ValidationEngine -> ValidationEngine [label = "test_execution_paths()"];
       ValidationEngine --> Agent [label = "validation_results"];
       deactivate ValidationEngine;

       // Commit changes
       Agent -> Agent [label = "commit_recompilation()"];
       Agent -> Agent [label = "clear_recompile_flag()"];
       Agent --> ConfigManager [label = "recompilation_complete"];
       deactivate Agent;

       ConfigManager --> Developer [label = "configuration_applied"];
       deactivate ConfigManager;

       // Error handling during recompilation
       === Recompilation Error ===
       Developer -> ConfigManager [label = "update_config(invalid_tools)"];
       ConfigManager -> Agent [label = "notify_config_change()"];
       Agent -> ToolRegistry [label = "update_tool_list(invalid_tools)"];
       ToolRegistry --> Agent [label = "ValidationError: Invalid tool", color = red];
       Agent -> Agent [label = "rollback_changes()"];
       Agent --> ConfigManager [label = "RecompilationError", color = red];
       ConfigManager --> Developer [label = "Configuration update failed", color = red];
   }
```

## Configuration Options

### Current PyDevelop-Docs Configuration

```python
# In config.py - Line 474
extensions = [
    "sphinxcontrib.seqdiag",     # Sequence diagram support
    # ... other extensions
]

# Basic seqdiag configuration (implicit defaults)
seqdiag_output_format = "svg"   # Vector output for web
seqdiag_fontpath = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
```

### Enhanced Configuration for Issue #6

```python
# Advanced seqdiag configuration for API documentation
seqdiag_output_format = "svg"               # SVG for scalability
seqdiag_html_image_format = "svg"           # HTML image format
seqdiag_latex_image_format = "pdf"          # LaTeX image format

# Font configuration for better typography
seqdiag_fontpath = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/System/Library/Fonts/Helvetica.ttc",  # macOS support
]

# Enhanced styling for API documentation
seqdiag_default_actor_color = "#f8fafc"     # Light background
seqdiag_default_edge_color = "#2563eb"      # Blue arrows (Furo theme)
seqdiag_default_text_color = "#1e293b"      # Dark text
seqdiag_default_fontsize = 11               # Readable size

# Sequence-specific settings
seqdiag_actor_width = 120                   # Actor box width
seqdiag_actor_height = 60                   # Actor box height
seqdiag_message_spacing = 40                # Vertical message spacing
seqdiag_activation_height = 30              # Activation bar height
seqdiag_note_width = 200                    # Note box width

# Responsive design
seqdiag_max_width = 1200                    # Maximum diagram width
seqdiag_mobile_scale = 0.8                  # Mobile scaling
seqdiag_dpi = 150                           # High DPI rendering

# Performance settings
seqdiag_cache_enabled = True                # Enable caching
seqdiag_parallel_processing = True          # Parallel rendering
seqdiag_timeout = 45                        # Rendering timeout
```

## Template Integration for Issue #6

### 1. Method Call Sequence Templates

```jinja2
{# In _autoapi_templates/python/class.rst #}

{% if obj.methods|length > 3 %}
**Method Interaction Sequence:**

.. seqdiag::
   :caption: {{ obj.name }} - Method Call Flow
   :align: center

   seqdiag {
       // Method participants
       Client; {{ obj.name }};
       {% for method in obj.methods[:5] %}
       {% if not method.name.startswith('_') %}
       {{ method.name|title }};
       {% endif %}
       {% endfor %}

       activation = none;
       edge_length = 180;

       // Typical usage sequence
       Client -> {{ obj.name }} [label = "instantiate()"];
       activate {{ obj.name }};

       {% for method in obj.methods[:5] %}
       {% if not method.name.startswith('_') and method.name != '__init__' %}
       Client -> {{ obj.name }} [label = "{{ method.name }}({{ method.args|join(', ') }})"];
       {% if method.return_annotation %}
       {{ obj.name }} --> Client [label = "{{ method.return_annotation }}"];
       {% endif %}
       {% endif %}
       {% endfor %}

       deactivate {{ obj.name }};

       {% if obj.bases %}
       // Inheritance interactions
       === Inheritance Calls ===
       {% for base in obj.bases[:2] %}
       Client -> {{ obj.name }} [label = "inherited_method()"];
       {{ obj.name }} -> {{ base.split('.')[-1] }} [label = "super().method()"];
       {{ base.split('.')[-1] }} --> {{ obj.name }} [label = "result"];
       {{ obj.name }} --> Client [label = "processed_result"];
       {% endfor %}
       {% endif %}
   }

{% endif %}
```

### 2. Agent Workflow Templates

```jinja2
{# For agent interaction documentation #}

.. seqdiag::
   :caption: Agent Interaction Workflow
   :scale: 90%

   seqdiag {
       // Workflow participants
       User; MultiAgent; ReactAgent; SimpleAgent; ToolEngine; StateManager;

       activation = none;
       edge_length = 200;

       // Main workflow
       User -> MultiAgent [label = "execute_workflow(task)"];
       activate MultiAgent;

       MultiAgent -> StateManager [label = "initialize_session()"];
       StateManager --> MultiAgent [label = "session_id"];

       // Agent selection and execution
       MultiAgent -> MultiAgent [label = "select_execution_strategy()"];

       {% if "react" in workflow_agents %}
       MultiAgent -> ReactAgent [label = "plan_and_reason(task)"];
       activate ReactAgent;
       ReactAgent -> ToolEngine [label = "select_tools()"];
       ToolEngine --> ReactAgent [label = "tool_list"];
       ReactAgent -> ReactAgent [label = "reasoning_loop()"];
       ReactAgent --> MultiAgent [label = "execution_plan"];
       deactivate ReactAgent;
       {% endif %}

       {% if "simple" in workflow_agents %}
       MultiAgent -> SimpleAgent [label = "execute_plan(plan)"];
       activate SimpleAgent;
       SimpleAgent -> ToolEngine [label = "execute_tools()"];
       ToolEngine --> SimpleAgent [label = "tool_results"];
       SimpleAgent -> SimpleAgent [label = "generate_response()"];
       SimpleAgent --> MultiAgent [label = "final_output"];
       deactivate SimpleAgent;
       {% endif %}

       // State finalization
       MultiAgent -> StateManager [label = "save_session_state()"];
       StateManager --> MultiAgent [label = "state_saved"];

       MultiAgent --> User [label = "workflow_result"];
       deactivate MultiAgent;
   }
```

### 3. Error Handling Sequences

```jinja2
{# Error handling documentation #}

.. seqdiag::
   :caption: Error Handling and Recovery Patterns
   :align: center

   seqdiag {
       // Error handling participants
       Client; Agent; ErrorHandler; Logger; RecoveryManager; NotificationService;

       activation = none;
       edge_length = 160;
       span_height = 35;

       // Normal execution
       Client -> Agent [label = "execute_task()"];
       activate Agent;

       Agent -> Agent [label = "validate_input()"];
       Agent -> Agent [label = "process_request()"];

       // Error occurs
       Agent -> Agent [label = "operation_fails()", color = red];
       Agent -> ErrorHandler [label = "handle_exception(error)", color = red];
       activate ErrorHandler;

       ErrorHandler -> Logger [label = "log_error(details)", color = red];
       Logger --> ErrorHandler [label = "logged"];

       ErrorHandler -> ErrorHandler [label = "classify_error()", color = red];
       ErrorHandler -> RecoveryManager [label = "attempt_recovery()", color = orange];
       activate RecoveryManager;

       RecoveryManager -> RecoveryManager [label = "analyze_recovery_options()", color = orange];

       alt "Recovery Successful" {
           RecoveryManager -> Agent [label = "retry_operation()", color = green];
           Agent -> Agent [label = "execute_successfully()", color = green];
           Agent --> Client [label = "recovered_result", color = green];
       }
       else "Recovery Failed" {
           RecoveryManager -> NotificationService [label = "notify_failure()", color = red];
           NotificationService --> RecoveryManager [label = "notification_sent"];
           RecoveryManager --> ErrorHandler [label = "recovery_failed", color = red];
           ErrorHandler --> Agent [label = "unrecoverable_error", color = red];
           Agent --> Client [label = "FinalError: Operation failed", color = red];
       }

       deactivate RecoveryManager;
       deactivate ErrorHandler;
       deactivate Agent;
   }
```

## Responsive Design and Mobile Optimization

### Mobile-Optimized CSS for Sequence Diagrams

```css
/* Sequence diagram responsive design */
.seqdiag-container {
    max-width: 100%;
    overflow-x: auto;
    margin: 1rem 0;
    background: var(--color-background-secondary);
    border: 2px solid var(--color-background-border);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.seqdiag-container svg {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
    background: transparent;
}

/* Mobile-specific optimizations */
@media (max-width: 768px) {
    .seqdiag-container {
        padding: 1rem;
        overflow-x: scroll;
        -webkit-overflow-scrolling: touch;
    }

    .seqdiag-container svg {
        min-width: 600px;  /* Maintain sequence readability */
        max-width: none;
    }

    /* Mobile navigation hint */
    .seqdiag-container::before {
        content = "👆 Scroll horizontally to explore sequence";
        display: block;
        text-align: center;
        font-size: 0.75rem;
        color: var(--color-foreground-secondary);
        margin-bottom: 1rem;
        padding: 0.5rem;
        background: var(--color-background-primary);
        border-radius: 6px;
        border: 1px solid var(--color-background-border);
    }
}

/* Sequence-specific styling */
.seqdiag-container .actor {
    fill: var(--color-api-background);
    stroke: var(--color-brand-primary);
    stroke-width: 2px;
}

.seqdiag-container .actor-label {
    fill: var(--color-foreground-primary);
    font-family: var(--font-stack);
    font-weight: 600;
    font-size: 11px;
}

.seqdiag-container .message-line {
    stroke: var(--color-brand-primary);
    stroke-width: 2px;
    marker-end: url(#arrowhead);
}

.seqdiag-container .message-label {
    fill: var(--color-foreground-primary);
    font-family: var(--font-stack);
    font-size: 10px;
    font-weight: 500;
}

.seqdiag-container .activation {
    fill: var(--color-brand-primary);
    fill-opacity: 0.3;
    stroke: var(--color-brand-primary);
    stroke-width: 1px;
}

.seqdiag-container .note {
    fill: #fef3c7;
    stroke: #f59e0b;
    stroke-width: 1px;
}

.seqdiag-container .note-text {
    fill: #92400e;
    font-family: var(--font-stack);
    font-size: 9px;
    font-style: italic;
}

/* Dark theme adjustments */
@media (prefers-color-scheme: dark) {
    .seqdiag-container {
        background: var(--color-background-secondary);
        border-color: var(--color-background-border);
    }

    .seqdiag-container .actor {
        fill: var(--color-background-secondary);
        stroke: var(--color-brand-primary);
    }

    .seqdiag-container .note {
        fill: #451a03;
        stroke: #f59e0b;
    }

    .seqdiag-container .note-text {
        fill: #fbbf24;
    }
}
```

### Touch-Friendly Interaction

```css
/* Touch interaction enhancements */
.seqdiag-container {
  position: relative;
  touch-action: pan-x; /* Allow horizontal panning */
}

/* Zoom controls for mobile */
.seqdiag-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 0.5rem;
  z-index: 10;
}

.seqdiag-controls button {
  background: var(--color-brand-primary);
  color: white;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  cursor: pointer;
  touch-action: manipulation;
}

.seqdiag-controls button:hover {
  background: var(--color-brand-content);
}

@media (max-width: 768px) {
  .seqdiag-controls {
    position: static;
    justify-content: center;
    margin-bottom: 1rem;
  }

  .seqdiag-controls button {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
    min-height: 44px; /* Touch-friendly size */
  }
}
```

## Performance Considerations

### Build-Time Optimization

```python
# Sequence diagram performance optimization
seqdiag_cache_dir = "_seqdiag_cache"        # Cache directory
seqdiag_cache_expiry = 86400                # 24 hour cache
seqdiag_parallel_workers = 3                # Parallel processing
seqdiag_memory_limit = "512m"               # Memory per process

# Conditional generation based on complexity
def should_generate_sequence_diagram(obj):
    """Determine if a sequence diagram adds value."""
    if obj.type == "class" and len(obj.methods) > 3:
        # Generate for classes with multiple methods
        return True
    elif obj.type == "function" and "async" in obj.signature:
        # Generate for async functions
        return True
    elif "workflow" in obj.name.lower() or "sequence" in obj.name.lower():
        # Generate for workflow-related objects
        return True
    return False

# Complexity limits
seqdiag_max_actors = 8                      # Maximum actors per diagram
seqdiag_max_messages = 25                   # Maximum messages per diagram
seqdiag_warn_complex = True                 # Warn about complex diagrams
```

### Memory Management

```python
# Memory-efficient seqdiag processing
seqdiag_cleanup_temp = True                 # Clean temporary files
seqdiag_batch_size = 5                      # Process diagrams in batches
seqdiag_gc_frequency = 10                   # Garbage collection frequency
```

## Integration with Other Extensions

### AutoAPI Integration

```python
# Enhanced AutoAPI with sequence diagrams
autoapi_seqdiag_enabled = True
autoapi_seqdiag_async_methods = True        # Generate for async methods
autoapi_seqdiag_interaction_flows = True    # Show method interactions
autoapi_seqdiag_min_methods = 3             # Minimum methods for diagrams
```

### Cross-Reference Support

```rst
.. seqdiag::
   :caption: Cross-Referenced Sequence

   seqdiag {
       Client; Agent; Tool;

       Client -> Agent [label = ":meth:`run`"];
       Agent -> Tool [label = ":meth:`execute`"];
       Tool --> Agent [label = "result"];
       Agent --> Client [label = ":class:`Response`"];
   }
```

## Current Implementation Status

### ✅ Production Ready Features

- **Sequence Diagram Support**: Full seqdiag integration with SVG output
- **Actor/Message Flow**: Clean representation of interactions
- **Basic Styling**: Color and layout customization
- **Async Pattern Support**: Documentation of async/await flows

### 🚀 Issue #6 Enhancement Opportunities

1. **AutoAPI Integration**: Automated method interaction diagrams
2. **Mobile Optimization**: Touch-friendly sequence exploration
3. **Interactive Elements**: Clickable actors and messages
4. **Performance Scaling**: Optimized for complex interaction flows
5. **Theme Integration**: Deep Furo theme color matching

### 📋 Implementation Roadmap

1. **Phase 1**: AutoAPI template integration for method sequences
2. **Phase 2**: Mobile-responsive interaction design
3. **Phase 3**: Performance optimization and caching
4. **Phase 4**: Interactive features and cross-references

## Best Practices

### 1. Sequence Complexity Management

- **Actor Limit**: Maximum 6-8 actors for readability
- **Message Limit**: Keep sequences under 20 messages
- **Logical Grouping**: Use separators for different scenarios
- **Clear Labels**: Descriptive message labels with parameters

### 2. Mobile-First Design

- **Horizontal Scrolling**: Allow touch-based navigation
- **Minimum Sizes**: Actors at least 100px wide for touch
- **Font Sizes**: Minimum 10pt for mobile readability
- **Touch Targets**: Interactive elements at least 44px

### 3. Documentation Integration

- **Method Flows**: Document complex method interactions
- **Error Scenarios**: Show error handling sequences
- **Async Patterns**: Illustrate async/await workflows
- **State Changes**: Document state management flows

---

**Status**: Specialized for API interaction documentation  
**Next Extension**: [sphinxcontrib.nwdiag](sphinxcontrib_nwdiag.md) - Network diagram specialization  
**Related**: [Async Programming Patterns](../../architecture/)
