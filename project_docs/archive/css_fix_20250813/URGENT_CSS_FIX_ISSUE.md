# URGENT: CSS White-on-White Issue Still Present

**Date**: August 13, 2025
**Issue**: CSS fixes are loaded but not taking effect
**Status**: CSS files present but insufficient specificity

## 🚨 Problem

Even though our CSS files are loading correctly (confirmed in HTML source):

```html
<link
  href="../../../../_static/furo-intense.css?v=5f6b010a"
  rel="stylesheet"
  type="text/css"
/>
```

The white-on-white text is still visible in dark mode at:
`file:///home/will/Projects/haive/backend/haive/tools/pydvlp-docs/test-projects/test-haive-template/docs/build/autoapi/testhaive/agents/react/index.html`

## 🔍 Root Cause Analysis

### 1. CSS Load Order Issue

Our fixes load AFTER Furo's main CSS but BEFORE some other CSS that might be overriding our fixes.

### 2. CSS Specificity Problem

Our selectors like `body[data-theme="dark"] .highlight` might not be specific enough to override all Furo defaults.

### 3. CSS Cascade Issue

Furo might have more specific selectors that are overriding our `!important` declarations.

## ✅ Immediate Fix Required

### Option 1: Increase CSS Specificity

Add more specific selectors to our dark mode fixes:

```css
/* Super specific dark mode fixes */
html body[data-theme="dark"] .highlight,
html body[data-theme="dark"] .highlight pre,
html body[data-theme="dark"] .highlight code {
  background-color: #1e293b !important;
  color: #e2e8f0 !important;
}

/* Target API documentation specifically */
html body[data-theme="dark"] .py-method .highlight,
html body[data-theme="dark"] .py-class .highlight,
html body[data-theme="dark"] .py-function .highlight {
  background-color: #1e293b !important;
  color: #e2e8f0 !important;
}
```

### Option 2: Move CSS to Last Position

Ensure our CSS loads AFTER all other CSS by modifying the Sphinx configuration.

### Option 3: Use CSS Custom Properties

Override Furo's CSS custom properties directly:

```css
body[data-theme="dark"] {
  --color-code-background: #1e293b !important;
  --color-code-foreground: #e2e8f0 !important;
  --color-highlight-background: #1e293b !important;
}
```

## 🎯 Next Steps

1. **IMMEDIATE**: Try Option 1 - increase CSS specificity
2. **BACKUP**: Try Option 3 - override CSS custom properties
3. **LAST RESORT**: Try Option 2 - change CSS load order

## 📊 Files to Update

- `/test-projects/test-haive-template/docs/source/_static/furo-intense.css`
- `/src/pydevelop_docs/templates/static/furo-intense.css`

Both files need the same super-specific CSS fixes to ensure they work everywhere.

---

**Priority**: HIGH - This affects all documentation readability in dark mode
