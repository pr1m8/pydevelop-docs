conf
====

.. py:module:: conf

.. autoapi-nested-parse::

   Simplified Sphinx configuration for test-haive-template.
   Focus on AutoAPI hierarchical testing.



Attributes
----------

.. autoapisummary::

   conf.author
   conf.autoapi_add_toctree_entry
   conf.autoapi_dirs
   conf.autoapi_keep_files
   conf.autoapi_member_order
   conf.autoapi_options
   conf.autoapi_own_page_level
   conf.autoapi_python_class_content
   conf.autoapi_root
   conf.autoapi_template_dir
   conf.autoapi_type
   conf.copyright
   conf.exclude_patterns
   conf.extensions
   conf.html_static_path
   conf.html_theme
   conf.html_theme_options
   conf.project
   conf.pygments_dark_style
   conf.pygments_style
   conf.release
   conf.templates_path


Functions
---------

.. autoapisummary::

   conf.setup


Module Contents
---------------

.. py:function:: setup(app)

   Sphinx setup hook.


.. py:data:: author
   :value: 'test-haive-template Team'


.. py:data:: autoapi_add_toctree_entry
   :value: True


.. py:data:: autoapi_dirs
   :value: ['../..']


.. py:data:: autoapi_keep_files
   :value: True


.. py:data:: autoapi_member_order
   :value: 'groupwise'


.. py:data:: autoapi_options
   :value: ['members', 'undoc-members', 'show-inheritance', 'show-module-summary']


.. py:data:: autoapi_own_page_level
   :value: 'module'


.. py:data:: autoapi_python_class_content
   :value: 'both'


.. py:data:: autoapi_root
   :value: 'api'


.. py:data:: autoapi_template_dir
   :value: '_autoapi_templates'


.. py:data:: autoapi_type
   :value: 'python'


.. py:data:: copyright
   :value: 'Uninferable, test-haive-template Team'


.. py:data:: exclude_patterns
   :value: []


.. py:data:: extensions
   :value: ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.viewcode', 'autoapi.extension', 'myst_parser']


.. py:data:: html_static_path
   :value: ['_static']


.. py:data:: html_theme
   :value: 'furo'


.. py:data:: html_theme_options

.. py:data:: project
   :value: 'test-haive-template'


.. py:data:: pygments_dark_style
   :value: 'monokai'


.. py:data:: pygments_style
   :value: 'sphinx'


.. py:data:: release
   :value: '0.1.0'


.. py:data:: templates_path
   :value: ['_templates']


