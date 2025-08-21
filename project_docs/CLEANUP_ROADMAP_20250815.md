# Pydvlppy Cleanup Roadmap

**Created**: 2025-08-15  
**Purpose**: Systematic cleanup plan for pydvlppy package
**Priority**: Critical - Blocking haive-mcp documentation fixes

## 🎯 Cleanup Objectives

1. **Fix immediate issues** - Get haive-mcp documentation working
2. **Reduce complexity** - Eliminate unnecessary cruft and duplication
3. **Improve maintainability** - Clear structure and documentation
4. **Establish standards** - Guidelines for future development

## 📋 Phase 1: Emergency Fixes (TODAY)

### 🚨 Critical Issues to Fix Immediately

#### 1.1 Template System Fix

**Problem**: Broken AutoAPI templates generating invalid directives
**Solution**: Replace with working templates from test project

```bash
# Backup broken templates
mv src/pydevelop_docs/templates/_autoapi_templates src/pydevelop_docs/templates/_autoapi_templates_BROKEN_BACKUP

# Copy working templates
cp -r test-projects/test-haive-template/docs/source/_autoapi_templates \
      src/pydevelop_docs/templates/

# Remove redundant backup
rm -rf src/pydevelop_docs/templates/_autoapi_templates_complex_backup
```

#### 1.2 CSS Dark Mode Fix

**Problem**: White-on-white text in dark mode
**Solution**: Update CSS rules in templates/static/css/furo-intense.css

#### 1.3 Test Emergency Fix

**Target**: Get haive-mcp documentation building with functions visible
**Validation**: All 9 functions in comprehensive_mcp_web.py should appear

### 📊 Phase 1 Success Metrics

- [ ] haive-mcp functions visible in documentation
- [ ] Dark mode text readable
- [ ] Hierarchical navigation working
- [ ] Build completes without critical errors

---

## 📋 Phase 2: Structure Cleanup (NEXT WEEK)

### 2.1 Documentation Consolidation

#### Current State: 132+ scattered documentation files

```
├── project_docs/ (50+ files)
├── docs/ (40+ files)
├── pydevelop_notes/ (5+ files)
└── Various README files
```

#### Cleanup Plan:

```bash
# Create new organized structure
mkdir -p docs/
├── user-guide/          # End-user documentation
├── developer-guide/     # Development documentation
├── reference/           # API reference
├── troubleshooting/     # Common issues and fixes
└── archive/             # Historical/outdated docs

# Consolidate scattered docs
# Keep only relevant, up-to-date information
# Archive or delete outdated analysis files
```

### 2.2 Configuration Cleanup

#### Current State: 5+ conf.py files

```
├── docs/source/conf.py
├── docs/source/conf_clean.py
├── docs/source/conf_generated.py
├── docs/source/conf_modular.py
├── docs/source/conf_test.py
└── templates/central_hub_conf.py
```

#### Cleanup Plan:

```bash
# Keep only essential configs
├── docs/source/conf.py           # Main documentation config
└── src/pydevelop_docs/config.py  # Package configuration

# Remove experimental/test configs
rm docs/source/conf_*.py
```

### 2.3 Template Structure Simplification

#### Current State: Complex inheritance system

```
_autoapi_templates/python/
├── _base/           # Base templates (broken)
├── _components/     # Component templates
├── _filters/        # Python filters
├── _macros/         # Jinja2 macros
└── *.rst            # Final templates
```

#### Cleanup Plan:

```bash
# Simplify to flat structure
_autoapi_templates/python/
├── attribute.rst    # Simple, working templates
├── class.rst        # Based on AutoAPI defaults
├── function.rst     # Minimal customization
├── index.rst        # Only necessary changes
├── method.rst
└── module.rst
```

---

## 📋 Phase 3: Quality & Standards (FOLLOWING WEEK)

### 3.1 Testing Framework

#### Establish Template Testing

```python
# tests/test_templates.py
def test_autoapi_templates_generate_valid_rst():
    """Test that templates generate valid RST syntax."""

def test_functions_appear_in_documentation():
    """Test that functions are visible in built docs."""

def test_dark_mode_css_rules():
    """Test that dark mode CSS provides proper contrast."""
```

### 3.2 Documentation Standards

#### Create Clear Guidelines

```markdown
# Template Customization Guide

1. Start with default AutoAPI templates
2. Make minimal, tested changes
3. Document all customizations
4. Test with real projects

# CSS Customization Guide

1. Use CSS variables for theming
2. Test in both light and dark modes
3. Target specific AutoAPI elements
4. Maintain accessibility standards
```

### 3.3 Build System Simplification

#### Standardize Build Process

```bash
# Single build command
pydvlppy build

# Clear build options
pydvlppy build --clean    # Clean build
pydvlppy build --watch    # Watch mode
pydvlppy build --serve    # Serve locally
```

---

## 📋 Phase 4: Long-term Maintenance (ONGOING)

### 4.1 Package Structure Reorganization

#### Target Structure:

```
src/pydevelop_docs/
├── __init__.py
├── cli.py              # Command-line interface
├── config.py           # Configuration management
├── builders/           # Build system
│   ├── sphinx.py       # Sphinx builder
│   └── templates.py    # Template management
├── templates/          # Template files (CLEAN)
│   ├── _autoapi_templates/  # AutoAPI templates only
│   └── static/              # CSS/JS assets only
└── utils/              # Utility functions
    ├── css.py          # CSS processing
    └── validation.py   # Template validation
```

### 4.2 Maintenance Guidelines

#### Regular Cleanup Tasks

```bash
# Monthly cleanup
- Review and archive old documentation
- Update templates with upstream AutoAPI changes
- Test with latest Sphinx/AutoAPI versions
- Check CSS compatibility with theme updates

# Before releases
- Run full test suite
- Validate generated documentation
- Check accessibility compliance
- Update documentation
```

## 🚨 Risk Management

### High-Risk Areas

1. **Template Changes**: Can break all documentation generation
2. **CSS Modifications**: Can break theming across projects
3. **Config Changes**: Can break builds or introduce conflicts
4. **File Deletion**: Risk of removing still-needed functionality

### Mitigation Strategies

```bash
# Always backup before changes
cp -r templates/ templates.backup.$(date +%Y%m%d)

# Test changes in isolated environment
cp -r test-projects/test-haive-template test-validation
# Make changes, test, validate

# Staged rollout
# 1. Test in test-haive-template
# 2. Test in haive-mcp
# 3. Test in full haive documentation
# 4. Deploy to other projects
```

## 📊 Success Metrics

### Phase 1 (Emergency)

- [ ] haive-mcp documentation functions visible
- [ ] Dark mode readable
- [ ] Build errors < 10 warnings

### Phase 2 (Cleanup)

- [ ] Documentation files reduced by 60%
- [ ] Configuration files reduced to 2
- [ ] Template complexity reduced by 80%

### Phase 3 (Quality)

- [ ] 90%+ template test coverage
- [ ] Clear documentation standards
- [ ] Simplified build process

### Phase 4 (Maintenance)

- [ ] Clean package structure
- [ ] Regular maintenance schedule
- [ ] Clear contribution guidelines

---

## 🚀 Immediate Next Steps

1. **Execute Phase 1.1** - Fix templates immediately
2. **Test on haive-mcp** - Validate functions appear
3. **Commit fixes** - Secure working state
4. **Plan Phase 2** - Schedule cleanup activities

**Ready to start cleanup? Let's begin with Phase 1.1 template fix.**
