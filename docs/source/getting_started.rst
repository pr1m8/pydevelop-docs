Getting Started
===============

Welcome to PyDevelop-Docs! This guide will help you get started with creating beautiful documentation for your Python projects.

.. contents:: Table of Contents
   :local:
   :depth: 2

Quick Start
-----------

PyDevelop-Docs provides a zero-configuration documentation system with 40+ pre-configured Sphinx extensions.

Installation
^^^^^^^^^^^^

Install PyDevelop-Docs using pip or poetry:

.. code-block:: bash

   pip install pydvlp-docs
   # or
   poetry add pydvlp-docs

Basic Usage
^^^^^^^^^^^

1. **Initialize documentation for your project:**

   .. code-block:: bash

      pydvlp-docs init

2. **Build the documentation:**

   .. code-block:: bash

      pydvlp-docs build

3. **View your documentation:**

   .. code-block:: bash

      pydvlp-docs serve
      # Open http://localhost:8000 in your browser

Project Types
-------------

PyDevelop-Docs automatically detects your project structure and configures itself accordingly.

Single Package
^^^^^^^^^^^^^^

For a standard Python package:

.. code-block:: bash

   my-package/
   ├── src/
   │   └── my_package/
   │       └── __init__.py
   ├── pyproject.toml
   └── README.md

Run ``pydvlp-docs init`` in the project root.

Monorepo
^^^^^^^^

For projects with multiple packages:

.. code-block:: bash

   my-monorepo/
   ├── packages/
   │   ├── package-a/
   │   ├── package-b/
   │   └── package-c/
   └── pyproject.toml

PyDevelop-Docs will detect the monorepo structure and offer to build documentation for all packages.

Features
--------

Automatic API Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

PyDevelop-Docs uses Sphinx AutoAPI to automatically generate comprehensive API documentation from your code:

- Hierarchical organization (not flat alphabetical lists)
- Classes, functions, and modules all documented
- Type hints and docstrings fully supported
- Pydantic model documentation with field details

Professional Themes
^^^^^^^^^^^^^^^^^^^

Comes pre-configured with the Furo theme:

- Modern, clean design
- Built-in dark mode support
- Mobile-responsive layout
- Fast search functionality

40+ Extensions
^^^^^^^^^^^^^^

All these extensions are pre-configured and ready to use:

- **Diagrams**: Mermaid, PlantUML, Graphviz
- **Code**: Syntax highlighting, copy buttons, line numbers
- **Enhancements**: Tabs, toggles, admonitions
- **SEO**: Sitemaps, OpenGraph, social cards
- **More**: Git integration, contributors, requirements tracking

Next Steps
----------

- Read the :doc:`configuration` guide for customization options
- Explore :doc:`themes` for styling your documentation  
- Check out :doc:`examples` for real-world usage
- View the :doc:`autoapi/index` for the complete API reference

Getting Help
------------

- **Issues**: `GitHub Issues <https://github.com/pydevelop/pydvlp-docs/issues>`_
- **Discussions**: `GitHub Discussions <https://github.com/pydevelop/pydvlp-docs/discussions>`_
- **Documentation**: You're reading it!