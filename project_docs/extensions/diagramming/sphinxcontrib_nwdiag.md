# sphinxcontrib.nwdiag - Network Diagram Support

**Extension**: `sphinxcontrib.nwdiag`  
**Purpose**: Network topology and infrastructure diagram visualization  
**Status**: ✅ Active in PyDevelop-Docs  
**Priority**: Medium - Specialized for network architecture documentation  
**Issue #6 Relevance**: Useful for deployment architecture and system networking

## Overview

The `sphinxcontrib.nwdiag` extension specializes in creating network diagrams that show the topology and connections between different network components, servers, and infrastructure elements. It's particularly valuable for documenting deployment architectures, microservice topologies, and distributed system designs.

### Visual Capabilities

- **Network Topologies**: Clear visualization of network structures
- **Server Relationships**: Physical and logical server connections
- **Infrastructure Layout**: Cloud and on-premise infrastructure diagrams
- **Service Dependencies**: Microservice communication patterns
- **Security Zones**: Network segmentation and security boundaries
- **Load Balancing**: Traffic distribution and routing patterns

## Diagram Types and Use Cases

### 1. Haive Framework Deployment Architecture

```rst
.. nwdiag::
   :caption: Haive Framework Production Deployment
   :align: center

   nwdiag {
       // Internet and external services
       internet [shape = cloud, color = "#e0f2fe"];

       // DMZ network
       network dmz {
           address = "10.0.1.0/24";
           color = "#fef3c7";

           loadbalancer [address = "10.0.1.10", color = "#fde68a"];
           cdn [address = "10.0.1.20", color = "#fcd34d"];
           waf [address = "10.0.1.30", color = "#fbbf24"];
       }

       // Application network
       network app_tier {
           address = "10.0.2.0/24";
           color = "#f0fdf4";

           app_server_1 [address = "10.0.2.10", color = "#dcfce7"];
           app_server_2 [address = "10.0.2.11", color = "#dcfce7"];
           app_server_3 [address = "10.0.2.12", color = "#dcfce7"];

           api_gateway [address = "10.0.2.20", color = "#bbf7d0"];
           agent_service [address = "10.0.2.30", color = "#86efac"];
           tool_service [address = "10.0.2.31", color = "#86efac"];
       }

       // Database network
       network data_tier {
           address = "10.0.3.0/24";
           color = "#f3e8ff";

           postgres_primary [address = "10.0.3.10", color = "#e9d5ff"];
           postgres_replica [address = "10.0.3.11", color = "#ddd6fe"];
           redis_cluster [address = "10.0.3.20", color = "#c4b5fd"];
           vector_db [address = "10.0.3.30", color = "#a78bfa"];
       }

       // Monitoring network
       network monitoring {
           address = "10.0.4.0/24";
           color = "#fef2f2";

           prometheus [address = "10.0.4.10", color = "#fecaca"];
           grafana [address = "10.0.4.20", color = "#fca5a5"];
           elasticsearch [address = "10.0.4.30", color = "#f87171"];
       }

       // External services
       network external {
           address = "external";
           color = "#fff7ed";

           openai_api [address = "external", color = "#fed7aa"];
           aws_services [address = "external", color = "#fdba74"];
           github_api [address = "external", color = "#fb923c"];
       }

       // Network connections
       internet -- loadbalancer;
       loadbalancer -- app_server_1, app_server_2, app_server_3;

       app_server_1, app_server_2, app_server_3 -- api_gateway;
       api_gateway -- agent_service, tool_service;

       agent_service -- postgres_primary, redis_cluster, vector_db;
       tool_service -- postgres_primary, redis_cluster;

       app_server_1, app_server_2, app_server_3 -- prometheus;
       prometheus -- grafana;

       agent_service -- openai_api, aws_services;
       tool_service -- github_api, aws_services;
   }
```

### 2. Microservice Communication Network

```rst
.. nwdiag::
   :caption: Haive Microservices Network Architecture
   :scale: 90%

   nwdiag {
       // Frontend network
       network frontend {
           address = "192.168.1.0/24";
           color = "#dbeafe";

           web_ui [address = "192.168.1.10", color = "#bfdbfe"];
           mobile_app [address = "192.168.1.20", color = "#93c5fd"];
           cli_interface [address = "192.168.1.30", color = "#60a5fa"];
       }

       // API Gateway network
       network gateway {
           address = "192.168.2.0/24";
           color = "#fef3c7";

           api_gateway [address = "192.168.2.10", color = "#fde68a"];
           auth_service [address = "192.168.2.20", color = "#fcd34d"];
           rate_limiter [address = "192.168.2.30", color = "#fbbf24"];
       }

       // Core services network
       network core_services {
           address = "192.168.3.0/24";
           color = "#f0fdf4";

           agent_orchestrator [address = "192.168.3.10", color = "#dcfce7"];
           tool_manager [address = "192.168.3.20", color = "#bbf7d0"];
           state_manager [address = "192.168.3.30", color = "#86efac"];
           workflow_engine [address = "192.168.3.40", color = "#4ade80"];
       }

       // Agent services network
       network agent_services {
           address = "192.168.4.0/24";
           color = "#ecfdf5";

           simple_agent_pool [address = "192.168.4.10", color = "#d1fae5"];
           react_agent_pool [address = "192.168.4.20", color = "#a7f3d0"];
           multi_agent_pool [address = "192.168.4.30", color = "#6ee7b7"];
           specialized_agents [address = "192.168.4.40", color = "#34d399"];
       }

       // Tool services network
       network tool_services {
           address = "192.168.5.0/24";
           color = "#f0fdfa";

           calculator_service [address = "192.168.5.10", color = "#ccfbf1"];
           web_search_service [address = "192.168.5.20", color = "#99f6e4"];
           file_service [address = "192.168.5.30", color = "#5eead4"];
           api_proxy_service [address = "192.168.5.40", color = "#2dd4bf"];
       }

       // Data layer network
       network data_layer {
           address = "192.168.6.0/24";
           color = "#f3e8ff";

           postgresql [address = "192.168.6.10", color = "#e9d5ff"];
           redis [address = "192.168.6.20", color = "#ddd6fe"];
           vector_store [address = "192.168.6.30", color = "#c4b5fd"];
           object_storage [address = "192.168.6.40", color = "#a78bfa"];
       }

       // Connections between networks
       web_ui, mobile_app, cli_interface -- api_gateway;
       api_gateway -- auth_service, rate_limiter;
       api_gateway -- agent_orchestrator;

       agent_orchestrator -- tool_manager, state_manager, workflow_engine;
       agent_orchestrator -- simple_agent_pool, react_agent_pool, multi_agent_pool;

       tool_manager -- calculator_service, web_search_service, file_service, api_proxy_service;

       state_manager, simple_agent_pool, react_agent_pool -- postgresql, redis, vector_store;
       file_service -- object_storage;
   }
```

### 3. Development and Testing Network

```rst
.. nwdiag::
   :caption: Development and CI/CD Network Infrastructure
   :align: center

   nwdiag {
       // Developer workstations
       network dev_workstations {
           address = "172.16.1.0/24";
           color = "#dbeafe";

           dev_laptop_1 [address = "172.16.1.10", color = "#bfdbfe"];
           dev_laptop_2 [address = "172.16.1.11", color = "#bfdbfe"];
           dev_desktop [address = "172.16.1.20", color = "#93c5fd"];
       }

       // Development environment
       network dev_env {
           address = "172.16.2.0/24";
           color = "#f0fdf4";

           dev_haive_api [address = "172.16.2.10", color = "#dcfce7"];
           dev_database [address = "172.16.2.20", color = "#bbf7d0"];
           dev_redis [address = "172.16.2.30", color = "#86efac"];
           mock_services [address = "172.16.2.40", color = "#4ade80"];
       }

       // Testing environment
       network test_env {
           address = "172.16.3.0/24";
           color = "#fef3c7";

           test_haive_api [address = "172.16.3.10", color = "#fde68a"];
           test_database [address = "172.16.3.20", color = "#fcd34d"];
           test_runner [address = "172.16.3.30", color = "#fbbf24"];
           integration_tests [address = "172.16.3.40", color = "#f59e0b"];
       }

       // Staging environment
       network staging_env {
           address = "172.16.4.0/24";
           color = "#f3e8ff";

           staging_haive_api [address = "172.16.4.10", color = "#e9d5ff"];
           staging_database [address = "172.16.4.20", color = "#ddd6fe"];
           staging_redis [address = "172.16.4.30", color = "#c4b5fd"];
           load_testing [address = "172.16.4.40", color = "#a78bfa"];
       }

       // CI/CD infrastructure
       network cicd {
           address = "172.16.5.0/24";
           color = "#fef2f2";

           jenkins [address = "172.16.5.10", color = "#fecaca"];
           github_actions [address = "172.16.5.20", color = "#fca5a5"];
           docker_registry [address = "172.16.5.30", color = "#f87171"];
           artifact_storage [address = "172.16.5.40", color = "#ef4444"];
       }

       // Monitoring and logging
       network monitoring {
           address = "172.16.6.0/24";
           color = "#f0fdfa";

           prometheus [address = "172.16.6.10", color = "#ccfbf1"];
           grafana [address = "172.16.6.20", color = "#99f6e4"];
           elk_stack [address = "172.16.6.30", color = "#5eead4"];
           jaeger [address = "172.16.6.40", color = "#2dd4bf"];
       }

       // Network flow connections
       dev_laptop_1, dev_laptop_2, dev_desktop -- dev_haive_api;
       dev_haive_api -- dev_database, dev_redis, mock_services;

       dev_haive_api -- jenkins, github_actions;
       jenkins, github_actions -- test_haive_api, staging_haive_api;

       test_runner -- test_haive_api, test_database;
       load_testing -- staging_haive_api, staging_database;

       jenkins -- docker_registry, artifact_storage;

       prometheus -- dev_haive_api, test_haive_api, staging_haive_api;
       grafana -- prometheus;
       elk_stack -- dev_haive_api, test_haive_api, staging_haive_api;
   }
```

### 4. PyDevelop-Docs Documentation Infrastructure

```rst
.. nwdiag::
   :caption: PyDevelop-Docs Documentation Infrastructure
   :scale: 85%

   nwdiag {
       // Content sources
       network content_sources {
           address = "10.1.1.0/24";
           color = "#dbeafe";

           git_repository [address = "10.1.1.10", color = "#bfdbfe"];
           python_packages [address = "10.1.1.20", color = "#93c5fd"];
           markdown_files [address = "10.1.1.30", color = "#60a5fa"];
           config_files [address = "10.1.1.40", color = "#3b82f6"];
       }

       // Build infrastructure
       network build_system {
           address = "10.1.2.0/24";
           color = "#f0fdf4";

           sphinx_builder [address = "10.1.2.10", color = "#dcfce7"];
           autoapi_processor [address = "10.1.2.20", color = "#bbf7d0"];
           diagram_generator [address = "10.1.2.30", color = "#86efac"];
           css_processor [address = "10.1.2.40", color = "#4ade80"];
       }

       // Extension services
       network extensions {
           address = "10.1.3.0/24";
           color = "#fef3c7";

           mermaid_renderer [address = "10.1.3.10", color = "#fde68a"];
           plantuml_server [address = "10.1.3.20", color = "#fcd34d"];
           graphviz_engine [address = "10.1.3.30", color = "#fbbf24"];
           blockdiag_processor [address = "10.1.3.40", color = "#f59e0b"];
       }

       // Output delivery
       network output_delivery {
           address = "10.1.4.0/24";
           color = "#f3e8ff";

           static_site_gen [address = "10.1.4.10", color = "#e9d5ff"];
           cdn_edge [address = "10.1.4.20", color = "#ddd6fe"];
           search_indexer [address = "10.1.4.30", color = "#c4b5fd"];
           analytics_tracker [address = "10.1.4.40", color = "#a78bfa"];
       }

       // External services
       network external_services {
           address = "external";
           color = "#fff7ed";

           github_pages [address = "external", color = "#fed7aa"];
           netlify [address = "external", color = "#fdba74"];
           vercel [address = "external", color = "#fb923c"];
           aws_s3 [address = "external", color = "#f97316"];
       }

       // Processing flow
       git_repository, python_packages, markdown_files -- sphinx_builder;
       sphinx_builder -- autoapi_processor, diagram_generator, css_processor;

       diagram_generator -- mermaid_renderer, plantuml_server, graphviz_engine, blockdiag_processor;

       autoapi_processor, css_processor -- static_site_gen;
       static_site_gen -- cdn_edge, search_indexer;

       cdn_edge -- github_pages, netlify, vercel, aws_s3;
       search_indexer -- analytics_tracker;
   }
```

## Configuration Options

### Current PyDevelop-Docs Configuration

```python
# In config.py - Line 475
extensions = [
    "sphinxcontrib.nwdiag",      # Network diagram support
    # ... other extensions
]

# Basic nwdiag configuration (implicit defaults)
nwdiag_output_format = "svg"     # Vector output for web
nwdiag_fontpath = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
```

### Enhanced Configuration for Issue #6

```python
# Advanced nwdiag configuration for infrastructure documentation
nwdiag_output_format = "svg"                # SVG for scalability
nwdiag_html_image_format = "svg"            # HTML image format
nwdiag_latex_image_format = "pdf"           # LaTeX image format

# Font configuration for better network diagrams
nwdiag_fontpath = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/System/Library/Fonts/Helvetica.ttc",  # macOS support
]

# Network-specific styling
nwdiag_default_network_color = "#f8fafc"    # Light network background
nwdiag_default_node_color = "#ffffff"       # White nodes
nwdiag_default_edge_color = "#64748b"       # Gray connections
nwdiag_default_text_color = "#1e293b"       # Dark text
nwdiag_default_fontsize = 10                # Readable font size

# Network diagram layout
nwdiag_network_width = 300                  # Network section width
nwdiag_node_width = 120                     # Individual node width
nwdiag_node_height = 60                     # Individual node height
nwdiag_span_width = 60                      # Connection spacing
nwdiag_span_height = 40                     # Vertical spacing

# Responsive design
nwdiag_max_width = 1400                     # Maximum diagram width
nwdiag_mobile_scale = 0.7                   # Mobile scaling factor
nwdiag_dpi = 150                            # High DPI rendering

# Performance settings
nwdiag_cache_enabled = True                 # Enable diagram caching
nwdiag_parallel_processing = True           # Parallel rendering
nwdiag_timeout = 60                         # Rendering timeout (networks can be complex)
```

## Template Integration for Issue #6

### 1. Infrastructure Documentation Templates

```jinja2
{# In _autoapi_templates/python/package.rst #}

{% if obj.name in ["deployment", "infrastructure", "network"] %}
**Infrastructure Overview:**

.. nwdiag::
   :caption: {{ obj.name|title }} - Network Architecture
   :align: center

   nwdiag {
       // Package service networks
       {% for module in obj.children %}
       {% if module.type == "module" %}
       network {{ module.name.replace('.', '_') }} {
           address = "10.{{ loop.index }}.0.0/24";
           color = "#f0fdf4";

           {% for child in module.children %}
           {% if child.type == "class" and "service" in child.name.lower() %}
           {{ child.name.lower() }} [address = "10.{{ loop.index0 }}.{{ loop.index }}.10", color = "#dcfce7"];
           {% endif %}
           {% endfor %}
       }
       {% endif %}
       {% endfor %}

       // External dependencies
       network external {
           address = "external";
           color = "#fff7ed";

           {% for imp in obj.imports[:3] %}
           {{ imp.replace('.', '_').replace('-', '_') }} [address = "external", color = "#fed7aa"];
           {% endfor %}
       }

       // Network connections (simplified)
       {% for module in obj.children[:3] %}
       {% for other_module in obj.children[:3] %}
       {% if module != other_module %}
       // {{ module.name.replace('.', '_') }} -- {{ other_module.name.replace('.', '_') }};
       {% endif %}
       {% endfor %}
       {% endfor %}
   }

{% endif %}
```

### 2. Service Architecture Templates

```jinja2
{# For service-oriented documentation #}

.. nwdiag::
   :caption: Service Architecture Network
   :scale: 90%

   nwdiag {
       // Frontend tier
       network frontend {
           address = "192.168.1.0/24";
           color = "#dbeafe";

           {% if "web" in services %}
           web_service [address = "192.168.1.10", color = "#bfdbfe"];
           {% endif %}
           {% if "mobile" in services %}
           mobile_api [address = "192.168.1.20", color = "#93c5fd"];
           {% endif %}
           {% if "cli" in services %}
           cli_interface [address = "192.168.1.30", color = "#60a5fa"];
           {% endif %}
       }

       // Application tier
       network application {
           address = "192.168.2.0/24";
           color = "#f0fdf4";

           {% for service in application_services %}
           {{ service.name }} [address = "192.168.2.{{ 10 + loop.index0 }}", color = "#dcfce7"];
           {% endfor %}
       }

       // Data tier
       network data {
           address = "192.168.3.0/24";
           color = "#f3e8ff";

           {% for db in databases %}
           {{ db.name }} [address = "192.168.3.{{ 10 + loop.index0 }}", color = "#e9d5ff"];
           {% endfor %}
       }

       // Service connections
       {% if "web" in services %}
       web_service -- {{ application_services[0].name }};
       {% endif %}

       {% for service in application_services %}
       {% for db in databases %}
       {{ service.name }} -- {{ db.name }};
       {% endfor %}
       {% endfor %}
   }
```

### 3. Deployment Environment Templates

```jinja2
{# For deployment documentation #}

.. nwdiag::
   :caption: Deployment Environment Network
   :align: center

   nwdiag {
       // Public internet
       internet [shape = cloud, color = "#e0f2fe"];

       // Load balancer tier
       network dmz {
           address = "10.0.1.0/24";
           color = "#fef3c7";

           load_balancer [address = "10.0.1.10", color = "#fde68a"];
           {% if ssl_termination %}
           ssl_terminator [address = "10.0.1.20", color = "#fcd34d"];
           {% endif %}
       }

       // Application tier
       network app_tier {
           address = "10.0.2.0/24";
           color = "#f0fdf4";

           {% for instance in app_instances %}
           app_{{ loop.index }} [address = "10.0.2.{{ 10 + loop.index0 }}", color = "#dcfce7"];
           {% endfor %}
       }

       // Database tier
       network db_tier {
           address = "10.0.3.0/24";
           color = "#f3e8ff";

           {% if database.primary %}
           db_primary [address = "10.0.3.10", color = "#e9d5ff"];
           {% endif %}
           {% if database.replica %}
           db_replica [address = "10.0.3.11", color = "#ddd6fe"];
           {% endif %}
       }

       // Network connections
       internet -- load_balancer;
       {% if ssl_termination %}
       load_balancer -- ssl_terminator;
       ssl_terminator -- app_1;
       {% else %}
       load_balancer -- app_1;
       {% endif %}

       {% for instance in app_instances %}
       app_{{ loop.index }} -- db_primary;
       {% endfor %}
   }
```

## Responsive Design and Mobile Optimization

### Mobile-Optimized CSS for Network Diagrams

```css
/* Network diagram responsive design */
.nwdiag-container {
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

.nwdiag-container svg {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
  background: transparent;
}

/* Network diagram header */
.nwdiag-container::before {
  content: "🌐 Network Architecture";
  position: absolute;
  top: 0;
  left: 0;
  background: var(--color-brand-primary);
  color: white;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-top-left-radius: 10px;
  border-bottom-right-radius: 8px;
  z-index: 1;
}

/* Mobile-specific optimizations */
@media (max-width: 768px) {
  .nwdiag-container {
    padding: 1rem;
    overflow-x: scroll;
    -webkit-overflow-scrolling: touch;
  }

  .nwdiag-container svg {
    min-width: 700px; /* Maintain network diagram readability */
    max-width: none;
  }

  .nwdiag-container::before {
    font-size: 0.75rem;
    padding: 0.375rem 0.75rem;
  }

  /* Touch navigation hint */
  .nwdiag-container::after {
    content: "👆 Scroll to explore network topology";
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

/* Network-specific styling */
.nwdiag-container .network {
  fill: var(--color-api-background);
  stroke: var(--color-background-border);
  stroke-width: 2px;
  rx: 8px; /* Rounded corners */
}

.nwdiag-container .network-label {
  fill: var(--color-foreground-primary);
  font-family: var(--font-stack);
  font-weight: 600;
  font-size: 12px;
}

.nwdiag-container .node {
  fill: var(--color-background-primary);
  stroke: var(--color-brand-primary);
  stroke-width: 2px;
  rx: 4px; /* Slightly rounded nodes */
}

.nwdiag-container .node-label {
  fill: var(--color-foreground-primary);
  font-family: var(--font-stack);
  font-size: 10px;
  font-weight: 500;
}

.nwdiag-container .connection {
  stroke: var(--color-brand-primary);
  stroke-width: 2px;
  stroke-dasharray: none;
}

.nwdiag-container .address-label {
  fill: var(--color-foreground-secondary);
  font-family: var(--font-stack--monospace);
  font-size: 8px;
}

/* Different network types */
.nwdiag-container .network.dmz {
  fill: #fef3c7;
  stroke: #f59e0b;
}

.nwdiag-container .network.internal {
  fill: #f0fdf4;
  stroke: #10b981;
}

.nwdiag-container .network.database {
  fill: #f3e8ff;
  stroke: #8b5cf6;
}

.nwdiag-container .network.external {
  fill: #fff7ed;
  stroke: #f97316;
}

/* Dark theme adjustments */
@media (prefers-color-scheme: dark) {
  .nwdiag-container {
    background: var(--color-background-secondary);
    border-color: var(--color-background-border);
  }

  .nwdiag-container .network {
    fill: var(--color-background-secondary);
    stroke: var(--color-background-border);
  }

  .nwdiag-container .node {
    fill: var(--color-background-primary);
    stroke: var(--color-brand-primary);
  }
}

/* Animation for network diagrams */
@keyframes networkFadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.nwdiag-container {
  animation: networkFadeIn 0.8s ease-out;
}
```

### Interactive Network Features

```css
/* Interactive network elements */
.nwdiag-container .node:hover {
  fill: var(--color-api-background-hover);
  cursor: pointer;
  transform: scale(1.05);
  transition: all 0.2s ease;
}

.nwdiag-container .connection:hover {
  stroke-width: 3px;
  stroke: var(--color-brand-content);
  cursor: pointer;
}

/* Network legend */
.nwdiag-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
  padding: 1rem;
  background: var(--color-background-primary);
  border-radius: 8px;
  border: 1px solid var(--color-background-border);
}

.nwdiag-legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.nwdiag-legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1px solid var(--color-background-border);
}

@media (max-width: 768px) {
  .nwdiag-legend {
    flex-direction: column;
    gap: 0.5rem;
  }
}
```

## Performance Considerations

### Build-Time Optimization

```python
# Network diagram performance optimization
nwdiag_cache_dir = "_nwdiag_cache"          # Cache directory
nwdiag_cache_expiry = 86400                 # 24 hour cache
nwdiag_parallel_workers = 2                 # Parallel processing (networks are complex)
nwdiag_memory_limit = "768m"                # Higher memory for network diagrams

# Conditional generation based on project type
def should_generate_network_diagram(obj):
    """Determine if a network diagram adds value."""
    network_keywords = ["deploy", "infrastructure", "network", "service", "api"]

    if obj.type == "package":
        # Generate for packages with network-related names
        return any(keyword in obj.name.lower() for keyword in network_keywords)
    elif obj.type == "module" and any(keyword in obj.name.lower() for keyword in network_keywords):
        # Generate for network-related modules
        return True
    elif obj.docstring and any(keyword in obj.docstring.lower() for keyword in network_keywords):
        # Generate if documentation mentions networking
        return True
    return False

# Complexity limits for network diagrams
nwdiag_max_networks = 6                     # Maximum networks per diagram
nwdiag_max_nodes_per_network = 8           # Maximum nodes per network
nwdiag_warn_complex = True                  # Warn about complex diagrams
```

### Memory Management

```python
# Memory-efficient nwdiag processing
nwdiag_cleanup_temp = True                  # Clean temporary files
nwdiag_batch_size = 3                       # Smaller batches for network diagrams
nwdiag_gc_frequency = 5                     # More frequent garbage collection
```

## Integration with Other Extensions

### AutoAPI Integration

```python
# Enhanced AutoAPI with network diagrams
autoapi_nwdiag_enabled = True
autoapi_nwdiag_deployment_diagrams = True   # Generate deployment diagrams
autoapi_nwdiag_service_diagrams = True      # Generate service architecture diagrams
autoapi_nwdiag_infrastructure_only = True   # Only for infrastructure packages
```

### Documentation Cross-References

```rst
.. nwdiag::
   :caption: Cross-Referenced Network

   nwdiag {
       network app {
           address = "10.0.1.0/24";
           web_server [address = "10.0.1.10"];
           api_server [address = "10.0.1.20"];
       }

       // Link to documentation
       web_server -- api_server;
   }

See :class:`WebServer` and :class:`APIServer` for implementation details.
```

## Current Implementation Status

### ✅ Production Ready Features

- **Network Diagram Support**: Full nwdiag integration with SVG output
- **Infrastructure Visualization**: Clear network topology representation
- **Multi-tier Architecture**: Support for complex network structures
- **Basic Styling**: Color-coded networks and nodes

### 🚀 Issue #6 Enhancement Opportunities

1. **AutoAPI Integration**: Automated infrastructure diagrams for deployment packages
2. **Interactive Elements**: Clickable nodes and networks with cross-references
3. **Mobile Optimization**: Touch-friendly network exploration
4. **Performance Scaling**: Optimized for complex network architectures
5. **Theme Integration**: Deep Furo theme color matching

### 📋 Implementation Roadmap

1. **Phase 1**: AutoAPI template integration for infrastructure documentation
2. **Phase 2**: Interactive network elements with cross-references
3. **Phase 3**: Mobile-responsive design implementation
4. **Phase 4**: Performance optimization and caching

## Best Practices

### 1. Network Complexity Management

- **Network Limit**: Maximum 5-6 networks per diagram
- **Node Limit**: Maximum 8 nodes per network for readability
- **Logical Grouping**: Group related services in same network
- **Clear Addressing**: Use consistent IP addressing schemes

### 2. Mobile-First Design

- **Horizontal Scrolling**: Allow touch-based network exploration
- **Minimum Sizes**: Networks and nodes large enough for touch
- **Font Sizes**: Minimum 10pt for network labels
- **Touch Targets**: Interactive elements at least 44px

### 3. Documentation Integration

- **Infrastructure Focus**: Use for deployment and architecture documentation
- **Service Topology**: Document microservice communication patterns
- **Security Boundaries**: Show network segmentation and zones
- **Cross-References**: Link nodes to relevant documentation

### 4. Performance Guidelines

- **Selective Generation**: Only create diagrams for network-related content
- **Complexity Limits**: Keep diagrams focused and readable
- **Caching Strategy**: Cache complex network diagrams
- **Batch Processing**: Process multiple diagrams efficiently

---

**Status**: Specialized for network and infrastructure documentation  
**Next Extension**: [sphinxcontrib.actdiag](sphinxcontrib_actdiag.md) - Activity diagram specialization  
**Related**: [Infrastructure Documentation Patterns](../../architecture/)
