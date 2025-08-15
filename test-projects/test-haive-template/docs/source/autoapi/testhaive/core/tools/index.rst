testhaive.core.tools
====================

.. py:module:: testhaive.core.tools

Tools module for testhaive.core.


.. autolink-examples:: testhaive.core.tools
   :collapse:


.. raw:: html
   
   <div class="autoapi-module-summary">
<span class="module-stat">1 classes</span>   </div>

.. autoapi-nested-parse::

   Tools module for testhaive.core.


   .. autolink-examples:: testhaive.core.tools
      :collapse:



.. admonition:: Submodules (1)
   :class: note

   .. toctree::
      :maxdepth: 1
      :titlesonly:

      /autoapi/testhaive/core/tools/base/index

      
            
            

.. admonition:: Classes (1)
   :class: note

   .. autoapisummary::

      testhaive.core.tools.BaseTool

            
            

.. dropdown:: :octicon:`book` Complete API Documentation
   :open:
   :class-title: sd-font-weight-bold sd-text-info
   :class-container: sd-border-info

   .. grid:: 1 2 2 3
      :gutter: 2

      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: BaseTool(/, **data: Any)

            Bases: :py:obj:`pydantic.BaseModel`


            Base class for all tools in testhaive framework.

            Create a new model by parsing and validating input data from keyword arguments.

            Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
            validated to form a valid model.

            `self` is explicitly positional-only to allow `self` as a field name.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: BaseTool
               :collapse:

            .. py:method:: execute(**kwargs) -> Dict[str, Any]

               Execute the tool with given parameters.


               .. autolink-examples:: execute
                  :collapse:


            .. py:attribute:: description
               :type:  str
               :value: None



            .. py:attribute:: name
               :type:  str
               :value: None






----

.. admonition:: Quick Reference
   :class: tip

   .. code-block:: python

      from testhaive.core.tools import *

      # Module provides type hints for mypy compatibility
      # View source: https://github.com/haive-ai/haive

