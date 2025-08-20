
PyDevelop-Docs 📚
=================

.. image:: https://img.shields.io/pypi/v/pydevelop-docs.svg
   :target: https://pypi.org/project/pydevelop-docs/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/pydevelop-docs.svg
   :target: https://pypi.org/project/pydevelop-docs/
   :alt: Python Versions

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT License

**The Universal Python Documentation Generator with 40+ Sphinx Extensions Pre-Configured**

Transform any Python project into beautiful, professional documentation in minutes.
**Zero configuration. Beautiful results. It just works.**

.. grid:: 1 2 2 3
   :gutter: 2

   .. grid-item-card:: 🎯 Zero Configuration
      :shadow: sm

      Works immediately with any Python project structure. No setup, no hassle.

   .. grid-item-card:: 📦 Universal Support
      :shadow: sm
      
      Monorepos, single packages, src layouts, flat layouts - all supported.

   .. grid-item-card:: 🎨 Beautiful Themes  
      :shadow: sm
      
      Professional Furo theme with dark mode and responsive design.

   .. grid-item-card:: 🔧 40+ Extensions
      :shadow: sm
      
      Complete extension ecosystem pre-configured and optimized.

   .. grid-item-card:: ⚡ Smart Detection
      :shadow: sm
      
      Automatically detects project structure and configures paths.

   .. grid-item-card:: 🚀 One Command
      :shadow: sm
      
      ``pydevelop-docs setup-general /project`` and you're done!

.. admonition:: ⚡ Quick Start - Any Python Project
   :class: tip

   .. code-block:: bash

      # Install
      pip install pydevelop-docs

      # Set up docs for ANY Python project
      pydevelop-docs setup-general /path/to/your/project

      # Build beautiful documentation  
      cd /path/to/your/project/docs && make html

      # Your docs are ready at build/html/index.html! 🎉

.. admonition:: 🎊 This Documentation Was Built With PyDevelop-Docs
   :class: note

   This very documentation you're reading was generated using PyDevelop-Docs itself!
   It showcases all the features: AutoAPI with hierarchical organization, 
   custom Jinja2 templates, 40+ extensions, and professional styling.

🌟 Core Features
----------------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: 🎯 **Zero Configuration**
      :shadow: md
      
      * Automatic project detection
      * Smart path configuration  
      * Metadata extraction from pyproject.toml
      * Works with Poetry, setuptools, pip, conda
      
   .. grid-item-card:: 📦 **Universal Project Support**
      :shadow: md
      
      * **Monorepos**: packages/ directory structures
      * **Src Layout**: src/package_name/ organization
      * **Flat Layout**: package in project root
      * **Simple Projects**: Basic Python files

   .. grid-item-card:: 🎨 **Professional Appearance**
      :shadow: md
      
      * Beautiful Furo theme with dark mode
      * Responsive design for all devices
      * Custom CSS enhancements
      * Professional navigation
      
   .. grid-item-card:: ⚡ **Smart CLI Commands**
      :shadow: md
      
      * ``setup-general``: Universal project setup
      * ``copy-setup``: Transfer between projects
      * Interactive and batch modes
      * Dry-run capability

🔧 Sphinx Extensions Ecosystem (40+)
------------------------------------

PyDevelop-Docs includes a carefully curated collection of 40+ Sphinx extensions, all pre-configured and optimized:

.. tab-set::

   .. tab-item:: 📚 Core Documentation

      * **sphinx.ext.autodoc** - Automatic API documentation
      * **sphinx.ext.napoleon** - Google/NumPy docstring support  
      * **sphinx.ext.viewcode** - Source code links
      * **sphinx.ext.intersphinx** - Cross-project linking
      * **sphinx.ext.todo** - TODO directive support
      * **sphinx.ext.coverage** - Documentation coverage analysis
      * **sphinx.ext.mathjax** - Mathematical notation support

   .. tab-item:: 🔍 API Documentation

      * **autoapi.extension** - Automatic API reference with **hierarchical organization**
      * **sphinx_autodoc_typehints** - Type hint documentation
      * **sphinxcontrib.autodoc_pydantic** - Pydantic model documentation
      
      .. admonition:: 🎯 AutoAPI Hierarchical Fix
         :class: tip
         
         We solve the flat API problem! Instead of 200+ classes in alphabetical chaos,
         get organized hierarchical navigation: ``autoapi_own_page_level = "module"``

   .. tab-item:: ✨ Enhanced Features

      * **myst_parser** - Markdown support in documentation
      * **sphinx_copybutton** - Copy code buttons
      * **sphinx_design** - Modern UI components (cards, grids, tabs)
      * **sphinx_tabs** - Tabbed content organization
      * **sphinx_togglebutton** - Collapsible content sections
      * **sphinx_inline_tabs** - Inline tab interfaces

   .. tab-item:: 📊 Diagramming & Visualization

      * **sphinxcontrib.mermaid** - Flowcharts and diagrams
      * **sphinxcontrib.plantuml** - UML diagrams  
      * **sphinxcontrib.blockdiag** - Block diagrams
      * **sphinxcontrib.seqdiag** - Sequence diagrams
      * **sphinx.ext.graphviz** - Graph visualization

   .. tab-item:: 💻 Code & Examples

      * **sphinx_codeautolink** - Automatic code linking
      * **sphinx_exec_code** - Execute and display code results
      * **sphinx_runpython** - Run Python code in docs
      
      .. code-block:: python
         :caption: Example: Auto-linked code
         
         from pydevelop_docs.config import get_haive_config
         config = get_haive_config("my-package", "../../src")

   .. tab-item:: 🎨 UI Enhancements

      * **sphinx_tippy** - Enhanced tooltips
      * **sphinx_favicon** - Custom favicon support
      * **sphinxemoji** - Emoji support in documentation
      
      Example: :bdg-primary:`Primary` :bdg-secondary:`Secondary` :bdg-success:`Success`

   .. tab-item:: 🔍 SEO & Discovery

      * **sphinx_sitemap** - SEO sitemaps for search engines
      * **sphinxext.opengraph** - Social media previews  
      * **sphinx_last_updated_by_git** - Git-based change tracking
      * **sphinx_reredirects** - URL redirection management

   .. tab-item:: 🛠️ Development Tools

      * **sphinx_toolbox** - Enhanced development utilities
      * **sphinxcontrib.treeview** - Directory tree visualization
      * **sphinxcontrib.enum_tools** - Enum documentation support
      * **sphinx_notfound_page** - Custom 404 page generation

🎨 Custom Jinja2 Templates
--------------------------

PyDevelop-Docs includes professionally designed Jinja2 templates for enhanced documentation:

.. grid:: 1 2 2 2
   :gutter: 2

   .. grid-item-card:: 📝 **AutoAPI Templates**
      :shadow: sm
      
      * Custom module and class layouts
      * Hierarchical organization
      * Enhanced navigation
      * Professional formatting

   .. grid-item-card:: 🎯 **Pydantic Templates**  
      :shadow: sm
      
      * Model configuration display
      * Validator documentation
      * Computed field support
      * Summary panels

   .. grid-item-card:: 🖥️ **CLI Templates**
      :shadow: sm
      
      * Command documentation
      * Option descriptions
      * Quick reference
      * Usage examples

   .. grid-item-card:: 🏷️ **Layout Templates**
      :shadow: sm
      
      * Custom page layouts
      * Badge systems
      * Warning displays
      * Enhanced branding

.. admonition:: 🎨 Template Customization
   :class: tip
   
   All templates are fully customizable! Check ``docs/source/_templates/`` to see
   how we've enhanced the standard Sphinx templates with modern design and functionality.

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   getting_started
   configuration
   themes
   
.. toctree::
   :maxdepth: 2  
   :caption: Reference:

   cli-reference
   autoapi/index
   examples
   
.. toctree::
   :maxdepth: 1
   :caption: Project:

   changelog
   guides/index

🚀 Why PyDevelop-Docs?
----------------------

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: ❌ **Before PyDevelop-Docs**
      :shadow: md
      :class-header: bg-danger text-white
      
      * **Hours** configuring Sphinx
      * Managing **dozens** of extensions  
      * Debugging theme issues
      * **Flat, unusable** API documentation
      * Inconsistent docs across projects
      * Complex build setups
      * Version conflicts and dependencies

   .. grid-item-card:: ✅ **With PyDevelop-Docs**
      :shadow: md
      :class-header: bg-success text-white
      
      * **5 minutes** to beautiful docs
      * Everything **pre-configured**
      * **Hierarchical** API documentation  
      * Consistent, professional results
      * Focus on **writing**, not configuring
      * One command setup
      * Zero dependency conflicts

.. admonition:: 📊 Comparison Table
   :class: tip

   .. list-table::
      :header-rows: 1
      :widths: 25 25 25 25

      * - Feature
        - **PyDevelop-Docs**
        - Manual Sphinx
        - Other Tools
      * - **Setup Time**
        - **< 1 minute**
        - Hours
        - Minutes
      * - **Extension Count**
        - **40+**
        - 0
        - 5-10
      * - **AutoAPI Hierarchy**
        - **✅ Fixed**
        - ❌ Flat
        - ❌ Flat
      * - **Project Detection**
        - **✅ Automatic**
        - ❌ Manual
        - ⚠️ Limited
      * - **Theme Quality**
        - **✅ Professional**
        - ⚠️ Basic
        - ⚠️ Varies
      * - **Jinja2 Templates**
        - **✅ Custom**
        - ❌ None
        - ❌ Basic

🏗️ Supported Project Structures
--------------------------------

PyDevelop-Docs intelligently detects and supports **all** Python project structures:

.. tab-set::

   .. tab-item:: 📦 Single Package Projects

      .. code-block:: text
      
         my-package/
         ├── src/
         │   └── my_package/
         │       ├── __init__.py
         │       └── core.py
         ├── tests/
         ├── docs/  # ← Created here
         └── pyproject.toml

      **Detection**: ✅ Single Package | **AutoAPI**: ``['../../src']``

   .. tab-item:: 🏢 Monorepo Projects

      .. code-block:: text
      
         my-monorepo/
         ├── packages/
         │   ├── package-a/
         │   │   └── src/package_a/
         │   ├── package-b/
         │   │   └── src/package_b/
         │   └── package-c/
         │       └── src/package_c/
         ├── docs/  # ← Central hub
         └── pyproject.toml

      **Detection**: ✅ Monorepo | **AutoAPI**: ``['../packages']``

   .. tab-item:: 📁 Flat Layout Projects

      .. code-block:: text
      
         my-project/
         ├── my_package/
         │   ├── __init__.py
         │   └── modules.py
         ├── tests/
         ├── docs/  # ← Created here
         └── pyproject.toml

      **Detection**: ✅ Flat Layout | **AutoAPI**: ``['../my_package']``

   .. tab-item:: 🧪 Simple Projects

      .. code-block:: text
      
         my-scripts/
         ├── main.py
         ├── utils.py
         ├── helpers.py
         ├── docs/  # ← Created here
         └── requirements.txt

      **Detection**: ✅ Simple Project | **AutoAPI**: ``['..']``

.. admonition:: 🎯 Smart Detection Magic
   :class: note
   
   No matter how complex your project structure, PyDevelop-Docs automatically:
   
   * **Detects** your project type (monorepo, single package, simple project)
   * **Extracts** metadata from pyproject.toml, setup.py, or package files
   * **Configures** AutoAPI paths for perfect documentation generation
   * **Sets up** all 40+ extensions with optimal configurations

Getting Help & Contact
----------------------

.. grid:: 1 2 2 2
   :gutter: 2

   .. grid-item-card:: 🐛 **Bug Reports & Features**
      :shadow: sm
      
      `GitHub Issues <https://github.com/pr1m8/pydevelop-docs/issues>`_
      
      Report bugs, request features, or suggest improvements.

   .. grid-item-card:: 💬 **Questions & Discussion**  
      :shadow: sm
      
      `GitHub Discussions <https://github.com/pr1m8/pydevelop-docs/discussions>`_
      
      Ask questions, share tips, and connect with the community.

   .. grid-item-card:: 📖 **Examples & Tutorials**
      :shadow: sm
      
      :doc:`examples`
      
      Real-world examples and step-by-step tutorials.

   .. grid-item-card:: 👨‍💻 **Author**
      :shadow: sm
      
      `William R. Astley <https://will.astley.dev>`_
      
      Personal website and portfolio.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
