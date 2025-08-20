testhaive.core.schema.meta
==========================

.. py:module:: testhaive.core.schema.meta

.. autoapi-nested-parse::

   Meta-schema classes for advanced state management.


   .. autolink-examples:: testhaive.core.schema.meta
      :collapse:


Classes
-------

.. autoapisummary::

   testhaive.core.schema.meta.MetaStateSchema
   testhaive.core.schema.meta.StateProjection
   testhaive.core.schema.meta.StateTransfer


Module Contents
---------------

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



