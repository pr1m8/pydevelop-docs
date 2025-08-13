testhaive.agents.simple.agent
=============================

.. py:module:: testhaive.agents.simple.agent

.. autoapi-nested-parse::

   Simple agent implementation (mimics SimpleAgent from haive.agents).

   This module provides a basic agent implementation for testing AutoAPI organization.



Classes
-------

.. autoapisummary::

   testhaive.agents.simple.agent.SimpleAgent
   testhaive.agents.simple.agent.SimpleAgentConfig


Module Contents
---------------

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


   .. py:method:: get_stats() -> Dict[str, Any]

      Get agent execution statistics.

      :returns: Dictionary with execution stats



   .. py:method:: reset() -> None

      Reset agent state.



   .. py:method:: run(input_text: str) -> str

      Execute the agent with input text.

      :param input_text: Input text to process

      :returns: Processed output text



   .. py:attribute:: config
      :type:  SimpleAgentConfig
      :value: None



   .. py:attribute:: name
      :type:  str
      :value: None



   .. py:attribute:: state
      :type:  Optional[testhaive.core.schema.base.BaseSchema]
      :value: None



.. py:class:: SimpleAgentConfig(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Configuration for SimpleAgent.

   :param name: Agent name
   :param engine: LLM configuration
   :param max_iterations: Maximum execution iterations
   :param verbose: Enable verbose logging

   Create a new model by parsing and validating input data from keyword arguments.

   Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
   validated to form a valid model.

   `self` is explicitly positional-only to allow `self` as a field name.


   .. py:attribute:: engine
      :type:  testhaive.core.engine.config.TestLLMConfig
      :value: None



   .. py:attribute:: max_iterations
      :type:  int
      :value: None



   .. py:attribute:: name
      :type:  str
      :value: None



   .. py:attribute:: verbose
      :type:  bool
      :value: None



