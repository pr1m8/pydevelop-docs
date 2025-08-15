# Haive Documentation Rebuild Guide

**Purpose**: Complete documentation rebuild for the entire Haive AI Agent Framework monorepo  
**Created**: 2025-08-15  
**Tools**: PyDevelop-Docs with specialized Haive utilities

## 🎯 Overview

This guide covers the complete rebuild of documentation for the Haive monorepo, including:

- **7 packages**: haive-core, haive-agents, haive-tools, haive-games, haive-mcp, haive-prebuilt, haive-dataflow
- **Master documentation hub**: Central hub with cross-package links
- **Modern CSS system**: Enhanced design with breadcrumb navigation
- **Hierarchical AutoAPI**: Proper package/module organization

## 🚀 Quick Start

### 1. Test the Setup

First, verify the utilities can detect the Haive structure:

```bash
cd /home/will/Projects/haive/backend/haive/tools/pydevelop-docs
poetry run python scripts/test_haive_utils.py
```

**Expected output**:

```
🧪 Haive Documentation Utils Test
==================================================
🔍 Testing Haive monorepo detection...
✅ Found Haive root: /home/will/Projects/haive/backend/haive
✅ Manager initialized successfully
   Packages dir: /home/will/Projects/haive/backend/haive/packages
   Master docs: /home/will/Projects/haive/backend/haive/docs
   Expected packages: 7
   Existing packages: 7
     ✅ haive-core
     ✅ haive-agents
     ✅ haive-tools
     ✅ haive-games
     ✅ haive-mcp
     ✅ haive-prebuilt
     ✅ haive-dataflow

📦 Testing package structure analysis...
[... package analysis ...]

==================================================
🎉 All tests passed!

✨ Ready to run: poetry run pydevelop-docs rebuild-haive
```

### 2. Full Rebuild (Recommended)

Run the complete rebuild with detailed logging:

```bash
cd /home/will/Projects/haive/backend/haive/

# Complete rebuild with logging
poetry run pydevelop-docs rebuild-haive --debug --save-log
```

**This will**:

1. **Clear** all existing documentation build artifacts
2. **Initialize** each package with modern CSS and shared config
3. **Build** each package with hierarchical AutoAPI structure
4. **Create** master documentation hub with cross-package links
5. **Save** detailed operations log for review

### 3. Monitor Progress

The rebuild shows real-time progress:

```
🎯 Haive Documentation Rebuild
📁 Root: /home/will/Projects/haive/backend/haive
============================================================

🧹 Clearing all Haive documentation...
✅ clear_all: Cleared 15 directories, 42 files (2.34s)

📚 Phase 1: Initializing 7 packages...
✅ init_package: Initialized haive-core (3.21s)
✅ init_package: Initialized haive-agents (2.89s)
✅ init_package: Initialized haive-tools (2.45s)
[... more packages ...]

🔨 Phase 2: Building 7 packages...
✅ build_package: Built haive-core (24.56s)
✅ build_package: Built haive-agents (31.23s)
[... more builds ...]

🏛️  Phase 3: Building master documentation hub...
✅ init_master: Initialized master documentation hub (4.12s)
✅ build_master: Built master hub (18.67s)

============================================================
📊 REBUILD SUMMARY
============================================================
📦 Packages: 7/7 built successfully
🏛️  Master Hub: ✅ Success
🧹 Cleared: 15 dirs, 42 files
⏱️  Total time: 127.3s
🔄 Operations: 23

🎉 Complete success! All documentation rebuilt.

🌐 View documentation: file:///home/will/Projects/haive/backend/haive/docs/build/html/index.html
   Or run: python -m http.server 8000 --directory docs/build/html/

📝 Detailed log: /home/will/Projects/haive/backend/haive/haive_docs_rebuild_20250815_143022.json
```

## 🛠️ Command Options

### Basic Commands

```bash
# Full rebuild (everything)
poetry run pydevelop-docs rebuild-haive

# Rebuild specific packages only
poetry run pydevelop-docs rebuild-haive -p haive-core -p haive-agents

# Rebuild without master hub (faster)
poetry run pydevelop-docs rebuild-haive --no-master

# Quiet mode (minimal output)
poetry run pydevelop-docs rebuild-haive --quiet

# Debug mode (detailed output)
poetry run pydevelop-docs rebuild-haive --debug

# Save detailed operations log
poetry run pydevelop-docs rebuild-haive --save-log
```

### Advanced Options

```bash
# Don't clean existing builds (faster, but may have stale content)
poetry run pydevelop-docs rebuild-haive --no-clean

# Combination: specific packages with debug logging
poetry run pydevelop-docs rebuild-haive -p haive-core -p haive-agents --debug --save-log

# Quick test rebuild (no master, no clean)
poetry run pydevelop-docs rebuild-haive --no-master --no-clean --quiet
```

## 📁 File Structure After Rebuild

The rebuilt documentation will have this structure:

```
haive/
├── docs/                           # Master documentation hub
│   ├── build/html/index.html      # 🌐 Main entry point
│   └── source/
│       ├── conf.py                 # Master configuration
│       ├── _static/                # Shared CSS and assets
│       └── _templates/             # Custom templates
├── packages/
│   ├── haive-core/
│   │   └── docs/
│   │       ├── build/html/         # Built package docs
│   │       └── source/
│   │           ├── conf.py         # ✅ Shared config
│   │           ├── _static/        # Modern CSS system
│   │           └── autoapi/        # 🎯 Hierarchical API
│   ├── haive-agents/
│   │   └── docs/                   # Same structure
│   └── [... all 7 packages ...]
└── haive_docs_rebuild_*.json       # 📊 Operations log
```

## 🎨 Features Included

### Modern CSS System

Each package gets comprehensive styling:

- **enhanced-design.css**: Complete modern design system
- **breadcrumb-navigation.css**: Breadcrumb navigation for Furo theme
- **mermaid-custom.css**: Diagram theming
- **tippy-enhancements.css**: Enhanced tooltip system

### Hierarchical AutoAPI

The key setting `autoapi_own_page_level = "module"` creates proper organization:

**Before (Flat)**:

```
API Reference
├── Agent (class)
├── BaseModel (class)
├── Calculator (class)
└── [200+ classes alphabetically]
```

**After (Hierarchical)**:

```
API Reference
├── haive.core
│   ├── haive.core.engine
│   │   ├── AugLLMConfig
│   │   └── BaseAgent
│   └── haive.core.schema
│       ├── StateSchema
│       └── MetaStateSchema
├── haive.agents
│   ├── haive.agents.simple
│   │   └── SimpleAgent
│   └── haive.agents.react
│       └── ReactAgent
```

### Master Documentation Hub

The master hub provides:

- **Package index**: Links to all 7 packages
- **Cross-references**: Inter-package API links
- **Search integration**: Global search across all packages
- **Navigation breadcrumbs**: Clear location context

## 🐛 Troubleshooting

### Common Issues

#### 1. "Not in a Haive monorepo directory"

**Problem**: Command can't find Haive structure.

**Solution**:

```bash
# Make sure you're in the Haive directory
cd /home/will/Projects/haive/backend/haive/

# Verify structure
ls -la  # Should see: packages/, CLAUDE.md, pyproject.toml
```

#### 2. Poetry command not found

**Problem**: Poetry not available in current environment.

**Solution**:

```bash
# Install poetry if needed
curl -sSL https://install.python-poetry.org | python3 -

# Or use the system poetry
which poetry

# Make sure you're in the pydevelop-docs directory
cd tools/pydevelop-docs/
poetry install
```

#### 3. Build timeouts

**Problem**: Builds taking too long and timing out.

**Solution**:

```bash
# Try building individual packages first
poetry run pydevelop-docs rebuild-haive -p haive-core --debug

# Check for memory issues
free -h

# Use quiet mode to reduce output overhead
poetry run pydevelop-docs rebuild-haive --quiet
```

#### 4. Missing dependencies

**Problem**: Sphinx or other dependencies not found.

**Solution**:

```bash
# Reinstall pydevelop-docs with all dependencies
cd tools/pydevelop-docs/
poetry install --all-extras

# Check specific package dependencies
cd packages/haive-core/
poetry install
```

### Debug Mode

For detailed troubleshooting, use debug mode:

```bash
poetry run pydevelop-docs rebuild-haive --debug --save-log
```

This will:

- Show detailed command execution
- Display build output and errors
- Save comprehensive operations log
- Show timing for each operation

### Operations Log

The `--save-log` option creates a detailed JSON log:

```json
{
  "total_operations": 23,
  "total_duration_seconds": 127.34,
  "operations_by_type": {
    "clear_all": { "success": 1, "error": 0 },
    "init_package": { "success": 7, "error": 0 },
    "build_package": { "success": 6, "error": 1 },
    "init_master": { "success": 1, "error": 0 },
    "build_master": { "success": 1, "error": 0 }
  },
  "timeline": [
    {
      "timestamp": "2025-08-15T14:30:22.123456",
      "operation": "clear_all",
      "status": "success",
      "details": "Cleared 15 directories, 42 files",
      "duration_ms": 2340.25
    }
    // ... detailed timeline of all operations
  ]
}
```

## 🎯 Success Verification

After a successful rebuild:

### 1. Check Master Hub

```bash
# Open master documentation
open /home/will/Projects/haive/backend/haive/docs/build/html/index.html

# Or serve locally
cd /home/will/Projects/haive/backend/haive/docs/build/html/
python -m http.server 8000
# Then visit: http://localhost:8000
```

### 2. Verify Package Structure

Check that each package has proper hierarchical API docs:

1. Navigate to **API Reference**
2. See organized package structure (not flat alphabetical list)
3. Test breadcrumb navigation (Home → API Reference → Package → Module)
4. Verify modern CSS styling and dark mode toggle

### 3. Test Cross-Package Links

1. In haive-core docs, click on a class reference
2. Should navigate to the correct module page
3. Breadcrumbs should show the proper hierarchy
4. Back button and navigation should work smoothly

## 🎉 What You Get

After running the complete rebuild:

✅ **7 packages** with modern documentation  
✅ **Hierarchical AutoAPI** structure for easy navigation  
✅ **Breadcrumb navigation** for better UX  
✅ **Modern CSS system** with dark mode support  
✅ **Master documentation hub** with cross-package links  
✅ **Comprehensive logging** for troubleshooting  
✅ **Consistent configuration** across all packages

The result is a professional, navigable documentation system that matches the quality of major open-source projects.

---

**Ready to run?**

```bash
cd /home/will/Projects/haive/backend/haive/
poetry run pydevelop-docs rebuild-haive --debug --save-log
```
