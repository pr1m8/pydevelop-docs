#!/usr/bin/env python3
"""
PyAutoDoc - Universal Python Documentation Generator

Drop this into any Python project and run it to automatically generate
beautiful Sphinx documentation for all your packages.

Usage:
    python pyautodoc.py init      # Initialize documentation
    python pyautodoc.py build     # Build documentation
    python pyautodoc.py serve     # Serve documentation locally
    python pyautodoc.py clean     # Clean build artifacts
"""

import os
import sys
import shutil
import subprocess
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import tempfile
import webbrowser
from contextlib import contextmanager

# Try to import tomllib (Python 3.11+) or fallback to tomli
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("Error: tomli/tomllib not found. Install with: pip install tomli")
        sys.exit(1)


@dataclass
class PackageInfo:
    """Information about a discovered package."""
    name: str
    path: Path
    has_setup_py: bool
    has_pyproject: bool
    has_src_layout: bool
    source_dir: Path
    is_namespace: bool = False
    version: str = "0.1.0"
    description: str = ""


class PyAutoDoc:
    """Universal documentation generator for Python projects."""
    
    # Embedded configuration template
    UNIFIED_CONFIG = '''"""
Auto-generated Sphinx configuration by PyAutoDoc.
This configuration is self-contained and works with any Python project.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Package-specific color schemes
PACKAGE_THEMES = {{
    'default': ('#2563eb', '#1d4ed8'),
}}

def get_package_version(package_path: Path) -> str:
    """Extract version from package."""
    try:
        # Try __version__.py
        version_file = package_path / "__version__.py"
        if version_file.exists():
            namespace = {{}}
            exec(version_file.read_text(), namespace)
            return namespace.get('__version__', '0.1.0')
        
        # Try __init__.py
        init_file = package_path / "__init__.py"
        if init_file.exists():
            content = init_file.read_text()
            for line in content.split('\\n'):
                if '__version__' in line and '=' in line:
                    version = line.split('=')[1].strip().strip('"\\\'')
                    return version
    except Exception:
        pass
    return '0.1.0'

def create_config(project_name: str, project_path: str, packages: List[Dict[str, Any]] = None, is_root: bool = False) -> Dict[str, Any]:
    """Create Sphinx configuration."""
    
    project_path = Path(project_path)
    
    # Add source paths to Python path
    if packages:
        for pkg in packages:
            src_path = Path(pkg['source_dir'])
            if src_path.exists():
                sys.path.insert(0, str(src_path))
    
    config = {
        # Project information
        'project': project_name,
        'author': project_name + ' Contributors',
        'copyright': '2025, ' + project_name + ' Contributors',
        'version': '0.1.0',
        'release': '0.1.0',
        
        # Extensions - essentials only
        'extensions': [
            'sphinx.ext.autodoc',
            'sphinx.ext.napoleon',
            'sphinx.ext.viewcode',
            'sphinx.ext.intersphinx',
            'myst_parser',
        ],
        
        # Paths
        'templates_path': ['_templates'],
        'exclude_patterns': ['_build', 'Thumbs.db', '.DS_Store'],
        
        # Source parsing
        'source_suffix': {
            '.rst': None,
            '.md': None,
        },
        'master_doc': 'index',
        'language': 'en',
        
        # Intersphinx
        'intersphinx_mapping': {
            'python': ('https://docs.python.org/3/', None),
        },
        
        # Napoleon settings
        'napoleon_google_docstring': True,
        'napoleon_numpy_docstring': True,
        'napoleon_include_init_with_doc': True,
        'napoleon_include_private_with_doc': False,
        'napoleon_include_special_with_doc': True,
        'napoleon_use_admonition_for_examples': True,
        'napoleon_use_admonition_for_notes': True,
        
        # Autodoc settings
        'autodoc_default_options': {
            'members': True,
            'member-order': 'bysource',
            'special-members': '__init__',
            'undoc-members': True,
            'exclude-members': '__weakref__',
        },
        
        # MyST settings
        'myst_enable_extensions': [
            'deflist',
            'tasklist',
            'colon_fence',
        ],
        
        # HTML output
        'html_theme': 'alabaster',
        'html_theme_options': {
            'description': f'Documentation for {project_name}',
            'fixed_sidebar': True,
        },
    }
    
    # Try to use better themes if available
    try:
        import sphinx_rtd_theme
        config['html_theme'] = 'sphinx_rtd_theme'
        config['html_theme_options'] = {
            'navigation_depth': 4,
            'collapse_navigation': False,
            'sticky_navigation': True,
        }
    except ImportError:
        try:
            import furo
            config['html_theme'] = 'furo'
            colors = PACKAGE_THEMES.get(project_name.lower(), PACKAGE_THEMES['default'])
            config['html_theme_options'] = {
                'light_css_variables': {
                    'color-brand-primary': colors[0],
                    'color-brand-content': colors[1],
                },
                'dark_css_variables': {
                    'color-brand-primary': colors[0],
                    'color-brand-content': colors[1],
                },
            }
        except ImportError:
            pass
    
    # Try to add optional extensions
    optional_extensions = [
        ('sphinx_copybutton', 'sphinx_copybutton'),
        ('autoapi', 'autoapi.extension'),
        ('myst_parser', 'myst_parser'),
    ]
    
    for module, extension in optional_extensions:
        try:
            __import__(module)
            if extension not in config['extensions']:
                config['extensions'].append(extension)
        except ImportError:
            continue
    
    # Configure autoapi if available
    if 'autoapi.extension' in config['extensions']:
        autoapi_dirs = []
        if packages:
            for pkg in packages:
                src_dir = Path(pkg['source_dir'])
                if src_dir.exists():
                    autoapi_dirs.append(str(src_dir))
        
        if autoapi_dirs:
            config['autoapi_dirs'] = autoapi_dirs
            config['autoapi_type'] = 'python'
            config['autoapi_options'] = [
                'members',
                'undoc-members',
                'show-inheritance',
                'show-module-summary',
            ]
    
    return config

# This will be populated by PyAutoDoc
PROJECT_NAME = "{project_name}"
PROJECT_PATH = "{project_path}"
PACKAGES = {packages}
IS_ROOT = {is_root}

# Generate configuration
globals().update(create_config(PROJECT_NAME, PROJECT_PATH, PACKAGES, IS_ROOT))
'''

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize PyAutoDoc for a project."""
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.docs_dir = self.project_root / "docs"
        self.build_dir = self.docs_dir / "_build"
        self.source_dir = self.docs_dir
        self.packages: List[PackageInfo] = []
        self.project_name = self.project_root.name
        
    def discover_packages(self) -> List[PackageInfo]:
        """Discover all Python packages in the project."""
        packages = []
        
        # Common package locations
        search_dirs = [
            self.project_root / "packages",  # Monorepo style
            self.project_root / "src",       # Src layout
            self.project_root,              # Direct packages
        ]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
                
            # Look for packages
            for path in search_dir.iterdir():
                if path.is_dir() and not path.name.startswith('.'):
                    pkg_info = self._analyze_package(path)
                    if pkg_info:
                        packages.append(pkg_info)
        
        # Also check if the project root itself is a package
        root_pkg = self._analyze_package(self.project_root)
        if root_pkg and not any(p.path == self.project_root for p in packages):
            packages.append(root_pkg)
        
        self.packages = packages
        return packages
    
    def _analyze_package(self, path: Path) -> Optional[PackageInfo]:
        """Analyze a directory to see if it's a Python package."""
        # Check for package indicators
        has_init = (path / "__init__.py").exists()
        has_setup = (path / "setup.py").exists()
        has_pyproject = (path / "pyproject.toml").exists()
        
        # Check for src layout
        src_dir = path / "src"
        has_src_layout = src_dir.exists()
        
        # Determine source directory
        if has_src_layout:
            # Check for packages in src/
            for subdir in src_dir.iterdir():
                if subdir.is_dir() and (subdir / "__init__.py").exists():
                    source_dir = src_dir
                    break
            else:
                source_dir = path
        else:
            source_dir = path
        
        # Is this a package?
        is_package = has_init or has_setup or has_pyproject or (
            has_src_layout and any(
                (src_dir / d / "__init__.py").exists() 
                for d in src_dir.iterdir() if d.is_dir()
            )
        )
        
        if not is_package:
            return None
        
        # Extract package info
        name = path.name
        version = "0.1.0"
        description = ""
        
        # Try to get info from pyproject.toml
        if has_pyproject:
            try:
                with open(path / "pyproject.toml", "rb") as f:
                    data = tomllib.load(f)
                    # Try Poetry format
                    poetry = data.get("tool", {}).get("poetry", {})
                    if poetry:
                        name = poetry.get("name", name)
                        version = poetry.get("version", version)
                        description = poetry.get("description", description)
                    # Try PEP 621 format
                    project = data.get("project", {})
                    if project:
                        name = project.get("name", name)
                        version = project.get("version", version)
                        description = project.get("description", description)
            except Exception:
                pass
        
        return PackageInfo(
            name=name,
            path=path,
            has_setup_py=has_setup,
            has_pyproject=has_pyproject,
            has_src_layout=has_src_layout,
            source_dir=source_dir,
            version=version,
            description=description
        )
    
    def init_docs(self, force: bool = False) -> bool:
        """Initialize documentation structure."""
        if self.docs_dir.exists() and not force:
            print(f"❌ Documentation already exists at {self.docs_dir}")
            print("   Use --force to overwrite")
            return False
        
        print("🔍 Discovering packages...")
        packages = self.discover_packages()
        
        if not packages:
            print("❌ No Python packages found!")
            print("   Make sure your project has __init__.py files or setup.py/pyproject.toml")
            return False
        
        print(f"📦 Found {len(packages)} package(s):")
        for pkg in packages:
            print(f"   - {pkg.name} at {pkg.path.relative_to(self.project_root)}")
        
        # Create documentation structure
        print(f"\n📁 Creating documentation at {self.docs_dir.relative_to(self.project_root)}/")
        self.docs_dir.mkdir(exist_ok=True)
        
        # Create conf.py
        self._create_conf_py()
        
        # Create index.rst
        self._create_index_rst()
        
        # Create .gitignore
        self._create_gitignore()
        
        # Create Makefile
        self._create_makefile()
        
        # Create requirements
        self._create_requirements()
        
        print("\n✅ Documentation initialized successfully!")
        print("\nNext steps:")
        print("1. Install documentation dependencies:")
        print(f"   pip install -r {self.docs_dir.relative_to(self.project_root)}/requirements.txt")
        print("2. Build documentation:")
        print("   python pyautodoc.py build")
        print("3. View documentation:")
        print("   python pyautodoc.py serve")
        
        return True
    
    def _create_conf_py(self):
        """Create Sphinx configuration file."""
        # Prepare package data for embedding
        packages_data = []
        for pkg in self.packages:
            packages_data.append({
                'name': pkg.name,
                'path': str(pkg.path),
                'source_dir': str(pkg.source_dir),
                'version': pkg.version,
            })
        
        # Get project name (try from pyproject.toml first)
        project_name = self.project_name
        if (self.project_root / "pyproject.toml").exists():
            try:
                with open(self.project_root / "pyproject.toml", "rb") as f:
                    data = tomllib.load(f)
                    project_name = (
                        data.get("tool", {}).get("poetry", {}).get("name") or
                        data.get("project", {}).get("name") or
                        project_name
                    )
            except Exception:
                pass
        
        # Format the configuration
        config_content = self.UNIFIED_CONFIG.format(
            project_name=project_name,
            project_path=str(self.project_root),
            packages=json.dumps(packages_data, indent=4),
            is_root=True
        )
        
        conf_path = self.source_dir / "conf.py"
        conf_path.write_text(config_content)
        print(f"   ✓ Created {conf_path.relative_to(self.project_root)}")
    
    def _create_index_rst(self):
        """Create main index.rst file."""
        # Build package list for toctree
        package_entries = []
        for pkg in self.packages:
            if pkg.path != self.project_root:  # Skip root package in list
                package_entries.append(f"   {pkg.name} <{pkg.name}/index>")
        
        content = f'''
{self.project_name} Documentation
{'=' * (len(self.project_name) + 14)}

Welcome to the documentation for {self.project_name}!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   api-reference
{chr(10).join(package_entries)}

Getting Started
---------------

This documentation was automatically generated by PyAutoDoc.

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install {self.project_name}

Quick Example
~~~~~~~~~~~~~

.. code-block:: python

   import {self.packages[0].name if self.packages else 'mypackage'}
   
   # Your example here

API Reference
-------------

The API documentation is automatically generated from the source code.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
'''
        
        index_path = self.source_dir / "index.rst"
        index_path.write_text(content)
        print(f"   ✓ Created {index_path.relative_to(self.project_root)}")
        
        # Create stub files
        (self.source_dir / "getting-started.rst").write_text(f'''
Getting Started
===============

Installation
------------

.. code-block:: bash

   pip install {self.project_name}

Basic Usage
-----------

Coming soon...
''')
        
        (self.source_dir / "api-reference.rst").write_text('''
API Reference
=============

.. automodule:: {module}
   :members:
   :undoc-members:
   :show-inheritance:
'''.format(module=self.packages[0].name if self.packages else 'mymodule'))
    
    def _create_gitignore(self):
        """Create .gitignore for docs directory."""
        content = '''
# Sphinx build output
_build/
_static/
_templates/

# Python
__pycache__/
*.py[cod]

# OS
.DS_Store
Thumbs.db
'''
        
        gitignore_path = self.docs_dir / ".gitignore"
        gitignore_path.write_text(content)
        print(f"   ✓ Created {gitignore_path.relative_to(self.project_root)}")
    
    def _create_makefile(self):
        """Create Makefile for Sphinx."""
        content = '''# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
'''
        
        makefile_path = self.docs_dir / "Makefile"
        makefile_path.write_text(content)
        print(f"   ✓ Created {makefile_path.relative_to(self.project_root)}")
    
    def _create_requirements(self):
        """Create requirements.txt for documentation."""
        content = '''# Documentation dependencies
sphinx>=7.0.0
myst-parser>=2.0.0

# Optional but recommended
sphinx-rtd-theme>=2.0.0
sphinx-copybutton>=0.5.0
sphinx-autoapi>=3.0.0

# For better theme (install one)
# furo>=2024.1.0
# sphinx-book-theme>=1.0.0
'''
        
        req_path = self.docs_dir / "requirements.txt"
        req_path.write_text(content)
        print(f"   ✓ Created {req_path.relative_to(self.project_root)}")
    
    def build_docs(self, clean: bool = False) -> bool:
        """Build the documentation."""
        if not self.docs_dir.exists():
            print("❌ Documentation not initialized. Run 'python pyautodoc.py init' first.")
            return False
        
        if clean and self.build_dir.exists():
            print("🧹 Cleaning build directory...")
            shutil.rmtree(self.build_dir)
        
        print("🔨 Building documentation...")
        
        # Run sphinx-build
        cmd = [
            sys.executable, "-m", "sphinx",
            "-b", "html",
            str(self.source_dir),
            str(self.build_dir / "html")
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Documentation built successfully!")
                print(f"   Output: {self.build_dir / 'html' / 'index.html'}")
                return True
            else:
                print("❌ Build failed!")
                print("Error output:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Build failed: {e}")
            return False
    
    def serve_docs(self, port: int = 8000) -> None:
        """Serve documentation locally."""
        html_dir = self.build_dir / "html"
        
        if not html_dir.exists():
            print("❌ Documentation not built. Run 'python pyautodoc.py build' first.")
            return
        
        print(f"🌐 Serving documentation at http://localhost:{port}")
        print("   Press Ctrl+C to stop")
        
        # Try to open browser
        webbrowser.open(f"http://localhost:{port}")
        
        # Start simple HTTP server
        os.chdir(html_dir)
        
        if sys.version_info >= (3, 0):
            from http.server import HTTPServer, SimpleHTTPRequestHandler
            httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
        else:
            import SimpleHTTPServer
            import SocketServer
            Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
            httpd = SocketServer.TCPServer(("localhost", port), Handler)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
    
    def clean_docs(self) -> None:
        """Clean build artifacts."""
        if self.build_dir.exists():
            print("🧹 Cleaning build directory...")
            shutil.rmtree(self.build_dir)
            print("✅ Build directory cleaned")
        else:
            print("ℹ️  Build directory doesn't exist")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="PyAutoDoc - Universal Python Documentation Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pyautodoc.py init          # Initialize documentation
  python pyautodoc.py build         # Build documentation
  python pyautodoc.py serve         # Serve documentation locally
  python pyautodoc.py clean         # Clean build artifacts
  
Advanced:
  python pyautodoc.py init --force  # Overwrite existing docs
  python pyautodoc.py build --clean # Clean before building
  python pyautodoc.py serve --port 9000  # Use custom port
"""
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize documentation')
    init_parser.add_argument('--force', action='store_true', help='Overwrite existing documentation')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build documentation')
    build_parser.add_argument('--clean', action='store_true', help='Clean before building')
    
    # Serve command
    serve_parser = subparsers.add_parser('serve', help='Serve documentation locally')
    serve_parser.add_argument('--port', type=int, default=8000, help='Port to serve on (default: 8000)')
    
    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Clean build artifacts')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create PyAutoDoc instance
    autodoc = PyAutoDoc()
    
    # Execute command
    if args.command == 'init':
        autodoc.init_docs(force=args.force)
    elif args.command == 'build':
        autodoc.build_docs(clean=args.clean)
    elif args.command == 'serve':
        autodoc.serve_docs(port=args.port)
    elif args.command == 'clean':
        autodoc.clean_docs()


if __name__ == "__main__":
    main()