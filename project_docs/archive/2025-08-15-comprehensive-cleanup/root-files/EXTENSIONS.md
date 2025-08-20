# PyDevelop-Docs: Complete Extension Reference

PyDevelop-docs includes 40+ carefully selected and pre-configured Sphinx extensions. This document explains what each extension provides and how they work together.

## 🎯 Extension Categories

### Core Documentation (Priority 1-10)

These are the foundational extensions that every documentation project needs:

#### `sphinx.ext.autodoc`

**Automatic documentation from docstrings**

- Extracts documentation from Python docstrings
- Supports classes, functions, modules, and attributes
- Pre-configured for optimal output

#### `sphinx.ext.napoleon`

**Google/NumPy style docstrings**

- Converts Google and NumPy style docstrings to reStructuredText
- Makes docstrings more readable in code
- Supports all major docstring sections (Args, Returns, Raises, etc.)

#### `sphinx.ext.viewcode`

**Source code links**

- Adds "[source]" links to generated documentation
- Links directly to the source code on your repository
- Helps developers understand implementation details

#### `sphinx.ext.intersphinx`

**Cross-project references**

- Links to external documentation (Python standard library, etc.)
- Pre-configured with common Python project mappings
- Enables rich cross-references between projects

### API Documentation (Priority 11-20)

Advanced API documentation with automatic generation:

#### `autoapi.extension`

**Automatic API documentation**

- Generates complete API documentation automatically
- Works without importing your code (safer than autodoc)
- Creates organized module/class hierarchies
- Pre-configured with sensible defaults

#### `sphinx_autodoc_typehints`

**Type hint support**

- Beautiful rendering of Python type hints
- Supports generics, unions, and complex types
- Integrates seamlessly with autodoc

#### `sphinxcontrib.autodoc_pydantic`

**Pydantic model documentation**

- Special support for Pydantic models
- Shows JSON schema, field types, and validators
- Renders model inheritance beautifully

### Content & Design (Priority 21-30)

Rich content features and beautiful design:

#### `myst_parser`

**Markdown support**

- Write documentation in Markdown or reStructuredText
- Supports advanced features like cross-references in Markdown
- MyST (Markedly Structured Text) with Sphinx directives

#### `sphinx_design`

**Bootstrap-style components**

- Cards, grids, badges, buttons, and more
- Responsive design components
- Professional-looking layouts

#### `sphinx_togglebutton`

**Collapsible sections**

- Add expandable/collapsible content sections
- Great for optional details or advanced topics
- Clean, accessible implementation

#### `sphinx_copybutton`

**Copy code buttons**

- One-click copying for all code blocks
- Automatic prompt removal (>>> and $)
- Essential for code-heavy documentation

#### `sphinx_tabs.tabs`

**Tabbed content**

- Organize related content in tabs
- Perfect for multi-language examples
- Supports nested tabs

### Execution & Testing (Priority 31-40)

Execute code and show real output:

#### `sphinxcontrib.programoutput`

**Execute shell commands**

- Run shell commands and include output in docs
- Great for CLI tool documentation
- Always shows current, accurate output

### Diagrams & Visualization (Priority 41-50)

Rich visual content:

#### `sphinx.ext.graphviz`

**Graphviz diagrams**

- Create diagrams using Graphviz DOT language
- Inheritance diagrams, flowcharts, network graphs
- Vector graphics that scale perfectly

#### `sphinxcontrib.mermaid`

**Mermaid diagrams**

- Modern diagram syntax (flowcharts, sequence diagrams, etc.)
- Popular, easy-to-learn syntax
- Great for architecture and process diagrams

#### `sphinxcontrib.plantuml`

**PlantUML diagrams**

- UML diagrams with simple text syntax
- Class diagrams, sequence diagrams, activity diagrams
- Professional UML standard compliance

### Utilities & SEO (Priority 51-60)

Essential utilities for professional documentation:

#### `sphinx_sitemap`

**SEO sitemap generation**

- Generates XML sitemaps for search engines
- Improves documentation discoverability
- Essential for public documentation

#### `sphinx_codeautolink`

**Automatic code linking**

- Automatically links code elements to their documentation
- Works across modules and packages
- Reduces manual cross-referencing work

### Navigation & UX (Priority 61-70)

Enhanced navigation and user experience:

#### `sphinx_treeview`

**Enhanced table of contents**

- Interactive, collapsible TOC navigation
- Better than default Sphinx TOC
- Improves large documentation navigation

### Advanced Features (Priority 71-80)

Professional documentation features:

#### `sphinx_toggleprompt`

**Toggle command prompts**

- Hide/show command prompts in code blocks
- Clean presentation for copy-paste
- User-controlled visibility

#### `sphinx_prompt`

**Enhanced prompts**

- Beautiful command-line prompt styling
- Supports different shell types
- Consistent prompt presentation

#### `sphinx_last_updated_by_git`

**Git-based update tracking**

- Shows when each page was last updated
- Uses Git history automatically
- Helps users understand content freshness

#### `sphinx_inlinecode`

**Enhanced inline code**

- Better styling for inline code snippets
- Syntax highlighting in inline code
- Improved readability

#### `sphinx_icontract`

**Design by contract**

- Documents function contracts (preconditions, postconditions)
- Integrates with icontract library
- Advanced API documentation

#### `sphinx_tippy`

**Rich hover tooltips**

- Interactive tooltips with rich content
- Enhances cross-references
- Better user experience for complex docs

### Documentation Tools (Priority 81-90)

Professional documentation management:

#### `sphinx_comments`

**Comment system**

- Adds comment functionality to documentation
- Multiple comment providers supported
- Community engagement features

#### `sphinx_contributors`

**Contributor recognition**

- Shows documentation contributors
- Integrates with Git history
- Recognizes documentation authors

#### `sphinx_issues`

**GitHub issue integration**

- Links to GitHub issues and pull requests
- Automatic issue linking
- Keeps docs connected to development

#### `sphinx_needs`

**Requirements tracking**

- Track requirements, specifications, and test cases
- Traceability matrices
- Professional requirements documentation

#### `sphinxarg.ext`

**Argument parser documentation**

- Documents argparse-based CLIs automatically
- Extracts help text and options
- Essential for CLI tool documentation

#### `notfound.extension`

**Custom 404 pages**

- Beautiful, helpful 404 error pages
- Better user experience for broken links
- Customizable error messaging

#### `sphinx_reredirects`

**URL redirects**

- Handle URL changes gracefully
- Maintain old link compatibility
- SEO-friendly redirects

#### `sphinxext.rediraffe`

**Advanced redirects**

- Automatic redirect detection
- Handles documentation restructuring
- Prevents broken links

#### `sphinx_git`

**Git integration**

- Shows Git changelog in documentation
- Tracks documentation changes
- Integrates development history

#### `sphinx_changelog`

**Changelog generation**

- Automatic changelog from Git or manual entries
- Professional change tracking
- Release note generation

#### `sphinx_debuginfo`

**Debug information**

- Shows build performance information
- Helps optimize documentation builds
- Development and debugging tool

#### `sphinxext.opengraph`

**Social media previews**

- Generates Open Graph tags for social sharing
- Beautiful previews on Twitter, LinkedIn, etc.
- Professional social media presence

#### `sphinx_tags`

**Content tagging**

- Tag documentation content by topic
- Create tag-based navigation
- Organize large documentation projects

#### `sphinx_favicon`

**Favicon support**

- Adds favicons to documentation
- Multiple favicon sizes and formats
- Professional branding

#### `sphinx_combine`

**Document combination**

- Combine multiple documents
- Create unified views
- Advanced document organization

## 🔧 How Extensions Work Together

PyDevelop-docs carefully configures all extensions to work harmoniously:

### AutoAPI + Pydantic

- AutoAPI discovers your Pydantic models
- autodoc_pydantic renders them beautifully
- Type hints show field types clearly

### Mermaid + Copy Buttons

- Mermaid creates diagrams from text
- Copy buttons let users copy diagram source
- Perfect for reproducible diagrams

### Git Integration

- sphinx_git tracks file changes
- sphinx_last_updated_by_git shows update times
- sphinx_changelog generates release notes
- Complete development integration

### SEO & Social

- sphinx_sitemap creates search engine sitemaps
- sphinxext.opengraph adds social media previews
- sphinx_favicon adds professional branding
- Complete web presence optimization

## 🎨 Pre-configured Themes

### Furo Theme

The default theme includes:

- **Dark mode toggle**: Automatic system preference detection
- **Responsive design**: Perfect on mobile and desktop
- **Customizable colors**: Easy brand color integration
- **Professional typography**: Optimized for readability
- **Sidebar navigation**: Collapsible, searchable navigation

### Theme Customization

All themes are pre-configured with:

- Custom CSS for better AutoAPI rendering
- Enhanced code block styling
- Professional color schemes
- Optimized mobile layouts

## 🚀 Zero Configuration

All 40+ extensions are:

- **Pre-configured** with optimal settings
- **Tested together** for compatibility
- **Optimized** for performance
- **Documented** with clear examples

You get professional documentation features without any configuration complexity.

## 📚 Learn More

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Furo Theme](https://pradyunsg.me/furo/)
- [MyST Parser](https://myst-parser.readthedocs.io/)
- [AutoAPI](https://sphinx-autoapi.readthedocs.io/)

---

**The beauty of PyDevelop-docs is that you don't need to understand all these extensions - they just work together to create beautiful documentation for your Python projects.**
