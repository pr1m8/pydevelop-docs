# 🚀 PyPI Release Guide for PyDevelop-Docs

## Prerequisites

1. **PyPI Account**: Create at https://pypi.org/account/register/
2. **API Token**: Get from https://pypi.org/manage/account/token/
3. **Configure Token**:
   ```bash
   poetry config pypi-token.pypi your-token-here
   ```

## Quick Release Process

### 1. Test Everything First
```bash
# Run complete test suite
poetry run pydevelop-docs test --coverage --lint --type-check

# Build and check package
poetry build
poetry run twine check dist/*
```

### 2. Test on TestPyPI (Recommended)
```bash
# Configure TestPyPI token
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi your-test-token

# Publish to TestPyPI
poetry run pydevelop-docs publish --test

# Test installation
pip install -i https://test.pypi.org/simple/ pydevelop-docs
```

### 3. Production Release
```bash
# Bump version (patch/minor/major)
poetry run pydevelop-docs release --part patch

# Or manually:
poetry version patch
poetry build
poetry publish
```

## Using the CLI Commands

### Test Command
```bash
# Run all tests with coverage
poetry run pydevelop-docs test

# Quick tests only
poetry run pydevelop-docs test --fast

# With linting and type checking
poetry run pydevelop-docs test --lint --type-check
```

### Publish Command
```bash
# Dry run first
poetry run pydevelop-docs publish --dry-run

# Publish to TestPyPI
poetry run pydevelop-docs publish --test

# Publish to PyPI (production)
poetry run pydevelop-docs publish
```

### Release Command
```bash
# Complete release workflow
poetry run pydevelop-docs release --part patch

# Check version first
poetry run pydevelop-docs release --check-version

# Dry run
poetry run pydevelop-docs release --dry-run
```

## Manual Process

If you prefer manual control:

```bash
# 1. Update version
poetry version patch  # or minor/major

# 2. Build distributions
poetry build

# 3. Check package
poetry run twine check dist/*

# 4. Upload to PyPI
poetry publish

# 5. Create git tag
git tag -a v$(poetry version -s) -m "Release v$(poetry version -s)"
git push origin v$(poetry version -s)
```

## Verification

After publishing:

1. **Check PyPI**: https://pypi.org/project/pydevelop-docs/
2. **Test Installation**:
   ```bash
   pip install pydevelop-docs
   pydevelop-docs --version
   ```
3. **Verify Docs**: https://pydevelop-docs.readthedocs.io

## Troubleshooting

- **Token Issues**: Ensure token has upload permissions
- **Version Conflicts**: Check existing versions on PyPI
- **Build Errors**: Run `poetry check` and `poetry install`
- **Network Issues**: Try `poetry publish --verbose`

## GitHub Release

After PyPI release:

```bash
gh release create v$(poetry version -s) \
  --title "PyDevelop-Docs v$(poetry version -s)" \
  --notes "See CHANGELOG.md for details" \
  --generate-notes
```

---

**Remember**: Always test on TestPyPI first!