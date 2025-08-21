# Breadcrumb Testing Approach

**Status**: Ready for implementation  
**Implementation**: Complete - just needs validation  
**Priority**: High (TODO #3)

## Testing Strategy

### 1. Test Environment Setup

```bash
# Use existing test-haive-template structure
cd /home/will/Projects/haive/backend/haive/tools/pydvlppy/test-projects/test-haive-template

# Regenerate with latest breadcrumb implementation
poetry run pydvlppy init --force

# Build and serve locally
poetry run sphinx-build -b html docs/source docs/build
python -m http.server 8003 --directory docs/build
```

### 2. Validation Points

#### A. Template Distribution

- [ ] Verify `layout.html` is copied to `docs/source/_templates/`
- [ ] Verify `breadcrumb-navigation.css` is copied to `docs/source/_static/`
- [ ] Check CLI `_copy_static_files()` method works correctly

#### B. CSS Integration

- [ ] Confirm `breadcrumb-navigation.css` is included in HTML head
- [ ] Test Furo CSS variable integration (light/dark mode)
- [ ] Verify responsive behavior on mobile

#### C. Breadcrumb Generation

- [ ] **Home page**: No breadcrumbs (expected)
- [ ] **AutoAPI index** (`autoapi/index.html`): Home → current
- [ ] **Module pages** (`autoapi/testhaive/core/index.html`): Home → API Reference → current
- [ ] **Deep pages** (`autoapi/testhaive/core/engine/index.html`): Home → API Reference → Testhaive → Core → current

#### D. Navigation Functionality

- [ ] All breadcrumb links clickable and working
- [ ] Current page shown as non-linked active item
- [ ] Proper aria-label for accessibility

### 3. Cross-Browser Testing

- [ ] Chrome (light/dark mode toggle)
- [ ] Firefox (CSS variable support)
- [ ] Safari (webkit prefixes)
- [ ] Mobile responsive (breakpoint behavior)

### 4. Integration with Existing Features

- [ ] No conflicts with existing Furo navigation
- [ ] No conflicts with existing CSS (6 files)
- [ ] Search functionality still works
- [ ] Copy buttons still work
- [ ] Dark mode toggle still works

## Implementation Details

### Files Created

1. **`layout.html`** - Furo template override with breadcrumb macro
2. **`breadcrumb-navigation.css`** - Furo-compatible styling
3. **Updated `cli.py`** - Distribution of new files
4. **Updated `config.py`** - CSS file inclusion

### Key Technical Decisions

#### Template Strategy

- **Extends Furo base**: `{% extends "furo/base.html" %}`
- **Override content block**: Injects breadcrumbs before page content
- **Smart path parsing**: Handles AutoAPI URL structure automatically
- **Conditional rendering**: Only shows breadcrumbs when relevant

#### CSS Strategy

- **Furo CSS variables**: Uses `--color-*` variables for consistency
- **Dark mode support**: `[data-theme="dark"]` selectors
- **Mobile responsive**: Progressive hiding of intermediate crumbs
- **Print styles**: Hidden in print media

#### URL Pattern Recognition

```jinja2
{% if "autoapi" in pagename and pagename != "autoapi/index" %}
  # Generate API Reference breadcrumb
  {% set path_parts = pagename.replace("autoapi/", "").split("/") %}
  # Parse hierarchical structure from URL
{% endif %}
```

## Expected Results

### Before (Current State)

- No breadcrumb navigation on any pages
- Users must use sidebar or back button for navigation
- Difficult to understand current location in deep API structures

### After (With Breadcrumbs)

- Clear navigation path: `Home → API Reference → Package → Module`
- Click any level to navigate up the hierarchy
- Consistent with modern documentation UX patterns
- Maintains Furo's clean aesthetic

## Risk Assessment

### Low Risk

- **Template override approach**: Standard Sphinx pattern, well-documented
- **CSS variables usage**: Leverages Furo's existing system
- **File distribution**: Uses existing CLI copy mechanism

### Medium Risk

- **Furo theme compatibility**: Need to test across Furo versions
- **CSS conflicts**: 6 existing CSS files to verify compatibility

### Mitigations

- **Fallback graceful**: If breadcrumbs fail, normal navigation still works
- **Minimal DOM impact**: Only adds `<nav>` element at top of content
- **Standard CSS**: Uses established patterns, no experimental features

## Success Criteria

1. **Functional**: Breadcrumbs appear and navigate correctly
2. **Visual**: Matches Furo design language perfectly
3. **Responsive**: Works on all screen sizes
4. **Accessible**: Proper ARIA labels and semantic HTML
5. **Performance**: No impact on page load times

## Next Steps After Validation

1. **Update documentation**: Add breadcrumb info to README
2. **Consider enhancements**:
   - Schema.org structured data for breadcrumbs
   - Keyboard navigation support
   - Custom breadcrumb separators
3. **Package distribution**: Ensure works across all project types
