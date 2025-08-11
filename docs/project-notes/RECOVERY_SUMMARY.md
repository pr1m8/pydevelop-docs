# Recovery Summary

## What We Recovered

✅ **Restored `docs/source/`** - The actual Sphinx documentation source
✅ **Restored `docs/config/`** - The YAML configuration system
✅ **Both directories are back**

## Current Documentation Structure

We now have **TWO different documentation systems**:

### 1. Original PyAutoDoc Documentation (in `docs/source/`)

- Auto-generated from YAML config files
- Has all the Sphinx extensions (70+)
- Used by `build-docs.sh` and `Makefile`
- This is what builds the actual project documentation

### 2. New Documentation Guides (in `docs/`)

- The markdown guides we created:
  - `user-guide.md`
  - `developer-guide.md`
  - `api-endpoints-guide.md`
  - etc.
- These are documentation ABOUT PyAutoDoc, not FROM PyAutoDoc

## What's the Confusion?

1. **Two `conf.py` files**:
   - `docs/conf.py` - For root-level docs (references deleted shared_config)
   - `docs/source/conf.py` - The actual working config (auto-generated)

2. **Two `index.rst` files**:
   - `docs/index.rst` - Root level
   - `docs/source/index.rst` - The actual documentation index

3. **Build paths**:
   - `Makefile` uses: `SOURCEDIR = source`
   - `build-docs.sh` uses: `docs/source → docs/build/html`

## What Should We Do?

### Option 1: Keep Both Systems

- `docs/source/` - For building PyAutoDoc's own documentation
- `docs/guides/` - Move the guides to a separate folder

### Option 2: Merge Everything

- Move all guides into `docs/source/`
- Update `docs/source/index.rst` to include them
- Delete duplicate files in `docs/`

### Option 3: Separate Projects

- Keep PyAutoDoc documentation as is
- Move the "portable PyAutoDoc tool" to a separate repository

## Current Status

- ✅ Original documentation is restored and should work
- ⚠️ We have duplicate/conflicting files
- ⚠️ The shared config files were part of a different system (monorepo docs)

The original documentation should now build with:

```bash
cd docs
make html
# or
poetry run sphinx-build -b html source build/html
```
