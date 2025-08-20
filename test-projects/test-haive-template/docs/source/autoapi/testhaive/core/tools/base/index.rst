testhaive.core.tools.base
=========================

.. py:module:: testhaive.core.tools.base

Base tool class for testhaive framework.


.. autolink-examples:: testhaive.core.tools.base
   :collapse:


.. raw:: html
   
   <div class="autoapi-module-summary">
<span class="module-stat">1 classes</span>   </div>

.. autoapi-nested-parse::

   Base tool class for testhaive framework.


   .. autolink-examples:: testhaive.core.tools.base
      :collapse:


      
            
            

.. admonition:: Classes (1)
   :class: note

   .. autoapisummary::

      testhaive.core.tools.base.BaseTool

            
            

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

      from testhaive.core.tools.base import *

      # Module provides type hints for mypy compatibility
      # View source: https://github.com/haive-ai/haive

