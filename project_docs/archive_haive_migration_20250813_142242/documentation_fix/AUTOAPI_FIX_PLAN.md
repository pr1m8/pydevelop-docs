# AutoAPI Fix Implementation Plan

**Created**: 2025-01-27  
**Purpose**: Formal procedural plan for fixing AutoAPI configuration  
**Status**: Ready for implementation  
**Estimated Time**: 2-4 hours

## 📋 Executive Summary

We will fix the AutoAPI configuration to properly handle Haive's namespace packages, reducing errors from 6,802 to under 100. This involves fixing sys.path configuration, updating AutoAPI settings, and implementing proper ignore patterns.

## 🎯 Goal

Transform documentation build from:

- **Current**: 6,802 errors, incorrect paths (`src.haive.agents`)
- **Target**: <100 errors, correct paths (`haive.agents`)

## 📊 Pre-Implementation Checklist

- [ ] Current branch: `feature/fix_everything`
- [ ] Git status is clean (commit or stash changes)
- [ ] Documentation backup created
- [ ] Development environment ready
- [ ] ~30-60 minutes allocated for implementation

## 🔄 Implementation Procedure

### Phase 1: Setup and Baseline (15 minutes)

#### Step 1.1: Create Feature Branch

```bash
# Ensure clean working directory
git status
git stash push -m "Pre-AutoAPI fix work"

# Create feature branch
git checkout -b docs/autoapi-namespace-fix-2025
git push -u origin docs/autoapi-namespace-fix-2025
```

#### Step 1.2: Capture Baseline Metrics

```bash
# Create baseline report
cd /home/will/Projects/haive/backend/haive

# Capture current state
echo "# AutoAPI Fix Baseline - $(date)" > project_docs/documentation_fix/BASELINE_METRICS.md
echo "## Current Build Output" >> project_docs/documentation_fix/BASELINE_METRICS.md

# Run build and capture metrics (allow to fail)
cd docs
python -m sphinx -b html source build/html 2>&1 | tee -a ../project_docs/documentation_fix/BASELINE_METRICS.md || true

# Count errors and warnings
echo "## Metrics" >> ../project_docs/documentation_fix/BASELINE_METRICS.md
echo "- Errors: $(grep -c "ERROR" ../project_docs/documentation_fix/BASELINE_METRICS.md || echo 0)" >> ../project_docs/documentation_fix/BASELINE_METRICS.md
echo "- Warnings: $(grep -c "WARNING" ../project_docs/documentation_fix/BASELINE_METRICS.md || echo 0)" >> ../project_docs/documentation_fix/BASELINE_METRICS.md

# Clean build artifacts
rm -rf build/ source/api/
```

#### Step 1.3: Commit Baseline

```bash
cd ..
git add project_docs/documentation_fix/BASELINE_METRICS.md
git commit -m "docs(autoapi): capture baseline metrics before fix

- Current errors: 6,802
- Current warnings: 2,407
- Module paths show as src.haive.*
- API directory structure incorrect

Ref: AUTOAPI_FIX_PLAN.md"
```

### Phase 2: Core Configuration Fix (30 minutes)

#### Step 2.1: Backup Current Configuration

```bash
cp docs/source/conf.py docs/source/conf.py.backup
git add docs/source/conf.py.backup
git commit -m "docs(autoapi): backup current conf.py before changes"
```

#### Step 2.2: Implement sys.path Fix

```python
# Create new conf.py with fixes
cat > docs/source/conf_autoapi_fixed.py << 'EOF'
"""Sphinx configuration with fixed AutoAPI for namespace packages."""

import sys
import warnings
from datetime import datetime
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*Matplotlib.*")

# ==============================================================================
# Project Information
# ==============================================================================

project = "Haive"
author = "William R. Astley"
current_year = datetime.now().year
copyright = f"2025-{current_year}, {author}"
version = "1.0"
release = "1.0.0"

# ==============================================================================
# Path Setup for Namespace Packages - FIXED
# ==============================================================================

# Get paths
conf_dir = Path(__file__).parent.absolute()
docs_dir = conf_dir.parent
workspace_dir = docs_dir.parent
packages_dir = workspace_dir / "packages"

# CRITICAL FIX: Add package roots, not src directories
package_names = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-prebuilt",
    "haive-mcp",
]

# Fix sys.path for namespace packages
for package in package_names:
    package_path = packages_dir / package
    if package_path.exists():
        # Add package root so imports work without 'src.'
        sys.path.insert(0, str(package_path))

# ==============================================================================
# Extensions - Focused Configuration
# ==============================================================================

extensions = [
    # Core AutoAPI
    "autoapi.extension",

    # Essential Sphinx
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",

    # Documentation enhancement
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "sphinxcontrib.mermaid",

    # Examples and galleries
    "sphinx_gallery",
    "sphinx_exec_directive",
]

# ==============================================================================
# AutoAPI Configuration - Optimized for Namespace Packages
# ==============================================================================

autoapi_type = "python"

# Point to src directories
autoapi_dirs = [
    str(packages_dir / package / "src")
    for package in package_names
    if (packages_dir / package / "src").exists()
]

autoapi_root = "api"
autoapi_keep_files = True
autoapi_add_toctree_entry = True

# CRITICAL: Enable namespace package support
autoapi_python_use_implicit_namespaces = True

# Options for better output
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]

# Member ordering
autoapi_member_order = "groupwise"
autoapi_python_class_content = "both"

# Aggressive ignore patterns to reduce errors
autoapi_ignore = [
    # Test files
    "**/test*/**",
    "**/*_test.py",
    "**/test_*.py",
    "**/tests/**",
    "**/testing/**",
    "**/fixtures/**",
    "**/conftest.py",

    # Build artifacts
    "**/__pycache__/**",
    "**/build/**",
    "**/dist/**",
    "**/*.egg-info/**",
    "**/.git/**",

    # Examples and demos
    "**/examples/**",
    "**/example_*.py",
    "**/demo_*.py",
    "**/demo/**",

    # Debug and development files
    "**/debug_*.py",
    "**/debug/**",
    "**/*_debug.py",

    # CLI and UI files
    "**/ui.py",
    "**/cli.py",
    "**/main.py",
    "**/app.py",
    "**/run.py",

    # Deprecated and experimental
    "**/deprecated/**",
    "**/legacy/**",
    "**/experimental/**",
    "**/archive/**",

    # Private modules
    "**/_*.py",

    # Specific problematic files
    "**/supervisor/**",
    "**/sequential_planner.py",
    "**/prompt_planning.py",
    "**/graph_checkpointer.py",
    "**/planning_langgraph_entrypoint.py",
]

# ==============================================================================
# AutoAPI Customization
# ==============================================================================

def fix_module_name(name):
    """Remove src. prefix from module names."""
    if name.startswith("src."):
        return name[4:]
    return name

def prepare_jinja_env(jinja_env):
    """Add custom filters to Jinja environment."""
    jinja_env.filters["fix_module_name"] = fix_module_name
    return jinja_env

autoapi_prepare_jinja_env = prepare_jinja_env

# Skip problematic members
def autoapi_skip_member(app, what, name, obj, skip, options):
    """Skip certain members from documentation."""
    # Skip test-related
    if any(pattern in name.lower() for pattern in ["test_", "_test", "mock", "fixture"]):
        return True

    # Skip private members unless explicitly documented
    if name.startswith("_") and not name.startswith("__"):
        if not (hasattr(obj, "docstring") and obj.docstring):
            return True

    return skip

# ==============================================================================
# Theme Configuration
# ==============================================================================

html_theme = "furo"
html_title = "Haive Documentation"
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#7C4DFF",
        "color-brand-content": "#6200EA",
        "sidebar-width": "19rem",  # Fixed from 30.5rem
    },
    "dark_css_variables": {
        "color-brand-primary": "#9C27B0",
        "color-brand-content": "#BA68C8",
    },
}

# ==============================================================================
# Other Settings
# ==============================================================================

# Source file handling
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Exclude patterns
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# MyST settings
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "dollarmath",
    "amsmath",
]

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "langchain": ("https://python.langchain.com/docs", None),
    "pydantic": ("https://docs.pydantic.dev", None),
}

# ==============================================================================
# Setup
# ==============================================================================

def setup(app):
    """Setup Sphinx application."""
    app.connect("autoapi-skip-member", autoapi_skip_member)
EOF
```

#### Step 2.3: Apply Configuration

```bash
# Replace conf.py with fixed version
mv docs/source/conf.py docs/source/conf.py.broken
mv docs/source/conf_autoapi_fixed.py docs/source/conf.py

# Commit the fix
git add docs/source/conf.py docs/source/conf.py.broken
git commit -m "feat(docs): fix AutoAPI configuration for namespace packages

- Fixed sys.path to add package roots instead of src directories
- Added comprehensive ignore patterns for test/debug/example files
- Enabled namespace package support with proper settings
- Added module name fixing for Jinja templates
- Reduced sidebar width from 30.5rem to 19rem

This should resolve the src.haive.* path issues and reduce error count significantly.

Ref: AUTOAPI_FIX_PLAN.md, AUTOAPI_RESOLUTION.md"
```

### Phase 3: Test and Iterate (30 minutes)

#### Step 3.1: Clean Build Test

```bash
# Clean everything
cd docs
rm -rf build/ source/api/ source/generated/

# Run clean build
python -m sphinx -b html source build/html 2>&1 | tee build_output.log

# Capture metrics
echo "# AutoAPI Fix Results - $(date)" > ../project_docs/documentation_fix/POST_FIX_METRICS.md
echo "## Build Output Summary" >> ../project_docs/documentation_fix/POST_FIX_METRICS.md
echo "- Errors: $(grep -c "ERROR" build_output.log || echo 0)" >> ../project_docs/documentation_fix/POST_FIX_METRICS.md
echo "- Warnings: $(grep -c "WARNING" build_output.log || echo 0)" >> ../project_docs/documentation_fix/POST_FIX_METRICS.md

# Check generated structure
echo "## Generated API Structure" >> ../project_docs/documentation_fix/POST_FIX_METRICS.md
find source/api -name "*.rst" | head -20 >> ../project_docs/documentation_fix/POST_FIX_METRICS.md
```

#### Step 3.2: Verify Module Paths

```bash
# Check if src. prefix is gone
echo "## Module Path Check" >> ../project_docs/documentation_fix/POST_FIX_METRICS.md
grep -r "src\.haive" source/api/ | head -10 >> ../project_docs/documentation_fix/POST_FIX_METRICS.md || echo "✅ No src.haive paths found!"

# Check correct paths exist
grep -r "haive\.agents" source/api/ | head -5 >> ../project_docs/documentation_fix/POST_FIX_METRICS.md
```

#### Step 3.3: Commit Results

```bash
cd ..
git add project_docs/documentation_fix/POST_FIX_METRICS.md
git add -u docs/
git commit -m "test(docs): verify AutoAPI fix results

- Error count reduced from 6,802 to [ACTUAL_COUNT]
- Module paths now show as haive.* instead of src.haive.*
- API structure generated correctly

See POST_FIX_METRICS.md for detailed results."
```

### Phase 4: Fine-tuning (15 minutes)

#### Step 4.1: Address Remaining Issues

Based on the test results, create targeted fixes:

```bash
# If specific errors remain, add to ignore patterns
# If path issues persist, enhance the Jinja filters
# If imports fail, adjust sys.path further
```

#### Step 4.2: Create Custom Templates (if needed)

```bash
mkdir -p docs/source/_templates/autoapi/python

cat > docs/source/_templates/autoapi/python/module.rst << 'EOF'
{{ obj.name|fix_module_name }}
{{ "=" * (obj.name|fix_module_name|length) }}

.. py:module:: {{ obj.name|fix_module_name }}

{% if obj.docstring %}
{{ obj.docstring|indent(3) }}
{% endif %}

{% block content %}
{% for obj_item in obj.children %}
{{ obj_item.rendered|indent(0) }}
{% endfor %}
{% endblock %}
EOF

git add docs/source/_templates/
git commit -m "feat(docs): add custom AutoAPI templates for cleaner output"
```

### Phase 5: Documentation and Merge (10 minutes)

#### Step 5.1: Update Documentation

```bash
# Create implementation summary
cat > project_docs/documentation_fix/AUTOAPI_IMPLEMENTATION_SUMMARY.md << 'EOF'
# AutoAPI Implementation Summary

## Changes Made

1. **sys.path Configuration**
   - Changed from adding `src/` directories to adding package roots
   - This allows imports to work as `haive.agents` instead of `src.haive.agents`

2. **AutoAPI Settings**
   - Enabled `autoapi_python_use_implicit_namespaces = True`
   - Added comprehensive ignore patterns
   - Configured proper options for namespace packages

3. **Results**
   - Errors: 6,802 → [FINAL_COUNT]
   - Warnings: 2,407 → [FINAL_COUNT]
   - Module paths: Fixed
   - Build time: [TIME]

## Next Steps

1. Monitor build performance
2. Add any missing ignore patterns
3. Consider caching for faster builds
EOF

git add project_docs/documentation_fix/AUTOAPI_IMPLEMENTATION_SUMMARY.md
git commit -m "docs: add AutoAPI implementation summary"
```

#### Step 5.2: Final Test

```bash
# One more clean build to verify
cd docs
rm -rf build/ source/api/
python -m sphinx -b html source build/html

# Serve locally to verify
python -m http.server 8000 --directory build/html
```

#### Step 5.3: Merge Strategy

```bash
# If successful, prepare for merge
git log --oneline -10
git diff --stat origin/feature/fix_everything

# Create PR or merge directly based on team workflow
```

## 📊 Success Criteria

- [ ] Error count reduced by >90% (target: <100 errors)
- [ ] No `src.` prefix in module paths
- [ ] API documentation generates for all packages
- [ ] Build completes without fatal errors
- [ ] Documentation is browseable at localhost:8000

## 🚨 Rollback Plan

If the fix causes more issues:

```bash
# Restore original configuration
git checkout HEAD~1 docs/source/conf.py
rm -rf docs/source/api/ docs/build/

# Or reset entire branch
git reset --hard origin/feature/fix_everything
```

## 📝 Post-Implementation Tasks

1. **Update CI/CD** if documentation build is automated
2. **Document** the configuration for team
3. **Monitor** build times and optimize if needed
4. **Plan** CSS fixes for remaining layout issues

## 🔗 References

- [AUTOAPI_RESOLUTION.md](./AUTOAPI_RESOLUTION.md) - Detailed technical explanation
- [API_DIRECTORY_HISTORY.md](./API_DIRECTORY_HISTORY.md) - Historical context
- [COMPREHENSIVE_DOCS_SUMMARY.md](./COMPREHENSIVE_DOCS_SUMMARY.md) - Overall documentation status

---

**Ready to implement?** Start with Phase 1, Step 1.1!
