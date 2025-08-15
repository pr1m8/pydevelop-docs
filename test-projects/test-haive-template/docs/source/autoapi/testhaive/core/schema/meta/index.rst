testhaive.core.schema.meta
==========================

.. py:module:: testhaive.core.schema.meta

Meta-schema classes for advanced state management.


.. autolink-examples:: testhaive.core.schema.meta
   :collapse:


.. raw:: html
   
   <div class="autoapi-module-summary">
<span class="module-stat">3 classes</span>   </div>

.. autoapi-nested-parse::

   Meta-schema classes for advanced state management.


   .. autolink-examples:: testhaive.core.schema.meta
      :collapse:


      
            
            

.. admonition:: Classes (3)
   :class: note

   .. autoapisummary::

      testhaive.core.schema.meta.MetaStateSchema
      testhaive.core.schema.meta.StateProjection
      testhaive.core.schema.meta.StateTransfer

            
            

.. dropdown:: :octicon:`book` Complete API Documentation
   :open:
   :class-title: sd-font-weight-bold sd-text-info
   :class-container: sd-border-info

   .. grid:: 1 2 2 3
      :gutter: 2

      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: MetaStateSchema(**kwargs)

            Bases: :py:obj:`testhaive.core.schema.base.StateSchema`


            Meta-state schema for complex state projections.

            Initialize BaseSchema with validation setup.

            :param \*\*kwargs: Keyword arguments for schema fields


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: MetaStateSchema
               :collapse:

            .. py:attribute:: agent_states
               :type:  Dict[str, Dict[str, Any]]
               :value: None




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: StateProjection(**kwargs)

            Bases: :py:obj:`testhaive.core.schema.base.StateSchema`


            State projection for filtered views.

            Initialize BaseSchema with validation setup.

            :param \*\*kwargs: Keyword arguments for schema fields


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: StateProjection
               :collapse:

            .. py:attribute:: projection_fields
               :type:  List[str]
               :value: None



            .. py:attribute:: source_state_id
               :type:  str
               :value: None




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: StateTransfer(**kwargs)

            Bases: :py:obj:`testhaive.core.schema.base.StateSchema`


            State transfer configuration.

            Initialize BaseSchema with validation setup.

            :param \*\*kwargs: Keyword arguments for schema fields


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: StateTransfer
               :collapse:

            .. py:attribute:: source_agent
               :type:  str
               :value: None



            .. py:attribute:: target_agent
               :type:  str
               :value: None



            .. py:attribute:: transfer_rules
               :type:  Dict[str, str]
               :value: None






----

.. admonition:: Quick Reference
   :class: tip

   .. code-block:: python

      from testhaive.core.schema.meta import *

      # Module provides type hints for mypy compatibility
      # View source: https://github.com/haive-ai/haive

