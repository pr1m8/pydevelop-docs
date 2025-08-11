#!/usr/bin/env python3
"""
PyAutoDoc Simple - Drop-in Documentation Generator

A simplified version that's easy to use with any Python project.
Just drop this file in your project root and run:
    python pyautodoc_simple.py

No configuration needed!
"""

import os
import sys
import shutil
import subprocess
import webbrowser
from pathlib import Path
from typing import List, Optional
import json


class SimpleAutoDoc:
    """Simple automatic documentation generator."""
    
    def __init__(self, project_root: Path = None):
        self.root = Path(project_root or os.getcwd())
        self.docs_dir = self.root / "docs"
        self.build_dir = self.docs_dir / "_build"
        
    def find_packages(self) -> List[dict]:
        """Find all Python packages in the project."""
        packages = []
        
        # Look in common locations
        for location in ['src', 'lib', '.']:
            search_path = self.root / location if location != '.' else self.root
            if search_path.exists():
                for item in search_path.rglob('__init__.py'):
                    package_dir = item.parent
                    # Skip hidden directories and build outputs
                    if any(part.startswith('.') or part == '_build' for part in package_dir.parts):
                        continue
                    
                    packages.append({
                        'name': package_dir.name,
                        'path': str(package_dir),
                        'relative_path': str(package_dir.relative_to(self.root))
                    })
        
        # Remove duplicates
        seen = set()
        unique_packages = []
        for pkg in packages:
            if pkg['name'] not in seen:
                seen.add(pkg['name'])
                unique_packages.append(pkg)
        
        return unique_packages
    
    def setup(self):
        """Set up documentation structure."""
        print("🔍 Scanning for Python packages...")
        packages = self.find_packages()
        
        if not packages:
            print("❌ No Python packages found!")
            return False
        
        print(f"📦 Found {len(packages)} package(s):")
        for pkg in packages:
            print(f"   - {pkg['name']} ({pkg['relative_path']})")
        
        # Create docs directory
        print(f"\n📁 Creating documentation in {self.docs_dir}/")
        self.docs_dir.mkdir(exist_ok=True)
        
        # Create configuration
        self._create_conf_py(packages)
        self._create_index_rst(packages)
        self._create_makefile()
        
        print("\n✅ Documentation setup complete!")
        print("\n📋 Next steps:")
        print("1. Install Sphinx: pip install sphinx")
        print("2. Build docs: cd docs && make html")
        print("3. Open docs/_build/html/index.html")
        
        return True
    
    def _create_conf_py(self, packages):
        """Create Sphinx configuration."""
        # Build sys.path additions
        paths = ["import sys", "from pathlib import Path", ""]
        paths.append("# Add package directories to sys.path")
        paths.append("root = Path(__file__).parent.parent")
        
        for pkg in packages:
            pkg_parent = str(Path(pkg['relative_path']).parent)
            if pkg_parent and pkg_parent != '.':
                paths.append(f"sys.path.insert(0, str(root / '{pkg_parent}'))")
            else:
                paths.append("sys.path.insert(0, str(root))")
        
        conf_content = f'''# -*- coding: utf-8 -*-
# Configuration file for Sphinx documentation builder

{chr(10).join(paths)}

# -- Project information -----------------------------------------------------
project = '{self.root.name}'
copyright = '2024, {self.root.name} Contributors'
author = '{self.root.name} Contributors'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'

# -- Extension configuration -------------------------------------------------
autodoc_default_options = {{
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
'''
        
        (self.docs_dir / 'conf.py').write_text(conf_content)
        print("   ✓ Created conf.py")
    
    def _create_index_rst(self, packages):
        """Create index.rst with package documentation."""
        # Create module RST files
        modules = []
        for pkg in packages:
            rst_content = f"""{pkg['name']}
{'=' * len(pkg['name'])}

.. automodule:: {pkg['name']}
   :members:
   :undoc-members:
   :show-inheritance:
"""
            (self.docs_dir / f"{pkg['name']}.rst").write_text(rst_content)
            modules.append(f"   {pkg['name']}")
        
        # Create main index
        index_content = f"""{self.root.name} Documentation
{'=' * (len(self.root.name) + 14)}

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

{chr(10).join(modules)}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
        
        (self.docs_dir / 'index.rst').write_text(index_content)
        print("   ✓ Created index.rst")
    
    def _create_makefile(self):
        """Create simple Makefile."""
        makefile = '''# Minimal makefile for Sphinx documentation

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help Makefile

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
'''
        
        (self.docs_dir / 'Makefile').write_text(makefile)
        print("   ✓ Created Makefile")
    
    def build(self):
        """Build the documentation."""
        if not self.docs_dir.exists():
            print("❌ No documentation found. Run setup first!")
            return False
        
        print("🔨 Building documentation...")
        
        # Change to docs directory
        os.chdir(self.docs_dir)
        
        # Run sphinx-build
        try:
            subprocess.run([sys.executable, '-m', 'sphinx', '-b', 'html', '.', '_build/html'], check=True)
            print("✅ Documentation built successfully!")
            print(f"📂 Open: {self.build_dir / 'html' / 'index.html'}")
            return True
        except subprocess.CalledProcessError:
            print("❌ Build failed! Make sure Sphinx is installed: pip install sphinx")
            return False
        except FileNotFoundError:
            print("❌ Sphinx not found! Install it with: pip install sphinx")
            return False
    
    def serve(self, port=8000):
        """Serve documentation locally."""
        html_dir = self.build_dir / 'html'
        if not html_dir.exists():
            print("❌ No built documentation found. Building now...")
            if not self.build():
                return
        
        print(f"\n🌐 Serving at http://localhost:{port}")
        print("   Press Ctrl+C to stop\n")
        
        # Open browser
        webbrowser.open(f'http://localhost:{port}')
        
        # Serve
        os.chdir(html_dir)
        if sys.version_info >= (3, 0):
            from http.server import HTTPServer, SimpleHTTPRequestHandler
            httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n✋ Stopped")
        else:
            print("❌ Python 3 required for serving")


def main():
    """Main entry point with simple interface."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='PyAutoDoc - Automatic Python Documentation',
        epilog='Just run without arguments to set up and build!'
    )
    parser.add_argument('command', nargs='?', choices=['setup', 'build', 'serve', 'clean'],
                       help='Command to run (optional)')
    parser.add_argument('--port', type=int, default=8000, help='Port for serving (default: 8000)')
    
    args = parser.parse_args()
    
    autodoc = SimpleAutoDoc()
    
    # If no command, do setup and build
    if not args.command:
        print("🚀 PyAutoDoc - Automatic Documentation Generator\n")
        if not autodoc.docs_dir.exists():
            if autodoc.setup():
                print("\n🔨 Building documentation...")
                autodoc.build()
        else:
            print("📁 Documentation already exists. Building...")
            autodoc.build()
    
    elif args.command == 'setup':
        autodoc.setup()
    
    elif args.command == 'build':
        autodoc.build()
    
    elif args.command == 'serve':
        autodoc.serve(args.port)
    
    elif args.command == 'clean':
        if autodoc.docs_dir.exists():
            shutil.rmtree(autodoc.docs_dir)
            print("✅ Cleaned documentation")
        else:
            print("ℹ️  Nothing to clean")


if __name__ == '__main__':
    main()