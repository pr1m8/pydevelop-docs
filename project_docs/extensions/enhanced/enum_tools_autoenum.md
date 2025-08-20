# Enum Tools AutoEnum - Enhanced Enumeration Documentation

**Extension Name**: `enum_tools.autoenum`  
**Official Documentation**: https://enum-tools.readthedocs.io/  
**PyDevelop-Docs Status**: ⚠️ **NOT CURRENTLY CONFIGURED** (Available for integration)  
**Progressive Disclosure Impact**: 🎯 **MEDIUM** - Specialized tool for clean enum documentation

## Overview

Enum Tools AutoEnum provides sophisticated documentation capabilities for Python enumerations, automatically generating comprehensive documentation with proper formatting, value tables, and usage examples. While not currently included in PyDevelop-Docs' default extension set, it would be valuable for projects with extensive enum usage, particularly for API documentation where enums represent configuration options, status codes, or type definitions.

## Core UI/UX Capabilities

### Automatic Enum Documentation

AutoEnum automatically generates comprehensive documentation for Python enums:

```python
# Example enum that would be documented
from enum import Enum, IntEnum

class APIStatus(IntEnum):
    """API response status codes."""

    SUCCESS = 200
    """Request completed successfully."""

    NOT_FOUND = 404
    """Requested resource not found."""

    SERVER_ERROR = 500
    """Internal server error occurred."""

class ThemeMode(Enum):
    """Documentation theme modes."""

    LIGHT = "light"
    """Light theme for daytime reading."""

    DARK = "dark"
    """Dark theme for low-light environments."""

    AUTO = "auto"
    """Automatic theme based on system preference."""
```

### Generated Documentation Output

AutoEnum would generate structured documentation like:

```rst
.. autoenum:: mypackage.APIStatus
   :members:
   :show-inheritance:

.. autoenum:: mypackage.ThemeMode
   :members:
   :show-inheritance:
```

## Integration with PyDevelop-Docs Configuration

To add enum_tools support to PyDevelop-Docs, the configuration would be:

```python
# Enhanced config.py with enum_tools support
def _get_complete_extensions(
    is_central_hub: bool, extra_extensions: Optional[List[str]] = None
) -> List[str]:
    extensions = [
        # ... existing extensions ...

        # Enhanced API documentation
        "sphinxcontrib.autodoc_pydantic",
        "sphinx_autodoc_typehints",
        "enum_tools.autoenum",  # ADD: Enhanced enum documentation

        # ... rest of extensions ...
    ]

    # Additional enum_tools configuration
    config.update({
        # Enum documentation settings
        "autoenum_generate_docs": True,
        "autoenum_show_values": True,
        "autoenum_show_inheritance": True,
        "autoenum_member_order": "definition",  # or "alphabetical", "value"
        "autoenum_show_module_summary": True,
    })

    return extensions
```

## AutoAPI Template Integration for Issue #6

### Enhanced Enum Documentation in Templates

```rst
{# _autoapi_templates/python/class.rst - Enhanced for enums #}
{% if obj.obj_type == "enum" %}
.. card:: {{ obj.name }} Enumeration
   :class-card: sd-card-enum sd-shadow-lg

   .. badge:: Enum
      :class: sd-badge-enum

   {{ obj.summary }}

   .. tab-set::
      :class: enum-tabs

      .. tab-item:: Values
         :class-label: tab-enum-values

         .. list-table:: Enumeration Values
            :header-rows: 1
            :class: enum-values-table

            * - Name
              - Value
              - Description
            {% for member in obj.members %}
            * - ``{{ member.name }}``
              - ``{{ member.value }}``
              - {{ member.description or "No description available." }}
            {% endfor %}

      .. tab-item:: Usage Examples
         :class-label: tab-enum-usage

         **Basic Usage:**

         .. code-block:: python
            :class: copyable-enum-basic

            from {{ obj.module }} import {{ obj.name }}

            # Access enum values
            {% for member in obj.members[:3] %}
            status = {{ obj.name }}.{{ member.name }}
            print(f"Status: {status} (value: {status.value})")
            {% endfor %}

         **Comparison and Validation:**

         .. code-block:: python
            :class: copyable-enum-validation

            # Compare enum values
            if current_status == {{ obj.name }}.{{ obj.members[0].name }}:
                print("Success!")

            # Validate input
            try:
                status = {{ obj.name }}(user_input)
            except ValueError:
                print("Invalid status value")

      .. tab-item:: Complete API
         :class-label: tab-enum-api

         .. autoenum:: {{ obj.id }}
            :members:
            :undoc-members:
            :show-inheritance:

{% else %}
{# Regular class template #}
{{ existing_class_template }}
{% endif %}
```

### Module Documentation with Enum Overview

```rst
{# Enhanced module template with enum support #}
{% if module.enums %}
Enumerations
^^^^^^^^^^^^

This module defines the following enumerations:

.. grid:: 1 1 2 3
   :class-container: sd-grid-enums

   {% for enum in module.enums %}
   .. grid-item-card:: {{ enum.name }}
      :class-card: sd-card-enum-summary
      :link: {{ enum.id }}

      .. badge:: {{ enum.members | length }} values
         :class: sd-badge-enum-count

      {{ enum.summary }}

      **Common values:**
      {% for member in enum.members[:3] %}
      ``{{ member.name }}``{% if not loop.last %}, {% endif %}
      {% endfor %}
      {% if enum.members | length > 3 %}...{% endif %}
   {% endfor %}

.. tab-set::
   :class: module-enum-tabs

   .. tab-item:: Quick Reference

      .. list-table:: All Enumerations
         :header-rows: 1
         :class: enum-summary-table

         * - Enum
           - Values
           - Purpose
         {% for enum in module.enums %}
         * - :class:`{{ enum.name }}`
           - {{ enum.members | length }}
           - {{ enum.summary }}
         {% endfor %}

   .. tab-item:: Usage Examples

      **Import all enumerations:**

      .. code-block:: python
         :class: copyable-enum-imports

         from {{ module.name }} import (
             {% for enum in module.enums %}
             {{ enum.name }},
             {% endfor %}
         )

      **Common patterns:**

      .. code-block:: python
         :class: copyable-enum-patterns

         {% for enum in module.enums[:2] %}
         # Using {{ enum.name }}
         {% for member in enum.members[:2] %}
         if value == {{ enum.name }}.{{ member.name }}:
             handle_{{ member.name | lower }}()
         {% endfor %}

         {% endfor %}

{% endif %}
```

## CSS Customization for Enum Documentation

### Enum-Specific Styling

```css
/* In api-docs.css - Enum documentation styling */
.sd-card-enum {
  border-left: 4px solid #6f42c1;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
}

.sd-badge-enum {
  background: #6f42c1;
  color: white;
  font-weight: 500;
}

.sd-badge-enum-count {
  background: #28a745;
  color: white;
  font-size: 0.8em;
}

/* Enum values table styling */
.enum-values-table {
  width: 100%;
  margin: 1rem 0;
  border-collapse: collapse;
}

.enum-values-table th {
  background: var(--color-brand-primary);
  color: white;
  padding: 8px 12px;
  text-align: left;
  font-weight: 500;
}

.enum-values-table td {
  padding: 8px 12px;
  border-bottom: 1px solid var(--color-background-border);
}

.enum-values-table td:first-child {
  font-family: var(--font-stack-monospace);
  background: var(--color-code-background);
  color: var(--color-code-foreground);
}

.enum-values-table td:nth-child(2) {
  font-family: var(--font-stack-monospace);
  font-weight: 500;
}

/* Enum summary cards */
.sd-card-enum-summary {
  transition: all 0.3s ease;
  border: 1px solid #e7e3ff;
}

.sd-card-enum-summary:hover {
  border-color: #6f42c1;
  box-shadow: 0 4px 12px rgba(111, 66, 193, 0.15);
  transform: translateY(-2px);
}

/* Enum hierarchy visualization */
.enum-hierarchy {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 1rem 0;
  padding: 12px;
  background: var(--color-background-secondary);
  border-radius: 6px;
}

.enum-hierarchy::before {
  content: "🔗";
  font-size: 1.2em;
}

/* Dark mode adjustments */
[data-theme="dark"] .sd-card-enum {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-left-color: #9d7bea;
}

[data-theme="dark"] .enum-values-table th {
  background: var(--color-brand-primary);
}
```

### Mobile-Optimized Enum Tables

```css
/* Responsive enum tables */
@media (max-width: 768px) {
  .enum-values-table {
    font-size: 0.9rem;
  }

  .enum-values-table th,
  .enum-values-table td {
    padding: 6px 8px;
  }

  /* Stack table on very small screens */
  @media (max-width: 480px) {
    .enum-values-table,
    .enum-values-table thead,
    .enum-values-table tbody,
    .enum-values-table th,
    .enum-values-table td,
    .enum-values-table tr {
      display: block;
    }

    .enum-values-table thead tr {
      position: absolute;
      top: -9999px;
      left: -9999px;
    }

    .enum-values-table tr {
      border: 1px solid var(--color-background-border);
      margin-bottom: 10px;
      padding: 10px;
      border-radius: 4px;
    }

    .enum-values-table td {
      border: none;
      padding: 5px 0;
      position: relative;
      padding-left: 50%;
    }

    .enum-values-table td:before {
      content: attr(data-label) ": ";
      position: absolute;
      left: 6px;
      width: 45%;
      padding-right: 10px;
      white-space: nowrap;
      font-weight: bold;
    }
  }
}
```

## JavaScript Enhancement for Interactive Enums

### Enum Value Search and Filter

```javascript
// In furo-enhancements.js
document.addEventListener("DOMContentLoaded", function () {
  enhanceEnumDocumentation();
});

function enhanceEnumDocumentation() {
  const enumTables = document.querySelectorAll(".enum-values-table");

  enumTables.forEach((table) => {
    addEnumSearch(table);
    addEnumFilters(table);
    addEnumCopyFunctionality(table);
  });
}

function addEnumSearch(table) {
  const container = table.parentElement;

  // Create search input
  const searchContainer = document.createElement("div");
  searchContainer.className = "enum-search-container";
  searchContainer.innerHTML = `
        <input type="search" 
               class="enum-search" 
               placeholder="Search enum values..." 
               aria-label="Search enum values">
        <span class="enum-search-results"></span>
    `;

  container.insertBefore(searchContainer, table);

  const searchInput = searchContainer.querySelector(".enum-search");
  const resultsSpan = searchContainer.querySelector(".enum-search-results");

  searchInput.addEventListener("input", function () {
    const query = this.value.toLowerCase();
    const rows = table.querySelectorAll("tbody tr");
    let visibleCount = 0;

    rows.forEach((row) => {
      const text = row.textContent.toLowerCase();
      const visible = text.includes(query);

      row.style.display = visible ? "" : "none";
      if (visible) visibleCount++;
    });

    resultsSpan.textContent = query
      ? `${visibleCount} of ${rows.length} values`
      : "";
  });
}

function addEnumFilters(table) {
  const container = table.parentElement;

  // Analyze enum values to create filters
  const rows = table.querySelectorAll("tbody tr");
  const valueTypes = new Set();

  rows.forEach((row) => {
    const valueCell = row.cells[1]; // Value column
    const value = valueCell.textContent.trim();

    if (/^\d+$/.test(value)) {
      valueTypes.add("integer");
    } else if (/^".*"$/.test(value)) {
      valueTypes.add("string");
    } else if (/^[A-Z_]+$/.test(value)) {
      valueTypes.add("constant");
    }
  });

  if (valueTypes.size > 1) {
    const filterContainer = document.createElement("div");
    filterContainer.className = "enum-filters";
    filterContainer.innerHTML = `
            <label>Filter by type:</label>
            <select class="enum-type-filter">
                <option value="">All types</option>
                ${Array.from(valueTypes)
                  .map((type) => `<option value="${type}">${type}</option>`)
                  .join("")}
            </select>
        `;

    container.insertBefore(filterContainer, table);

    const select = filterContainer.querySelector(".enum-type-filter");
    select.addEventListener("change", function () {
      const filterType = this.value;

      rows.forEach((row) => {
        if (!filterType) {
          row.style.display = "";
          return;
        }

        const value = row.cells[1].textContent.trim();
        let matches = false;

        switch (filterType) {
          case "integer":
            matches = /^\d+$/.test(value);
            break;
          case "string":
            matches = /^".*"$/.test(value);
            break;
          case "constant":
            matches = /^[A-Z_]+$/.test(value);
            break;
        }

        row.style.display = matches ? "" : "none";
      });
    });
  }
}

function addEnumCopyFunctionality(table) {
  const rows = table.querySelectorAll("tbody tr");

  rows.forEach((row) => {
    const nameCell = row.cells[0];
    const valueCell = row.cells[1];

    // Add copy buttons
    nameCell.style.position = "relative";
    valueCell.style.position = "relative";

    const nameCopyBtn = createCopyButton(nameCell.textContent.trim());
    const valueCopyBtn = createCopyButton(valueCell.textContent.trim());

    nameCell.appendChild(nameCopyBtn);
    valueCell.appendChild(valueCopyBtn);
  });
}

function createCopyButton(text) {
  const button = document.createElement("button");
  button.className = "enum-copy-btn";
  button.innerHTML = "📋";
  button.title = "Copy to clipboard";
  button.setAttribute("aria-label", `Copy ${text} to clipboard`);

  button.addEventListener("click", function (e) {
    e.preventDefault();
    e.stopPropagation();

    navigator.clipboard.writeText(text).then(() => {
      button.innerHTML = "✓";
      button.style.background = "#28a745";

      setTimeout(() => {
        button.innerHTML = "📋";
        button.style.background = "";
      }, 1500);
    });
  });

  return button;
}
```

### Enum Usage Pattern Generator

```javascript
function addEnumUsageGenerator() {
  const enumCards = document.querySelectorAll(".sd-card-enum");

  enumCards.forEach((card) => {
    const enumName = card.querySelector("h1, h2, h3").textContent.trim();
    const table = card.querySelector(".enum-values-table");

    if (!table) return;

    const generateBtn = document.createElement("button");
    generateBtn.className = "enum-generate-usage";
    generateBtn.textContent = "Generate Usage Examples";
    generateBtn.style.margin = "1rem 0";

    generateBtn.addEventListener("click", function () {
      const examples = generateEnumUsageExamples(enumName, table);
      showEnumExamples(card, examples);
    });

    card.appendChild(generateBtn);
  });
}

function generateEnumUsageExamples(enumName, table) {
  const rows = table.querySelectorAll("tbody tr");
  const values = Array.from(rows).map((row) => ({
    name: row.cells[0].textContent.trim(),
    value: row.cells[1].textContent.trim(),
    description: row.cells[2].textContent.trim(),
  }));

  return {
    imports: `from mymodule import ${enumName}`,
    basic: values
      .slice(0, 3)
      .map((v) => `# ${v.description}\nstatus = ${enumName}.${v.name}`)
      .join("\n\n"),
    validation: `
# Validate enum value
try:
    status = ${enumName}(user_input)
except ValueError:
    print("Invalid value")
        `.trim(),
    comparison: `
# Compare enum values
if current_status == ${enumName}.${values[0].name}:
    print("${values[0].description}")
        `.trim(),
  };
}
```

## Integration with Other Extensions

### Sphinx Design Integration

```rst
.. grid:: 1 1 2 2
   :class-container: enum-overview-grid

   .. grid-item-card:: Status Codes
      :class-card: sd-card-enum-category

      .. autoenum:: myapi.StatusCode
         :members:

   .. grid-item-card:: Configuration Options
      :class-card: sd-card-enum-category

      .. autoenum:: myapi.ConfigOption
         :members:
```

### Copy Button Integration

```rst
.. code-block:: python
   :class: copyable-enum-usage
   :caption: Complete enum usage example

   from mypackage import APIStatus, ThemeMode

   # Status checking
   if response.status == APIStatus.SUCCESS:
       process_success()

   # Theme configuration
   theme = ThemeMode.AUTO
```

## Accessibility Features

### Screen Reader Support

```javascript
function enhanceEnumAccessibility() {
  const enumTables = document.querySelectorAll(".enum-values-table");

  enumTables.forEach((table) => {
    // Add table description
    const caption = document.createElement("caption");
    caption.textContent = "Enumeration values and descriptions";
    caption.className = "sr-only";
    table.insertBefore(caption, table.firstChild);

    // Add scope attributes to headers
    const headers = table.querySelectorAll("th");
    headers.forEach((header) => {
      header.setAttribute("scope", "col");
    });

    // Add row headers for value names
    const rows = table.querySelectorAll("tbody tr");
    rows.forEach((row) => {
      const nameCell = row.cells[0];
      nameCell.setAttribute("scope", "row");
    });
  });
}
```

## Template Patterns for Different Enum Types

### API Status Codes

```rst
.. autoenum:: myapi.HTTPStatus
   :members:
   :show-inheritance:

**HTTP Status Code Reference:**

.. tab-set::
   :class: status-code-tabs

   .. tab-item:: Success (2xx)

      {% for status in http_status.success_codes %}
      **{{ status.name }}** ({{ status.value }})
         {{ status.description }}
      {% endfor %}

   .. tab-item:: Client Error (4xx)

      {% for status in http_status.client_error_codes %}
      **{{ status.name }}** ({{ status.value }})
         {{ status.description }}
      {% endfor %}

   .. tab-item:: Server Error (5xx)

      {% for status in http_status.server_error_codes %}
      **{{ status.name }}** ({{ status.value }})
         {{ status.description }}
      {% endfor %}
```

### Configuration Enums

```rst
.. autoenum:: mypackage.LogLevel
   :members:

**Usage in Configuration:**

.. code-block:: python
   :class: copyable-config-enum

   import logging
   from mypackage import LogLevel

   # Convert enum to logging level
   level_mapping = {
       LogLevel.DEBUG: logging.DEBUG,
       LogLevel.INFO: logging.INFO,
       LogLevel.WARNING: logging.WARNING,
       LogLevel.ERROR: logging.ERROR,
       LogLevel.CRITICAL: logging.CRITICAL,
   }

   logging.basicConfig(level=level_mapping[LogLevel.INFO])
```

## Best Practices for Enum Documentation

1. **Clear descriptions** - Provide meaningful docstrings for each enum member
2. **Logical grouping** - Group related enums in the same module
3. **Value consistency** - Use consistent value types within enums
4. **Usage examples** - Show practical usage patterns
5. **Cross-references** - Link to related functions and classes
6. **Mobile optimization** - Ensure enum tables work on small screens

While not currently included in PyDevelop-Docs, enum_tools.autoenum would provide excellent support for projects with extensive enumeration usage, enhancing API documentation clarity and developer experience.
