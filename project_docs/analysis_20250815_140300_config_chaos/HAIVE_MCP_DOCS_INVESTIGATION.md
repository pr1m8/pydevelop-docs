# haive-mcp Documentation Investigation

**Date**: 2025-08-15 14:10:00
**Purpose**: Understanding the actual broken documentation being viewed

## Key Discovery

The documentation at `http://localhost:8003/autoapi/mcp/downloader/config/index.html` is from **haive-mcp**, NOT Pydvlppy!

## haive-mcp Documentation Configuration

### Location

- **Package**: `/home/will/Projects/haive/backend/haive/packages/haive-mcp/`
- **Docs config**: `/docs/conf.py`
- **Build output**: `/docs/build/`

### Configuration Analysis

```python
# From haive-mcp/docs/conf.py
project = "haive-mcp"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",  # NOT AutoAPI!
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    # ... other extensions
    "mcp_doc_generator",  # Custom extension
]

html_theme = "sphinx_rtd_theme"  # NOT Furo!
```

### Critical Findings

1. **NOT using Pydvlppy** - This is a hand-written conf.py
2. **NOT using Furo theme** - Using sphinx_rtd_theme instead
3. **NOT using sphinx-autoapi** - Using autosummary instead
4. **Has custom extension** - `mcp_doc_generator`

### But Wait... AutoAPI Directory Exists!

Despite not having `autoapi.extension` in the extensions list, the build output has:

```
docs/build/autoapi/
├── index.html
├── mcp/
│   ├── agents/
│   ├── cli/
│   ├── config/
│   ├── downloader/
│   │   └── config/
│   │       └── index.html  # The page user is viewing!
```

### Hypothesis

1. **Hidden AutoAPI usage** - Maybe added by custom extension or imported config
2. **Multiple builds** - Previous build with AutoAPI, current without
3. **Mixed configuration** - Some parts using Pydvlppy generated config

## The Real Problems

### 1. No Navigation Sidebar

- sphinx_rtd_theme SHOULD provide sidebar
- But it's completely missing from HTML output
- Something is breaking theme integration

### 2. No Clickable Links

- AutoAPI/autosummary tables have no links
- Just plain text where links should be
- CSS/JS not properly loaded

### 3. Full Module Paths in TOC

- Shows `mcp.downloader.config.DownloaderConfig`
- Instead of just `DownloaderConfig`
- Makes navigation overwhelming

### 4. No Breadcrumbs

- Theme should provide breadcrumb navigation
- Completely missing from output
- Can't navigate up hierarchy

## Build System Confusion

### Possible Scenarios

1. **Pydvlppy was used initially**
   - Generated initial conf.py
   - Later modified by hand
   - Lost critical settings

2. **Manual configuration**
   - Never used Pydvlppy
   - Manually configured Sphinx
   - Missing key settings

3. **Hybrid approach**
   - Some Pydvlppy templates
   - Some manual configuration
   - Conflicting settings

## What's Actually Happening

When viewing the documentation:

1. **Server**: `python -m http.server 8003 --directory docs/build`
2. **URL**: `http://localhost:8003/autoapi/mcp/downloader/config/index.html`
3. **Result**: Page loads but has no navigation, no links, ugly appearance

## Next Investigation Steps

1. **Check if Pydvlppy was ever used**
   - Look for `.pydvlppy` markers
   - Check git history of conf.py
   - Look for Pydvlppy templates

2. **Find where AutoAPI is configured**
   - Check imported configurations
   - Look at mcp_doc_generator extension
   - Search for hidden autoapi settings

3. **Understand theme failure**
   - Why is sphinx_rtd_theme not rendering navigation?
   - Are static files being served correctly?
   - Is there a JavaScript error?

## Critical Questions

1. **Was this ever working?** Or always broken?
2. **Who configured this?** Pydvlppy or manual?
3. **Why two different systems?** (autosummary in conf.py but autoapi in output)
4. **Where is the navigation?** Theme should provide it automatically

## Impact

This reveals a bigger problem:

- **Pydvlppy may be generating broken configs**
- **Or users are mixing manual and generated configs**
- **Or there's a fundamental theme integration issue**

The broken documentation is NOT Pydvlppy' own docs, but a project that either:

1. Used Pydvlppy and it generated broken config
2. Never used Pydvlppy and has its own broken config
3. Mixed both approaches and created conflicts
