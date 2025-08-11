# Careful Cleanup Plan for PyAutoDoc

## What to Keep (Full Versions Only)

### Core Working System

- `shared-docs-config/shared_config.py` - Main configuration ✓ (recovered)
- `shared-docs-config/shared_config_simple.py` - Simplified config ✓ (recovered)
- `shared-docs-config/unified_config.py` - New unified config
- `scripts/build-monorepo-docs.py` - Main build script ✓
- `docs/source/` - Main documentation source ✓ (recovered)

### Documentation

- `docs/` - All existing documentation
- Keep the guides we created in `docs/`:
  - `user-guide.md`
  - `developer-guide.md`
  - `api-endpoints-guide.md`
  - `seed-intersphinx-guide.md`

## What to Remove (Extra/Simple Versions)

### Remove These Files

1. `pyautodoc.py` - Complex version with issues
2. `pyautodoc_simple.py` - Simple version (you don't want)
3. `standalone/pyautodoc_standalone.py` - Another simple version
4. `install.py` - Installer for simple version
5. `integrate.sh` - Integration script for simple version

### Remove These Docs (About Simple Versions)

1. `UNIVERSAL_README.md` - About the simple tool
2. `INTEGRATION_GUIDE.md` - How to use simple tool
3. `PROJECT_STRUCTURE.md` - Mixed up structure
4. `CLEANUP_SUMMARY.md` - Previous cleanup attempt
5. `CLEANUP_PLAN.md` - Previous cleanup plan
6. `CAREFUL_CLEANUP_PLAN.md` - This file (after we're done)

### Remove Empty Directory

1. `standalone/` - After removing its contents

## Step-by-Step Cleanup Process

### Step 1: Remove simple tool versions

```bash
git rm pyautodoc.py pyautodoc_simple.py
git rm standalone/pyautodoc_standalone.py
git rm -r standalone/
git rm install.py
```

### Step 2: Remove integration scripts

```bash
git rm scripts/integrate.sh
```

### Step 3: Remove extra documentation

```bash
git rm UNIVERSAL_README.md INTEGRATION_GUIDE.md
git rm PROJECT_STRUCTURE.md CLEANUP_SUMMARY.md
```

### Step 4: Clean up any untracked files

```bash
rm CLEANUP_PLAN.md CAREFUL_CLEANUP_PLAN.md
```

### Step 5: Update main README

- Remove references to simple tools
- Focus on the monorepo documentation system

### Step 6: Commit everything

```bash
git add -A
git commit -m "cleanup: remove simple tool versions, keep full documentation system"
git push
```

## After Cleanup Structure

```
pyautodoc/
├── docs/                       # Documentation
│   ├── source/                # Main Sphinx source (working)
│   └── *.md                   # Guides we created
├── packages/                   # Example packages
│   ├── haive-core/
│   ├── haive-ml/
│   └── haive-api/
├── shared-docs-config/         # Configuration system
│   ├── shared_config.py
│   ├── shared_config_simple.py
│   └── unified_config.py
├── scripts/                    # Build scripts
│   └── build-monorepo-docs.py
└── README.md                   # Main documentation
```

Ready to proceed with this careful cleanup?
