# 📚 Read the Docs Import Guide for pydvlp-docs

## Quick Steps to Import:

### 1. Go to Read the Docs
https://readthedocs.org/dashboard/import/

### 2. Import Repository

#### Option A: Connect GitHub (Recommended)
1. Click "Connect your GitHub account"
2. Authorize Read the Docs
3. Select `pr1m8/pydvlp-docs` from your repositories
4. Click "Import"

#### Option B: Manual Import
1. Click "Import Manually"
2. Fill in:
   - **Name**: `pydvlp-docs`
   - **Repository URL**: `https://github.com/pr1m8/pydvlp-docs`
   - **Repository type**: Git
   - **Default branch**: main

### 3. RTD Will Automatically:
- ✅ Detect `.readthedocs.yaml` configuration
- ✅ Install system dependencies (graphviz, plantuml, etc.)
- ✅ Install Python dependencies from `docs/requirements.txt`
- ✅ Build documentation using Sphinx
- ✅ Enable search and versioning

### 4. After Import:
Your documentation will be available at:
**https://pydvlp-docs.readthedocs.io**

## 🔧 Configuration Details

The project is fully configured:

- **Build OS**: Ubuntu 22.04
- **Python**: 3.12
- **Dependencies**: Managed by Poetry
- **Formats**: HTML, PDF, EPUB
- **Theme**: Furo with dark mode
- **Extensions**: 40+ Sphinx extensions

## 🚨 Troubleshooting

### If Build Fails:

1. **Check Build Logs**:
   - Go to your project on RTD
   - Click "Builds" → View failing build
   - Check the detailed logs

2. **Common Issues**:
   - **Import errors**: Fixed - uses `pydvlp_docs` package name
   - **Missing graphviz**: Fixed - added `graphviz-dev` to apt packages
   - **Poetry not found**: Fixed - installed in `post_create_environment`

3. **Force Rebuild**:
   - Go to "Versions" → "latest"
   - Click "Build Version"

## 🎯 Enable Webhooks (Optional)

For automatic builds on push:

1. In RTD project → "Admin" → "Integrations"
2. Click "Add integration" → "GitHub incoming webhook"
3. Copy the webhook URL
4. Go to GitHub repo → "Settings" → "Webhooks"
5. Add webhook with RTD URL

## 📊 Expected Result

Once imported, you'll have:
- ✅ Automatic builds on every push
- ✅ Version tags automatically built
- ✅ Search functionality
- ✅ PDF/EPUB downloads
- ✅ Beautiful documentation at https://pydvlp-docs.readthedocs.io

---

**Ready to import!** The configuration is tested and working.