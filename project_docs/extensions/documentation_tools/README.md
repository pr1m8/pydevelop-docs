# Documentation Tools Extensions - Quick Implementation Guide

**Focus**: Practical configuration and template integration for PyDevelop-Docs

## Extensions Overview (11 total)

| Extension                 | Status        | Template Ready | Priority |
| ------------------------- | ------------- | -------------- | -------- |
| sphinx_comments           | ✅ Configured | 🔄 Partial     | Medium   |
| sphinx_contributors       | ✅ Configured | ✅ Ready       | High     |
| sphinx_issues             | ✅ Configured | ✅ Ready       | High     |
| sphinx_needs              | ✅ Configured | 🔄 Partial     | Medium   |
| sphinxarg.ext             | ✅ Configured | ✅ Ready       | High     |
| notfound.extension        | ✅ Configured | ✅ Ready       | High     |
| sphinx_library            | ✅ Configured | 🔄 Partial     | Medium   |
| sphinx_icontract          | ✅ Configured | 🔄 Partial     | Low      |
| sphinx_tags               | ✅ Configured | ✅ Ready       | High     |
| sphinx_inlinecode         | ❌ Disabled   | ❌ Conflicts   | Low      |
| sphinxcontrib.collections | ✅ Hub Only   | ✅ Ready       | High     |

## Quick Implementation Patterns

### 1. Template Integration (Issue #6 Focus)

```jinja2
{# Enhanced AutoAPI class template with tools integration #}
{% if obj.docstring %}
.. py:class:: {{ obj.name }}

   {{ obj.docstring|indent(3, True) }}

   {# Add contributor info #}
   .. container:: contributors
      :name: contributors-{{ obj.name }}

   {# Add issue tracking #}
   {% if issues_github_path %}
   :Issues: `Report issues <{{ issues_uri.format(issue='new') }}>`_
   {% endif %}

   {# Add tags for organization #}
   {% if obj.tags %}
   :Tags: {% for tag in obj.tags %}:doc:`{{ tag }}</tag>`{% if not loop.last %}, {% endif %}{% endfor %}
   {% endif %}

{% endif %}
```

### 2. Configuration Consolidation

```python
# Essential configs for template integration
extensions = [
    # ... other extensions ...
    "sphinx_contributors",     # Author attribution
    "sphinx_issues",          # GitHub integration
    "sphinx_tags",            # Content organization
    "notfound.extension",     # Professional 404s
    "sphinxarg.ext",          # CLI documentation
]

# Streamlined configuration
contributors_show_contribution_counts = True
issues_github_path = "haive-ai/haive"
tags_create_badges = True
notfound_template = "page.html"
```

### 3. Template Macros for Efficiency

```jinja2
{# _autoapi_templates/python/macros.rst #}
{% macro render_metadata(obj) %}
   {# Contributors #}
   {% if obj.contributors %}
   .. contributors:: {{ obj.contributors|join(", ") }}
   {% endif %}

   {# Tags #}
   {% if obj.tags %}
   .. tags:: {{ obj.tags|join(", ") }}
   {% endif %}

   {# Issues #}
   :Issues: `Report <{{ issues_uri.format(issue='new') }}>`_
{% endmacro %}
```

## Key Integration Points

### For AutoAPI Templates

- **sphinx_contributors**: Author attribution in class/module headers
- **sphinx_issues**: "Report Bug" links for each API component
- **sphinx_tags**: Automatic categorization and discovery
- **notfound.extension**: Professional 404 for broken API links

### For Build Automation

- **sphinxcontrib.collections**: Multi-package aggregation
- **sphinx_needs**: Requirements traceability
- **sphinxarg.ext**: Automatic CLI documentation

## Performance Optimizations

```python
# Disable heavy features for faster builds
if os.getenv('SPHINX_FAST_BUILD'):
    extensions.remove('sphinx_contributors')  # Skip git analysis
    needs_statuses = []  # Disable requirements tracking
```

## Next Steps

1. **Template Integration**: Add metadata macros to all AutoAPI templates
2. **Workflow Automation**: Enable GitHub integration for issues/contributors
3. **Content Organization**: Implement tag-based navigation
4. **Quality Assurance**: Add automated validation with sphinx_needs

---

**Focus**: Practical implementation over comprehensive documentation. Templates and configuration examples prioritized.
