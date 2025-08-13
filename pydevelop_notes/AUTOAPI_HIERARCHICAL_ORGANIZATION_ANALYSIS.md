# AutoAPI Hierarchical Organization Analysis

**Created**: 2025-08-13
**Purpose**: Comprehensive analysis of AutoAPI flattening issue and solutions for nested/recursive module organization
**Status**: Active Research
**Related**: @project_docs/pydevelop_docs/COMPREHENSIVE_DOCUMENTATION_ISSUES_20250813.md Issue #4

## Problem Statement

AutoAPI is generating flat, alphabetical listings of all classes/functions instead of maintaining the logical hierarchical package structure. For the Haive monorepo with 7 packages, this creates an unusable flat list of 200+ items rather than organized package-based navigation.

### Current Flat Structure Issue

```
API Reference (Current - BAD)
├── All Classes (A-Z)
    ├── Agent
    ├── AugLLMConfig
    ├── BaseModel
    ├── ExecutionMode
    ├── MultiAgent
    ├── ReactAgent
    └── [190+ more classes in flat alphabetical list]
```

### Desired Hierarchical Structure

```
API Reference (Desired - GOOD)
├── haive-core
│   ├── Engine
│   │   ├── AugLLMConfig
│   │   └── BaseAgent
│   ├── Schema
│   │   ├── StateSchema
│   │   └── MetaStateSchema
│   └── Tools
├── haive-agents
│   ├── Simple Agents
│   │   └── SimpleAgent
│   ├── React Agents
│   │   └── ReactAgent
│   └── Multi Agents
│       └── MultiAgent
└── haive-tools
    ├── Calculator
    └── SearchTool
```

## Root Cause Analysis

### 1. AutoAPI Default Behavior

- **Flat-first approach**: AutoAPI's default templates prioritize alphabetical listing over hierarchical organization
- **Template-driven**: The structure is controlled by Jinja2 templates in `_autoapi_templates/`
- **Single-page philosophy**: Default `autoapi_own_page_level` setting determines granularity

### 2. Current Configuration Issues

From our research of Haive's documentation dependencies in `pyproject.toml`:

```toml
[tool.poetry.group.docs.dependencies]
sphinx-autoapi = "^3.6.0"           # Latest version
furo = "^2024.8.6"                  # Modern theme but needs toc config
sphinx-copybutton = "^0.5.2"
sphinx-togglebutton = "^0.3.2"
# 40+ other sphinx extensions...
```

**Missing key configurations**:

- No `autoapi_own_page_level` setting
- No custom `autoapi_template_dir`
- No Furo-specific TOC configuration
- No `autoapi_options` for controlling display

## Solutions Research

### 1. AutoAPI Configuration Options

#### `autoapi_own_page_level` Setting

Controls granularity of page generation (descending hierarchy):

- **`"module"`**: Only packages/modules get pages (classes inline) - **RECOMMENDED**
- **`"class"`**: Modules and classes get pages (functions inline) - _Default_
- **`"function"`**: Everything gets pages (most granular)
- **`"attribute"`**: Everything including attributes gets pages (too granular)

```python
# In conf.py - RECOMMENDED FIX
autoapi_own_page_level = 'module'  # Keep hierarchy, reduce page explosion
```

#### `autoapi_options` Setting

Controls what gets documented and how:

```python
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',  # KEY: Shows module-level organization
    'special-members',
]
```

#### Template Directory Customization

```python
autoapi_template_dir = '_autoapi_templates'
autoapi_add_toctree_entry = True  # Ensure proper TOC integration
```

### 2. Furo Theme TOC Configuration

Furo theme supports specific TOC options for better navigation:

```python
html_theme_options = {
    "navigation_with_keys": True,
    "sidebar_hide_name": True,
    "navigation_depth": 4,  # Allow 4 levels of nesting
    "collapse_navigation": False,  # Keep sections expanded
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,  # Show all headers
}
```

### 3. Custom AutoAPI Templates

**Key template files to customize**:

- `python/module.rst` - Controls module page layout
- `python/index.rst` - Controls main API index structure
- `python/class.rst` - Controls class documentation format

**Template strategy**:

1. Copy default templates from `autoapi/templates/` to local `_autoapi_templates/`
2. Modify `index.rst` to group by package instead of alphabetical
3. Enhance `module.rst` to show clear hierarchical structure

### 4. Package-Based Organization Strategy

Instead of flat alphabetical, organize by logical packages:

```rst
# In custom python/index.rst template
API Reference
=============

Core Framework (haive-core)
---------------------------

.. toctree::
   :maxdepth: 2

   /autoapi/haive/core/index

Agent Implementations (haive-agents)
-----------------------------------

.. toctree::
   :maxdepth: 2

   /autoapi/haive/agents/index

Tools & Utilities (haive-tools)
------------------------------

.. toctree::
   :maxdepth: 2

   /autoapi/haive/tools/index
```

## Implementation Plan

### Phase 1: Quick Fix (Configuration)

**Target**: Fix the worst flattening with minimal changes

1. **Update AutoAPI configuration in conf.py**:

```python
# Hierarchical organization settings
autoapi_own_page_level = 'module'  # Keep classes with their modules
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',  # KEY for organization
]

# Furo theme TOC settings
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "titles_only": False,
}
```

2. **Test the impact**: Check if this alone improves the structure

### Phase 2: Template Customization (Major Fix)

**Target**: Complete hierarchical reorganization

1. **Create custom templates**:
   - Copy AutoAPI's default templates to `_autoapi_templates/`
   - Modify `python/index.rst` for package-based organization
   - Update `python/module.rst` for better module display

2. **Package grouping logic**:
   - Group modules by package (haive-core, haive-agents, etc.)
   - Add package-level descriptions
   - Maintain alphabetical within packages

3. **Cross-references**:
   - Add inter-package linking
   - Maintain inheritance diagrams
   - Preserve search functionality

### Phase 3: Integration with pydevelop-docs

**Target**: Make this fix available to all projects using pydevelop-docs

1. **Add configuration options to pydevelop-docs**:

```bash
pydevelop-docs init --with-hierarchical-api --api-page-level module
```

2. **Template distribution**:
   - Include custom templates in pydevelop-docs package
   - Make them configurable per project type (monorepo vs single package)

3. **Auto-detection**:
   - Detect monorepo structure (packages/ directory)
   - Auto-configure hierarchical organization
   - Provide sensible defaults per project type

## Technical Details

### AutoAPI Template Variables Available

In custom templates, these variables are available:

- `packages` - List of all packages
- `modules` - List of all modules
- `pkg_name` - Current package name
- `obj.name` - Object name
- `obj.children` - Child objects
- `obj.inherited_members` - Inherited items

### Furo Theme Integration

Furo's sidebar can be enhanced to work better with hierarchical APIs:

- Use `navigation_depth` to show nested structure
- Leverage `collapse_navigation` for package sections
- Integrate with `sphinx-copybutton` for code examples

### Performance Considerations

**Current flat structure**: Generates ~80 individual `.rst` files for haive-agents alone
**Hierarchical structure**: Could reduce to ~20 module-level files with better organization
**Build time**: Should improve due to fewer files and better caching

## Testing Strategy

### 1. Haive Repository Testing

- Test configuration changes on current Haive docs
- Measure before/after navigation usability
- Verify all cross-references still work
- Check search functionality preservation

### 2. pydevelop-docs Integration Testing

- Test with monorepo structure (Haive)
- Test with single-package structure
- Verify template customization works
- Test CLI options for hierarchical organization

### 3. Multi-Theme Compatibility

- Test with Furo (primary)
- Test with PyData theme
- Test with RTD theme
- Ensure templates work across themes

## Success Metrics

### 1. Navigation Improvement

- **Before**: 200+ items in flat alphabetical list
- **After**: ~7 package sections with logical sub-organization
- **Target**: <3 clicks to find any API item

### 2. Build Performance

- **Before**: 80+ individual files for haive-agents
- **After**: ~20 module-level files
- **Target**: 20% reduction in build time

### 3. Documentation Quality

- Maintain all current functionality (inheritance, search, cross-refs)
- Improve discoverability of related functionality
- Better mobile navigation experience

## Related Resources

### AutoAPI Documentation

- [Configuration Options](https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html)
- [Templates Reference](https://sphinx-autoapi.readthedocs.io/en/latest/reference/templates.html)
- [How-to Guides](https://sphinx-autoapi.readthedocs.io/en/latest/how_to.html)

### Furo Theme

- [TOC Customization](https://github.com/pradyunsg/furo/blob/main/docs/customisation/toc.md)
- [Navigation Configuration](https://pradyunsg.me/furo/customisation/sidebar/)

### Related Issues

- [AutoAPI TOC Ordering Issue](https://github.com/readthedocs/sphinx-autoapi/issues/226)
- [Classes Having Own Pages](https://github.com/readthedocs/sphinx-autoapi/issues/226)

## Implementation Status

- [x] **Research completed**: Understanding of root cause and solutions
- [x] **Dependencies audited**: Confirmed all needed packages available in Haive
- [x] **Phase 1 testing**: ✅ **SUCCESSFUL** - Configuration fix validated in test environment
- [ ] **Template development**: 📅 **OPTIONAL** - Phase 1 sufficient for most cases
- [ ] **pydevelop-docs integration**: CLI options and auto-detection
- [ ] **Full deployment**: Updated documentation across all Haive packages

---

## ✅ PHASE 1 VALIDATION RESULTS

**Test Environment**: `/home/will/Projects/haive/backend/haive/test-haive-template/`

### Configuration Applied:

```python
# KEY FIX: Change page level from 'class' to 'module'
autoapi_own_page_level = "module"

# Enhanced options for better organization
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",  # KEY: Shows module-level organization
]

# Furo theme configuration for hierarchical navigation
html_theme_options = {
    "navigation_depth": 4,  # Allow 4 levels of nesting
    "collapse_navigation": False,  # Keep sections expanded by default
    "sticky_navigation": True,
    "titles_only": False,  # Show all headers, not just titles
}
```

### Results Achieved:

**🔴 BEFORE (Flat Structure):**

- 25 individual class pages in alphabetical order
- No logical grouping or hierarchy
- Unusable navigation for large projects

**✅ AFTER (Hierarchical Structure):**

```
API Reference
└── testhaive
    ├── testhaive.agents
    │   ├── testhaive.agents.react
    │   │   └── testhaive.agents.react.agent (ReactAgent, ReactConfig, ThoughtProcess, ActionPlan)
    │   └── testhaive.agents.simple
    │       └── testhaive.agents.simple.agent (SimpleAgent, SimpleAgentConfig)
    ├── testhaive.core
    │   ├── testhaive.core.engine
    │   │   └── testhaive.core.engine.config (TestLLMConfig, EngineMode)
    │   ├── testhaive.core.schema
    │   │   ├── testhaive.core.schema.base (BaseSchema, ValidationMixin, etc.)
    │   │   ├── testhaive.core.schema.meta (MetaStateSchema, StateProjection)
    │   │   └── testhaive.core.schema.state (AgentState, WorkflowState, etc.)
    │   └── testhaive.core.tools
    │       └── testhaive.core.tools.base (BaseTool)
    └── testhaive.tools
```

### Key Improvements:

- **Reduced from 25 individual pages to ~8 organized module pages**
- **4-level hierarchical navigation** (package → subpackage → module → classes)
- **Logical grouping** by functionality and architecture
- **Collapsible navigation** with Furo theme integration
- **All classes still documented** - just better organized

### File to View Results:

```
file:///home/will/Projects/haive/backend/haive/test-haive-template/docs/build/autoapi/index.html
```

**Next Steps**:

1. ✅ **COMPLETE**: Phase 1 configuration validated successfully
2. 🔄 **CURRENT**: Apply configuration to main Haive documentation
3. 📅 **OPTIONAL**: Custom templates for advanced package-based grouping

**Cross-References**:

- @project_docs/pydevelop_docs/COMPREHENSIVE_DOCUMENTATION_ISSUES_20250813.md - Issue #4: Flat API Reference
- @project_docs/pydevelop_docs/ - Root documentation analysis directory
