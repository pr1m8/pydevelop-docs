# 🚀 Quick Release Instructions for PyDevelop-Docs

## Current Status
- ✅ **Version**: 0.1.0
- ✅ **Built**: dist/pydevelop_docs-0.1.0-py3-none-any.whl
- ✅ **Repository**: https://github.com/pr1m8/pydvlp-docs (PUBLIC)
- ✅ **Workflows**: Running (fixing deprecated actions)
- ⏳ **PyPI**: Not published yet
- ⏳ **Read the Docs**: Not imported yet

## 1. PyPI Release (When Ready)

### Option A: Using Poetry (Recommended)
```bash
# 1. Get PyPI token from: https://pypi.org/manage/account/token/
# 2. Configure token:
poetry config pypi-token.pypi pypi-YOUR_TOKEN_HERE

# 3. Publish to PyPI:
poetry publish

# Or use the CLI:
poetry run pydvlp-docs publish
```

### Option B: Using Twine
```bash
# 1. Set environment variable:
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE

# 2. Upload:
poetry run twine upload dist/*
```

## 2. Read the Docs Import

1. Go to: https://readthedocs.org/dashboard/import/
2. Click "Import Manually" or connect GitHub
3. Repository URL: `https://github.com/pr1m8/pydvlp-docs`
4. RTD will auto-detect `.readthedocs.yaml`

## 3. Verify Installation

After PyPI release:
```bash
# Install from PyPI
pip install pydvlp-docs

# Test it works
pydvlp-docs --version
pydvlp-docs --help
```

## 4. GitHub Release (Optional)

```bash
gh release create v0.1.0 \
  --title "PyDevelop-Docs v0.1.0 - Initial Release" \
  --notes "Universal Python documentation generator with 40+ Sphinx extensions" \
  --generate-notes
```

## Package is Ready!

The package is built and tested. Just need:
1. PyPI token to publish
2. Read the Docs import

Everything else is automated!