# PyDevelop-Docs Project Documentation

**Last Updated**: 2025-08-13
**Purpose**: Central hub for all PyDevelop-Docs documentation

## 📁 Documentation Structure

```
project_docs/
├── README.md                                    # This file - documentation hub
├── issues/                                      # Issue tracking and analysis
│   ├── COMPREHENSIVE_DOCUMENTATION_ISSUES_20250813.md  # Master issue list
│   └── issue_06_autoapi_jinja2_templates.md   # Specific issue docs
├── archive_haive_migration_20250813_142242/    # Migrated from Haive root
│   ├── AUTOAPI_HIERARCHICAL_ORGANIZATION_ANALYSIS.md
│   ├── CSS_FILES_COMPARISON_20250813.md
│   └── PyDevelop_Documentation_Plan_20250813.md
├── testing/                                     # Testing results and progress
│   └── TESTING_PROGRESS_SUMMARY_20250813.md
└── architecture/                                # Architecture decisions
    └── CLI_CONFIG_CONSOLIDATION.md
```

## 🎯 Current Status

### ✅ Completed

1. **CLI Consolidation** - CLI now uses shared config module
2. **Hierarchical API Fix** - Recursive nested structure working
3. **CSS White-on-White Fix** - Dark mode fixes implemented
4. **Extension Loading Order** - Fixed sphinx_toolbox order

### 🔄 In Progress

- Issue #6: Custom Jinja2 templates for AutoAPI

### 📅 Pending

- Issue #1: Fix broken TOC references
- Issue #3: Add getting started content
- Issues #5-12: Various UI/UX improvements

## 📋 Key Documents

### For Understanding Issues

- [Comprehensive Issues List](issues/COMPREHENSIVE_DOCUMENTATION_ISSUES_20250813.md) - All 12 issues with priorities
- [AutoAPI Hierarchical Analysis](archive_haive_migration_20250813_142242/AUTOAPI_HIERARCHICAL_ORGANIZATION_ANALYSIS.md) - Deep dive into Issue #4

### For Implementation

- [CLI Config Consolidation](architecture/CLI_CONFIG_CONSOLIDATION.md) - How we unified configuration
- [Testing Progress](testing/TESTING_PROGRESS_SUMMARY_20250813.md) - What's been tested

### For Reference

- [CSS Comparison](archive_haive_migration_20250813_142242/CSS_FILES_COMPARISON_20250813.md) - CSS consolidation analysis
- [PyDevelop Plan](archive_haive_migration_20250813_142242/PyDevelop_Documentation_Plan_20250813.md) - Original vision

## 🔗 Quick Links

- **Main CLAUDE.md**: `/CLAUDE.md` - Project memory hub
- **Source Code**: `/src/pydevelop_docs/`
- **Test Project**: `/test-projects/test-haive-template/`
- **Templates**: `/src/pydevelop_docs/templates/`
