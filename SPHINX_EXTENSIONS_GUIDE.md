# PyAutoDoc Sphinx Extensions Guide

## Overview

This project uses a comprehensive set of Sphinx extensions for hyper-organized documentation with intense Furo theming. The extensions are organized by priority and functionality.

## Extension Categories & Usage

### 🔥 Core Extensions (Priority 1-10)

#### `sphinx.ext.autodoc` (Priority 1)

- **What**: Core automatic documentation generation
- **Usage**: Automatically documents Python modules, classes, functions
- **Config**: Already configured with `autoapi_options`

#### `autoapi.extension` (Priority 2)

- **What**: Advanced automatic API documentation
- **Usage**: Replaces traditional `autodoc` with better file discovery
- **Config**: `autoapi_dirs = ["../../src"]`
- **Features**:
  - Auto-discovers all Python files
  - Generates complete API reference
  - Custom templates support

### 📊 Enhanced API Documentation (Priority 11-20)

#### `sphinxcontrib.autodoc_pydantic` (Priority 11)

- **What**: Specialized Pydantic model documentation
- **Usage**: Beautifully renders Pydantic models with schema info
- **Config**: `autodoc_pydantic_model_show_json = True`
- **Features**:
  - JSON schema generation
  - Field validation display
  - Model inheritance trees

#### `sphinx_autodoc_typehints` (Priority 12)

- **What**: Enhanced type hint support
- **Usage**: Converts Python type annotations to documentation
- **Config**: `typehints_fully_qualified = False`

### 🎨 Content & Design (Priority 21-30)

#### `sphinx_design` (Priority 22) - KEY EXTENSION

- **What**: Modern design components for documentation
- **Usage**: Cards, buttons, grids, tabs, badges
- **Features**:

  ```rst
  :::{card} Card Title
  Card content with enhanced styling
  :::

  :::{button-ref} target
  :color: primary
  Button text
  :::
  ```

#### `sphinx_togglebutton` (Priority 23)

- **What**: Collapsible content sections
- **Usage**: Add toggle functionality to content blocks
- **Example**:
  ```rst
  :::{toggle}
  Hidden content here
  :::
  ```

#### `sphinx_copybutton` (Priority 24)

- **What**: Copy buttons for code blocks
- **Usage**: Automatic copy buttons on all code examples
- **Config**: `copybutton_prompt_text` removes prompts

#### `sphinx_tabs.tabs` (Priority 25)

- **What**: Tabbed content interface
- **Usage**: Create multi-tab code examples
- **Example**:

  ````rst
  :::{tab-set}
  :::{tab-item} Python
  ```python
  print("Hello")
  ````

  :::
  :::{tab-item} JavaScript

  ```javascript
  console.log("Hello");
  ```

  :::
  :::

  ```

  ```

### 🎯 Enhanced Features (Priority 71-80)

#### `sphinx_paramlinks` - Parameter Linking

- **What**: Enhanced parameter cross-references
- **Usage**: Auto-links function parameters
- **Config**: `paramlinks_hyperlink_param = True`

#### `sphinx_toggleprompt` - Interactive Code Prompts

- **What**: Toggle Python prompts in code blocks
- **Usage**: Adds toggle buttons to `>>>` prompts
- **Config**: `toggleprompt_default_hidden = "true"`

#### `sphinx_last_updated_by_git` - Git Timestamps

- **What**: Shows last modification time from git
- **Usage**: Automatically adds "Last updated" to pages
- **Config**: `git_last_updated_format = "%Y-%m-%d %H:%M"`

#### `sphinx_inlinecode` - Enhanced Inline Code

- **What**: Better styling for inline code
- **Usage**: Improved `code` rendering
- **Config**: `inlinecode_highlight_language = "python"`

#### `sphinx_library` - Library Documentation

- **What**: Enhanced library-specific documentation features
- **Usage**: Better module summaries and organization
- **Config**: `library_show_summary = True`

#### `sphinx_icontract` - Contract Documentation

- **What**: Documents preconditions, postconditions, invariants
- **Usage**: Integrates with icontract library
- **Config**: `icontract_include_repr = True`

### 📖 TOC Enhancements (Priority 61-70)

#### `sphinxcontrib.fulltoc` - Full Table of Contents

- **What**: Shows complete TOC structure in sidebar
- **Usage**: Better navigation for large documentation sets
- **Features**: Recursive TOC trees without path repetition

#### `sphinx_treeview` - Collapsible Navigation

- **What**: Dynamic collapsible tree view sidebar
- **Usage**: Expandable/collapsible documentation sections
- **Config**:
  ```python
  treeview_expand_all = False
  treeview_collapse_inactive = True
  treeview_max_depth = 4
  ```

### 🛠 Documentation Tools (Priority 81-90)

#### `sphinx_comments` - Annotations

- **What**: Add comments and annotations to docs
- **Usage**: Interactive commenting system
- **Config**: `comments_config = {"hypothesis": True}`

#### `sphinx_contributors` - Contributors

- **What**: Show contributor information
- **Usage**: Displays contribution statistics
- **Config**: `contributors_show_contribution_counts = True`

#### `sphinx_issues` - GitHub Integration

- **What**: Link to GitHub issues and PRs
- **Usage**: `:issue:`123`` links to GitHub issues
- **Config**: `issues_github_path = "yourusername/pyautodoc"`

### 📈 Diagrams (Priority 41-50)

#### `sphinxcontrib.mermaid` - Mermaid Diagrams

- **What**: Interactive diagrams and flowcharts
- **Usage**:
  ```rst
  :::{mermaid}
  graph TD
      A[Start] --> B[End]
  :::
  ```
- **Config**: Custom theming with `mermaid_params`

#### `sphinxcontrib.plantuml` - UML Diagrams

- **What**: UML diagram generation
- **Usage**: PlantUML syntax support
- **Config**: `plantuml_output_format = "svg"`

### 🔧 Utilities (Priority 51-60)

#### `sphinx_sitemap` - SEO Sitemap

- **What**: Generates XML sitemap for SEO
- **Usage**: Automatic sitemap.xml generation
- **Config**: `html_baseurl = "https://pyautodoc.readthedocs.io/"`

#### `sphinx_codeautolink` - Code Linking

- **What**: Automatic links from code examples
- **Usage**: Links code references to documentation
- **Config**: `codeautolink_autodoc_inject = True`

## 🎨 Intense Furo Theme Configuration

### Custom CSS Variables

The documentation uses custom CSS variables for intense branding:

```css
--color-brand-primary: #2563eb; /* Blue-600 */
--color-brand-content: #1d4ed8; /* Blue-700 */
--color-background-primary: #ffffff;
--color-background-secondary: #f8fafc; /* Slate-50 */
```

### Dark Mode Support

- Fixed code visibility issues
- Custom syntax highlighting colors
- Enhanced contrast for readability

### Interactive Elements

- Hover effects on cards and buttons
- Smooth animations and transitions
- Enhanced copy buttons
- Toggle functionality

## 🚀 Best Practices

### Extension Loading Order

1. **Core extensions first** (autodoc, autoapi)
2. **API enhancements** (pydantic, typehints)
3. **Design and content** (sphinx-design, tabs)
4. **Utilities last** (sitemap, codeautolink)

### Configuration Management

- **Hyper-organized**: Extensions grouped by priority
- **YAML + .env**: Planned for future modular config
- **Compatibility checking**: Extensions tested with Sphinx 8.2.3

### Performance Optimization

- **Priority loading**: Most important extensions loaded first
- **Selective enabling**: Only necessary extensions active
- **Caching**: Built-in Sphinx caching for faster rebuilds

## 📋 Available But Not Currently Active

These extensions are installed but commented out due to compatibility or configuration requirements:

- `sphinx_external_toc` - Requires `_toc.yml` file
- `sphinx_typesafe` - Compatibility issues with current setup
- Various specialized extensions for specific use cases

## 🔍 Testing Your Setup

To test extension functionality:

1. **Build documentation**: `sphinx-build docs/source docs/build/html`
2. **Check for errors**: Look for extension loading messages
3. **Test features**: Verify interactive elements work
4. **Check themes**: Toggle between light/dark modes

## 🎯 Current Extension Count

- **Active Extensions**: ~25 out of 150+ available
- **Core Functionality**: Fully operational
- **Enhanced Features**: Interactive and modern
- **Performance**: Optimized loading order

## 💡 Future Enhancements

Planned improvements:

- YAML-based extension configuration
- Environment-specific extension profiles
- A/B testing for different extension combinations
- Custom extension development for specialized needs

---

_This guide is automatically updated as extensions are added or modified._
