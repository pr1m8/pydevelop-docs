testhaive.agents.simple
=======================

.. py:module:: testhaive.agents.simple

Simple agent implementations.


.. autolink-examples:: testhaive.agents.simple
   :collapse:


.. raw:: html
   
   <div class="autoapi-module-summary">
<span class="module-stat">1 classes</span>   </div>

.. autoapi-nested-parse::

   Simple agent implementations.


   .. autolink-examples:: testhaive.agents.simple
      :collapse:



.. admonition:: Submodules (1)
   :class: note

   .. toctree::
      :maxdepth: 1
      :titlesonly:

      /autoapi/testhaive/agents/simple/agent/index

      
            
            

.. admonition:: Classes (1)
   :class: note

   .. autoapisummary::

      testhaive.agents.simple.SimpleAgent

            
            

.. dropdown:: :octicon:`book` Complete API Documentation
   :open:
   :class-title: sd-font-weight-bold sd-text-info
   :class-container: sd-border-info

   .. grid:: 1 2 2 3
      :gutter: 2

      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: SimpleAgent(/, **data: Any)

            Bases: :py:obj:`pydantic.BaseModel`


            Simple agent implementation.

            This agent provides basic functionality for testing documentation structure.
            It mimics the patterns used in haive.agents.simple.SimpleAgent.

            :param name: Agent identifier
            :param config: Agent configuration
            :param state: Current agent state

            .. rubric:: Examples

            Basic usage::

                from testhaive.core.engine.config import TestLLMConfig

                config = TestLLMConfig(name="test", model="gpt-4")
                agent_config = SimpleAgentConfig(name="simple", engine=config)
                agent = SimpleAgent(name="my_agent", config=agent_config)

            With custom configuration::

                config = TestLLMConfig(
                    name="advanced",
                    model="gpt-4",
                    temperature=0.3,
                    tools=["calculator"]
                )
                agent_config = SimpleAgentConfig(
                    name="advanced_agent",
                    engine=config,
                    max_iterations=10,
                    verbose=True
                )
                agent = SimpleAgent(name="advanced", config=agent_config)

            Create a new model by parsing and validating input data from keyword arguments.

            Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
            validated to form a valid model.

            `self` is explicitly positional-only to allow `self` as a field name.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: SimpleAgent
               :collapse:

            .. py:method:: get_stats() -> Dict[str, Any]

               Get agent execution statistics.

               :returns: Dictionary with execution stats


               .. autolink-examples:: get_stats
                  :collapse:


            .. py:method:: reset() -> None

               Reset agent state.


               .. autolink-examples:: reset
                  :collapse:


            .. py:method:: run(input_text: str) -> str

               Execute the agent with input text.

               :param input_text: Input text to process

               :returns: Processed output text


               .. autolink-examples:: run
                  :collapse:


            .. py:attribute:: _execution_count
               :type:  int
               :value: None



            .. py:attribute:: config
               :type:  SimpleAgentConfig
               :value: None



            .. py:attribute:: name
               :type:  str
               :value: None



            .. py:attribute:: state
               :type:  Optional[testhaive.core.schema.base.BaseSchema]
               :value: None






----

.. admonition:: Quick Reference
   :class: tip

   .. code-block:: python

      from testhaive.agents.simple import *

      # Module provides type hints for mypy compatibility
      # View source: https://github.com/haive-ai/haive

