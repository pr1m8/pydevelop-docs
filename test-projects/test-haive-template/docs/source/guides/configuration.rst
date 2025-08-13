Configuration Guide
===================

Comprehensive guide to configuring test-haive-template for your specific needs.

.. contents:: Table of Contents
   :local:
   :depth: 3

Overview
--------

test-haive-template can be configured through:

- Configuration files (recommended)
- Environment variables
- Runtime parameters
- API configuration


Advanced Configuration
----------------------


**Intersphinx Mapping:**

.. code-block:: python

   # Link to external documentation
   intersphinx_mapping = {
       "python": ("https://docs.python.org/3", None),
       "sphinx": ("https://www.sphinx-doc.org/en/master", None),
       "pydantic": ("https://docs.pydantic.dev/latest", None),
   }

**MyST (Markdown) Support:**

.. code-block:: python

   # Enhanced Markdown features
   myst_enable_extensions = [
       "colon_fence",      # ::: code blocks
       "deflist",          # Definition lists  
       "fieldlist",        # Field lists
       "html_admonition",  # HTML-style admonitions
       "html_image",       # HTML images
       "linkify",          # Auto-link URLs
       "replacements",     # Text replacements
       "smartquotes",      # Smart quotes
       "strikethrough",    # ~~strikethrough~~
       "substitution",     # Variable substitution
       "tasklist",         # - [ ] Task lists
   ]

Environment Variables
---------------------


Common Customizations
---------------------

**Adding Custom Extensions:**

.. code-block:: python

   # Add to existing extensions
   extensions.extend([
       "sphinx_click",           # CLI documentation
       "sphinxcontrib.openapi",  # OpenAPI specs
       "sphinx_external_toc",    # External TOC
   ])

**Custom Code Block Styling:**

.. code-block:: python

   # Syntax highlighting
   pygments_style = "sphinx"
   pygments_dark_style = "monokai"  # Dark mode
   
   # Code block options
   highlight_language = "python"
   highlight_options = {
       "stripnl": False,
       "stripall": False,
   }

**PDF Output (LaTeX):**

.. code-block:: python

   # LaTeX configuration for PDF
   latex_elements = {
       "papersize": "letterpaper",
       "pointsize": "10pt",
       "preamble": r"\usepackage{sphinx}",
   }
   
   latex_documents = [(
       "index",               # Source start file
       "test-haive-template.tex",  # Target name
       "test-haive-template Documentation",  # Title
       "Your Team",           # Author
       "manual",              # Document class
   )]

Real-World Examples
-------------------

**Example 1: API-Heavy Project**

.. code-block:: python

   # Focus on API documentation
   autoapi_options = [
       "members", "undoc-members", "show-inheritance",
       "show-module-summary", "special-members",
   ]
   
   # Detailed API display
   autodoc_default_options = {
       "members": True,
       "inherited-members": True,
       "show-inheritance": True,
   }

**Example 2: Tutorial-Heavy Project**

.. code-block:: python

   # Emphasis on narrative documentation
   html_theme_options.update({
       "navigation_depth": 3,
       "collapse_navigation": True,  # Collapse API sections
   })
   
   # Custom TOC structure
   html_sidebars = {
       "**": [
           "sidebar/brand.html",
           "sidebar/search.html", 
           "sidebar/navigation.html",
       ]
   }


Troubleshooting Configuration
-----------------------------

**Common Issues:**

.. tab-set::

    .. tab-item:: Extension Conflicts

        .. code-block:: python

            # Check extension loading order
            extensions = [
                "autoapi.extension",      # Must be first
                # ... other extensions
                "sphinx_toolbox",         # Before sphinx_autodoc_typehints
                "sphinx_autodoc_typehints",  # Must be after sphinx_toolbox
            ]

    .. tab-item:: Import Errors

        .. code-block:: bash

            # Ensure package is importable
            python -c "import your_package"
            
            # Check PYTHONPATH
            export PYTHONPATH=/path/to/your/src:$PYTHONPATH

    .. tab-item:: Build Warnings

        .. code-block:: bash

            # Build with detailed warnings
            sphinx-build -b html source build -W --keep-going -v

**Debug Mode:**

.. code-block:: bash

   # Enable Sphinx debug output
   sphinx-build -b html source build -v -v -v
   

**Configuration Validation:**

.. code-block:: python

   # Add to conf.py for debugging
   def setup(app):
       """Sphinx setup hook for debugging."""
       print(f"Extensions loaded: {app.config.extensions}")
       print(f"AutoAPI dirs: {app.config.autoapi_dirs}")
       print(f"Theme: {app.config.html_theme}")

Migration from Other Tools
--------------------------


**From Plain Sphinx:**

1. Backup existing ``conf.py``
2. Run ``test-haive-template init`` to generate new config
3. Merge custom settings from backup
4. Test build and adjust as needed

Best Practices
--------------

**Performance:**

- Use ``autoapi_own_page_level = "module"`` for better organization
- Enable parallel builds: ``sphinx-build -j auto``
- 
**Maintainability:**

- Document your customizations in comments
- Use version control for ``conf.py``
- Test builds in CI/CD
- Keep extensions up to date

**User Experience:**

- Enable search functionality
- Use clear navigation structure
- Add cross-references between sections
- Include examples and tutorials

Getting Help
------------

**Configuration Issues:**

1. Check the `configuration examples <https://github.com/your-org/test-haive-template/tree/main/examples>`_
2. Search `GitHub issues <https://github.com/your-org/test-haive-template/issues?q=configuration>`_
3. Ask in `discussions <https://github.com/your-org/test-haive-template/discussions>`_

**Next Steps:**

- 🚀 **Quick Start**: :doc:`quickstart` - Get up and running
- 📖 **Installation**: :doc:`installation` - Detailed setup
- 💡 **Examples**: :doc:`../examples/index` - Real-world configurations
- 🎯 **Tutorials**: :doc:`../tutorials/first_steps` - Step-by-step guides

.. tip::
   **Pro Tip**: Start with shared configuration and only customize what you need. Most projects work great with the defaults!