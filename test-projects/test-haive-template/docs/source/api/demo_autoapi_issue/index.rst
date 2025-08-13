demo_autoapi_issue
==================

.. py:module:: demo_autoapi_issue

.. autoapi-nested-parse::

   Demonstration of the AutoAPI flattening issue.

   This script simulates what AutoAPI discovers in our complex nested structure
   and shows how it creates a flat alphabetical list instead of hierarchical organization.



Functions
---------

.. autoapisummary::

   demo_autoapi_issue.discover_classes_in_file
   demo_autoapi_issue.main
   demo_autoapi_issue.scan_packages
   demo_autoapi_issue.show_flat_structure
   demo_autoapi_issue.show_hierarchical_structure


Module Contents
---------------

.. py:function:: discover_classes_in_file(file_path: pathlib.Path) -> Dict[str, List[str]]

   Discover classes in a Python file (simulates AutoAPI discovery).


.. py:function:: main()

   Demonstrate the AutoAPI flattening issue.


.. py:function:: scan_packages() -> Dict[str, Dict[str, List[str]]]

   Scan all packages and discover their structure.


.. py:function:: show_flat_structure(packages: Dict[str, Dict[str, List[str]]])

   Show the current flat AutoAPI structure (the problem).


.. py:function:: show_hierarchical_structure(packages: Dict[str, Dict[str, List[str]]])

   Show the desired hierarchical structure (the solution).


