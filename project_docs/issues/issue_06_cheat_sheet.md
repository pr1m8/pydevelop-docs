# Issue #6 Cheat Sheet: AutoAPI + Jinja2 Template Customization

**Quick Reference for Custom AutoAPI Templates**

## 🎯 Core Concepts

### Jinja2 Basics

```jinja2
{{ variable }}                  # Output variable
{% if/for/block %}{% endif %}   # Control structures
{# comment #}                   # Comments
{{ var|filter }}                # Apply filters
{% macro name() %}{% endmacro %} # Reusable components
```

### AutoAPI Template Location

```python
# conf.py
autoapi_template_dir = '_autoapi_templates'  # Your custom templates here
```

## 📁 Template Structure

```
_autoapi_templates/
└── python/
    ├── module.rst      # For modules
    ├── class.rst       # For classes
    ├── function.rst    # For functions
    ├── method.rst      # For methods
    └── attribute.rst   # For attributes
```

## 🔑 Key Variables Available

### Always Available

- `obj` - The Python object being documented
- `autoapi_options` - Config options from conf.py
- `include_summaries` - Bool for summary tables
- `own_page_types` - Which types get own pages

### Common `obj` Attributes

```jinja2
obj.name              # Simple name (e.g., "MyClass")
obj.id                # Full path (e.g., "package.module.MyClass")
obj.type              # "class", "function", "module", etc.
obj.docstring         # Full docstring
obj.short_description # First line of docstring

# Class-specific
obj.bases             # Base classes
obj.methods           # List of methods
obj.attributes        # List of attributes
obj.is_abstract       # True if abstract

# Function-specific
obj.signature         # Full signature
obj.parameters        # Parameter list
obj.returns           # Return annotation
obj.is_async          # True if async
```

## ⚡ Quick Patterns

### Progressive Disclosure

```jinja2
{# Show summary first #}
{{ obj.short_description }}

{# Details in collapsible #}
{% if obj.docstring != obj.short_description %}
<details>
    <summary>More Details</summary>
    {{ obj.docstring }}
</details>
{% endif %}
```

### Type Detection

```jinja2
{% if 'BaseModel' in obj.bases|map(attribute='name')|list %}
    {# It's a Pydantic model! #}
{% elif 'Agent' in obj.bases|map(attribute='name')|list %}
    {# It's an Agent class! #}
{% endif %}
```

### Safe Attribute Access

```jinja2
{# Always check existence #}
{% if obj.methods %}
    {% for method in obj.methods %}
        {{ method.name }}
    {% endfor %}
{% endif %}
```

### Method Filtering

```jinja2
{# Public methods only #}
{% for method in obj.methods if not method.name.startswith('_') %}
    {{ method.name }}
{% endfor %}
```

## 🛠️ Jinja2 Environment Customization

```python
# conf.py
def autoapi_prepare_jinja_env(jinja_env):
    # Add custom filter
    jinja_env.filters['shorten'] = lambda s, n=50: s[:n] + '...' if len(s) > n else s

    # Add custom test
    jinja_env.tests['pydantic'] = lambda obj: any('BaseModel' in str(b) for b in (obj.bases or []))

    # Add global function
    jinja_env.globals['get_icon'] = lambda t: {'class': '🏛️', 'function': '⚡'}.get(t, '📄')
```

## 🚨 Critical Gotchas

### 1. Can't Extend Default Templates

```jinja2
{# ❌ WRONG - Causes infinite recursion #}
{% extends 'python/class.rst' %}

{# ✅ RIGHT - Copy entire template #}
{# Must copy default template and modify #}
```

### 2. reStructuredText Indentation

```jinja2
{# ❌ WRONG - RST needs indentation #}
:Parameters:
{% for p in obj.parameters %}
* {{ p.name }}
{% endfor %}

{# ✅ RIGHT - Proper indentation #}
:Parameters:
   {% for p in obj.parameters %}
   * {{ p.name }}
   {% endfor %}
```

### 3. Whitespace Control

```jinja2
{# Remove extra whitespace #}
{%- if condition -%}
    content
{%- endif -%}
```

## 📊 Useful Filters

```jinja2
{{ text|truncate(50) }}           # Shorten text
{{ items|length }}                # Count items
{{ items|join(', ') }}            # Join list
{{ value|default('N/A') }}        # Default value
{{ name|upper }}                  # Uppercase
{{ items|sort(attribute='name') }} # Sort by attribute
{{ items|select }}                # Filter truthy
{{ items|reject }}                # Filter falsy
{{ items|map(attribute='name') }} # Extract attribute
```

## 🎨 Quick Wins

### 1. Better Class Header

```jinja2
{{ obj.name }}
{{ "=" * obj.name|length }}

{% if obj.bases %}
*Inherits from:* {{ obj.bases|map(attribute='name')|join(', ') }}
{% endif %}

{{ obj.short_description }}
```

### 2. Smart Method List

```jinja2
{% set public = obj.methods|rejectattr('name', 'match', '^_')|list %}
{% set private = obj.methods|selectattr('name', 'match', '^_')|list %}

{% if public %}
**Public Methods** ({{ public|length }})
   {% for m in public|sort(attribute='name') %}
   * :meth:`{{ m.name }}`
   {% endfor %}
{% endif %}
```

### 3. Pydantic Model Fields

```jinja2
{% if obj|pydantic %}
**Fields:**
   {% for attr in obj.attributes %}
   * **{{ attr.name }}** ({{ attr.annotation|default('Any') }})
   {% endfor %}
{% endif %}
```

## 🔍 Debugging

```jinja2
{# See all available attributes #}
<pre>{{ obj.__dict__|pprint }}</pre>

{# Check variable type #}
Type: {{ obj.type }}
Bases: {{ obj.bases|map(attribute='name')|list }}

{# Test if attribute exists #}
{% if obj.some_attr is defined %}
    {{ obj.some_attr }}
{% endif %}
```

## 📝 Quick Setup

1. Create directory: `mkdir -p _autoapi_templates/python`
2. Add to conf.py: `autoapi_template_dir = '_autoapi_templates'`
3. Copy default template: Find in `site-packages/autoapi/templates/python/`
4. Modify as needed
5. Test with: `sphinx-build -b html . _build`

## 🎯 Remember

- **Start simple** - Modify one template at a time
- **Test often** - Small changes can break RST formatting
- **Check output** - Verify HTML renders correctly
- **Keep logic minimal** - Complex logic belongs in Python
- **Document changes** - Future you will thank you
