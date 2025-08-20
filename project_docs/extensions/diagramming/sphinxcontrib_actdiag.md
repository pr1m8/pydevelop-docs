# sphinxcontrib.actdiag - Activity Diagram Creation

**Extension**: `sphinxcontrib.actdiag`  
**Purpose**: Activity and workflow diagram visualization for process documentation  
**Status**: ✅ Active in PyDevelop-Docs  
**Priority**: Medium - Specialized for workflow and process documentation  
**Issue #6 Relevance**: Valuable for documenting agent workflows and decision processes

## Overview

The `sphinxcontrib.actdiag` extension specializes in creating activity diagrams that show workflows, decision processes, and step-by-step procedures. It's particularly effective for documenting agent decision trees, build processes, user workflows, and complex business logic flows.

### Visual Capabilities

- **Process Workflows**: Clear step-by-step process visualization
- **Decision Trees**: Branching logic and conditional flows
- **Parallel Activities**: Concurrent process execution
- **Error Handling**: Exception paths and recovery workflows
- **Loop Structures**: Iterative and recursive processes
- **Start/End Points**: Clear process boundaries and outcomes

## Diagram Types and Use Cases

### 1. Agent Decision Process Workflows

```rst
.. actdiag::
   :caption: ReactAgent Decision and Execution Workflow
   :align: center

   actdiag {
       // Activity workflow for ReactAgent processing

       // Initial processing
       start [shape = beginpoint, color = "#dbeafe"];
       receive_input [label = "Receive User Input", color = "#bfdbfe"];
       validate_input [label = "Validate Input\nFormat", color = "#93c5fd"];

       // Input validation decision
       input_valid [shape = diamond, label = "Input\nValid?", color = "#fef3c7"];
       input_error [label = "Return Input\nError", color = "#fef2f2"];

       // Context analysis
       analyze_context [label = "Analyze Request\nContext", color = "#f0fdf4"];
       extract_intent [label = "Extract User\nIntent", color = "#dcfce7"];

       // Tool selection process
       need_tools [shape = diamond, label = "Tools\nRequired?", color = "#fef3c7"];
       select_tools [label = "Select Appropriate\nTools", color = "#bbf7d0"];
       validate_tools [label = "Validate Tool\nAvailability", color = "#86efac"];

       // Reasoning loop
       reasoning_start [shape = beginpoint, label = "Start\nReasoning", color = "#e0f2fe"];
       generate_plan [label = "Generate\nExecution Plan", color = "#b3e5fc"];
       evaluate_plan [label = "Evaluate Plan\nFeasibility", color = "#81d4fa"];

       plan_good [shape = diamond, label = "Plan\nAcceptable?", color = "#fef3c7"];
       refine_plan [label = "Refine and\nImprove Plan", color = "#4fc3f7"];

       // Tool execution
       execute_tools [label = "Execute Selected\nTools", color = "#f0fdf4"];
       process_results [label = "Process Tool\nResults", color = "#dcfce7"];

       // Error handling in tool execution
       tool_success [shape = diamond, label = "Tool Execution\nSuccessful?", color = "#fef3c7"];
       handle_tool_error [label = "Handle Tool\nError", color = "#fef2f2"];
       retry_tool [label = "Retry with\nAlternative", color = "#fecaca"];

       max_retries [shape = diamond, label = "Max Retries\nReached?", color = "#fef3c7"];
       tool_failure [label = "Report Tool\nFailure", color = "#fca5a5"];

       // Response generation
       synthesize_response [label = "Synthesize Final\nResponse", color = "#f3e8ff"];
       format_output [label = "Format Output\nfor User", color = "#e9d5ff"];

       // Quality check
       quality_check [shape = diamond, label = "Response\nQuality OK?", color = "#fef3c7"];
       improve_response [label = "Improve Response\nQuality", color = "#ddd6fe"];

       // Final steps
       log_interaction [label = "Log Interaction\nHistory", color = "#f8fafc"];
       update_state [label = "Update Agent\nState", color = "#f1f5f9"];
       return_response [label = "Return Final\nResponse", color = "#e2e8f0"];
       end [shape = endpoint, color = "#64748b"];

       // Flow connections
       start -> receive_input -> validate_input -> input_valid;

       // Input validation branch
       input_valid -> input_error [label = "No", color = "red"];
       input_valid -> analyze_context [label = "Yes", color = "green"];
       input_error -> end;

       // Context analysis flow
       analyze_context -> extract_intent -> need_tools;

       // Tool selection branch
       need_tools -> select_tools [label = "Yes", color = "green"];
       need_tools -> reasoning_start [label = "No", color = "blue"];
       select_tools -> validate_tools -> reasoning_start;

       // Reasoning loop
       reasoning_start -> generate_plan -> evaluate_plan -> plan_good;
       plan_good -> refine_plan [label = "No", color = "red"];
       plan_good -> execute_tools [label = "Yes", color = "green"];
       refine_plan -> generate_plan;

       // Tool execution flow
       execute_tools -> process_results -> tool_success;
       tool_success -> synthesize_response [label = "Yes", color = "green"];
       tool_success -> handle_tool_error [label = "No", color = "red"];

       // Error handling loop
       handle_tool_error -> max_retries;
       max_retries -> tool_failure [label = "Yes", color = "red"];
       max_retries -> retry_tool [label = "No", color = "blue"];
       retry_tool -> execute_tools;
       tool_failure -> end;

       // Response generation flow
       synthesize_response -> format_output -> quality_check;
       quality_check -> improve_response [label = "No", color = "red"];
       quality_check -> log_interaction [label = "Yes", color = "green"];
       improve_response -> synthesize_response;

       // Final flow
       log_interaction -> update_state -> return_response -> end;
   }
```

### 2. PyDevelop-Docs Build Process Workflow

```rst
.. actdiag::
   :caption: PyDevelop-Docs Documentation Build Process
   :scale: 90%

   actdiag {
       // Build process workflow

       start [shape = beginpoint, color = "#dbeafe"];
       check_config [label = "Check Project\nConfiguration", color = "#bfdbfe"];
       detect_type [label = "Detect Project\nType", color = "#93c5fd"];

       // Project type decision
       project_type [shape = diamond, label = "Project\nType?", color = "#fef3c7"];
       setup_single [label = "Setup Single\nPackage Config", color = "#f0fdf4"];
       setup_monorepo [label = "Setup Monorepo\nConfig", color = "#dcfce7"];

       // Configuration generation
       generate_conf [label = "Generate Sphinx\nconf.py", color = "#bbf7d0"];
       apply_autoapi [label = "Apply AutoAPI\nHierarchical Fix", color = "#86efac"];
       setup_extensions [label = "Configure 40+\nExtensions", color = "#4ade80"];

       // Source scanning
       scan_sources [label = "Scan Python\nSource Files", color = "#f3e8ff"];
       extract_docstrings [label = "Extract Function\nDocstrings", color = "#e9d5ff"];
       process_markdown [label = "Process Markdown\nFiles", color = "#ddd6fe"];

       // Extension processing - parallel activities
       extension_start [shape = beginpoint, label = "Start Extension\nProcessing", color = "#e0f2fe"];

       // Parallel extension processing
       process_autoapi [label = "Process AutoAPI\nGeneration", color = "#b3e5fc"];
       render_mermaid [label = "Render Mermaid\nDiagrams", color = "#81d4fa"];
       generate_plantuml [label = "Generate PlantUML\nDiagrams", color = "#4fc3f7"];
       process_graphviz [label = "Process Graphviz\nDiagrams", color = "#29b6f6"];

       extension_sync [shape = beginpoint, label = "Sync Extension\nResults", color = "#03a9f4"];

       // Content generation
       generate_html [label = "Generate HTML\nPages", color = "#fef3c7"];
       process_css [label = "Process CSS\nStyling", color = "#fde68a"];
       bundle_js [label = "Bundle JavaScript\nFiles", color = "#fcd34d"];

       // Optimization
       optimize_images [label = "Optimize Images\nand Assets", color = "#f0fdf4"];
       generate_sitemap [label = "Generate XML\nSitemap", color = "#dcfce7"];
       create_search [label = "Create Search\nIndex", color = "#bbf7d0"];

       // Quality checks
       validate_html [label = "Validate HTML\nOutput", color = "#fef2f2"];
       check_links [label = "Check Internal\nLinks", color = "#fecaca"];

       // Quality decision
       quality_ok [shape = diamond, label = "Quality\nChecks Pass?", color = "#fef3c7"];
       fix_issues [label = "Fix Identified\nIssues", color = "#fca5a5"];

       // Final steps
       deploy_ready [label = "Mark as Deploy\nReady", color = "#f3e8ff"];
       cleanup_temp [label = "Cleanup Temporary\nFiles", color = "#e9d5ff"];
       end [shape = endpoint, color = "#64748b"];

       // Flow connections
       start -> check_config -> detect_type -> project_type;

       // Project type branches
       project_type -> setup_single [label = "Single", color = "blue"];
       project_type -> setup_monorepo [label = "Monorepo", color = "green"];

       // Configuration flow
       setup_single -> generate_conf;
       setup_monorepo -> generate_conf;
       generate_conf -> apply_autoapi -> setup_extensions;

       // Source processing
       setup_extensions -> scan_sources;
       scan_sources -> extract_docstrings -> process_markdown -> extension_start;

       // Parallel extension processing
       extension_start -> process_autoapi;
       extension_start -> render_mermaid;
       extension_start -> generate_plantuml;
       extension_start -> process_graphviz;

       // Sync parallel processes
       process_autoapi -> extension_sync;
       render_mermaid -> extension_sync;
       generate_plantuml -> extension_sync;
       process_graphviz -> extension_sync;

       // Content generation flow
       extension_sync -> generate_html -> process_css -> bundle_js;

       // Optimization flow
       bundle_js -> optimize_images -> generate_sitemap -> create_search;

       // Quality checks
       create_search -> validate_html -> check_links -> quality_ok;

       // Quality decision
       quality_ok -> fix_issues [label = "No", color = "red"];
       quality_ok -> deploy_ready [label = "Yes", color = "green"];
       fix_issues -> validate_html;

       // Final flow
       deploy_ready -> cleanup_temp -> end;
   }
```

### 3. Multi-Agent Coordination Workflow

```rst
.. actdiag::
   :caption: Multi-Agent Task Coordination Process
   :align: center

   actdiag {
       // Multi-agent coordination workflow

       start [shape = beginpoint, color = "#dbeafe"];
       receive_task [label = "Receive Complex\nTask Request", color = "#bfdbfe"];
       analyze_complexity [label = "Analyze Task\nComplexity", color = "#93c5fd"];

       // Task decomposition
       decompose_task [label = "Decompose into\nSubtasks", color = "#f0fdf4"];
       assign_priorities [label = "Assign Task\nPriorities", color = "#dcfce7"];

       // Agent selection
       select_agents [label = "Select Appropriate\nAgents", color = "#bbf7d0"];
       validate_agents [label = "Validate Agent\nAvailability", color = "#86efac"];

       // Execution strategy decision
       execution_mode [shape = diamond, label = "Execution\nMode?", color = "#fef3c7"];

       // Sequential execution path
       sequential_start [shape = beginpoint, label = "Sequential\nExecution", color = "#e0f2fe"];
       agent_1_exec [label = "Execute Agent 1\n(Planning)", color = "#b3e5fc"];
       agent_1_result [label = "Process Agent 1\nResult", color = "#81d4fa"];

       agent_2_exec [label = "Execute Agent 2\n(Implementation)", color = "#4fc3f7"];
       agent_2_result [label = "Process Agent 2\nResult", color = "#29b6f6"];

       sequential_merge [label = "Merge Sequential\nResults", color = "#03a9f4"];

       // Parallel execution path
       parallel_start [shape = beginpoint, label = "Parallel\nExecution", color = "#e8f5e8"];

       agent_a_exec [label = "Execute Agent A\n(Research)", color = "#c8e6c9"];
       agent_b_exec [label = "Execute Agent B\n(Analysis)", color = "#a5d6a7"];
       agent_c_exec [label = "Execute Agent C\n(Synthesis)", color = "#81c784"];

       parallel_sync [shape = beginpoint, label = "Sync Parallel\nResults", color = "#66bb6a"];
       parallel_merge [label = "Merge Parallel\nResults", color = "#4caf50"];

       // Result processing
       process_results [label = "Process Combined\nResults", color = "#fef3c7"];
       validate_output [label = "Validate Output\nQuality", color = "#fde68a"];

       // Quality check
       output_quality [shape = diamond, label = "Output Quality\nAcceptable?", color = "#fef3c7"];
       refine_output [label = "Refine Output\nwith Feedback", color = "#fcd34d"];

       // Error handling
       error_occurred [shape = diamond, label = "Any Errors\nOccurred?", color = "#fef2f2"];
       handle_errors [label = "Handle Agent\nErrors", color = "#fecaca"];

       retry_decision [shape = diamond, label = "Retry\nPossible?", color = "#fef3c7"];
       retry_failed_agents [label = "Retry Failed\nAgents", color = "#fca5a5"];
       escalate_error [label = "Escalate Error\nto User", color = "#f87171"];

       // Final steps
       finalize_response [label = "Finalize Combined\nResponse", color = "#f3e8ff"];
       update_agent_states [label = "Update All Agent\nStates", color = "#e9d5ff"];
       log_coordination [label = "Log Coordination\nMetrics", color = "#ddd6fe"];

       end [shape = endpoint, color = "#64748b"];

       // Main flow
       start -> receive_task -> analyze_complexity -> decompose_task;
       decompose_task -> assign_priorities -> select_agents -> validate_agents;
       validate_agents -> execution_mode;

       // Sequential execution branch
       execution_mode -> sequential_start [label = "Sequential", color = "blue"];
       sequential_start -> agent_1_exec -> agent_1_result;
       agent_1_result -> agent_2_exec -> agent_2_result -> sequential_merge;

       // Parallel execution branch
       execution_mode -> parallel_start [label = "Parallel", color = "green"];
       parallel_start -> agent_a_exec;
       parallel_start -> agent_b_exec;
       parallel_start -> agent_c_exec;

       agent_a_exec -> parallel_sync;
       agent_b_exec -> parallel_sync;
       agent_c_exec -> parallel_sync;
       parallel_sync -> parallel_merge;

       // Merge results
       sequential_merge -> process_results;
       parallel_merge -> process_results;

       // Quality and error handling
       process_results -> validate_output -> output_quality;
       output_quality -> refine_output [label = "No", color = "red"];
       output_quality -> error_occurred [label = "Yes", color = "green"];
       refine_output -> validate_output;

       error_occurred -> handle_errors [label = "Yes", color = "red"];
       error_occurred -> finalize_response [label = "No", color = "green"];

       handle_errors -> retry_decision;
       retry_decision -> retry_failed_agents [label = "Yes", color = "blue"];
       retry_decision -> escalate_error [label = "No", color = "red"];

       retry_failed_agents -> agent_1_exec;  // Loop back to retry
       escalate_error -> end;

       // Final flow
       finalize_response -> update_agent_states -> log_coordination -> end;
   }
```

### 4. Tool Integration and Error Recovery Workflow

```rst
.. actdiag::
   :caption: Tool Integration and Error Recovery Process
   :scale: 85%

   actdiag {
       // Tool integration workflow

       start [shape = beginpoint, color = "#dbeafe"];
       analyze_request [label = "Analyze User\nRequest", color = "#bfdbfe"];
       identify_tools [label = "Identify Required\nTools", color = "#93c5fd"];

       // Tool availability check
       check_tools [label = "Check Tool\nAvailability", color = "#f0fdf4"];
       tools_available [shape = diamond, label = "All Tools\nAvailable?", color = "#fef3c7"];

       // Missing tools handling
       find_alternatives [label = "Find Alternative\nTools", color = "#fef2f2"];
       alternatives_found [shape = diamond, label = "Alternatives\nFound?", color = "#fef3c7"];
       report_missing [label = "Report Missing\nTools", color = "#fecaca"];

       // Tool preparation
       prepare_tools [label = "Prepare Tool\nExecutors", color = "#dcfce7"];
       validate_inputs [label = "Validate Tool\nInputs", color = "#bbf7d0"];

       // Tool execution loop
       execution_start [shape = beginpoint, label = "Start Tool\nExecution", color = "#e0f2fe"];
       execute_tool [label = "Execute Current\nTool", color = "#b3e5fc"];

       // Tool execution result
       tool_result [shape = diamond, label = "Tool Execution\nSuccessful?", color = "#fef3c7"];
       process_success [label = "Process Successful\nResult", color = "#81d4fa"];
       handle_failure [label = "Handle Tool\nFailure", color = "#fef2f2"];

       // Error analysis
       analyze_error [label = "Analyze Error\nType", color = "#fecaca"];
       error_type [shape = diamond, label = "Error\nType?", color = "#fef3c7"];

       // Different error handling paths
       retry_tool [label = "Retry Tool\nExecution", color = "#fca5a5"];
       use_alternative [label = "Use Alternative\nTool", color = "#f87171"];
       skip_tool [label = "Skip Optional\nTool", color = "#ef4444"];

       // Retry logic
       retry_count [shape = diamond, label = "Retry Count\n< Max?", color = "#fef3c7"];
       increment_retry [label = "Increment Retry\nCounter", color = "#dc2626"];

       // More tools check
       more_tools [shape = diamond, label = "More Tools\nto Execute?", color = "#fef3c7"];
       next_tool [label = "Move to Next\nTool", color = "#4fc3f7"];

       // Result aggregation
       aggregate_results [label = "Aggregate All\nTool Results", color = "#f3e8ff"];
       validate_completeness [label = "Validate Result\nCompleteness", color = "#e9d5ff"];

       // Completeness check
       results_complete [shape = diamond, label = "Results\nComplete?", color = "#fef3c7"];
       fill_gaps [label = "Fill Missing\nInformation", color = "#ddd6fe"];

       // Final processing
       format_output [label = "Format Final\nOutput", color = "#c4b5fd"];
       cleanup_resources [label = "Cleanup Tool\nResources", color = "#a78bfa"];

       end [shape = endpoint, color = "#64748b"];

       // Main flow
       start -> analyze_request -> identify_tools -> check_tools -> tools_available;

       // Tool availability branches
       tools_available -> find_alternatives [label = "No", color = "red"];
       tools_available -> prepare_tools [label = "Yes", color = "green"];

       // Alternative tools handling
       find_alternatives -> alternatives_found;
       alternatives_found -> report_missing [label = "No", color = "red"];
       alternatives_found -> prepare_tools [label = "Yes", color = "green"];
       report_missing -> end;

       // Tool preparation
       prepare_tools -> validate_inputs -> execution_start;

       // Tool execution loop
       execution_start -> execute_tool -> tool_result;

       // Success path
       tool_result -> process_success [label = "Yes", color = "green"];

       // Failure path
       tool_result -> handle_failure [label = "No", color = "red"];
       handle_failure -> analyze_error -> error_type;

       // Error handling branches
       error_type -> retry_tool [label = "Transient", color = "blue"];
       error_type -> use_alternative [label = "Tool Error", color = "orange"];
       error_type -> skip_tool [label = "Input Error", color = "red"];

       // Retry logic
       retry_tool -> retry_count;
       retry_count -> increment_retry [label = "Yes", color = "blue"];
       retry_count -> use_alternative [label = "No", color = "red"];
       increment_retry -> execute_tool;

       // Alternative and skip paths
       use_alternative -> execute_tool;
       skip_tool -> more_tools;

       // Continue to next tool
       process_success -> more_tools;
       more_tools -> next_tool [label = "Yes", color = "blue"];
       more_tools -> aggregate_results [label = "No", color = "green"];
       next_tool -> execute_tool;

       // Result processing
       aggregate_results -> validate_completeness -> results_complete;
       results_complete -> fill_gaps [label = "No", color = "red"];
       results_complete -> format_output [label = "Yes", color = "green"];
       fill_gaps -> aggregate_results;

       // Final flow
       format_output -> cleanup_resources -> end;
   }
```

## Configuration Options

### Current PyDevelop-Docs Configuration

```python
# In config.py - Line 476
extensions = [
    "sphinxcontrib.actdiag",     # Activity diagram support
    # ... other extensions
]

# Basic actdiag configuration (implicit defaults)
actdiag_output_format = "svg"   # Vector output for web
actdiag_fontpath = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
```

### Enhanced Configuration for Issue #6

```python
# Advanced actdiag configuration for workflow documentation
actdiag_output_format = "svg"               # SVG for scalability
actdiag_html_image_format = "svg"           # HTML image format
actdiag_latex_image_format = "pdf"          # LaTeX image format

# Font configuration for activity diagrams
actdiag_fontpath = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/System/Library/Fonts/Helvetica.ttc",  # macOS support
]

# Activity-specific styling
actdiag_default_node_color = "#f8fafc"      # Light background for activities
actdiag_default_edge_color = "#2563eb"      # Blue arrows (Furo theme)
actdiag_default_text_color = "#1e293b"      # Dark text
actdiag_default_fontsize = 10               # Readable font size

# Activity diagram layout
actdiag_node_width = 140                    # Activity node width
actdiag_node_height = 60                    # Activity node height
actdiag_lane_width = 200                    # Lane width for complex workflows
actdiag_span_width = 50                     # Horizontal spacing
actdiag_span_height = 40                    # Vertical spacing

# Decision diamond settings
actdiag_diamond_width = 100                 # Decision diamond width
actdiag_diamond_height = 80                 # Decision diamond height

# Responsive design
actdiag_max_width = 1200                    # Maximum diagram width
actdiag_mobile_scale = 0.8                  # Mobile scaling factor
actdiag_dpi = 150                           # High DPI rendering

# Performance settings
actdiag_cache_enabled = True                # Enable diagram caching
actdiag_parallel_processing = True          # Parallel rendering
actdiag_timeout = 45                        # Rendering timeout (workflows can be complex)
```

## Template Integration for Issue #6

### 1. Method Workflow Templates

```jinja2
{# In _autoapi_templates/python/class.rst #}

{% if obj.methods|length > 3 and obj.name|lower not in ['meta', 'abstract'] %}
**Method Execution Workflow:**

.. actdiag::
   :caption: {{ obj.name }} - Method Execution Flow
   :align: center

   actdiag {
       start [shape = beginpoint, color = "#dbeafe"];
       instantiate [label = "Instantiate\n{{ obj.name }}", color = "#bfdbfe"];

       {% for method in obj.methods[:6] %}
       {% if not method.name.startswith('_') and method.name != '__init__' %}
       {{ method.name }}_call [label = "Call {{ method.name }}()", color = "#f0fdf4"];
       {{ method.name }}_process [label = "Process in\n{{ method.name }}", color = "#dcfce7"];

       {% if method.return_annotation %}
       {{ method.name }}_return [label = "Return\n{{ method.return_annotation }}", color = "#bbf7d0"];
       {% endif %}
       {% endif %}
       {% endfor %}

       end [shape = endpoint, color = "#64748b"];

       // Flow connections
       start -> instantiate;

       {% set methods = obj.methods|rejectattr("name", "startswith", "_")|list %}
       {% if methods %}
       instantiate -> {{ methods[0].name }}_call;

       {% for method in methods[:5] %}
       {% if not method.name.startswith('_') and method.name != '__init__' %}
       {{ method.name }}_call -> {{ method.name }}_process;
       {% if method.return_annotation %}
       {{ method.name }}_process -> {{ method.name }}_return;
       {% if loop.index < methods|length and loop.index < 5 %}
       {{ method.name }}_return -> {{ methods[loop.index].name }}_call;
       {% else %}
       {{ method.name }}_return -> end;
       {% endif %}
       {% else %}
       {% if loop.index < methods|length and loop.index < 5 %}
       {{ method.name }}_process -> {{ methods[loop.index].name }}_call;
       {% else %}
       {{ method.name }}_process -> end;
       {% endif %}
       {% endif %}
       {% endif %}
       {% endfor %}
       {% endif %}
   }

{% endif %}
```

### 2. Package Build Process Templates

```jinja2
{# For build and deployment documentation #}

.. actdiag::
   :caption: Package Build and Deployment Process
   :scale: 90%

   actdiag {
       start [shape = beginpoint, color = "#dbeafe"];

       // Source preparation
       prepare_sources [label = "Prepare Source\nFiles", color = "#bfdbfe"];
       validate_syntax [label = "Validate Python\nSyntax", color = "#93c5fd"];

       syntax_ok [shape = diamond, label = "Syntax\nValid?", color = "#fef3c7"];
       fix_syntax [label = "Fix Syntax\nErrors", color = "#fef2f2"];

       // Documentation generation
       scan_docstrings [label = "Scan Function\nDocstrings", color = "#f0fdf4"];
       generate_api_docs [label = "Generate API\nDocumentation", color = "#dcfce7"];
       render_diagrams [label = "Render Activity\nDiagrams", color = "#bbf7d0"];

       // Quality checks
       validate_docs [label = "Validate\nDocumentation", color = "#86efac"];
       run_tests [label = "Run Test\nSuite", color = "#4ade80"];

       tests_pass [shape = diamond, label = "Tests\nPass?", color = "#fef3c7"];
       fix_tests [label = "Fix Test\nFailures", color = "#fef2f2"];

       // Build package
       build_package [label = "Build Python\nPackage", color = "#fef3c7"];
       create_wheel [label = "Create Wheel\nDistribution", color = "#fde68a"];

       // Deployment decision
       deploy_target [shape = diamond, label = "Deploy\nTarget?", color = "#fef3c7"];

       // Development deployment
       deploy_dev [label = "Deploy to\nDevelopment", color = "#f0fdf4"];
       test_dev [label = "Test in Dev\nEnvironment", color = "#dcfce7"];

       // Production deployment
       deploy_staging [label = "Deploy to\nStaging", color = "#f3e8ff"];
       test_staging [label = "Test in Staging\nEnvironment", color = "#e9d5ff"];

       staging_ok [shape = diamond, label = "Staging\nTests Pass?", color = "#fef3c7"];
       deploy_prod [label = "Deploy to\nProduction", color = "#ddd6fe"];

       // Final steps
       notify_users [label = "Notify Users of\nDeployment", color = "#c4b5fd"];
       cleanup [label = "Cleanup Build\nArtifacts", color = "#a78bfa"];

       end [shape = endpoint, color = "#64748b"];

       // Flow connections
       start -> prepare_sources -> validate_syntax -> syntax_ok;

       syntax_ok -> fix_syntax [label = "No", color = "red"];
       syntax_ok -> scan_docstrings [label = "Yes", color = "green"];
       fix_syntax -> validate_syntax;

       scan_docstrings -> generate_api_docs -> render_diagrams;
       render_diagrams -> validate_docs -> run_tests -> tests_pass;

       tests_pass -> fix_tests [label = "No", color = "red"];
       tests_pass -> build_package [label = "Yes", color = "green"];
       fix_tests -> run_tests;

       build_package -> create_wheel -> deploy_target;

       deploy_target -> deploy_dev [label = "Development", color = "blue"];
       deploy_target -> deploy_staging [label = "Production", color = "green"];

       deploy_dev -> test_dev -> end;

       deploy_staging -> test_staging -> staging_ok;
       staging_ok -> deploy_prod [label = "Yes", color = "green"];
       staging_ok -> fix_tests [label = "No", color = "red"];

       deploy_prod -> notify_users -> cleanup -> end;
   }
```

### 3. Error Handling Workflow Templates

```jinja2
{# For error handling documentation #}

.. actdiag::
   :caption: Error Handling and Recovery Workflow
   :align: center

   actdiag {
       start [shape = beginpoint, color = "#dbeafe"];
       operation_start [label = "Start\nOperation", color = "#bfdbfe"];

       // Normal execution
       execute_operation [label = "Execute Main\nOperation", color = "#f0fdf4"];
       operation_result [shape = diamond, label = "Operation\nSuccessful?", color = "#fef3c7"];

       // Success path
       process_success [label = "Process Success\nResult", color = "#dcfce7"];

       // Error path
       detect_error [label = "Detect Error\nCondition", color = "#fef2f2"];
       classify_error [label = "Classify Error\nType", color = "#fecaca"];

       error_type [shape = diamond, label = "Error\nType?", color = "#fef3c7"];

       // Different error types
       handle_validation [label = "Handle Validation\nError", color = "#fca5a5"];
       handle_network [label = "Handle Network\nError", color = "#f87171"];
       handle_system [label = "Handle System\nError", color = "#ef4444"];
       handle_unknown [label = "Handle Unknown\nError", color = "#dc2626"];

       // Recovery attempts
       attempt_recovery [label = "Attempt Error\nRecovery", color = "#fcd34d"];
       recovery_success [shape = diamond, label = "Recovery\nSuccessful?", color = "#fef3c7"];

       // Retry logic
       retry_count [shape = diamond, label = "Retry Count\n< Maximum?", color = "#fef3c7"];
       increment_retry [label = "Increment Retry\nCounter", color = "#fbbf24"];

       // Fallback options
       try_fallback [label = "Try Fallback\nMethod", color = "#f59e0b"];
       fallback_available [shape = diamond, label = "Fallback\nAvailable?", color = "#fef3c7"];

       // Final error handling
       escalate_error [label = "Escalate Error\nto User", color = "#ef4444"];
       log_error [label = "Log Error\nDetails", color = "#dc2626"];

       // Cleanup and finalization
       cleanup_resources [label = "Cleanup\nResources", color = "#f3e8ff"];
       update_state [label = "Update System\nState", color = "#e9d5ff"];

       end [shape = endpoint, color = "#64748b"];

       // Flow connections
       start -> operation_start -> execute_operation -> operation_result;

       // Success path
       operation_result -> process_success [label = "Yes", color = "green"];
       process_success -> cleanup_resources;

       // Error path
       operation_result -> detect_error [label = "No", color = "red"];
       detect_error -> classify_error -> error_type;

       // Error type branches
       error_type -> handle_validation [label = "Validation", color = "blue"];
       error_type -> handle_network [label = "Network", color = "orange"];
       error_type -> handle_system [label = "System", color = "red"];
       error_type -> handle_unknown [label = "Unknown", color = "purple"];

       // Recovery attempts
       handle_validation -> attempt_recovery;
       handle_network -> attempt_recovery;
       handle_system -> attempt_recovery;
       handle_unknown -> attempt_recovery;

       attempt_recovery -> recovery_success;

       // Recovery success
       recovery_success -> process_success [label = "Yes", color = "green"];
       recovery_success -> retry_count [label = "No", color = "red"];

       // Retry logic
       retry_count -> increment_retry [label = "Yes", color = "blue"];
       retry_count -> fallback_available [label = "No", color = "red"];
       increment_retry -> execute_operation;

       // Fallback handling
       fallback_available -> try_fallback [label = "Yes", color = "green"];
       fallback_available -> escalate_error [label = "No", color = "red"];
       try_fallback -> operation_result;

       // Final error handling
       escalate_error -> log_error -> cleanup_resources;

       // Cleanup and end
       cleanup_resources -> update_state -> end;
   }
```

## Responsive Design and Mobile Optimization

### Mobile-Optimized CSS for Activity Diagrams

```css
/* Activity diagram responsive design */
.actdiag-container {
  max-width: 100%;
  overflow-x: auto;
  margin: 1.5rem 0;
  background: var(--color-background-secondary);
  border: 2px solid var(--color-background-border);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  position: relative;
}

.actdiag-container svg {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
  background: transparent;
}

/* Activity diagram header */
.actdiag-container::before {
  content: "⚡ Activity Workflow";
  position: absolute;
  top: 0;
  right: 0;
  background: var(--color-brand-primary);
  color: white;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-bottom-left-radius: 8px;
  border-top-right-radius: 10px;
  z-index: 1;
}

/* Mobile-specific optimizations */
@media (max-width: 768px) {
  .actdiag-container {
    padding: 1rem;
    overflow-x: scroll;
    -webkit-overflow-scrolling: touch;
  }

  .actdiag-container svg {
    min-width: 650px; /* Maintain workflow readability */
    max-width: none;
  }

  .actdiag-container::before {
    font-size: 0.75rem;
    padding: 0.375rem 0.75rem;
  }

  /* Touch navigation hint */
  .actdiag-container::after {
    content: "👆 Scroll to explore workflow steps";
    display: block;
    text-align: center;
    font-size: 0.75rem;
    color: var(--color-foreground-secondary);
    margin-top: 1rem;
    padding: 0.5rem;
    background: var(--color-background-primary);
    border-radius: 6px;
    border: 1px solid var(--color-background-border);
  }
}

/* Activity-specific styling */
.actdiag-container .activity {
  fill: var(--color-api-background);
  stroke: var(--color-brand-primary);
  stroke-width: 2px;
  rx: 8px; /* Rounded corners for activities */
}

.actdiag-container .activity-label {
  fill: var(--color-foreground-primary);
  font-family: var(--font-stack);
  font-weight: 500;
  font-size: 10px;
  text-anchor: middle;
}

.actdiag-container .decision {
  fill: var(--color-background-primary);
  stroke: var(--color-brand-primary);
  stroke-width: 2px;
}

.actdiag-container .decision-label {
  fill: var(--color-foreground-primary);
  font-family: var(--font-stack);
  font-weight: 600;
  font-size: 9px;
  text-anchor: middle;
}

.actdiag-container .flow-arrow {
  stroke: var(--color-brand-primary);
  stroke-width: 2px;
  marker-end: url(#arrowhead);
}

.actdiag-container .flow-label {
  fill: var(--color-foreground-primary);
  font-family: var(--font-stack);
  font-size: 8px;
  font-weight: 500;
}

.actdiag-container .start-end {
  fill: var(--color-brand-primary);
  stroke: var(--color-brand-content);
  stroke-width: 2px;
}

.actdiag-container .start-end-label {
  fill: white;
  font-family: var(--font-stack);
  font-weight: 600;
  font-size: 9px;
  text-anchor: middle;
}

/* Activity state colors */
.actdiag-container .activity.input {
  fill: #dbeafe;
  stroke: #2563eb;
}

.actdiag-container .activity.process {
  fill: #f0fdf4;
  stroke: #10b981;
}

.actdiag-container .activity.output {
  fill: #fef3c7;
  stroke: #f59e0b;
}

.actdiag-container .activity.error {
  fill: #fef2f2;
  stroke: #ef4444;
}

.actdiag-container .activity.decision {
  fill: #f3e8ff;
  stroke: #8b5cf6;
}

/* Dark theme adjustments */
@media (prefers-color-scheme: dark) {
  .actdiag-container {
    background: var(--color-background-secondary);
    border-color: var(--color-background-border);
  }

  .actdiag-container .activity {
    fill: var(--color-background-secondary);
    stroke: var(--color-brand-primary);
  }

  .actdiag-container .decision {
    fill: var(--color-background-primary);
    stroke: var(--color-brand-primary);
  }
}

/* Interactive enhancements */
.actdiag-container .activity:hover {
  fill: var(--color-api-background-hover);
  cursor: pointer;
  transform: scale(1.02);
  transition: all 0.2s ease;
}

.actdiag-container .decision:hover {
  fill: var(--color-api-background-hover);
  cursor: pointer;
  transform: scale(1.05);
  transition: all 0.2s ease;
}

/* Workflow progression animation */
@keyframes workflowProgress {
  0% {
    stroke-dashoffset: 100;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

.actdiag-container .flow-arrow.animated {
  stroke-dasharray: 10, 5;
  animation: workflowProgress 2s linear infinite;
}
```

### Touch-Friendly Interaction

```css
/* Touch interaction enhancements */
.actdiag-container {
  touch-action: pan-x pan-y; /* Allow panning in both directions */
}

/* Mobile workflow navigation */
.actdiag-workflow-nav {
  display: none;
  position: sticky;
  top: 0;
  background: var(--color-background-primary);
  border-bottom: 1px solid var(--color-background-border);
  padding: 0.5rem;
  z-index: 10;
}

.actdiag-workflow-nav button {
  background: var(--color-brand-primary);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  margin: 0 0.25rem;
  font-size: 0.75rem;
  cursor: pointer;
  touch-action: manipulation;
}

@media (max-width: 768px) {
  .actdiag-workflow-nav {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .actdiag-workflow-nav button {
    min-height: 44px; /* Touch-friendly size */
    flex: 1;
    min-width: 80px;
  }
}
```

## Performance Considerations

### Build-Time Optimization

```python
# Activity diagram performance optimization
actdiag_cache_dir = "_actdiag_cache"        # Cache directory
actdiag_cache_expiry = 86400                # 24 hour cache
actdiag_parallel_workers = 2                # Parallel processing workers
actdiag_memory_limit = "768m"               # Higher memory for complex workflows

# Conditional generation based on content
def should_generate_activity_diagram(obj):
    """Determine if an activity diagram adds value."""
    workflow_keywords = ["process", "workflow", "steps", "procedure", "algorithm"]

    if obj.type == "function" and any(keyword in obj.name.lower() for keyword in workflow_keywords):
        # Generate for workflow-related functions
        return True
    elif obj.type == "class" and any(keyword in obj.docstring.lower() for keyword in workflow_keywords):
        # Generate for classes that describe processes
        return True
    elif obj.type == "module" and "workflow" in obj.name.lower():
        # Generate for workflow modules
        return True
    return False

# Complexity limits for activity diagrams
actdiag_max_activities = 20                 # Maximum activities per diagram
actdiag_max_decisions = 8                   # Maximum decision points
actdiag_warn_complex = True                 # Warn about complex workflows
```

### Memory Management

```python
# Memory-efficient actdiag processing
actdiag_cleanup_temp = True                 # Clean temporary files
actdiag_batch_size = 4                      # Process workflows in small batches
actdiag_gc_frequency = 8                    # Frequent garbage collection
```

## Integration with Other Extensions

### AutoAPI Integration

```python
# Enhanced AutoAPI with activity diagrams
autoapi_actdiag_enabled = True
autoapi_actdiag_workflow_methods = True     # Generate for workflow methods
autoapi_actdiag_process_classes = True      # Generate for process classes
autoapi_actdiag_algorithm_functions = True  # Generate for algorithmic functions
```

### Cross-Reference Support

```rst
.. actdiag::
   :caption: Cross-Referenced Workflow

   actdiag {
       start [shape = beginpoint];
       process [label = ":meth:`process_data`"];
       validate [label = ":func:`validate_input`"];
       end [shape = endpoint];

       start -> process -> validate -> end;
   }
```

## Current Implementation Status

### ✅ Production Ready Features

- **Activity Diagram Support**: Full actdiag integration with SVG output
- **Workflow Visualization**: Clear step-by-step process representation
- **Decision Logic**: Diamond-shaped decision points with branching
- **Process Flow**: Start/end points with clear flow direction

### 🚀 Issue #6 Enhancement Opportunities

1. **AutoAPI Integration**: Automated workflow diagrams for process methods
2. **Interactive Elements**: Clickable activities with cross-references
3. **Mobile Optimization**: Touch-friendly workflow exploration
4. **Performance Scaling**: Optimized for complex workflow documentation
5. **Theme Integration**: Deep Furo theme color matching

### 📋 Implementation Roadmap

1. **Phase 1**: AutoAPI template integration for workflow documentation
2. **Phase 2**: Interactive workflow elements with cross-references
3. **Phase 3**: Mobile-responsive design implementation
4. **Phase 4**: Performance optimization and advanced features

## Best Practices

### 1. Workflow Complexity Management

- **Activity Limit**: Maximum 15-20 activities for readability
- **Decision Limit**: Maximum 6-8 decision points per workflow
- **Logical Grouping**: Use swim lanes for complex multi-actor workflows
- **Clear Labels**: Descriptive activity names with action verbs

### 2. Mobile-First Design

- **Horizontal Flow**: Design workflows that work in horizontal scrolling
- **Minimum Sizes**: Activities large enough for touch interaction
- **Font Sizes**: Minimum 10pt for activity labels
- **Touch Navigation**: Provide touch-friendly workflow navigation

### 3. Documentation Integration

- **Process Focus**: Use for documenting algorithms and workflows
- **Decision Documentation**: Show branching logic and error handling
- **Step-by-Step**: Break complex processes into manageable steps
- **Cross-References**: Link activities to relevant code documentation

### 4. Performance Guidelines

- **Selective Generation**: Only create diagrams for workflow-related content
- **Complexity Monitoring**: Track and limit diagram complexity
- **Caching Strategy**: Cache complex workflow diagrams
- **Incremental Building**: Support incremental diagram updates

---

**Status**: Specialized for workflow and process documentation  
**Related Extensions**: [All Diagramming Extensions](./README.md)  
**Implementation**: [Issue #6 Visual Enhancement Goals](../../issues/issue_06/)
