Configuration
=============

PyDevelop-Docs provides extensive configuration options while maintaining zero-configuration defaults.

.. contents:: Table of Contents
   :local:
   :depth: 2

Configuration Methods
---------------------

There are three ways to configure PyDevelop-Docs:

1. **Zero Configuration** (Default)
   
   Just run ``pydevelop-docs init`` and it works out of the box.

2. **Shared Configuration** (Recommended)
   
   Import the pre-configured settings in your ``conf.py``:

   .. code-block:: python

      from pydevelop_docs.config import get_haive_config
      
      config = get_haive_config(
          package_name="my-package",
          package_path="../../src"
      )
      globals().update(config)

3. **Custom Configuration**
   
   Extend or override any settings as needed.

Core Configuration
------------------

Package Configuration
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   config = get_haive_config(
       package_name="my-package",        # Your package name
       package_path="../../src",         # Path to source code
       is_central_hub=False,            # True for monorepo hubs
       extra_extensions=["my.extension"] # Additional extensions
   )

AutoAPI Configuration
^^^^^^^^^^^^^^^^^^^^^

The key to hierarchical (not flat) API documentation:

.. code-block:: python

   autoapi_own_page_level = "module"  # Group classes with modules
   autoapi_options = [
       "members",
       "undoc-members", 
       "show-inheritance",
       "show-module-summary",  # Important for hierarchy
   ]

Theme Configuration
^^^^^^^^^^^^^^^^^^^

Furo theme with professional styling:

.. code-block:: python

   html_theme = "furo"
   html_theme_options = {
       "light_css_variables": {
           "color-brand-primary": "#2563eb",
           "color-brand-content": "#1d4ed8",
       },
       "dark_css_variables": {
           "color-brand-primary": "#60a5fa",
           "color-brand-content": "#3b82f6",
       }
   }

Extension Configuration
-----------------------

MyST Parser
^^^^^^^^^^^

For Markdown support with extended features:

.. code-block:: python

   myst_enable_extensions = [
       "deflist",
       "tasklist", 
       "html_image",
       "colon_fence",
       "smartquotes",
       "replacements",
       "linkify",
       "strikethrough",
   ]

Mermaid Diagrams
^^^^^^^^^^^^^^^^

.. code-block:: python

   mermaid_params = [
       "--theme", "neutral",
       "--width", "800",
       "--backgroundColor", "transparent"
   ]

Pydantic Models
^^^^^^^^^^^^^^^

Enhanced documentation for Pydantic models:

.. code-block:: python

   autodoc_pydantic_model_show_json = True
   autodoc_pydantic_model_show_config_summary = True
   autodoc_pydantic_model_show_validator_summary = True
   autodoc_pydantic_model_show_field_summary = True

Advanced Configuration
----------------------

Monorepo Central Hub
^^^^^^^^^^^^^^^^^^^^

For documentation hubs that aggregate multiple packages:

.. code-block:: python

   from pydevelop_docs.config import get_central_hub_config
   
   config = get_central_hub_config()
   globals().update(config)

This enables sphinx-collections for aggregating package docs.

Custom Templates
^^^^^^^^^^^^^^^^

Override default templates:

.. code-block:: python

   templates_path = ["_templates"]
   autoapi_template_dir = "_autoapi_templates"

Custom CSS/JS
^^^^^^^^^^^^^

Add custom styling and scripts:

.. code-block:: python

   html_css_files = [
       "custom.css",
       "theme-overrides.css",
   ]
   
   html_js_files = [
       "custom.js",
       ("analytics.js", {"async": "async"}),
   ]

Environment Variables
---------------------

PyDevelop-Docs respects these environment variables:

- ``PYDEVELOP_DOCS_THEME``: Override default theme
- ``PYDEVELOP_DOCS_DEBUG``: Enable debug output
- ``PYDEVELOP_DOCS_WORKERS``: Number of parallel workers

Command Line Options
--------------------

Configuration via CLI flags:

.. code-block:: bash

   # Force regeneration
   pydevelop-docs build --force
   
   # Use specific config file
   pydevelop-docs build --config myconfig.yaml
   
   # Enable debug mode
   pydevelop-docs build --debug
   
   # Parallel builds for monorepos
   pydevelop-docs build-all --parallel 4

Best Practices
--------------

1. **Use Shared Configuration**
   
   Start with ``get_haive_config()`` and override only what you need.

2. **Keep It Simple**
   
   The defaults are carefully tuned. Only change what's necessary.

3. **Version Control**
   
   Commit your ``docs/source/conf.py`` to track configuration changes.

4. **Test Locally**
   
   Always test with ``pydevelop-docs build && pydevelop-docs serve`` before deploying.

5. **Monitor Build Output**
   
   Use ``--debug`` flag to diagnose configuration issues.

Troubleshooting
---------------

Common Issues
^^^^^^^^^^^^^

**Flat API Documentation**
   Ensure ``autoapi_own_page_level = "module"`` is set.

**Missing Extensions**
   Install with ``pip install pydevelop-docs[all]``

**Theme Not Loading**
   Check that Furo is installed: ``pip install furo``

**Build Errors**
   Run with ``--debug`` flag for detailed output.

Debug Mode
^^^^^^^^^^

Enable comprehensive debugging:

.. code-block:: bash

   pydevelop-docs build --debug --save-log
   
   # View the log
   cat /tmp/pydevelop_build.log

Next Steps
----------

- Explore :doc:`themes` for visual customization
- Read about :doc:`getting_started` for quick setup
- Check :doc:`examples` for real-world configurations