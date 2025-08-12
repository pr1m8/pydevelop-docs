# Enhanced Sphinx Build Logging Guide

This guide documents the comprehensive logging and debugging infrastructure created for Sphinx documentation builds.

## Overview

The enhanced logging system provides:

- Real-time build monitoring with Rich console dashboard
- Comprehensive warning/error categorization
- Post-build analysis and recommendations
- Integration with Sphinx's built-in logging API
- Debug configuration profiles
- CI/CD integration support

## Components

### 1. Enhanced Build Logger (`scripts/enhanced_build_logger.py`)

Real-time Sphinx build monitoring with live dashboard.

#### Usage

```bash
# Basic usage
poetry run python scripts/enhanced_build_logger.py

# Custom command
poetry run python scripts/enhanced_build_logger.py \
  --command "sphinx-build -b html docs build" \
  --directory /path/to/project \
  --output logs/

# Debug mode (shows warnings/errors during build)
poetry run python scripts/enhanced_build_logger.py --debug

# Filter specific warnings
poetry run python scripts/enhanced_build_logger.py \
  -f import_resolution \
  -f deprecated
```

#### Features

- **Live Dashboard**: Shows progress, file count, warnings, errors in real-time
- **Categorized Warnings**: Automatically categorizes warnings by type
- **Performance Metrics**: Tracks build duration and phase timing
- **JSON Analysis**: Generates structured analysis reports
- **Recommendations**: Provides actionable suggestions based on issues

#### Example Output

```
                            🔨 Sphinx Build Monitor
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value           ┃ Details                                  ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Progress        │ 65%             │ [█████████████░░░░░░]                   │
│ Files Processed │ 456             │ AutoAPI reading                          │
│ Elapsed Time    │ 145.3s          │                                          │
│ Warnings        │ 125             │ import_resolution: 89, general: 36      │
│ Errors          │ 0               │ None                                     │
│ Current Phase   │ reading sources │                                          │
└─────────────────┴─────────────────┴──────────────────────────────────────────┘
```

### 2. Build Log Analyzer (`scripts/analyze_build_log.py`)

Post-build analysis tool for existing Sphinx build logs.

#### Usage

```bash
# Analyze a build log
poetry run python scripts/analyze_build_log.py path/to/sphinx-build.log

# Generate JSON report
poetry run python scripts/analyze_build_log.py build.log --json

# Save analysis
poetry run python scripts/analyze_build_log.py build.log --save analysis.json
```

#### Analysis Provides

- **Build Summary**: Lines processed, files, progress, warnings/errors
- **Warning Breakdown**: Categorized by type with percentages
- **Import Issues**: Top modules with import resolution problems
- **Deprecated Packages**: Packages triggering deprecation warnings
- **Recommendations**: Actionable suggestions for fixing issues

### 3. Sphinx Debug Extension (`src/pydevelop_docs/sphinx_debug.py`)

Custom Sphinx extension following best practices.

#### Features

- **Phase Timing**: Tracks duration of each build phase
- **Warning Analysis**: Categorizes and tracks all warnings
- **Debug Reports**: Generates comprehensive JSON and HTML reports
- **Event Hooks**: Monitors all Sphinx build events
- **Performance Profiling**: Optional profiling integration

#### Setup in `conf.py`

```python
# Add to extensions
extensions = [
    # ... other extensions
    'pydevelop_docs.sphinx_debug',
]

# Configure debug level
pydevelop_debug_level = 2  # 0-3, higher = more verbose
pydevelop_debug_categories = ['import_resolution', 'deprecation']
```

### 4. Debug Configuration (`src/pydevelop_docs/config_debug.py`)

Enhanced configuration with debug profiles.

#### Usage

```python
from pydevelop_docs.config_debug import enhance_config_with_debug

# In conf.py
if os.environ.get('SPHINX_DEBUG'):
    # Get current config
    current_config = {k: v for k, v in globals().items() if not k.startswith('_')}

    # Enhance with debug features
    debug_config = enhance_config_with_debug(
        current_config,
        debug_mode=True,
        ci_mode=os.environ.get('CI') is not None
    )

    # Apply enhanced config
    globals().update(debug_config)
```

#### Debug Profiles

- **minimal**: Basic logging, no performance impact
- **standard**: Moderate logging with phase timing
- **verbose**: Detailed logging with profiling
- **full**: Everything enabled including measurements

#### Environment Variables

```bash
# Enable debug mode
export SPHINX_DEBUG=1

# Set debug level (0-3)
export SPHINX_DEBUG_LEVEL=2

# CI mode (strict checking)
export CI=true

# Parallel builds
export SPHINX_PARALLEL=4
```

## Warning Categories

The system automatically categorizes warnings:

1. **import_resolution**: Module import failures
2. **deprecation**: Deprecated package/API usage
3. **duplicate_reference**: Duplicate object definitions
4. **undefined_reference**: Missing references
5. **extension**: Extension-related issues
6. **autoapi**: AutoAPI-specific warnings
7. **pydantic**: Pydantic schema warnings
8. **general**: Uncategorized warnings

## Integration Patterns

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Build Documentation with Enhanced Logging
  run: |
    export SPHINX_DEBUG=1
    export CI=true
    poetry run python tools/pydevelop-docs/scripts/enhanced_build_logger.py \
      --command "sphinx-build -b html docs build" \
      --output artifacts/logs/

- name: Analyze Build Results
  if: always()
  run: |
    poetry run python tools/pydevelop-docs/scripts/analyze_build_log.py \
      artifacts/logs/sphinx-build-*.log \
      --json \
      --save artifacts/build-analysis.json

- name: Upload Build Analysis
  uses: actions/upload-artifact@v3
  with:
    name: sphinx-build-analysis
    path: artifacts/
```

### Makefile Integration

```makefile
# Enhanced build targets
.PHONY: docs-debug
docs-debug:
	SPHINX_DEBUG=1 poetry run python scripts/enhanced_build_logger.py \
		--command "sphinx-build -b html source build/html -v"

.PHONY: docs-analyze
docs-analyze:
	poetry run python scripts/analyze_build_log.py \
		logs/sphinx-build-*.log --json

.PHONY: docs-clean-build
docs-clean-build: clean docs-debug docs-analyze
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: sphinx-build-check
      name: Check Sphinx Build
      entry: poetry run python tools/pydevelop-docs/scripts/enhanced_build_logger.py
      language: system
      files: '\.(py|rst|md)$'
      pass_filenames: false
```

## Best Practices

### 1. Development Workflow

```bash
# During development - use debug mode
SPHINX_DEBUG=1 make docs

# Check specific issues
poetry run python scripts/analyze_build_log.py logs/latest.log \
  | grep "import_resolution"

# CI builds - strict mode
CI=true SPHINX_DEBUG_LEVEL=3 make docs
```

### 2. Filtering Noisy Warnings

```python
# In conf.py with debug config
from pydevelop_docs.config_debug import setup_logging_filters

def setup(app):
    setup_logging_filters(
        app,
        ignore_patterns=[
            r'Cannot resolve import of unknown module',
            r'pkg_resources is deprecated',
        ],
        log_file=Path(app.outdir) / '_debug' / 'filtered.log'
    )
```

### 3. Performance Optimization

```python
# Use minimal debug in production
if not os.environ.get('CI'):
    debug_profile = 'minimal'
else:
    debug_profile = 'full'

from pydevelop_docs.config_debug import get_debug_profile
debug_config = get_debug_profile(debug_profile)
```

## Troubleshooting

### High Warning Count

1. Run analyzer to categorize warnings
2. Focus on most common categories
3. Use `autoapi_ignore_patterns` for import issues
4. Update deprecated dependencies

### Slow Builds

1. Enable profiling with `verbose` or `full` profile
2. Check phase timing in debug report
3. Consider parallel builds with `SPHINX_PARALLEL`
4. Reduce autoapi directories if needed

### Memory Issues

1. Use `minimal` debug profile
2. Filter warnings to reduce memory usage
3. Split large documentation into sub-projects

## Output Files

### Log Files

- `sphinx-build-YYYYMMDD-HHMMSS.log`: Full build output
- `build-analysis-YYYYMMDD-HHMMSS.json`: Structured analysis
- `_debug/build_debug.json`: Debug extension report
- `_debug/debug_report.html`: HTML debug summary

### Analysis Reports

```json
{
  "build_info": {
    "start_time": "2025-01-12T01:09:24",
    "duration_seconds": 350.4,
    "log_file": "path/to/log"
  },
  "statistics": {
    "files_processed": 701,
    "total_warnings": 4448,
    "total_errors": 387
  },
  "warning_breakdown": {
    "general": 4236,
    "import_resolution": 209,
    "extension": 3
  },
  "recommendations": [...]
}
```

## Future Enhancements

1. **Real-time Web Dashboard**: WebSocket-based monitoring
2. **Historical Analysis**: Track build metrics over time
3. **Automated Fixes**: Suggest and apply common fixes
4. **Integration with sphinx-autobuild**: Live reload with logging
5. **Custom Warning Handlers**: Plugin system for warning processors
