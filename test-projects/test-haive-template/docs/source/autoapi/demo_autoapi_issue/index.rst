demo_autoapi_issue
==================

.. py:module:: demo_autoapi_issue

Demonstration of the AutoAPI flattening issue.

This script simulates what AutoAPI discovers in our complex nested structure
and shows how it creates a flat alphabetical list instead of hierarchical organization.


.. autolink-examples:: demo_autoapi_issue
   :collapse:


.. raw:: html
   
   <div class="autoapi-module-summary">
<span class="module-stat">5 functions</span>   </div>

.. autoapi-nested-parse::

   Demonstration of the AutoAPI flattening issue.

   This script simulates what AutoAPI discovers in our complex nested structure
   and shows how it creates a flat alphabetical list instead of hierarchical organization.


   .. autolink-examples:: demo_autoapi_issue
      :collapse:


      
            
            
            

.. admonition:: Functions (5)
   :class: info

   .. autoapisummary::

      demo_autoapi_issue.discover_classes_in_file
      demo_autoapi_issue.main
      demo_autoapi_issue.scan_packages
      demo_autoapi_issue.show_flat_structure
      demo_autoapi_issue.show_hierarchical_structure

            

.. dropdown:: :octicon:`book` Complete API Documentation
   :open:
   :class-title: sd-font-weight-bold sd-text-info
   :class-container: sd-border-info

   .. grid:: 1 2 2 3
      :gutter: 2

      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:function:: discover_classes_in_file(file_path: pathlib.Path) -> Dict[str, List[str]]

            Discover classes in a Python file (simulates AutoAPI discovery).


            .. autolink-examples:: discover_classes_in_file
               :collapse:


      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:function:: main()

            Demonstrate the AutoAPI flattening issue.


            .. autolink-examples:: main
               :collapse:


      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:function:: scan_packages() -> Dict[str, Dict[str, List[str]]]

            Scan all packages and discover their structure.


            .. autolink-examples:: scan_packages
               :collapse:


      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:function:: show_flat_structure(packages: Dict[str, Dict[str, List[str]]])

            Show the current flat AutoAPI structure (the problem).


            .. autolink-examples:: show_flat_structure
               :collapse:


      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:function:: show_hierarchical_structure(packages: Dict[str, Dict[str, List[str]]])

            Show the desired hierarchical structure (the solution).


            .. autolink-examples:: show_hierarchical_structure
               :collapse:




----

.. admonition:: Quick Reference
   :class: tip

   .. code-block:: python

      from demo_autoapi_issue import *

      # Module provides type hints for mypy compatibility
      # View source: https://github.com/haive-ai/haive

