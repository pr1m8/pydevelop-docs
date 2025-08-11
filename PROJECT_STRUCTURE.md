# PyAutoDoc Project Structure

Clean, organized structure after cleanup:

```
pyautodoc/
│
├── 📄 Core Tools (Ready to Use!)
│   ├── pyautodoc_simple.py      # ⭐ Main tool - drop this in any project
│   ├── pyautodoc.py             # Full-featured version
│   └── install.py               # One-line installer
│
├── 📁 standalone/               # Standalone versions
│   ├── pyautodoc_standalone.py # Self-contained with TOML parser
│   └── README.md               # Standalone documentation
│
├── 📁 docs/                    # Project documentation
│   ├── user-guide.md           # How to use PyAutoDoc
│   ├── developer-guide.md      # How to extend PyAutoDoc
│   ├── api-endpoints-guide.md  # API security guide
│   ├── quick-reference.md      # Quick command reference
│   ├── seed-intersphinx-guide.md # Auto-linking guide
│   ├── conf.py                 # Sphinx config for these docs
│   ├── index.rst              # Documentation index
│   └── README.md              # About this documentation
│
├── 📁 shared-docs-config/      # Shared configuration
│   ├── unified_config.py       # Unified config system
│   └── __init__.py
│
├── 📁 scripts/                 # Utility scripts
│   ├── build-monorepo-docs.py # Monorepo builder
│   ├── cleanup-project.py     # Cleanup utility
│   └── integrate.sh           # Integration helper
│
├── 📁 packages/                # Example packages (for testing)
│   ├── haive-core/
│   ├── haive-ml/
│   └── haive-api/
│
├── 📁 src/                     # Example source code
│   ├── base/
│   └── core/
│
└── 📄 Documentation Files
    ├── README.md              # Main project README
    ├── UNIVERSAL_README.md    # Guide for universal usage
    ├── CLEANUP_SUMMARY.md     # What we cleaned up
    └── PROJECT_STRUCTURE.md   # This file
```

## What Each File Does

### Essential Files (What You Need)

1. **`pyautodoc_simple.py`** ⭐
   - The main tool you copy to other projects
   - Zero configuration needed
   - Just drop and run

2. **`install.py`**
   - Downloads and sets up PyAutoDoc
   - Use for one-line installation

3. **`integrate.sh`**
   - Helps integrate PyAutoDoc into existing projects
   - Copies files and provides instructions

### Documentation

- **User Guides**: How to use PyAutoDoc
- **Developer Guides**: How to extend and customize
- **API Guides**: Security-focused documentation

### For PyAutoDoc Development

- **`shared-docs-config/`**: Configuration system for complex setups
- **`scripts/`**: Build and maintenance scripts
- **`packages/`**: Example packages for testing

## Quick Start

To use PyAutoDoc in another project:

```bash
# Copy the main tool
cp pyautodoc_simple.py /path/to/other/project/

# Or use the integration script
./scripts/integrate.sh /path/to/other/project
```

## What We Cleaned Up

- ✅ Removed `docs/source/` (duplicate documentation)
- ✅ Removed `docs/config/` (unused YAML system)
- ✅ Removed old config files (`shared_config.py`, `shared_config_simple.py`)
- ✅ Removed empty directories (`docs/data/`, `docs/logs/`)
- ✅ Removed build artifacts (`_build/`, `__pycache__/`)

The project is now clean and organized!