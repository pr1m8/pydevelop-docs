# Documentation Tools Guide - Haive Project

**Created**: 2025-07-28
**Purpose**: Comprehensive guide for using documentation tools consistently

## 🛠️ Available Tools Overview

### Code Formatters (We Have)

- **ruff** (^0.11.6) - Fast, all-in-one linter/formatter configured for Google style
- **yapf** (^0.43.0) - Google's formatter (but we have empty .style.yapf)
- **docformatter** (^1.7.7) - Specialized for docstring formatting

### Documentation Validators

- **pydocstyle** (^6.3.0) - Checks Google-style compliance
- **darglint** (^1.8.1) - Validates Args/Returns match actual code
- **interrogate** (^1.5.0) - Measures docstring coverage

### Other Relevant Tools

- **autopep8** (^2.3.2) - PEP 8 formatting (NOT installed but mentioned)
- **black** (^25.1.0) - Opinionated formatter (NOT installed)
- **autoflake** (^2.3.1) - Remove unused imports
- **monkeytype** (^23.3.0) - Generate type annotations from runtime

## 📋 Tool Usage Matrix

| Task                      | Primary Tool   | Alternative                 | When to Use                            |
| ------------------------- | -------------- | --------------------------- | -------------------------------------- |
| **Format docstrings**     | `docformatter` | `ruff format`               | Always use docformatter for docstrings |
| **Check Google style**    | `pydocstyle`   | `ruff check --select=D`     | Use pydocstyle for detailed reports    |
| **Validate Args/Returns** | `darglint`     | `pydoclint` (not installed) | Use darglint for semantic validation   |
| **Measure coverage**      | `interrogate`  | -                           | Always use for coverage metrics        |
| **Format code**           | `ruff format`  | `yapf`                      | Use ruff (it's configured)             |
| **Remove unused imports** | `autoflake`    | `ruff check --fix`          | Use autoflake for focused cleanup      |
| **Type annotations**      | `monkeytype`   | Manual                      | Use for missing type hints             |

## 🔧 Configuration Status

### ✅ Configured in pyproject.toml

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint.pydocstyle]
convention = "google"  # ← Google style configured!

[tool.ruff.lint.mccabe]
max-complexity = 12

[tool.ruff.lint.isort]
known-first-party = ["haive"]
combine-as-imports = true
force-sort-within-sections = true
```

### ⚠️ Missing Configurations

- **docformatter**: No [tool.docformatter] section
- **pydocstyle**: No [tool.pydocstyle] section
- **darglint**: No [tool.darglint] section
- **interrogate**: No [tool.interrogate] section
- **yapf**: Empty .style.yapf file

## 🎯 Recommended Workflow

### 1. Analysis Phase (Read-Only)

```bash
# Measure current coverage
poetry run interrogate packages/haive-games/src/ --verbose

# Check Google-style compliance
poetry run pydocstyle packages/haive-games/src/ --convention=google

# Validate semantic correctness
poetry run darglint packages/haive-games/src/ --strictness=short

# Check with ruff
poetry run ruff check packages/haive-games/src/ --select=D
```

### 2. Preview Phase (What Would Change)

```bash
# Preview docstring formatting
poetry run docformatter --diff packages/haive-games/src/haive/games/tic_tac_toe.py

# Preview import cleanup
poetry run autoflake --check --remove-all-unused-imports packages/haive-games/src/

# Preview ruff fixes
poetry run ruff check packages/haive-games/src/ --select=D --diff
```

### 3. Safe Application Phase

```bash
# In submodule directory
cd packages/haive-games
git checkout -b docs/formatting-test

# Apply to single file first
poetry run docformatter --in-place src/haive/games/tic_tac_toe.py

# If good, apply to package
poetry run docformatter --in-place --recursive src/
```

## 📝 Recommended Configurations to Add

### 1. docformatter Configuration

```toml
[tool.docformatter]
recursive = true
wrap-summaries = 88
wrap-descriptions = 88
blank = true
pre-summary-newline = true
make-summary-multi-line = true
force-wrap = false
tab-width = 4
```

### 2. pydocstyle Configuration ✅ **Supports pyproject.toml**

```toml
[tool.pydocstyle]
convention = "google"
add-ignore = ["D100", "D104"]  # Module and package docstrings optional
match-dir = "(?!test).*"
ignore-decorators = ["typing.overload"]
```

**Note**: Requires `pydocstyle[toml]` to be installed for pyproject.toml support.

### 3. interrogate Configuration ✅ **Full pyproject.toml Support**

```toml
[tool.interrogate]
# Coverage settings
fail-under = 80.0
ignore-init-method = true
ignore-init-module = true
ignore-magic = false
ignore-semiprivate = false
ignore-private = false
ignore-property-decorators = false
ignore-module = false

# File filtering
exclude = ["tests", "docs", "build", "migrations"]
ignore-regex = ["^get$", "^post$", "^put$", "^delete$"]
ext = ["py"]

# Output settings
verbose = 1
quiet = false
whitelist-regex = []
color = true

# Badge generation
generate-badge = "docs/"
badge-format = "svg"
badge-style = "flat-square-modified"
```

### 4. darglint Configuration ⚠️ **No pyproject.toml Support**

**Must use `.darglint` file or setup.cfg**

Create `.darglint` file:

```ini
[darglint]
docstring_style = google
strictness = short
ignore = DAR003,DAR203
message_template = {path}:{line} {msg_id} {msg}
enable_disabled_checks = DAR103,DAR203
```

**Alternative**: Use `darglint2` (maintained fork) which supports `.darglint2` files with same syntax.

### 5. monkeytype Configuration (Optional)

**Runtime Type Collection Setup**

```bash
# Installation with Poetry
poetry add --group dev MonkeyType

# Usage workflow
poetry run monkeytype run your_script.py    # Collect types
poetry run monkeytype stub your.module      # Generate stubs
poetry run monkeytype apply your.module     # Apply to code
```

**For complex projects, create `monkeytype_config.py`:**

```python
from monkeytype.config import DefaultConfig

class MonkeyConfig(DefaultConfig):
    def sample_rate(self) -> float:
        return 0.01  # Sample 1% of calls for performance

CONFIG = MonkeyConfig()
```

## 🛠️ Complete Setup Guide

### Step 1: Install Missing Dependencies

```bash
# Check if we need to add any tools
poetry show | grep -E "pydocstyle|darglint|interrogate|docformatter|monkeytype"

# Add missing tools (if needed)
poetry add --group dev "pydocstyle[toml]"  # For pyproject.toml support
poetry add --group dev darglint2           # Maintained fork
poetry add --group dev MonkeyType          # For type generation
```

### Step 2: Create Configuration Files

**Add to pyproject.toml:**

```toml
# Add the pydocstyle and interrogate sections from above
[tool.pydocstyle]
convention = "google"
add-ignore = ["D100", "D104"]
match-dir = "(?!test).*"

[tool.interrogate]
fail-under = 80.0
ignore-init-method = true
generate-badge = "docs/"
badge-format = "svg"
```

**Create `.darglint` file in project root:**

```ini
[darglint]
docstring_style = google
strictness = short
ignore = DAR003,DAR203
```

### Step 3: Test Configuration

```bash
# Verify each tool works with new config
poetry run pydocstyle --version
poetry run darglint --version
poetry run interrogate --version
poetry run docformatter --version
```

### Step 4: Generate Documentation Badge

```bash
# Create docs directory if it doesn't exist
mkdir -p docs/

# Generate initial badge
poetry run interrogate packages/haive-games/src/ --generate-badge docs/docstring_coverage.svg
```

## 🚀 Safe Execution Order

1. **Always start with read-only analysis**
2. **Use --diff or --check flags first**
3. **Test on single files before directories**
4. **Work in feature branches within submodules**
5. **Commit after each successful tool run**

## ⚠️ Tool Conflicts to Avoid

- **Don't use**: `black` (not installed, conflicts with ruff)
- **Don't use**: `autopep8` for docstrings (use docformatter)
- **Don't configure**: Multiple code formatters (stick with ruff)
- **Be careful**: yapf has empty config, prefer ruff

## 🎯 Recommended Tool Chain

For comprehensive documentation improvement:

```bash
# 1. Measure baseline
poetry run interrogate packages/haive-games/src/ --verbose

# 2. Clean imports
poetry run autoflake --in-place --remove-all-unused-imports --recursive packages/haive-games/src/

# 3. Format docstrings
poetry run docformatter --in-place --recursive packages/haive-games/src/

# 4. Validate Google style
poetry run pydocstyle packages/haive-games/src/ --convention=google

# 5. Check semantic correctness
poetry run darglint packages/haive-games/src/

# 6. Final measurement
poetry run interrogate packages/haive-games/src/ --verbose
```

## 🔄 Integration with CI/CD

Add to pre-commit hooks:

```yaml
repos:
  - repo: https://github.com/PyCQA/docformatter
    rev: v1.7.7
    hooks:
      - id: docformatter
        args: [--in-place, --config, pyproject.toml]

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.11.6
    hooks:
      - id: ruff
        args: [--fix, --select=D]
```

## 📋 Complete Execution Checklist

### Phase 1: Setup and Configuration

- [ ] Install missing dependencies (`pydocstyle[toml]`, `darglint2`, `MonkeyType`)
- [ ] Add tool configurations to `pyproject.toml`
- [ ] Create `.darglint` configuration file
- [ ] Test all tools work with `--version` flags
- [ ] Generate initial documentation badge

### Phase 2: Analysis and Baseline

- [ ] Run `interrogate` for coverage baseline
- [ ] Run `pydocstyle` for Google-style compliance check
- [ ] Run `darglint` for semantic validation
- [ ] Document current state and issues found

### Phase 3: Safe Automated Fixes

- [ ] Run `autoflake` to clean unused imports
- [ ] Run `docformatter` to standardize existing docstrings
- [ ] Verify changes with `git diff`
- [ ] Test that tools still work after changes

### Phase 4: Validation and Measurement

- [ ] Re-run all validation tools
- [ ] Generate updated coverage badge
- [ ] Compare before/after metrics
- [ ] Document improvements achieved

### Phase 5: Manual Documentation (If Needed)

- [ ] Add missing docstrings for critical functions
- [ ] Fix semantic issues found by darglint
- [ ] Use monkeytype for missing type hints
- [ ] Final validation run

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

**1. "No module named 'toml'" when using pydocstyle**

```bash
# Install toml support
poetry add --group dev "pydocstyle[toml]"
```

**2. "darglint command not found"**

```bash
# Original darglint is archived, use darglint2
poetry add --group dev darglint2
```

**3. "Badge generation failed"**

```bash
# Ensure docs directory exists
mkdir -p docs/
# Check permissions
ls -la docs/
```

**4. "MonkeyType no traces found"**

```bash
# Ensure you ran the script first
poetry run monkeytype run your_script.py
# Check for .sqlite3 file
ls -la monkeytype.sqlite3
```

**5. "pydocstyle not reading pyproject.toml"**

```bash
# Verify toml support is installed
poetry run python -c "import toml; print('TOML support available')"
# Check configuration syntax
poetry run python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
```

## 📊 Success Metrics

### Baseline Measurements (Haive-Games Results)

- **interrogate coverage**: 89% ✅ **GOOD** (2,177/2,444)
- **pydocstyle violations**: 645 ⚠️ **HIGH** (mostly formatting)
- **darglint violations**: 508 ⚠️ **HIGH** (semantic issues)
- **docformatter**: Successfully applied (minimal changes)

### Target Improvements

- **interrogate coverage**: Maintain > 85% (already good)
- **pydocstyle violations**: Reduce from 645 → 150 (77% reduction target)
- **darglint violations**: Reduce from 508 → 300 (40% reduction target)
- **Format consistency**: All docstrings follow Google-style line-wrapping

### Proven Automation Success Rate

- **docformatter**: ✅ Works - minimal safe formatting changes
- **pydocstyle detection**: ✅ Works - found 645 real issues
- **darglint detection**: ✅ Works - found 508 semantic issues
- **ruff auto-fixes**: 🔄 **Next to test** - should fix ~200 formatting issues
- **autopep8**: 🔄 **Next to test** - additional spacing fixes
- **Manual documentation**: Required for missing docstrings and semantic fixes

### Realistic Improvement Projections

**Phase 1 (Automated)**: 645 → 400 violations (38% reduction)
**Phase 2 (Scripts)**: 400 → 250 violations (23% additional)  
**Phase 3 (Manual)**: 250 → 150 violations (16% additional)
**Total Achievable**: **77% reduction in violations**
