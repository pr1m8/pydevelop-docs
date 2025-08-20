# Quick Build Commands for Haive Documentation

## 🚀 One-Line Commands

### Build Everything (Recommended)

```bash
cd /home/will/Projects/haive/backend/haive && poetry run pydvlp-docs build --all
```

### Build Individual Packages

```bash
# Build haive-core only
cd /home/will/Projects/haive/backend/haive/packages/haive-core && poetry run pydvlp-docs init --force && poetry run pydvlp-docs build

# Build haive-agents only
cd /home/will/Projects/haive/backend/haive/packages/haive-agents && poetry run pydvlp-docs init --force && poetry run pydvlp-docs build

# Build haive-tools only
cd /home/will/Projects/haive/backend/haive/packages/haive-tools && poetry run pydvlp-docs init --force && poetry run pydvlp-docs build
```

### Build Central Hub Only

```bash
cd /home/will/Projects/haive/backend/haive && poetry run pydvlp-docs init --project-type central-hub && poetry run pydvlp-docs build --hub-only
```

## 📁 Where to Find Built Documentation

After building, documentation is located at:

- **Central Hub**: `/home/will/Projects/haive/backend/haive/docs/build/html/index.html`
- **haive-core**: `/home/will/Projects/haive/backend/haive/packages/haive-core/docs/build/html/index.html`
- **haive-agents**: `/home/will/Projects/haive/backend/haive/packages/haive-agents/docs/build/html/index.html`
- **haive-tools**: `/home/will/Projects/haive/backend/haive/packages/haive-tools/docs/build/html/index.html`
- **haive-games**: `/home/will/Projects/haive/backend/haive/packages/haive-games/docs/build/html/index.html`
- **haive-mcp**: `/home/will/Projects/haive/backend/haive/packages/haive-mcp/docs/build/html/index.html`
- **haive-dataflow**: `/home/will/Projects/haive/backend/haive/packages/haive-dataflow/docs/build/html/index.html`
- **haive-prebuilt**: `/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/docs/build/html/index.html`

## 🌐 View Documentation

### Using Python HTTP Server

```bash
# View central hub
cd /home/will/Projects/haive/backend/haive/docs/build/html && python -m http.server 8000
# Open: http://localhost:8000

# View specific package (e.g., haive-core)
cd /home/will/Projects/haive/backend/haive/packages/haive-core/docs/build/html && python -m http.server 8001
# Open: http://localhost:8001
```

### Using xdg-open (opens in default browser)

```bash
# Open central hub
xdg-open /home/will/Projects/haive/backend/haive/docs/build/html/index.html

# Open specific package
xdg-open /home/will/Projects/haive/backend/haive/packages/haive-core/docs/build/html/index.html
```

## 🧹 Clean Builds

```bash
# Clean and rebuild everything
cd /home/will/Projects/haive/backend/haive && poetry run pydvlp-docs clean --all && poetry run pydvlp-docs build --all

# Clean specific package
cd /home/will/Projects/haive/backend/haive/packages/haive-core && poetry run pydvlp-docs clean && poetry run pydvlp-docs build
```

## 🔧 Advanced Options

### Parallel Building (faster for multiple packages)

```bash
cd /home/will/Projects/haive/backend/haive && poetry run pydvlp-docs build --all --parallel
```

### Watch Mode (auto-rebuild on changes)

```bash
cd /home/will/Projects/haive/backend/haive && poetry run pydvlp-docs build --watch
```

### Dry Run (preview what would be built)

```bash
cd /home/will/Projects/haive/backend/haive && poetry run pydvlp-docs build --all --dry-run
```

## 📝 Using the Build Script

We've also created a convenient build script:

```bash
# Make it executable (only needed once)
chmod +x /home/will/Projects/haive/backend/haive/tools/pydvlp-docs/scripts/build-haive-docs.sh

# Build everything
/home/will/Projects/haive/backend/haive/tools/pydvlp-docs/scripts/build-haive-docs.sh all

# Build just the hub
/home/will/Projects/haive/backend/haive/tools/pydvlp-docs/scripts/build-haive-docs.sh hub

# Build all packages
/home/will/Projects/haive/backend/haive/tools/pydvlp-docs/scripts/build-haive-docs.sh packages

# Build specific package
/home/will/Projects/haive/backend/haive/tools/pydvlp-docs/scripts/build-haive-docs.sh haive-core
```

## ⚡ Super Quick Test

To quickly test if everything is working:

```bash
# 1. Go to Haive root
cd /home/will/Projects/haive/backend/haive

# 2. Initialize and build
poetry run pydvlp-docs init --project-type monorepo --force && poetry run pydvlp-docs build --all

# 3. Open documentation
xdg-open docs/build/html/index.html
```

That's it! The documentation should now be built with:

- ✅ Hierarchical API structure (not flat)
- ✅ Beautiful Furo theme with dark mode
- ✅ All 45+ extensions working
- ✅ Cross-package navigation
- ✅ Intelligent templates applied
