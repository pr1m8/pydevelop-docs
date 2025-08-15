# CLI CSS Unification Implementation

**Started**: 2025-08-15  
**Purpose**: Fix CLI template CSS configuration and remove unused files  
**Status**: ⚡ **IN PROGRESS**

## Implementation Plan

### Phase 1: Update CLI Template CSS Configuration ⚡ **CURRENT**

**Problem**: CLI template uses legacy `css/custom.css` while shared config uses modern 4-file system

**Target**: Unify both approaches to use the same modern CSS configuration

#### **Files to Modify**:

1. `src/pydevelop_docs/cli.py` - Update hardcoded template CSS configuration
2. Test the updated configuration with breadcrumb integration

#### **Expected Changes**:

```python
# BEFORE (legacy)
html_css_files = ["css/custom.css"]

# AFTER (modern)
html_css_files = [
    "enhanced-design.css",
    "breadcrumb-navigation.css",
    "mermaid-custom.css",
    "tippy-enhancements.css",
]
```

### Phase 2: Clean Up File Distribution 🧹 **NEXT**

**Problem**: CLI distributes 7 CSS files but only 4 are used (47% waste)

**Files to Remove from Distribution**:

- `css/furo-intense.css` - Superseded by enhanced-design.css
- `api-docs.css` - Unused, overlaps with enhanced-design.css
- `toc-enhancements.css` - Unused, conflicts with Furo navigation

**Files to Keep**:

- `enhanced-design.css` ✅ (primary design system)
- `breadcrumb-navigation.css` ✅ (new breadcrumb navigation)
- `mermaid-custom.css` ✅ (diagram theming)
- `tippy-enhancements.css` ✅ (tooltip system)
- `css/custom.css` ⚠️ (keep for now, may deprecate later)

### Phase 3: Validation and Testing 🧪 **FINAL**

**Test Points**:

- [ ] CLI-generated projects use modern CSS files
- [ ] Breadcrumb navigation works with CLI approach
- [ ] Visual consistency between CLI and shared config approaches
- [ ] No missing styles or broken functionality

## Implementation Log

### Step 1: Locate CLI Template CSS Configuration ✅ **COMPLETED**

**Location Found**: Line 642 in `src/pydevelop_docs/cli.py`

**Before**:

```python
html_css_files = [
    "css/custom.css",
]
```

### Step 2: Update CLI Template CSS Configuration ✅ **COMPLETED**

**Updated CLI template** to use modern 4-file CSS system:

```python
html_css_files = [
    "enhanced-design.css",      # Complete modern design system
    "breadcrumb-navigation.css", # Breadcrumb navigation for Furo
    "mermaid-custom.css",       # Mermaid diagram theming
    "tippy-enhancements.css",   # Enhanced tooltip system
]
```

**Impact**: CLI-generated projects now get the same comprehensive CSS as shared config projects.

### Step 3: Clean Up File Distribution 🔄 **IN PROGRESS**

**Next**: Remove unused CSS files from CLI distribution list
