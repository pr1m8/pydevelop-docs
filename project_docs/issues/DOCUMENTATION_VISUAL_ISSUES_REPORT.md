# Documentation Visual Issues Report - PyDevelop-Docs

**Created**: 2025-08-17
**Purpose**: Document visual and structural issues found in generated documentation
**Status**: Issues Identified - Further Investigation Needed
**Based on**: haive-mcp documentation screenshots

## 📝 Update: Initial Assessment Revised

After further investigation, the HTML content is actually present and properly structured. The issue appears to be with the screenshot tool's CSS selectors rather than the documentation itself.

## 🔍 Actual Findings

### 1. TOC Tree Structure - Present but Different Selectors

**Status**: Needs Verification
**Investigation**: HTML inspection shows toctree elements ARE present

**HTML Analysis**:

- ✅ Found: `<li class="toctree-l1">` elements
- ✅ Found: Nested navigation with proper hierarchy
- ✅ Found: Collapsible navigation with checkboxes
- ❌ Selector `.toc-tree` might be incorrect for Furo theme

**Correct Selectors for Furo**:

- `.toctree-l1, .toctree-l2, .toctree-l3` - TOC levels
- `.sidebar-tree` - Main navigation container
- `input.toctree-checkbox` - Expandable sections

### 2. AutoAPI Content - Generated Successfully

**Status**: Content Present  
**Investigation**: AutoAPI pages contain full documentation

**HTML Analysis**:

- ✅ Found: `<h1>📚 <strong>API Documentation</strong></h1>`
- ✅ Found: Module navigation structure
- ✅ Found: Hierarchical organization (mcp → agents → submodules)
- ❌ Selector `.autoapi` might not exist in current templates

**Actual Content Structure**:

```html
<div class="sidebar-tree">
  <ul class="current">
    <li class="toctree-l1">API Documentation</li>
    <li class="toctree-l2">mcp</li>
    <li class="toctree-l3">mcp.agents</li>
    <!-- etc -->
  </ul>
</div>
```

### 3. Visual Rendering Verification Needed

**Status**: Screenshots Captured - Manual Review Required
**Files**: Located in `debug/screenshots/quick_test/`

**Screenshot Files Created**:

- `index_light.png` (99KB) - Homepage light theme
- `index_dark.png` (100KB) - Homepage dark theme
- `autoapi_index_light.png` (409KB) - API index light theme
- `autoapi_index_dark.png` (400KB) - API index dark theme
- `mcp_module_light.png` (216KB) - MCP module light theme
- `mcp_module_dark.png` (195KB) - MCP module dark theme

The file sizes suggest content is present (especially the 400KB+ API index pages).

## 📊 Test Results Summary

### Pages Tested:

1. **index.html** (Main documentation homepage)
   - ✅ Page loads successfully
   - ❌ Missing TOC tree
   - ✅ Theme switching works (light/dark)

2. **autoapi/index.html** (API Reference Index)
   - ✅ Page loads successfully
   - ❌ Missing TOC tree
   - ❌ Missing AutoAPI content
   - ⚠️ Should show package hierarchy

3. **autoapi/mcp/index.html** (MCP Module Documentation)
   - ✅ Page loads successfully
   - ❌ Missing TOC tree
   - ❌ Missing AutoAPI content
   - ⚠️ Should show module contents

## 🔍 Root Cause Analysis

### 1. TOC Generation Issue

The toctree might not be properly configured in index.rst or the Furo theme settings might be interfering.

**Check**:

```rst
# In index.rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   autoapi/index
```

### 2. AutoAPI Template Problem

The hierarchical organization (`autoapi_own_page_level = "module"`) might be causing template issues.

**Check**:

- AutoAPI files in build/autoapi/
- Template rendering errors in build log
- autoapi_keep_files = True setting

### 3. JavaScript/CSS Loading

Modern themes rely heavily on JavaScript for navigation. Check browser console for errors.

## 🛠️ Recommended Actions

### 1. Update Screenshot Tool Selectors

The screenshot tool needs to use Furo-specific selectors:

```python
# Update in comprehensive_screenshot.py
# Old selectors (incorrect):
toc = await page.query_selector('.toc-tree')
api_content = await page.query_selector('.autoapi')

# New selectors (correct for Furo):
toc = await page.query_selector('.sidebar-tree')
api_content = await page.query_selector('#api-documentation, .sd-sphinx-override')
navigation = await page.query_selector('.toctree-l1')
```

### 2. Visual Inspection Checklist

Open the screenshots in `debug/screenshots/quick_test/` and verify:

- [ ] **Navigation sidebar** is visible on left side
- [ ] **TOC tree** shows hierarchical structure
- [ ] **Dark/light themes** both render correctly
- [ ] **API documentation** shows module listings
- [ ] **Typography** is readable in both themes
- [ ] **Code blocks** have proper syntax highlighting
- [ ] **Admonitions** show correct semantic colors
- [ ] **Search box** is visible and functional

### 3. Known Good Indicators

Based on HTML analysis, these features ARE working:

✅ **Hierarchical API structure** - `autoapi_own_page_level = "module"` is working
✅ **Furo theme integration** - Theme files loading correctly  
✅ **Navigation generation** - TOC tree HTML is present
✅ **Module organization** - Proper nesting (mcp → agents → submodules)
✅ **Dark mode support** - Color scheme meta tag present

### 4. Potential CSS Issues to Check

If visual issues are found in screenshots:

```css
/* Check if these Furo CSS variables are working */
.sidebar-tree {
  /* Should be visible */
}
.toctree-l1 {
  /* Should show hierarchy */
}
.toctree-checkbox {
  /* Should allow expand/collapse */
}

/* Dark mode specific */
html[data-theme="dark"] .sidebar-tree {
  /* Should be visible in dark mode */
}
```

## 🚨 NEW: CSS and Admonition Issues

### Critical CSS Problems Reported

**User Feedback**: "the admonitions and css is terrible"

This suggests visual styling issues with:

1. **Admonition Styling** - Despite removing the color override, admonitions may still have issues
2. **General CSS** - Overall styling may be conflicting or broken
3. **Theme Integration** - CSS files may not be loading in correct order

### Potential CSS Conflicts

PyDevelop-Docs loads multiple CSS files that could conflict:

```python
# From config.py
"html_css_files": [
    "enhanced-design.css",      # Main design system
    "breadcrumb-navigation.css", # Breadcrumb styles
    "mermaid-custom.css",       # Diagram styling
    "tippy-enhancements.css",   # Tooltip styling
]
```

These may be overriding Furo's built-in styles too aggressively.

### Immediate Investigation Needed

1. **Check admonition rendering** in the screenshots
2. **Verify CSS load order** in the HTML
3. **Look for !important overrides** in custom CSS
4. **Test with minimal CSS** to isolate issues

## 📋 Updated Action Items

1. **Critical (CSS Issues)**:
   - [ ] Review screenshots for admonition styling problems
   - [ ] Check enhanced-design.css for aggressive overrides
   - [ ] Test with Furo theme defaults only
   - [ ] Document specific CSS issues found

2. **Immediate**:
   - [ ] Fix screenshot tool selectors
   - [ ] Manually review generated screenshots
   - [ ] Check browser console for CSS errors

3. **Short-term**:
   - [ ] Reduce CSS complexity
   - [ ] Use Furo's semantic styling
   - [ ] Remove unnecessary !important rules

4. **Long-term**:
   - [ ] Create visual regression tests
   - [ ] Establish CSS best practices
   - [ ] Document theme customization guidelines

## 🔴 Additional Content/CSS Issues Found

### Duplicate Module Descriptions

**Issue**: Module docstrings are being duplicated in the HTML output

**Example Found**:

```
Dynamic Activation MCP Server Implementation.
This module provides MCP (Model Context Protocol) integration...
<span class="module-stat">4 classes</span>

Dynamic Activation MCP Server Implementation.
This module provides MCP (Model Context Protocol) integration...
Classes (4)
```

**Cause**: The module description appears to be rendered twice - once in a card/box format and once as regular content.

### CSS Design Issues

1. **Card-based layout** may be too aggressive for API documentation
2. **Module stats** (`<span class="module-stat">`) add visual clutter
3. **Duplicate content** makes pages unnecessarily long
4. **Enhanced design CSS** may be overriding Furo's clean documentation style

### Suggested CSS Fixes

1. **Remove enhanced-design.css** temporarily to test
2. **Simplify module templates** to avoid duplication
3. **Use Furo's default styling** for API documentation
4. **Keep custom CSS minimal** - only for specific needs

## 🔗 Related Files

- Screenshots: `/debug/screenshots/quick_test/`
- Build output: `/home/will/Projects/haive/backend/haive/packages/haive-mcp/docs/build/`
- Configuration: `src/pydevelop_docs/config.py`
- CSS Files: `/docs/source/_static/`
- Templates: `src/pydevelop_docs/templates/`

## 📊 Summary of Issues

1. **CSS Over-styling**: Custom CSS is too aggressive, making docs look bad
2. **Content Duplication**: Module descriptions appearing twice
3. **Admonition Problems**: Despite fixes, still rendering poorly
4. **Theme Conflicts**: Multiple CSS files fighting with Furo
5. **Template Issues**: AutoAPI templates may need simplification

---

**Immediate Recommendation**:

1. **Disable custom CSS** - Test with Furo defaults only
2. **Check AutoAPI templates** - Look for duplication in module rendering
3. **Simplify configuration** - Remove unnecessary styling
4. **Focus on content** - Let Furo handle the presentation
