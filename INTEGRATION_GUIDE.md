# PyAutoDoc Integration Guide

How to add PyAutoDoc to your Python projects - it's super easy!

## 🚀 Quick Start (30 seconds)

### Option 1: Direct Copy
```bash
# Go to your project
cd /path/to/your/project

# Copy PyAutoDoc
cp /home/will/Projects/nonsense/pyautodoc/pyautodoc_simple.py .

# Run it!
python pyautodoc_simple.py
```

### Option 2: Using Integration Script
```bash
# Run from PyAutoDoc directory
/home/will/Projects/nonsense/pyautodoc/scripts/integrate.sh /path/to/your/project
```

### Option 3: Download from URL
```bash
# In your project directory
curl -O https://raw.githubusercontent.com/yourusername/pyautodoc/main/pyautodoc_simple.py
python pyautodoc_simple.py
```

## 📋 What Happens

When you run PyAutoDoc in your project:

1. **Discovers** all Python packages automatically
2. **Creates** a `docs/` folder with Sphinx configuration
3. **Generates** RST files for each package
4. **Builds** HTML documentation (if Sphinx is installed)
5. **Serves** docs locally at http://localhost:8000

## 🎯 Integration Examples

### For a Django Project
```bash
cd ~/myproject/django-app
cp /home/will/Projects/nonsense/pyautodoc/pyautodoc_simple.py build_docs.py
python build_docs.py
```

### For a Flask Project
```bash
cd ~/myproject/flask-api
cp /home/will/Projects/nonsense/pyautodoc/pyautodoc_simple.py docs.py
python docs.py serve
```

### For a Data Science Project
```bash
cd ~/myproject/ml-model
cp /home/will/Projects/nonsense/pyautodoc/pyautodoc_simple.py .
python pyautodoc_simple.py
```

### For a Library
```bash
cd ~/myproject/awesome-lib
cp /home/will/Projects/nonsense/pyautodoc/pyautodoc_simple.py .
python pyautodoc_simple.py
git add pyautodoc_simple.py
git commit -m "Add documentation generator"
```

## 🔧 Customization Options

### Rename for Your Project
```bash
# Give it a project-specific name
mv pyautodoc_simple.py build_docs.py

# Or something descriptive
mv pyautodoc_simple.py generate_api_docs.py
```

### Add to Makefile
```makefile
.PHONY: docs
docs:
	python pyautodoc_simple.py build

.PHONY: docs-serve  
docs-serve:
	python pyautodoc_simple.py serve

.PHONY: docs-clean
docs-clean:
	python pyautodoc_simple.py clean
```

### Add to package.json
```json
{
  "scripts": {
    "docs": "python pyautodoc_simple.py",
    "docs:build": "python pyautodoc_simple.py build",
    "docs:serve": "python pyautodoc_simple.py serve"
  }
}
```

### Add to pyproject.toml
```toml
[tool.taskipy.tasks]
docs = "python pyautodoc_simple.py"
docs-serve = "python pyautodoc_simple.py serve"
```

### Create Shell Alias
```bash
# Add to ~/.bashrc or ~/.zshrc
alias builddocs='python pyautodoc_simple.py'

# Then use anywhere
cd /any/project
builddocs
```

## 📁 Works With Any Structure

### Single Package
```
myproject/
├── mypackage/
│   └── __init__.py
└── pyautodoc_simple.py
```

### Multiple Packages
```
myproject/
├── package1/
│   └── __init__.py
├── package2/
│   └── __init__.py
└── pyautodoc_simple.py
```

### Src Layout
```
myproject/
├── src/
│   └── mypackage/
│       └── __init__.py
└── pyautodoc_simple.py
```

### Tests Included
```
myproject/
├── mypackage/
│   └── __init__.py
├── tests/
│   └── test_mypackage.py
└── pyautodoc_simple.py
```

## 🛠️ Advanced Integration

### Global Installation
```bash
# Copy to system bin
sudo cp /home/will/Projects/nonsense/pyautodoc/pyautodoc_simple.py /usr/local/bin/pyautodoc
sudo chmod +x /usr/local/bin/pyautodoc

# Now use anywhere
cd /any/project
pyautodoc
```

### As a Git Submodule
```bash
cd your-project
git submodule add https://github.com/yourusername/pyautodoc.git tools/pyautodoc
ln -s tools/pyautodoc/pyautodoc_simple.py build_docs.py
```

### In Docker
```dockerfile
# Add to Dockerfile
COPY pyautodoc_simple.py /usr/local/bin/pyautodoc
RUN chmod +x /usr/local/bin/pyautodoc

# Build docs during image build
RUN cd /app && pyautodoc build
```

## 📝 Tips

1. **First Time**: Just copy and run - it figures everything out
2. **CI/CD**: Add `python pyautodoc_simple.py build` to your build pipeline
3. **Team Use**: Commit the file to your repo so everyone has it
4. **Multiple Projects**: Keep one copy and symlink to it

## 🎉 That's It!

PyAutoDoc is designed to be the simplest way to add documentation to any Python project. Just drop it in and run - no configuration needed!