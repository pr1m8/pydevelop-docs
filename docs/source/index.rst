
PyDevelop-Docs
==============

.. image:: https://img.shields.io/pypi/v/pydevelop-docs.svg
   :target: https://pypi.org/project/pydevelop-docs/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/pydevelop-docs.svg
   :target: https://pypi.org/project/pydevelop-docs/
   :alt: Python Versions

Welcome to PyDevelop-Docs - the universal Python documentation generator with 40+ Sphinx extensions pre-configured!

**Zero configuration. Beautiful documentation. It just works.**

.. admonition:: Quick Start
   :class: tip

   .. code-block:: bash

      # Install
      pip install pydevelop-docs

      # Initialize docs
      pydevelop-docs init

      # Build documentation  
      pydevelop-docs build

      # View your docs
      pydevelop-docs serve

Features
--------

- ✨ **Zero Configuration** - Works out of the box for any Python project
- 📚 **40+ Extensions** - All pre-configured and ready to use
- 🎨 **Modern Theme** - Beautiful Furo theme with dark mode
- 🔍 **Smart Detection** - Automatically detects project structure
- 📦 **Monorepo Support** - Build docs for multiple packages
- 🚀 **Fast & Reliable** - Optimized build system with error recovery

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

Why PyDevelop-Docs?
-------------------

**Before PyDevelop-Docs:**

- Hours configuring Sphinx
- Managing dozens of extensions
- Debugging theme issues
- Flat, unusable API documentation
- Inconsistent documentation across projects

**With PyDevelop-Docs:**

- 5 minutes to beautiful docs
- Everything pre-configured
- Hierarchical API documentation
- Consistent, professional results
- Focus on writing, not configuring

Project Types
-------------

PyDevelop-Docs supports all Python project structures:

**Single Package**
   Standard Python packages with ``src/`` or flat layout

**Monorepo**
   Multiple packages in one repository

**Django/Flask**
   Web applications with special structure

**Data Science**
   Jupyter notebooks and research projects

**Mixed Projects**
   Any combination of the above

Getting Help
------------

- **GitHub Issues**: `Report bugs and request features <https://github.com/pydevelop/pydevelop-docs/issues>`_
- **Discussions**: `Ask questions and share tips <https://github.com/pydevelop/pydevelop-docs/discussions>`_
- **Examples**: Check out the :doc:`examples` page

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
