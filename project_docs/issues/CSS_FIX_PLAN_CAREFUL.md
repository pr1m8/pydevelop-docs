# Careful CSS Fix Plan - PyDevelop-Docs

**Created**: 2025-08-17
**Purpose**: Step-by-step plan to carefully fix CSS issues
**Status**: Ready to Execute

## 🎯 Goal

Remove marketing-style CSS while preserving functionality. Make documentation clean and professional.

## 📋 Current State

### CSS Files Being Loaded:

1. **From html_css_files**:
   - enhanced-design.css (PROBLEM - marketing style)
   - breadcrumb-navigation.css (GOOD - keep)
   - mermaid-custom.css (GOOD - keep)
   - tippy-enhancements.css (GOOD - keep)

2. **From setup() function**:
   - custom.css (CHECK - might be okay)
   - tippy-enhancements.css (DUPLICATE!)
   - api-docs.css (PROBLEM - badges and gradients)

## 🔧 Step-by-Step Fix Plan

### Step 1: Backup Current Configuration

```bash
# Create backup branch
git checkout -b backup/css-before-fix
git add -A
git commit -m "backup: CSS configuration before simplification"
git checkout -
```

### Step 2: Remove enhanced-design.css

- Edit config.py line 408
- Remove or comment out "enhanced-design.css"
- Keep breadcrumb, mermaid, and tippy CSS

### Step 3: Fix Duplicate CSS Loading

- Edit setup() function around line 830-833
- Remove duplicate tippy-enhancements.css (line 832)
- Remove aggressive api-docs.css (line 833)
- Keep custom.css if it's minimal

### Step 4: Create Minimal API Styling (if needed)

- Only if API pages look too plain
- Simple borders instead of cards
- No gradients or shadows

### Step 5: Test Incrementally

- Build test project after each change
- Take screenshots
- Compare with current state

## 📝 Specific Changes

### config.py Changes:

```python
# Line 407-413, change from:
"html_css_files": [
    "enhanced-design.css",  # Modern design system - contains all styling
    # Removed conflicting files: furo-intense.css, api-docs.css, toc-enhancements.css
    "breadcrumb-navigation.css",  # Breadcrumb navigation for Furo
    "mermaid-custom.css",  # Keep diagram-specific styling
    "tippy-enhancements.css",  # Keep tooltip-specific styling
],

# To:
"html_css_files": [
    # "enhanced-design.css",  # REMOVED - too aggressive marketing style
    "breadcrumb-navigation.css",  # Breadcrumb navigation for Furo
    "mermaid-custom.css",  # Keep diagram-specific styling
    "tippy-enhancements.css",  # Keep tooltip-specific styling
    # May add minimal-api.css later if needed
],
```

### setup() function changes:

```python
# Lines 830-833, change from:
# Add custom CSS for better styling (enhanced-design.css is already in html_css_files)
app.add_css_file("custom.css", priority=600)
app.add_css_file("tippy-enhancements.css", priority=601)
app.add_css_file("api-docs.css", priority=602)

# To:
# Add minimal custom CSS
app.add_css_file("css/custom.css", priority=600)
# Removed tippy-enhancements.css - already in html_css_files
# Removed api-docs.css - too aggressive with badges and gradients
```

## 🧪 Testing Plan

1. **Before Changes**:

   ```bash
   cd test-projects/test-haive-template
   poetry run python ../../scripts/debug/quick_screenshot_test.py
   mv debug/screenshots/quick_test debug/screenshots/before_fix
   ```

2. **After Each Change**:

   ```bash
   poetry run pydvlp-docs init --force
   poetry run sphinx-build -b html docs/source docs/build
   python -m http.server 8003 --directory docs/build
   # Check in browser
   ```

3. **Final Comparison**:
   ```bash
   poetry run python ../../scripts/debug/quick_screenshot_test.py
   mv debug/screenshots/quick_test debug/screenshots/after_fix
   # Compare screenshots
   ```

## ✅ Success Criteria

1. **No blue gradient boxes** on API pages
2. **No duplicate module descriptions**
3. **Clean, readable documentation**
4. **Proper semantic admonition colors**
5. **Fast page loads**
6. **Professional appearance**

## 🚨 Rollback Plan

If something goes wrong:

```bash
git stash
git checkout backup/css-before-fix
```

Ready to proceed with Step 1?
