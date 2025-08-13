testhaive.core.engine
=====================

.. py:module:: testhaive.core.engine

.. autoapi-nested-parse::

   Engine module for testhaive.core configuration.


   .. autolink-examples:: testhaive.core.engine
      :collapse:


Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/testhaive/core/engine/config/index


Classes
-------

.. autoapisummary::

   testhaive.core.engine.EngineMode
   testhaive.core.engine.TestLLMConfig


Package Contents
----------------

.. py:class:: EngineMode

   Bases: :py:obj:`str`, :py:obj:`enum.Enum`


   Engine execution modes (mimics Haive's patterns).

   Initialize self.  See help(type(self)) for accurate signature.


   .. autolink-examples:: __init__
      :collapse:


   .. autolink-examples:: EngineMode
      :collapse:

   .. py:attribute:: MULTI_AGENT
      :value: 'multi_agent'



   .. py:attribute:: REACT
      :value: 'react'



   .. py:attribute:: SIMPLE
      :value: 'simple'



   .. py:attribute:: STREAMING
      :value: 'streaming'



.. py:class:: TestLLMConfig(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Main LLM configuration class (mimics AugLLMConfig).

   This class mimics the complexity and patterns of AugLLMConfig.

   :param name: Configuration name
   :param model: LLM model identifier
   :param mode: Engine execution mode
   :param temperature: Sampling temperature (0.0-2.0)
   :param max_tokens: Maximum output tokens
   :param tools: List of available tools
   :param system_message: System prompt
   :param metadata: Additional configuration metadata

   .. rubric:: Examples

   Basic configuration::

       config = TestLLMConfig(
           name="simple_config",
           model="gpt-4",
           mode=EngineMode.SIMPLE,
           temperature=0.7
       )

   React agent configuration::

       config = TestLLMConfig(
           name="react_config",
           model="gpt-4",
           mode=EngineMode.REACT,
           temperature=0.3,
           max_tokens=1000,
           tools=["calculator", "search"],
           system_message="You are a helpful assistant."
       )

   Create a new model by parsing and validating input data from keyword arguments.

   Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
   validated to form a valid model.

   `self` is explicitly positional-only to allow `self` as a field name.


   .. autolink-examples:: __init__
      :collapse:


   .. autolink-examples:: TestLLMConfig
      :collapse:

   .. py:method:: add_tool(tool_name: str) -> None

      Add a tool to the configuration.

      :param tool_name: Name of the tool to add


      .. autolink-examples:: add_tool
         :collapse:


   .. py:method:: get_summary() -> Dict[str, Any]

      Get configuration summary.

      :returns: Dictionary containing configuration summary


      .. autolink-examples:: get_summary
         :collapse:


   .. py:method:: remove_tool(tool_name: str) -> None

      Remove a tool from the configuration.

      :param tool_name: Name of the tool to remove


      .. autolink-examples:: remove_tool
         :collapse:


   .. py:method:: with_tools(tools: List[str]) -> TestLLMConfig

      Create a new config with specified tools.

      :param tools: List of tool names

      :returns: New TestLLMConfig instance with tools


      .. autolink-examples:: with_tools
         :collapse:


   .. py:attribute:: max_tokens
      :type:  Optional[int]
      :value: None



   .. py:attribute:: metadata
      :type:  Dict[str, Any]
      :value: None



   .. py:attribute:: mode
      :type:  EngineMode
      :value: None



   .. py:attribute:: model
      :type:  str
      :value: None



   .. py:attribute:: name
      :type:  str
      :value: None



   .. py:attribute:: system_message
      :type:  Optional[str]
      :value: None



   .. py:attribute:: temperature
      :type:  float
      :value: None



   .. py:attribute:: tools
      :type:  List[str]
      :value: None



