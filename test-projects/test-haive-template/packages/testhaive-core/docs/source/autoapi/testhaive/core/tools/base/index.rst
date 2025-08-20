testhaive.core.tools.base
=========================

.. py:module:: testhaive.core.tools.base

.. autoapi-nested-parse::

   Base tool class for testhaive framework.


   .. autolink-examples:: testhaive.core.tools.base
      :collapse:


Classes
-------

.. autoapisummary::

   testhaive.core.tools.base.BaseTool


Module Contents
---------------

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



