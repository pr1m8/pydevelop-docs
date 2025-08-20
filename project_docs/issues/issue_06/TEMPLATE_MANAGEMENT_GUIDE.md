# Template Management Guide for Issue #6 - Custom Jinja2 Templates

**Created**: 2025-08-13
**Status**: Ready for Implementation
**Priority**: High
**For Agent**: Working on Issue #6 (Custom Jinja2 templates)

## Overview

This guide explains the current template structure and where to implement custom AutoAPI templates for Issue #6.

## Current Template Structure

### 1. **PyDevelop-Docs Templates** (Our Templates)

Located in: `/src/pydevelop_docs/templates/`

```
templates/
├── central_hub_conf.py.jinja2      # Central documentation hub config
├── central_hub_index.rst.jinja2    # Central hub index page
├── doc_templates/                  # Documentation content templates
│   ├── configuration.rst.jinja2    # Configuration guide template
│   ├── installation.rst.jinja2     # Installation guide template
│   ├── quickstart.rst.jinja2       # Quickstart guide template
│   └── section_index.rst.jinja2    # Section index template
└── static/                         # Static assets
    ├── css/                        # CSS files (including furo-intense.css)
    └── js/                         # JavaScript files
```

### 2. **AutoAPI Templates** (Need to Create)

**Target Location**: `/src/pydevelop_docs/templates/_autoapi_templates/`

This directory needs to be created and will contain custom AutoAPI Jinja2 templates.

**NOTE**: There are already some custom AutoAPI templates in the docs directory:

- `/docs/source/_autoapi_templates/python/class.rst` - Custom class template
- `/docs/source/_autoapi_templates/python/dataclass.rst` - Custom dataclass template
- `/docs/source/_autoapi_templates/python/module.rst` - Custom module template

These can serve as a starting point for your customizations.

## Implementation Plan for Issue #6

### Step 1: Create AutoAPI Template Directory

```bash
mkdir -p /home/will/Projects/haive/backend/haive/tools/pydvlp-docs/src/pydevelop_docs/templates/_autoapi_templates/python/
```

### Step 2: Copy Default AutoAPI Templates

Default templates are located in the virtual environment:

```
.venv/lib/python3.12/site-packages/autoapi/templates/python/
```

Key templates to customize:

- `module.rst` - Module documentation template
- `class.rst` - Class documentation template
- `function.rst` - Function documentation template
- `index.rst` - API index template
- `package.rst` - Package documentation template

### Step 3: Template Structure to Create

```
_autoapi_templates/
└── python/
    ├── module.rst          # Custom module template
    ├── class.rst          # Custom class template
    ├── function.rst       # Custom function template
    ├── method.rst         # Custom method template
    ├── attribute.rst      # Custom attribute template
    ├── data.rst          # Custom data/constant template
    ├── exception.rst      # Custom exception template
    ├── package.rst        # Custom package template
    └── index.rst          # Custom API index template
```

### Step 4: CLI Integration

The CLI needs to copy these templates when initializing a new project.

**File to modify**: `/src/pydevelop_docs/cli.py`

In the `_copy_static_files()` method, add:

```python
# Copy AutoAPI templates
autoapi_template_src = self.template_path / "_autoapi_templates"
if autoapi_template_src.exists():
    autoapi_template_dst = Path(self.project_path) / "docs/source/_autoapi_templates"
    shutil.copytree(autoapi_template_src, autoapi_template_dst, dirs_exist_ok=True)
```

### Step 5: Configuration Update

In `config.py`, add AutoAPI template directory configuration:

```python
# In get_haive_config() or get_central_hub_config()
"autoapi_template_dir": "_autoapi_templates",
```

## Key Customizations for Issue #6

Based on the issue description, focus on:

1. **Improved Class Documentation** (`class.rst`)
   - Better organization of methods
   - Clearer inheritance visualization
   - Grouped attributes by category

2. **Enhanced Module Layout** (`module.rst`)
   - Better separation of classes, functions, and constants
   - Visual hierarchy improvements
   - Category-based grouping

3. **Cleaner Function Documentation** (`function.rst`)
   - Simplified parameter tables
   - Better return value documentation
   - Example code highlighting

4. **Organized API Index** (`index.rst`)
   - Package-based grouping (already achieved with hierarchical fix)
   - Visual cards for packages
   - Better navigation structure

## Template Variables Available

AutoAPI provides these variables to templates:

```jinja2
{{ obj.name }}              # Object name
{{ obj.type }}              # Object type (class, function, etc.)
{{ obj.docstring }}         # Parsed docstring
{{ obj.children }}          # Child objects
{{ obj.properties }}        # Object properties
{{ obj.methods }}           # Class methods
{{ obj.attributes }}        # Class attributes
{{ obj.bases }}             # Base classes
{{ obj.signatures }}        # Function/method signatures
{{ obj.parameters }}        # Function parameters
{{ obj.returns }}           # Return documentation
{{ obj.yields }}            # Yield documentation
{{ obj.raises }}            # Exception documentation
{{ obj.examples }}          # Code examples
{{ obj.see_also }}          # See also references
{{ obj.notes }}             # Additional notes
{{ obj.warnings }}          # Warning messages
```

## Example Custom Template (class.rst)

```jinja2
{# Custom class template with better organization #}
{{ obj.name }}
{{ "=" * obj.name|length }}

.. currentmodule:: {{ obj.module }}

.. autoclass:: {{ obj.name }}
   :members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__

   {% if obj.docstring %}
   {{ obj.docstring|indent(3) }}
   {% endif %}

   {% if obj.attributes %}
   **Attributes**

   .. list-table::
      :widths: 30 70
      :header-rows: 1

      * - Attribute
        - Description
      {% for attr in obj.attributes %}
      * - ``{{ attr.name }}``
        - {{ attr.docstring|first_line }}
      {% endfor %}
   {% endif %}

   {% if obj.methods %}
   **Methods**

   {% for method in obj.methods|sort(attribute='name') %}
   .. automethod:: {{ method.name }}
   {% endfor %}
   {% endif %}
```

## Testing Your Templates

1. **Create test templates** in the `_autoapi_templates` directory
2. **Run documentation build**:
   ```bash
   cd test-projects/test-haive-template
   poetry run sphinx-build -b html docs/source docs/build/html
   ```
3. **Check generated documentation** for your customizations
4. **Iterate** on template design

## Integration with PyDevelop-Docs

Once templates are created:

1. **Update CLI** to copy templates during `init`
2. **Update TemplateManager** to handle AutoAPI templates
3. **Test with various project types** (single package, monorepo)
4. **Document template customization** in user guides

## Files You'll Need to Modify

1. `/src/pydevelop_docs/cli.py` - Add template copying
2. `/src/pydevelop_docs/config.py` - Add template directory config
3. `/src/pydevelop_docs/template_manager.py` - Add AutoAPI template handling
4. Create all files in `/src/pydevelop_docs/templates/_autoapi_templates/python/`

## Resources

- [AutoAPI Template Documentation](https://sphinx-autoapi.readthedocs.io/en/latest/reference/templates.html)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- Default templates: `.venv/lib/python3.12/site-packages/autoapi/templates/python/`

## Success Criteria

- [ ] Custom templates created in `_autoapi_templates/python/`
- [ ] Templates improve readability and organization
- [ ] CLI copies templates during project initialization
- [ ] Templates work with hierarchical organization (autoapi_own_page_level = "module")
- [ ] Documentation is cleaner and more navigable

---

**Note**: The color visibility fixes have been completed and pushed. The templates are ready for your custom Jinja2 implementation!
