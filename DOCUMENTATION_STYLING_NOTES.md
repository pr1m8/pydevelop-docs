# PyDevelop-Docs Styling Notes & Issues

**Created**: 2025-08-18
**Purpose**: Document styling issues and improvements needed for PyDevelop-Docs
**Reference**: haive-mcp documentation example

## 🎨 Styling Issues Identified

### 1. Function Signatures Appear White/Unstyled

**Problem**: Function signatures in the API documentation have no background styling, making them blend into the page.

**Example from haive-mcp**:

```html
<dt
  class="sig sig-object py"
  id="mcp.haive_agent_mcp_integration.demo_discovery_to_agent"
>
  <span class="sig-name descname"
    ><span class="pre">demo_discovery_to_agent</span></span
  >
</dt>
```

**Expected**: Functions should have:

- Light gray background (`#f1f5f9`) in light mode
- Dark background (`#1e293b`) in dark mode
- Clear visual separation from regular text
- Proper padding and border radius

**Solution**: Need to add CSS for `.sig` and `.sig-object` classes:

```css
/* api-docs.css or custom.css */
.sig-object {
  background-color: var(--color-api-background, #f1f5f9);
  border: 1px solid var(--color-api-background-hover, #e2e8f0);
  border-radius: 0.25rem;
  padding: 0.5rem 1rem;
  margin: 1rem 0;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  body[data-theme="dark"] .sig-object {
    background-color: #1e293b;
    border-color: #334155;
  }
}
```

### 2. Missing [source] Links

**Problem**: No "view source" links appear next to function/class definitions.

**Root Cause**: Using `viewcode` extension instead of `linkcode`, and missing GitHub integration.

**Solution**:

1. Keep `viewcode` extension (it's working)
2. Configure `viewcode` properly:

```python
# In config.py
viewcode_enable_epub = False
viewcode_follow_imported_members = True
```

3. Ensure AutoAPI is configured to show source:

```python
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",  # Important for source links
]
```

### 3. Better Use of Admonitions

**Current**: Basic tip box at bottom of module pages

**Improvements Needed**:

#### A. Module-Level Admonitions

Add informative admonitions at the top of modules:

```rst
.. note::
   This module provides MCP (Model Context Protocol) integration for Haive agents.

.. tip::
   For a complete example, see :func:`demo_discovery_to_agent`

.. warning::
   Requires MCP server to be installed and running.
```

#### B. Function-Level Admonitions

Use admonitions in docstrings:

```python
def my_function():
    """Do something important.

    .. note::
       This function requires async execution.

    .. warning::
       Do not call this in a sync context.

    .. seealso::
       :func:`other_function` for related functionality
    """
```

#### C. Admonition Types to Use

- `.. note::` - General information
- `.. tip::` - Best practices
- `.. warning::` - Important cautions
- `.. danger::` - Critical warnings
- `.. seealso::` - Related content
- `.. versionadded::` - New features
- `.. deprecated::` - Deprecation notices
- `.. todo::` - Future improvements

### 4. Empty Function Bodies

**Problem**: Functions show empty card bodies:

```html
<div class="sd-card-body docutils"></div>
```

**Solution**: Ensure docstrings are properly formatted and AutoAPI extracts them.

### 5. CSS Variables Not Properly Applied

**Issue**: CSS variables defined but not used consistently.

**Fix**: Create a unified CSS file that properly applies variables:

```css
/* api-function-styling.css */
:root {
  --api-function-bg: #f8f9fa;
  --api-function-border: #dee2e6;
  --api-function-hover: #e9ecef;
  --api-param-color: #495057;
  --api-return-color: #0066cc;
}

[data-theme="dark"] {
  --api-function-bg: #1e293b;
  --api-function-border: #334155;
  --api-function-hover: #334155;
  --api-param-color: #cbd5e1;
  --api-return-color: #60a5fa;
}

/* Apply to all function signatures */
dl.function > dt,
dl.method > dt,
dl.class > dt,
dl.attribute > dt {
  background-color: var(--api-function-bg);
  border: 1px solid var(--api-function-border);
  border-radius: 0.375rem;
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  font-family: "SF Mono", Monaco, Consolas, monospace;
}

dl.function > dt:hover,
dl.method > dt:hover {
  background-color: var(--api-function-hover);
}
```

## 📋 Implementation Plan

### 1. Create New CSS File

Create `api-function-styling.css` with proper function styling.

### 2. Update config.py

Add the new CSS file to html_css_files:

```python
"html_css_files": [
    "api-function-styling.css",  # NEW
    "breadcrumb-navigation.css",
    "mermaid-custom.css",
    "tippy-enhancements.css",
],
```

### 3. Enhanced AutoAPI Templates

Create custom AutoAPI templates that include:

- Better admonition placement
- Source code links
- Parameter/return type highlighting

### 4. Template Enhancements

Update the Jinja2 templates to automatically add:

- Module overview admonitions
- Usage examples in tip boxes
- Warning admonitions for async functions

## 🎯 Expected Results

1. **Clear Visual Hierarchy**: Functions/classes stand out with proper backgrounds
2. **Easy Navigation**: [source] links for all items
3. **Better Documentation**: Strategic use of admonitions for guidance
4. **Consistent Styling**: All API elements follow the same visual pattern
5. **Dark Mode Support**: Proper contrast in both themes

## 🔧 Quick Fix for Testing

Add this to `docs/source/_static/css/custom.css`:

```css
/* Quick API styling fix */
.sig.sig-object {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 8px 12px;
  margin: 8px 0;
}

[data-theme="dark"] .sig.sig-object {
  background: #1e293b;
  border-color: #334155;
}

/* Add [source] link styling */
.viewcode-link {
  float: right;
  font-size: 0.875rem;
  color: var(--color-brand-primary);
}
```

## 📚 Additional Enhancements

### 1. Parameter Tables

Style parameter lists better:

```css
.field-list {
  background: var(--color-background-secondary);
  border-radius: 0.25rem;
  padding: 1rem;
}
```

### 2. Return Type Highlighting

Make return types more visible:

```css
.sig-return {
  color: var(--api-return-color);
  font-weight: 500;
}
```

### 3. Inheritance Diagrams

Ensure inheritance diagrams are properly styled:

```css
.inheritance-diagram {
  background: white;
  border: 1px solid var(--color-background-border);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1rem 0;
}
```

## 🚀 Next Steps

1. Implement the CSS fixes
2. Test on haive-mcp documentation
3. Create custom AutoAPI templates if needed
4. Document the styling patterns
5. Apply to all template styles (minimal, modern, classic)
