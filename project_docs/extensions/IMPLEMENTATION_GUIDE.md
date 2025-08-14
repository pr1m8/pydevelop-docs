# Extensions Implementation Guide - Practical Integration

**Purpose**: Efficient implementation of 45+ extensions in PyDevelop-Docs  
**Focus**: Configuration patterns and template integration for Issue #6

## Quick Start: Priority Extensions for Issue #6

### Critical Template Integration (Top 5)

1. **sphinx_design** - Grid layouts, cards, badges for progressive disclosure
2. **sphinx_togglebutton** - Collapsible sections for information management
3. **autoapi.extension** - Core API documentation with template customization
4. **sphinxcontrib.mermaid** - Modern inheritance diagrams replacing Graphviz
5. **sphinx_copybutton** - Essential UX for code examples

### Configuration Template

```python
# Essential config for Issue #6 template enhancements
extensions = [
    "autoapi.extension",           # MUST be first
    "sphinx_design",               # Modern UI components
    "sphinx_togglebutton",         # Progressive disclosure
    "sphinxcontrib.mermaid",       # Beautiful diagrams
    "sphinx_copybutton",           # Code UX
    # ... rest of extensions
]

# Key settings for template integration
autoapi_template_dir = "_autoapi_templates"
autoapi_own_page_level = "module"  # Hierarchical organization
mermaid_params = ["--theme", "neutral", "--backgroundColor", "transparent"]
copybutton_prompt_is_regexp = True
```

## Template Integration Patterns

### 1. Enhanced Class Template with Progressive Disclosure

```jinja2
{# _autoapi_templates/python/class.rst #}
{% from "macros.rst" import progressive_section, render_badges %}

{{ obj.name }}
{{ "=" * obj.name|length }}

{# Type detection and badges #}
{% set class_type = obj|detect_type %}
{{ render_badges(obj, class_type) }}

{# Progressive disclosure sections #}
{{ progressive_section(
    "Overview",
    obj.docstring or "No description available.",
    "overview-" + obj.name,
    "expanded"
) }}

{% if obj.methods %}
{{ progressive_section(
    "Methods (" + obj.methods|length|string + ")",
    render_methods(obj.methods),
    "methods-" + obj.name,
    "collapsed"
) }}
{% endif %}

{# Inheritance diagram with Mermaid #}
{% if obj.bases %}
{{ progressive_section(
    "Inheritance",
    render_mermaid_inheritance(obj),
    "inheritance-" + obj.name,
    "collapsed"
) }}
{% endif %}
```

### 2. Macro Library for Reusability

```jinja2
{# _autoapi_templates/python/macros.rst #}
{% macro progressive_section(title, content, id, state="collapsed") %}
.. container:: progressive-section

   .. container:: section-header
      :name: toggle-{{ id }}

      **{{ title }}** {% if state == "collapsed" %}▶{% else %}▼{% endif %}

   .. container:: section-content
      :name: content-{{ id }}
      :class: {% if state == "collapsed" %}collapsed{% else %}expanded{% endif %}

      {{ content }}
{% endmacro %}

{% macro render_mermaid_inheritance(obj) %}
.. mermaid::

   graph TD
   {% for base in obj.bases %}
   {{ base }} --> {{ obj.name }}
   {% endfor %}

   classDef current fill:#fff3b8,stroke:#f57c00;
   class {{ obj.name }} current;
{% endmacro %}
```

### 3. CSS Integration (6 Consolidated Files)

```css
/* api-docs.css - Enhanced API styling */
.progressive-section {
  margin: 1rem 0;
  border: 1px solid var(--color-background-border);
  border-radius: 0.375rem;
}

.section-header {
  padding: 0.75rem 1rem;
  background: var(--color-background-secondary);
  cursor: pointer;
  user-select: none;
}

.section-content.collapsed {
  display: none;
}

.section-content.expanded {
  padding: 1rem;
  border-top: 1px solid var(--color-background-border);
}

/* Mobile responsive */
@media (max-width: 768px) {
  .progressive-section {
    margin: 0.5rem 0;
  }

  .section-header {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }
}
```

## Extension Configuration Matrix

### Production-Ready Configuration

```python
def get_optimized_extensions(is_production=False):
    """Get extension list optimized for environment."""

    # Core extensions (always enabled)
    core = [
        "autoapi.extension",
        "sphinx.ext.autodoc",
        "sphinx.ext.napoleon",
        "sphinx.ext.viewcode",
        "sphinx.ext.intersphinx",
    ]

    # UI enhancements (critical for Issue #6)
    ui = [
        "sphinx_design",
        "sphinx_togglebutton",
        "sphinx_copybutton",
        "sphinx_tabs.tabs",
        "myst_parser",
    ]

    # Visual enhancements
    visual = [
        "sphinxcontrib.mermaid",
        "sphinx_tippy",
        "sphinx_favicon",
    ]

    # Production utilities
    production = [
        "sphinx_sitemap",
        "sphinxext.opengraph",
        "sphinx_last_updated_by_git",
    ] if is_production else []

    # Performance-heavy (disable for fast builds)
    heavy = [
        "sphinx_contributors",
        "sphinx_git",
        "sphinx_needs",
    ] if not os.getenv('SPHINX_FAST_BUILD') else []

    return core + ui + visual + production + heavy
```

## Template Directory Structure

```
_autoapi_templates/
└── python/
    ├── base/
    │   ├── _layout.rst          # Foundation template
    │   ├── _macros.rst          # Shared components
    │   └── _variables.rst       # Common variables
    ├── types/
    │   ├── pydantic_model.rst   # Pydantic-specific
    │   ├── agent_class.rst      # Agent-specific
    │   ├── enum_class.rst       # Enum-specific
    │   └── standard_class.rst   # Default class
    ├── components/
    │   ├── _inheritance.rst     # Mermaid diagrams
    │   ├── _methods.rst         # Method display
    │   └── _parameters.rst      # Parameter tables
    └── [main templates]         # class.rst, module.rst, etc.
```

## Performance Optimization

### Build Speed Optimizations

```python
# Fast build environment variable
if os.getenv('SPHINX_FAST_BUILD'):
    # Disable heavy extensions
    extensions = [ext for ext in extensions if ext not in [
        'sphinx_contributors', 'sphinx_git', 'sphinx_needs'
    ]]

    # Reduce Mermaid quality for speed
    mermaid_params = ["--theme", "neutral", "--width", "400"]

    # Disable some AutoAPI features
    autoapi_add_class_diagram = False
```

### Template Caching

```jinja2
{# Cache expensive operations #}
{% set cached_inheritance = obj.id + "_inheritance" %}
{% if not cache.get(cached_inheritance) %}
  {% set inheritance_diagram = render_mermaid_inheritance(obj) %}
  {% do cache.set(cached_inheritance, inheritance_diagram) %}
{% endif %}
{{ cache.get(cached_inheritance) }}
```

## Implementation Checklist

### Phase 1: Core Setup (Week 1)

- [ ] Configure top 5 critical extensions
- [ ] Create basic progressive disclosure templates
- [ ] Add essential CSS styling
- [ ] Test with sample API objects

### Phase 2: Enhanced UX (Week 2)

- [ ] Implement Mermaid inheritance diagrams
- [ ] Add responsive mobile design
- [ ] Create type-specific templates
- [ ] Add interactive tooltips

### Phase 3: Production Polish (Week 3)

- [ ] Enable SEO extensions (sitemap, opengraph)
- [ ] Add performance monitoring
- [ ] Implement caching strategies
- [ ] Add error handling and fallbacks

## Quick Commands

```bash
# Fast build for development
SPHINX_FAST_BUILD=1 sphinx-build -b html docs/source docs/build

# Full production build
sphinx-build -b html docs/source docs/build -W --keep-going

# Test template changes
sphinx-build -b html docs/source docs/build -E -a
```

---

**Result**: Practical, implementation-focused guide for efficiently using all 45+ extensions in PyDevelop-Docs templates and configuration.
