# Master Implementation Plan - Pydvlppy Enhancement

**Goal**: Implement Issue #6 AutoAPI template improvements using the 45+ extensions  
**Timeline**: 3-week phased approach  
**Priority**: Fix critical issues first, then enhance progressively

## 🚨 Phase 0: Critical Fixes (Day 1)

### 1. Fix Template Distribution System

**Problem**: Templates exist but aren't copied to projects  
**Impact**: No one gets custom templates

```python
# In cli.py, add to _generate_structure():
def _copy_autoapi_templates(self):
    """Copy custom AutoAPI templates to project."""
    source = Path(__file__).parent / "templates" / "_autoapi_templates"
    target = self.docs_source_path / "_autoapi_templates"

    if source.exists():
        shutil.copytree(source, target, dirs_exist_ok=True)
        self.console.print("✅ Copied AutoAPI templates")

# Add to init command after _generate_conf_py()
self._copy_autoapi_templates()
```

### 2. Move Templates to Distribution Location

```bash
# Move templates from docs to package
mkdir -p src/pydevelop_docs/templates/_autoapi_templates/python
mv docs/source/_autoapi_templates/* src/pydevelop_docs/templates/_autoapi_templates/
```

### 3. Fix Extension Loading Order

```python
# In config.py line 449, ensure correct order:
extensions = [
    "autoapi.extension",  # MUST be first
    # ... other extensions ...
    "sphinx_toolbox",  # MUST be before sphinx_autodoc_typehints
    "sphinx_autodoc_typehints",  # MUST be after sphinx_toolbox
]
```

## 🎯 Phase 1: Core Template System (Days 2-3)

### 1. Create Base Template Structure

```
_autoapi_templates/python/
├── base/
│   ├── _layout.rst         # Base template with blocks
│   ├── _macros.rst         # Reusable components
│   └── _progressive.rst    # Progressive disclosure macros
├── class.rst               # Main class template
├── module.rst              # Module template
└── function.rst            # Function template
```

### 2. Implement Progressive Disclosure Base

```jinja2
{# _autoapi_templates/python/base/_progressive.rst #}
{% macro progressive_section(title, content, id, priority="medium", state="collapsed") %}
.. container:: progressive-section progressive-{{ priority }}
   :name: section-{{ id }}

   .. raw:: html

      <button class="progressive-toggle" data-target="{{ id }}">
         <span class="toggle-icon">{{ "▼" if state == "expanded" else "▶" }}</span>
         {{ title }}
      </button>

   .. container:: progressive-content
      :name: content-{{ id }}
      :class: {{ state }}

      {{ content|indent(6) }}
{% endmacro %}
```

### 3. Create Smart Class Template

```jinja2
{# _autoapi_templates/python/class.rst #}
{% from "base/_macros.rst" import render_badges, render_inheritance %}
{% from "base/_progressive.rst" import progressive_section %}

{{ obj.name }}
{{ "=" * obj.name|length }}

{# Quick identification badges #}
{{ render_badges(obj) }}

{# Always visible summary #}
.. container:: class-summary

   {{ obj.summary or obj.docstring.split('\n')[0] if obj.docstring else "No description available." }}

{# Progressive disclosure sections #}
{% if obj.docstring and obj.docstring.split('\n')|length > 1 %}
{{ progressive_section("Full Description", obj.docstring, obj.id + "-desc", "high", "expanded") }}
{% endif %}

{% if obj.methods %}
{{ progressive_section("Methods (" + obj.methods|length|string + ")", render_methods(obj.methods), obj.id + "-methods", "medium") }}
{% endif %}

{% if obj.attributes %}
{{ progressive_section("Attributes (" + obj.attributes|length|string + ")", render_attributes(obj.attributes), obj.id + "-attrs", "low") }}
{% endif %}
```

## 🚀 Phase 2: Visual Enhancements (Days 4-6)

### 1. Replace Graphviz with Mermaid

```jinja2
{# In _macros.rst #}
{% macro render_inheritance(obj) %}
{% if obj.bases %}
.. mermaid::
   :align: center

   graph TD
   {% for base in obj.bases %}
   {{ base }}["{{ base }}"] --> {{ obj.name }}["{{ obj.name }}"]
   {% endfor %}

   classDef current fill:#2563eb,stroke:#1d4ed8,stroke-width:3px,color:#fff;
   classDef base fill:#f3f4f6,stroke:#d1d5db,stroke-width:2px;

   class {{ obj.name }} current;
   {% for base in obj.bases %}
   class {{ base }} base;
   {% endfor %}
{% endif %}
{% endmacro %}
```

### 2. Add CSS for Progressive Disclosure

```css
/* In _static/css/api-progressive.css */
.progressive-section {
  margin: 1rem 0;
  border: 1px solid var(--color-background-border);
  border-radius: 0.5rem;
  overflow: hidden;
}

.progressive-toggle {
  width: 100%;
  padding: 0.75rem 1rem;
  background: var(--color-background-secondary);
  border: none;
  text-align: left;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progressive-toggle:hover {
  background: var(--color-background-hover);
}

.progressive-content {
  padding: 1rem;
  border-top: 1px solid var(--color-background-border);
}

.progressive-content.collapsed {
  display: none;
}

/* Priority-based styling */
.progressive-high .progressive-toggle {
  background: var(--color-brand-content);
  color: white;
}

/* Mobile optimization */
@media (max-width: 768px) {
  .progressive-section {
    margin: 0.5rem -1rem;
    border-radius: 0;
  }
}
```

### 3. Add JavaScript for Interactivity

```javascript
// In _static/js/api-progressive.js
document.addEventListener("DOMContentLoaded", function () {
  // Progressive disclosure toggles
  document.querySelectorAll(".progressive-toggle").forEach((button) => {
    button.addEventListener("click", function () {
      const targetId = this.dataset.target;
      const content = document.getElementById("content-" + targetId);
      const icon = this.querySelector(".toggle-icon");

      if (content.classList.contains("collapsed")) {
        content.classList.remove("collapsed");
        icon.textContent = "▼";
        localStorage.setItem("section-" + targetId, "expanded");
      } else {
        content.classList.add("collapsed");
        icon.textContent = "▶";
        localStorage.setItem("section-" + targetId, "collapsed");
      }
    });

    // Restore state from localStorage
    const targetId = button.dataset.target;
    const savedState = localStorage.getItem("section-" + targetId);
    if (savedState === "expanded") {
      button.click();
    }
  });
});
```

## 🎨 Phase 3: Type-Specific Templates (Days 7-9)

### 1. Create Type Detection System

```python
# In src/pydevelop_docs/template_helpers.py
class TypeDetector:
    @staticmethod
    def detect_class_type(obj):
        """Smart type detection for AutoAPI objects."""
        # Check inheritance chain
        bases = ' '.join(str(base) for base in obj.bases) if hasattr(obj, 'bases') else ''

        # Pydantic detection
        if any(indicator in bases for indicator in ['BaseModel', 'BaseSettings', 'pydantic.']):
            return 'pydantic_model'

        # Agent detection (Haive-specific)
        if any(indicator in bases for indicator in ['Agent', 'BaseAgent', 'ReactAgent']):
            return 'agent_class'

        # Enum detection
        if any(indicator in bases for indicator in ['Enum', 'IntEnum', 'Flag']):
            return 'enum_class'

        # Dataclass detection
        if hasattr(obj, 'decorators') and '@dataclass' in ' '.join(obj.decorators):
            return 'dataclass'

        return 'standard_class'
```

### 2. Register with Jinja2

```python
# In config.py, add:
def autoapi_prepare_jinja_env(jinja_env):
    """Enhance Jinja2 environment for AutoAPI."""
    from pydevelop_docs.template_helpers import TypeDetector

    # Add type detection
    jinja_env.filters['detect_type'] = TypeDetector.detect_class_type

    # Add other useful filters
    jinja_env.filters['count_public'] = lambda items: len([i for i in items if not i.name.startswith('_')])
    jinja_env.tests['pydantic_model'] = lambda obj: TypeDetector.detect_class_type(obj) == 'pydantic_model'
```

### 3. Create Type-Specific Templates

```jinja2
{# _autoapi_templates/python/types/pydantic_model.rst #}
.. container:: pydantic-model

   .. grid:: 2
      :gutter: 2

      .. grid-item-card:: Model Overview
         :class-header: bg-primary

         **{{ obj.name }}**

         {{ render_badges(obj, ['pydantic', 'validated']) }}

         {{ obj.summary }}

      .. grid-item-card:: Quick Example
         :class-header: bg-info

         .. code-block:: python
            :class: copyable

            from {{ obj.module }} import {{ obj.name }}

            # Create instance
            model = {{ obj.name }}(
                {% for field in obj.fields[:3] %}
                {{ field.name }}={{ field.example_value }},
                {% endfor %}
            )

   {# Field documentation with validation info #}
   {{ progressive_section("Fields (" + obj.fields|length|string + ")", render_pydantic_fields(obj.fields), obj.id + "-fields", "high", "expanded") }}
```

## 📋 Phase 4: Integration & Testing (Days 10-12)

### 1. Update Configuration

```python
# Add to config.py
config = {
    # ... existing config ...

    # AutoAPI enhancements
    "autoapi_prepare_jinja_env": autoapi_prepare_jinja_env,

    # CSS files (consolidated)
    "html_css_files": [
        "css/api-progressive.css",  # New progressive disclosure styles
        "css/api-types.css",         # Type-specific styling
        "furo-intense.css",          # Existing dark mode fixes
        "mermaid-custom.css",        # Diagram styling
    ],

    # JavaScript files
    "html_js_files": [
        "js/api-progressive.js",     # Progressive disclosure behavior
        "js/api-enhancements.js",    # Other enhancements
    ],
}
```

### 2. Test with Real Projects

```bash
# Test with sample project
cd test-projects/test-haive-template
poetry run pydvlppy init --force
poetry run sphinx-build -b html docs/source docs/build

# Validate:
# - Templates are copied correctly
# - Progressive disclosure works
# - Type detection is accurate
# - Mobile experience is good
```

### 3. Create Test Suite

```python
# tests/test_template_integration.py
def test_template_distribution():
    """Ensure templates are copied to projects."""
    # Run init command
    # Check _autoapi_templates exists
    # Verify template content

def test_type_detection():
    """Test type detection accuracy."""
    # Test Pydantic models
    # Test Agent classes
    # Test standard classes

def test_progressive_disclosure():
    """Test progressive disclosure rendering."""
    # Test collapsed/expanded states
    # Test localStorage persistence
```

## 🚀 Phase 5: Performance & Polish (Days 13-15)

### 1. Optimize Build Performance

```python
# Template caching
TEMPLATE_CACHE = {}

def cached_render(template_name, context):
    cache_key = f"{template_name}:{hash(str(context))}"
    if cache_key not in TEMPLATE_CACHE:
        TEMPLATE_CACHE[cache_key] = render_template(template_name, context)
    return TEMPLATE_CACHE[cache_key]
```

### 2. Add Mobile Optimizations

- Touch-friendly toggle buttons (44px targets)
- Responsive grid layouts
- Optimized font sizes
- Horizontal scroll for diagrams

### 3. Documentation & Examples

- Update README with new features
- Create example outputs
- Document template customization
- Add troubleshooting guide

## 📊 Success Metrics

### Week 1 Goals

- ✅ Templates distributed to all projects
- ✅ Basic progressive disclosure working
- ✅ Mermaid diagrams replacing Graphviz

### Week 2 Goals

- ✅ Type-specific templates implemented
- ✅ Mobile experience optimized
- ✅ Performance acceptable (<10% slower)

### Week 3 Goals

- ✅ All extensions integrated effectively
- ✅ Documentation complete
- ✅ Tests passing

## 🎯 Next Steps

1. **Start with Phase 0** - Fix critical issues today
2. **Test incrementally** - Validate each phase before moving on
3. **Get feedback early** - Test with real users after Phase 2
4. **Document as you go** - Keep implementation notes

---

**Ready to start?** Begin with Phase 0 critical fixes!
