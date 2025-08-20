# MyST Parser - Advanced Markdown for Sphinx Documentation

**Extension Name**: `myst_parser`  
**Official Documentation**: https://myst-parser.readthedocs.io/  
**PyDevelop-Docs Status**: ✅ **FULLY CONFIGURED**  
**Progressive Disclosure Impact**: 🔥 **CRITICAL** - Primary markup language for modern documentation

## Overview

MyST Parser (Markedly Structured Text) is the backbone of modern Sphinx documentation, providing a powerful Markdown dialect that seamlessly integrates with reStructuredText. In PyDevelop-Docs, MyST enables rich, accessible documentation with extensive UI/UX capabilities that are essential for Issue #6's progressive disclosure goals.

## UI/UX Capabilities

### Content Structure & Hierarchy

MyST Parser provides the foundation for creating scannable, hierarchical documentation:

```markdown
# Primary Section (H1) - Always document title

## Secondary Section (H2) - Major concepts

### Subsection (H3) - Detailed explanations

#### Details (H4) - Implementation specifics
```

### Progressive Disclosure Patterns

**Collapsible Content with Details/Summary**:

````markdown
```{details} Advanced Configuration
:class: sd-dropdown

This section contains advanced configuration options that most users won't need.

* Complex setting A
* Complex setting B
* Expert-level customization
```
````

`````

**Tabbed Information Architecture**:
```markdown
````{tab-set}

```{tab-item} Quick Start
:class: sd-tab-item

Basic setup instructions for getting started quickly.
`````

```{tab-item} Full Configuration
:class: sd-tab-item

Complete configuration options for advanced users.
```

`````
```

## Current PyDevelop-Docs Configuration

In `/src/pydevelop_docs/config.py`, MyST is comprehensively configured:

```python
"myst_enable_extensions": [
    "deflist",        # Definition lists for API glossaries
    "tasklist",       # GitHub-style task lists for checklists
    "html_image",     # Enhanced image handling with responsive sizing
    "colon_fence",    # :::{directive} syntax for better readability
    "smartquotes",    # Typography enhancement for professional appearance
    "replacements",   # Text replacements (e.g., (c) → ©)
    "linkify",        # Auto-link URLs for better connectivity
    "strikethrough",  # ~~text~~ for version changes
    "attrs_inline",   # {class="highlight"} for styling
    "attrs_block",    # Block-level attributes for layout control
],
"myst_heading_anchors": 3,  # Auto-generate anchor links for ToC
"myst_fence_as_directive": ["mermaid", "note", "warning"],  # Enhanced code blocks
```

## Template Integration for Progressive Disclosure

### AutoAPI Template Enhancement

For Issue #6, MyST can dramatically improve AutoAPI templates:

```markdown
<!-- In _autoapi_templates/python/module.rst -->
# {module.name} Module

```{eval-rst}
.. currentmodule:: {module.name}
```

```{note}
:class: sd-note-light

This module provides {module.summary}. For implementation details,
expand the sections below.
```

```{details} Module Overview
:class: sd-dropdown sd-card-header

{module.docstring}
```

<!-- Progressive disclosure for different member types -->
````{tab-set}
:class: sd-tabs-api

```{tab-item} Classes
:class: sd-tab-item

{% for class in module.classes %}
```{details} {class.name}
:class: sd-dropdown sd-fade-in

{class.summary}

```{eval-rst}
.. autoclass:: {class.id}
   :members:
   :undoc-members:
```
```
{% endfor %}
```

```{tab-item} Functions
:class: sd-tab-item

{% for function in module.functions %}
```{card} {function.name}
:class: sd-card-hover

{function.summary}

```{eval-rst}
.. autofunction:: {function.id}
```
```
{% endfor %}
```

`````

````

### Responsive Design Patterns

**Mobile-First Documentation Structure**:
```markdown
```{grid} 1 1 2 3
:class: sd-grid-responsive

```{grid-item-card} Quick Reference
:class: sd-card-hover sd-card-primary

Essential commands and examples for immediate use.
````

```{grid-item-card} Detailed Guide
:class: sd-card-hover sd-card-secondary

Comprehensive documentation for deep understanding.
```

```{grid-item-card} Advanced Topics
:class: sd-card-hover sd-card-info

Expert-level customization and integration patterns.
```

```

```

## JavaScript Integration

MyST seamlessly integrates with interactive JavaScript features:

````markdown
```{code-block} python
:linenos:
:emphasize-lines: 2,3
:caption: Interactive Example

def enhanced_function():
    # This line is highlighted
    return "Interactive documentation"
```
````

<!-- Auto-copying code examples -->

```{literalinclude} ../examples/config.py
:language: python
:lines: 1-20
:caption: Full Configuration Example
```

````

## CSS Customization for Visual Hierarchy

MyST integrates with PyDevelop-Docs CSS system:

```markdown
```{note}
:class: sd-note-primary sd-shadow-lg

Primary information that users need to see immediately.
````

```{warning}
:class: sd-warning-dark sd-border-left

Critical warnings with enhanced visual prominence.
```

```{tip}
:class: sd-tip-light sd-rounded

Helpful tips with modern styling.
```

````

## Accessibility Features (WCAG Compliance)

### Semantic Structure
```markdown
<!-- Proper heading hierarchy for screen readers -->
# Main Topic (Role: heading, level 1)
## Subtopic (Role: heading, level 2)
### Details (Role: heading, level 3)

<!-- Alt text for images -->
![API Flow Diagram](images/api-flow.png "Detailed flow of API request processing")

<!-- Accessible links -->
[Download the full documentation](https://docs.example.com "PDF version of complete documentation")
````

### Keyboard Navigation

````markdown
```{details} Advanced Configuration
:class: sd-dropdown
:tabindex: 0

Content accessible via keyboard navigation with proper focus management.
```
````

````

## Advanced Code Examples

### Definition Lists for API Documentation
```markdown
API Endpoints
: RESTful endpoints for data access

Authentication
: OAuth 2.0 with JWT tokens

Rate Limiting
: 1000 requests per hour per API key

Error Handling
: Standard HTTP status codes with detailed error messages
````

### Task Lists for User Checklists

```markdown
## Setup Checklist

- [ ] Install PyDevelop-Docs
- [ ] Configure project structure
- [ ] Set up documentation sections
- [x] Review this guide
- [ ] Customize templates for your project
```

### Enhanced Link Patterns

```markdown
<!-- Cross-references with MyST -->

{doc}`../installation` - Link to other documentation
{ref}`api-reference` - Link to specific sections
{meth}`MyClass.method` - Link to API methods

<!-- External references with context -->

For more details, see the [official Sphinx documentation](https://www.sphinx-doc.org/).
```

## Integration with Other Extensions

### Sphinx Design Components

````markdown
```{button-ref} installation
:ref-type: doc
:color: primary
:class: sd-rounded-pill

Get Started with Installation
```
````

````{card} Feature Highlight
:class: sd-card-hover sd-shadow-md

```{image} images/feature.png
:class: sd-card-img-top
````

Complete integration with modern design components.

```

```

### Mermaid Diagram Integration

````markdown
```{mermaid}
graph TD
    A[User Documentation] --> B{Progressive Disclosure}
    B -->|Scannable| C[Quick Reference]
    B -->|Detailed| D[Complete Guide]
    B -->|Expert| E[Advanced Topics]
```
````

`````

## Template Patterns for Issue #6

### Scannable API Documentation
```markdown
<!-- Module header with progressive disclosure -->
````{grid} 1 1 1 2
:class: sd-grid-api-header

```{grid-item}
# {module.name}

```{badge} {module.type}
:class: sd-badge-primary
`````

{module.summary}

````

```{grid-item}
```{button-link} #{module.name}-details
:color: secondary
:class: sd-btn-outline

View Details
````

```{button-link} #{module.name}-examples
:color: info
:class: sd-btn-outline

See Examples
```

```

```

<!-- Collapsible detailed documentation -->

```{details} Complete Documentation
:class: sd-dropdown sd-card
:name: {module.name}-details

{module.docstring}
```

`````

### Mobile-Optimized Content
```markdown
```{only} html

<!-- Desktop layout -->
````{grid} 1 1 2 3
:class: sd-grid-desktop-only

```{grid-item-card} Overview
Quick summary for desktop users
`````

```{grid-item-card} Reference
Detailed reference material
```

```{grid-item-card} Examples
Code examples and tutorials
```

````

<!-- Mobile layout -->
```{dropdown} Documentation Sections
:class: sd-mobile-only

* {doc}`overview` - Quick summary
* {doc}`reference` - Detailed reference
* {doc}`examples` - Code examples
```

```

## Performance Considerations

### Lazy Loading Patterns
```markdown
```{details} Heavy Content Section
:class: sd-dropdown sd-lazy-load

This section contains extensive documentation that loads on demand.

```{include} heavy-content.md
```
```
```

### Optimized Image Handling
```markdown
```{figure} images/architecture.png
:class: sd-figure-responsive
:width: 100%
:alt: System architecture diagram

System Architecture Overview
```
```

## Best Practices for PyDevelop-Docs

1. **Use semantic heading hierarchy** - Always start with H1, increment logically
2. **Implement progressive disclosure** - Hide complexity behind expandable sections
3. **Optimize for scanning** - Use cards, badges, and visual hierarchy
4. **Ensure accessibility** - Include alt text, proper ARIA labels
5. **Test on mobile** - Use responsive grid patterns
6. **Leverage cross-references** - Link related documentation sections

## Integration with PyDevelop-Docs Workflow

```python
# In template_manager.py enhancement
def create_myst_content(self, content_type: str, data: dict) -> str:
    """Generate MyST content with progressive disclosure patterns."""
    template = f"""
# {data['title']}

```{{note}}
:class: sd-note-primary

{data['summary']}
```

```{{details}} Complete Information
:class: sd-dropdown

{data['details']}
```
"""
    return template
```

MyST Parser serves as the foundation for all progressive disclosure features in PyDevelop-Docs, enabling beautiful, accessible, and highly functional documentation that scales from quick reference to comprehensive guides.
````
