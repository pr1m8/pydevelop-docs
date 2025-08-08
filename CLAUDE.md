# PyAutoDoc - Multi-Version Documentation Testing Project

**Created:** 2025-01-08 15:45:00 UTC  
**Last Updated:** 2025-01-08 15:45:00 UTC  
**Status:** Active Development  
**Purpose:** Testing advanced Sphinx documentation features with multi-version, multi-theme support

---

## 📁 Project Structure

```
pyautodoc/
├── src/                           # Source code
│   ├── base/                      # Base models and configuration
│   │   ├── models.py             # Pydantic User model
│   │   ├── enums.py              # UserRole enum with enum-tools
│   │   └── config/               # Configuration management
│   │       ├── __init__.py       # Exports: settings, Environment, etc.
│   │       ├── system.py         # SystemConfig, Environment enum
│   │       └── settings.py       # Pydantic BaseSettings (NEW)
│   └── core/                     # Core business logic (ENHANCED)
│       ├── __init__.py           # Main exports
│       ├── exceptions.py         # Exception hierarchy (NEW)
│       ├── data_structures.py   # Dataclasses: Task, Point, Result (NEW)
│       ├── services.py           # Repository pattern, async services (NEW)
│       └── utils.py              # Utility functions, decorators (NEW)
├── docs/                         # Documentation system
│   ├── source/                   # Sphinx source
│   │   ├── conf.py              # Main Sphinx config
│   │   ├── conf_modular.py      # Modular config approach (NEW)
│   │   ├── conf_modules/        # Modular configuration (NEW)
│   │   │   ├── base.py          # Base Sphinx settings
│   │   │   ├── autoapi.py       # AutoAPI configuration
│   │   │   ├── pydantic.py      # Pydantic docs config
│   │   │   ├── enums.py         # Enum documentation
│   │   │   └── extensions.py    # Extension management
│   │   ├── _static/             # Static assets
│   │   │   └── css/
│   │   │       └── custom.css   # Custom styling (NEW)
│   │   ├── _templates/          # Jinja templates
│   │   ├── _autoapi_templates/  # AutoAPI templates
│   │   ├── modules/             # Module-specific docs (NEW)
│   │   ├── api/                 # API documentation (NEW)
│   │   ├── guides/              # User guides (NEW)
│   │   └── examples/            # Code examples (NEW)
│   ├── build/                   # Generated HTML
│   └── Makefile                 # Build commands
├── pyproject.toml               # Poetry dependencies
├── .gitignore                   # Git ignore rules (UPDATED)
├── README.md                    # Project overview
└── CLAUDE.md                    # This file - project notes
```

---

## 🎯 Current Objectives

### Phase 1: Enhanced Code Structure ✅ COMPLETED

- [x] @core-module: Created comprehensive core module with dataclasses, services, utils
- [x] @base-config: Enhanced configuration management with Pydantic BaseSettings
- [x] @documentation: Set up modular Sphinx configuration system
- [x] @dependencies: Added erdantic, sphinx-toolbox, enum-tools

### Phase 2: Multi-Version Documentation 🚧 IN PROGRESS

- [ ] @multiversion: Integrate sphinx-multiversion for Git-based versioning
- [ ] @themes: Test multiple themes (furo, pydata, rtd, book-theme)
- [ ] @automation: Set up GitHub Actions for multi-version builds
- [ ] @comparison: Create theme/version comparison dashboard

### Phase 3: Advanced Features 📋 PLANNED

- [ ] @cross-linking: Cross-version reference system
- [ ] @api-versioning: Document different API versions
- [ ] @feature-flags: Enable/disable features per version
- [ ] @performance: Optimize build times and output size

---

## 📝 Note-Taking System

### Timestamp Format

All notes use UTC timestamps in ISO format: `YYYY-MM-DD HH:MM:SS UTC`

### Area Tags (@-mentions)

- `@core-module` - Core business logic development
- `@base-config` - Configuration and settings
- `@documentation` - Sphinx documentation system
- `@multiversion` - Multi-version functionality
- `@themes` - Theme testing and customization
- `@dependencies` - Package management and dependencies
- `@automation` - CI/CD and build automation
- `@performance` - Performance optimization
- `@testing` - Testing and validation
- `@deployment` - Deployment and hosting

### File Tree Mirroring Notes

```
Notes mirror the repository structure:

src/core/ → @core-module notes
├── exceptions.py → @core-module @error-handling
├── data_structures.py → @core-module @dataclasses @typing
├── services.py → @core-module @async @repository-pattern
└── utils.py → @core-module @utilities @decorators

docs/ → @documentation notes
├── source/conf_modules/ → @documentation @modular-config
├── source/_static/ → @documentation @styling @themes
└── build/ → @documentation @output @automation

pyproject.toml → @dependencies @poetry
```

---

## 📋 Documentation Guide

### Building Documentation

```bash
# Standard build
cd docs && make html

# Clean build
cd docs && make clean html

# Multi-version build (once set up)
sphinx-multiversion source build/html

# Serve locally
cd docs/build/html && python -m http.server 8080
```

### Adding New Modules

1. **Create Python module** in `src/`
2. **Update `__init__.py`** with exports
3. **Add docstrings** following Google style
4. **Update conf_modules/** if special config needed
5. **Rebuild docs** to see AutoAPI generation

### Theme Testing Workflow

1. **Add theme to dependencies**: `poetry add sphinx-theme-name --group docs`
2. **Create theme config** in `conf_modules/`
3. **Test build** with new theme
4. **Compare output** and document differences
5. **Update styling** if needed in `_static/css/`

---

## 🔧 Dependencies Status

### Core Dependencies

- `pydantic` - Data validation and settings management
- `enum-tools` - Enhanced enum documentation ✅
- `sphinx-toolbox` - Required by enum-tools ✅
- `erdantic` - Entity relationship diagrams ✅

### Documentation Dependencies

- `sphinx` 8.2.3
- `sphinx-autoapi` - Automatic API documentation ✅
- `sphinxcontrib-autodoc-pydantic` - Pydantic model docs ✅
- `sphinx-multiversion` - Multi-version support 🚧 ADDING
- `furo` - Modern Sphinx theme ✅
- `myst-parser` - Markdown support ✅
- `sphinx-togglebutton` - Collapsible sections ✅
- `sphinx-sitemap` - SEO sitemap generation ✅

### Planned Additions

- `sphinx-book-theme` - Jupyter Book style theme
- `pydata-sphinx-theme` - PyData community theme
- `sphinx-rtd-theme` - Read the Docs theme
- Theme comparison and switching tools

---

## 📊 Testing Matrix

### Sphinx Features to Test

- [x] **AutoAPI**: Automatic API documentation generation
- [x] **Pydantic Models**: Model docs with JSON schema, validators
- [x] **Enums**: enum-tools integration with enhanced docs
- [x] **Dataclasses**: Field documentation and inheritance
- [x] **Type Hints**: Advanced typing with generics
- [x] **Inheritance Diagrams**: Graphviz class relationships
- [ ] **Multi-Version**: Git branch/tag based versions
- [ ] **Cross-References**: Inter-version linking
- [ ] **Custom Directives**: Domain-specific extensions

### Theme Compatibility Matrix

```
Feature              | Furo | PyData | RTD | Book
---------------------|------|--------|-----|------
Pydantic Models      | ✅   | ?      | ?   | ?
Enum Documentation   | ✅   | ?      | ?   | ?
Toggle Sections      | ✅   | ?      | ?   | ?
Dark Mode           | ✅   | ?      | ?   | ?
Mobile Responsive   | ✅   | ?      | ?   | ?
Multi-Version       | ?    | ?      | ?   | ?
```

---

## 🚀 Next Steps

### Immediate (Today)

1. @dependencies: Add sphinx-multiversion via poetry
2. @multiversion: Configure basic multi-version setup
3. @testing: Test current build with new dependencies
4. @documentation: Update configuration for multi-version

### Short Term (This Week)

1. @themes: Add and test additional themes
2. @automation: Set up GitHub Actions workflow
3. @comparison: Create side-by-side theme comparison
4. @performance: Measure build times and optimize

### Long Term (Next Weeks)

1. @features: Advanced Sphinx features testing
2. @deployment: Deploy to Read the Docs or GitHub Pages
3. @documentation: Comprehensive usage guide
4. @optimization: Performance tuning and best practices

---

## 💡 Ideas and Experiments

### Multi-Version Concepts

- **Branch-based versions**: `main`, `dev`, `stable`
- **Tag-based releases**: `v1.0.0`, `v0.9.0`, etc.
- **Feature branches**: Document experimental features
- **API versions**: Different API documentation per version

### Theme Switching Ideas

- **JavaScript theme switcher**: Live theme changes
- **Build matrix**: Generate all theme combinations
- **User preferences**: Remember theme choice
- **Responsive themes**: Adapt to device/screen size

### Advanced Documentation Features

- **Interactive examples**: Code execution in docs
- **API playground**: Test API calls in browser
- **Version migration guides**: Automated diff generation
- **Search across versions**: Unified search experience

---

## 📈 Metrics and Tracking

### Build Performance

- Build time per theme: TBD
- Total build time: TBD
- Output size per theme: TBD
- Memory usage: TBD

### Documentation Quality

- Coverage: AutoAPI covers all modules ✅
- Cross-references: Working internal links ✅
- External links: Intersphinx mappings ✅
- Mobile compatibility: Responsive themes ✅

---

## 🐛 Known Issues and Workarounds

### Current Issues

1. **@dependencies**: Toggle directive `:icon:` option not supported
   - **Status**: Fixed by removing unsupported option
   - **Workaround**: Use basic toggle without icons

2. **@documentation**: Multiple duplicate object warnings
   - **Status**: Known issue with enum-tools + autoapi
   - **Impact**: Warnings only, doesn't break build

3. **@styling**: Some Pydantic CSS not optimized for all themes
   - **Status**: Custom CSS added to compensate
   - **Solution**: Theme-specific CSS overrides

---

## 📚 References and Resources

### Documentation

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [sphinx-multiversion](https://holzhaus.github.io/sphinx-multiversion/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [enum-tools Documentation](https://enum-tools.readthedocs.io/)

### Themes

- [Furo Theme](https://pradyunsg.me/furo/)
- [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/)
- [Sphinx Book Theme](https://sphinx-book-theme.readthedocs.io/)
- [Sphinx Themes Gallery](https://sphinx-themes.org/)

### Tools

- [Poetry Documentation](https://python-poetry.org/docs/)
- [GitHub Actions for Sphinx](https://github.com/marketplace/actions/build-sphinx-documentation)

---

**@project-status**: Active development - multi-version integration in progress  
**@next-update**: After sphinx-multiversion configuration complete  
**@contact**: William R. Astley via Claude Code session
