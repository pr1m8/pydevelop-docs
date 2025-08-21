test-haive-template Quick Start
===============================

Welcome to test-haive-template! This guide will get you up and running in under 5 minutes.

.. contents:: Table of Contents
   :local:
   :depth: 2

Installation
------------

Install test-haive-template using pip::

    pip install test-haive-template

Or with Poetry::

    poetry add test-haive-template

Or for development::

    git clone https://github.com/your-org/test-haive-template.git
    cd test-haive-template
    poetry install

First Steps
-----------

1. **Initialize Documentation**

   Navigate to your Python project and run::

       pydvlppy init

   This creates a ``docs/`` directory with everything configured.

2. **Build Documentation**

   Generate your documentation::

       pydvlppy build

   Or for a clean build::

       pydvlppy build --clean

3. **View Documentation**

   Open ``docs/build/html/index.html`` in your browser, or serve it locally::

       python -m http.server 8000 --directory docs/build/html

   Then visit http://localhost:8000

What You Get
------------

Pydvlppy automatically configures:

✅ **Automatic API Documentation**
   Your entire codebase is documented with AutoAPI

✅ **40+ Sphinx Extensions**
   All the best documentation tools, pre-configured

✅ **Beautiful Theme**
   Modern, responsive Furo theme with dark mode

✅ **Search Functionality**
   Full-text search across all documentation

✅ **Hierarchical Navigation**
   Nested module structure, not flat lists

Example Project Structure
-------------------------

After initialization::

    your-project/
    ├── docs/
    │   ├── source/
    │   │   ├── conf.py          # Sphinx configuration
    │   │   ├── index.rst        # Main documentation page
    │   │   ├── _static/         # CSS/JS customizations
    │   │   └── _templates/      # Custom templates
    │   └── build/               # Generated documentation
    ├── src/                     # Your source code
    └── pyproject.toml          # Project configuration

Configuration
-------------

The generated ``conf.py`` uses our shared configuration system. To customize, edit ``docs/source/conf.py``:

.. code-block:: python

    # Add custom extensions
    extensions.append("sphinx_click")
    
    # Change theme
    html_theme = "sphinx_rtd_theme"
    
    # Add custom CSS
    html_css_files = ["custom.css"]

Common Commands
---------------

.. code-block:: bash

    # Initialize with all sections
    pydvlppy init --with-examples --with-tutorials --with-guides
    
    # Build specific package (monorepo)
    pydvlppy build --package my-package
    
    # Clean all build artifacts
    pydvlppy clean
    
    # Check for issues
    pydvlppy doctor

Troubleshooting
---------------

**Import Errors**
    Ensure your package is installed::
    
        pip install -e .

**Missing API Documentation**
    Check ``autoapi_dirs`` in ``conf.py`` points to your source code.

**Build Warnings**
    Run with ``--keep-going`` to see all issues::
    
        poetry run sphinx-build -b html docs/source docs/build -W --keep-going

Next Steps
----------

- :doc:`/guides/configuration` - Customize your documentation
- :doc:`/tutorials/first_steps` - Detailed walkthrough
- :doc:`/examples/index` - See real examples
- :doc:`/cli/commands` - CLI reference

Getting Help
------------

- `Documentation <https://pydvlppy.readthedocs.io>`_
- `GitHub Issues <https://github.com/your-org/test-haive-template/issues>`_
- `Discussions <https://github.com/your-org/test-haive-template/discussions>`_

Happy documenting! 🚀