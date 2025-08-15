# AutoAPI Build Artifacts Analysis

**Date**: 2025-08-15 14:05:00
**Purpose**: Deep dive into what AutoAPI is actually generating

## Build Directory Structure

```
docs/build/
├── autoapi/
│   ├── index.html              # Main API index
│   ├── pydevelop_docs/         # Main package
│   │   ├── index.html
│   │   ├── cli/               # Submodules
│   │   ├── config/
│   │   └── ...
│   └── _filters/              # What is this?
│       └── type_filters/
```

Wait... this is NOT the haive-mcp documentation! This is PyDevelop-Docs' own documentation.

## Configuration Confusion

### We're Looking at Wrong Documentation!

The user showed a URL: `http://localhost:8003/autoapi/mcp/downloader/config/index.html`

But our build directory has:

- `/autoapi/pydevelop_docs/...`
- No `/autoapi/mcp/...`

**This means**: The user is looking at a DIFFERENT project's documentation!

## The Real Issue

1. **We're analyzing PyDevelop-Docs documentation** (at `/tools/pydevelop-docs/docs/build`)
2. **User is viewing haive-mcp documentation** (somewhere else)
3. **The broken documentation is in the haive-mcp package**, not PyDevelop-Docs itself

## Where is haive-mcp Documentation?

Likely locations:

- `/home/will/Projects/haive/backend/haive/packages/haive-mcp/docs/build/`
- Or served from a different directory

## What This Means

1. **PyDevelop-Docs generated bad config** for haive-mcp
2. **haive-mcp is using the broken CLI template**
3. **We need to check haive-mcp's conf.py**
4. **The issue is in GENERATED projects**, not PyDevelop-Docs itself

## Action Items

1. Find where haive-mcp documentation is being built
2. Check its `docs/source/conf.py`
3. Verify it's using the broken CLI template
4. Understand why navigation is completely missing
5. Fix the CLI template generation

## Key Insight

The problem isn't with PyDevelop-Docs' own documentation - it's with the documentation that PyDevelop-Docs GENERATES for other projects!
