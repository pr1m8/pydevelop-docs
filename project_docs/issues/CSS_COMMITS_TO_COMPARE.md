# CSS Commits to Compare - PyDevelop-Docs

**Created**: 2025-08-17
**Purpose**: List of commits with different CSS states to compare and find the best configuration

## 📊 Key Commits to Check

### 1. **Before Enhanced Design** (Best candidates for clean CSS)

- **`3497afe`** (2025-08-15 06:32:42) - "FINAL FIX - replace broken templates with correct AutoAPI defaults"
  - Before enhanced-design.css was added
  - Has original CSS files
  - Good baseline to compare

- **`df36ff7`** (2025-08-13 17:09:33) - "fix(css): resolve comprehensive light mode text visibility issues"
  - Focus on fixing visibility issues
  - Before major design changes
  - Likely has working CSS

- **`384eff9`** (2025-08-13 16:31:25) - "fix: resolve static file copying issue - complete CSS and JS distribution"
  - Complete CSS distribution
  - Before enhanced design system

### 2. **After Enhanced Design Added** (Problematic)

- **`090d988`** (2025-08-15 07:34:37) - "feat(templates): enhance AutoAPI templates with modern design and dropdowns"
  - ADDED enhanced-design.css
  - Beginning of marketing-style design
  - When problems started

- **`16c6b50`** (2025-08-15 07:52:31) - "refactor: simplify AutoAPI module template from dropdowns to clean admonitions"
  - Tried to simplify after enhanced design
  - May have partial fixes

### 3. **CSS Consolidation Attempts**

- **`31e74b6`** (2025-08-15 11:20:37) - "feat(autoapi): comprehensive template customization for modern documentation"
  - Claims to consolidate CSS from 6 to 3 files
  - Added breadcrumb navigation
  - Removed some CSS files

### 4. **Current State** (User says terrible)

- **`c0d09bb`** (2025-08-15 20:34:44) - "fix: remove admonition over-styling to restore Furo semantic theming"
  - Attempted admonition fix
  - Still has enhanced-design.css
  - User still unhappy

## 🔍 Commands to Compare

### Check CSS files at each commit:

```bash
# Check what CSS files existed before enhanced design
git show 3497afe:src/pydevelop_docs/config.py | grep -A10 "html_css_files"

# Check original CSS visibility fixes
git show df36ff7:src/pydevelop_docs/config.py | grep -A10 "html_css_files"

# Check when enhanced-design.css was added
git show 090d988:src/pydevelop_docs/config.py | grep -A10 "html_css_files"

# Check current state
git show HEAD:src/pydevelop_docs/config.py | grep -A10 "html_css_files"
```

### View actual CSS content:

```bash
# Check if enhanced-design.css exists in different commits
git show 3497afe:src/pydevelop_docs/templates/static/enhanced-design.css 2>/dev/null || echo "Not found"
git show 090d988:src/pydevelop_docs/templates/static/enhanced-design.css | head -50

# Check api-docs.css evolution
git show 3497afe:src/pydevelop_docs/templates/static/api-docs.css | head -50
git show HEAD:src/pydevelop_docs/templates/static/api-docs.css | head -50
```

### Build docs at specific commit:

```bash
# Checkout specific commit to test
git checkout 3497afe
cd test-projects/test-haive-template
poetry run pydevelop-docs init --force
poetry run sphinx-build -b html docs/source docs/build
# View results

# Return to current
git checkout -
```

## 📋 Recommended Comparison Order

1. **Start with `3497afe`** - Before enhanced design, should be cleanest
2. **Check `df36ff7`** - Has CSS visibility fixes, might be good baseline
3. **Compare with `090d988`** - See what enhanced-design.css added
4. **Look at current** - Understand why it's still "terrible"

## 🎯 What to Look For

### Good Signs:

- Simple, minimal CSS files
- No gradients or hero sections
- No card-based designs
- Clean admonition styling
- Furo theme doing most of the work

### Bad Signs:

- enhanced-design.css present
- Multiple CSS files doing same thing
- Badges and icons everywhere
- Shadow effects
- Marketing-style elements

## 💡 Best Approach

The commit **`3497afe`** (before enhanced-design.css) is likely the best starting point. We can:

1. Check what CSS it had
2. See if docs looked clean
3. Use that as baseline
4. Add only minimal enhancements needed
