Themes and Styling
==================

PyDevelop-Docs comes with professional theming out of the box, featuring the modern Furo theme with extensive customization options.

.. contents:: Table of Contents
   :local:
   :depth: 2

Default Theme: Furo
-------------------

PyDevelop-Docs uses `Furo <https://pradyunsg.me/furo/>`_, a clean and modern Sphinx theme designed for technical documentation.

Features
^^^^^^^^

- **Clean, modern design** focused on readability
- **Built-in dark mode** with automatic OS detection
- **Mobile responsive** layout that works on all devices
- **Fast search** with keyboard shortcuts
- **Customizable colors** via CSS variables
- **Professional typography** with system font stacks

Color Customization
-------------------

Brand Colors
^^^^^^^^^^^^

Customize your documentation's brand colors:

.. code-block:: python

   html_theme_options = {
       "light_css_variables": {
           "color-brand-primary": "#2563eb",    # Primary brand color
           "color-brand-content": "#1d4ed8",    # Links and accents
       },
       "dark_css_variables": {
           "color-brand-primary": "#60a5fa",    # Primary in dark mode
           "color-brand-content": "#3b82f6",    # Links in dark mode
       }
   }

Complete Color System
^^^^^^^^^^^^^^^^^^^^^

All available CSS variables:

.. code-block:: python

   "light_css_variables": {
       # Brand colors
       "color-brand-primary": "#2563eb",
       "color-brand-content": "#1d4ed8", 
       
       # Background colors
       "color-background-primary": "#ffffff",
       "color-background-secondary": "#f8fafc",
       "color-background-hover": "#e2e8f0",
       "color-background-border": "#cbd5e1",
       
       # Code blocks
       "color-code-background": "#1e293b",
       "color-code-foreground": "#e2e8f0",
       
       # Sidebar
       "color-sidebar-background": "#0f172a",
       "color-sidebar-foreground": "#cbd5e1",
       
       # API documentation
       "color-api-background": "#f1f5f9",
       "color-api-background-hover": "#e2e8f0",
   }

Custom CSS
----------

Adding Custom Styles
^^^^^^^^^^^^^^^^^^^^

1. Create custom CSS file:

   .. code-block:: bash

      touch docs/source/_static/custom.css

2. Add to configuration:

   .. code-block:: python

      html_css_files = [
          "custom.css",
      ]

3. Write your custom styles:

   .. code-block:: css

      /* Custom styles */
      .my-custom-class {
          background-color: var(--color-brand-primary);
          color: white;
          padding: 1rem;
          border-radius: 0.5rem;
      }

CSS Architecture
^^^^^^^^^^^^^^^^

PyDevelop-Docs includes these CSS files:

- ``api-docs.css`` - API documentation styling
- ``custom.css`` - General customizations
- ``furo-intense.css`` - Dark mode enhancements
- ``mermaid-custom.css`` - Diagram styling
- ``tippy-enhancements.css`` - Tooltip improvements
- ``toc-enhancements.css`` - Table of contents styling

Dark Mode
---------

Automatic Detection
^^^^^^^^^^^^^^^^^^^

Dark mode automatically activates based on:

1. User's OS preference
2. Manual toggle in documentation
3. Time of day (if configured)

Customizing Dark Mode
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: css

   /* Target dark mode specifically */
   [data-theme="dark"] {
       --color-custom: #your-color;
   }
   
   /* Override specific dark mode elements */
   [data-theme="dark"] .admonition {
       background-color: rgba(255, 255, 255, 0.05);
   }

Advanced Styling
----------------

Custom Admonitions
^^^^^^^^^^^^^^^^^^

Create custom styled boxes:

.. code-block:: css

   .admonition.custom-note {
       border-left: 4px solid var(--color-brand-primary);
       background-color: rgba(37, 99, 235, 0.1);
   }
   
   .admonition.custom-note > .admonition-title {
       background-color: rgba(37, 99, 235, 0.2);
   }

API Documentation Styling
^^^^^^^^^^^^^^^^^^^^^^^^^

Enhance API documentation appearance:

.. code-block:: css

   /* Style class documentation */
   .py.class {
       border-left: 3px solid var(--color-brand-primary);
       padding-left: 1rem;
       margin: 1rem 0;
   }
   
   /* Style function signatures */
   .sig-prename {
       color: var(--color-brand-content);
       font-weight: 600;
   }

Responsive Design
^^^^^^^^^^^^^^^^^

Mobile-first responsive utilities:

.. code-block:: css

   /* Mobile styles */
   @media (max-width: 768px) {
       .custom-grid {
           grid-template-columns: 1fr;
       }
   }
   
   /* Tablet and up */
   @media (min-width: 769px) {
       .custom-grid {
           grid-template-columns: repeat(2, 1fr);
       }
   }
   
   /* Desktop */
   @media (min-width: 1024px) {
       .custom-grid {
           grid-template-columns: repeat(3, 1fr);
       }
   }

Theme Components
----------------

Navigation
^^^^^^^^^^

Customize the navigation sidebar:

.. code-block:: python

   html_theme_options = {
       "sidebar_hide_name": False,  # Show project name
       "navigation_with_keys": True,  # Keyboard navigation
   }

Footer
^^^^^^

Add custom footer content:

.. code-block:: python

   html_theme_options = {
       "footer_icons": [
           {
               "name": "GitHub",
               "url": "https://github.com/yourproject",
               "html": "<svg>...</svg>",
           },
       ],
   }

Announcements
^^^^^^^^^^^^^

Add announcement banners:

.. code-block:: python

   html_theme_options = {
       "announcement": "🚀 <strong>New version released!</strong> Check out the latest features.",
   }

Using Other Themes
------------------

While Furo is the default and recommended theme, you can use others:

Sphinx Book Theme
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install sphinx-book-theme

.. code-block:: python

   html_theme = "sphinx_book_theme"

PyData Theme
^^^^^^^^^^^^

.. code-block:: bash

   pip install pydata-sphinx-theme

.. code-block:: python

   html_theme = "pydata_sphinx_theme"

Read the Docs Theme
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install sphinx-rtd-theme

.. code-block:: python

   html_theme = "sphinx_rtd_theme"

Best Practices
--------------

1. **Use CSS Variables**
   
   Leverage Furo's CSS variables for consistency:
   
   .. code-block:: css
   
      .custom-element {
          color: var(--color-brand-primary);
          background: var(--color-background-secondary);
      }

2. **Test Dark Mode**
   
   Always test your customizations in both light and dark modes.

3. **Mobile First**
   
   Design for mobile devices first, then enhance for larger screens.

4. **Performance**
   
   - Minimize custom CSS
   - Use CSS variables instead of hard-coded colors
   - Avoid heavy JavaScript modifications

5. **Accessibility**
   
   - Maintain color contrast ratios
   - Test with screen readers
   - Provide keyboard navigation

Examples
--------

Modern Card Layout
^^^^^^^^^^^^^^^^^^

.. code-block:: css

   .feature-cards {
       display: grid;
       grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
       gap: 1.5rem;
       margin: 2rem 0;
   }
   
   .feature-card {
       background: var(--color-background-secondary);
       border: 1px solid var(--color-background-border);
       border-radius: 0.5rem;
       padding: 1.5rem;
       transition: transform 0.2s, box-shadow 0.2s;
   }
   
   .feature-card:hover {
       transform: translateY(-2px);
       box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
   }

Gradient Headers
^^^^^^^^^^^^^^^^

.. code-block:: css

   .hero-gradient {
       background: linear-gradient(
           135deg,
           var(--color-brand-primary),
           var(--color-brand-content)
       );
       color: white;
       padding: 3rem 2rem;
       border-radius: 0.5rem;
       text-align: center;
   }

Next Steps
----------

- Review :doc:`configuration` for theme configuration options
- Check :doc:`examples` for real-world theme customizations
- Explore the `Furo documentation <https://pradyunsg.me/furo/>`_ for advanced features