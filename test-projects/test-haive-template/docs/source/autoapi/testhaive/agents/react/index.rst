testhaive.agents.react
======================

.. py:module:: testhaive.agents.react

React agent implementations with reasoning and action loops.


.. autolink-examples:: testhaive.agents.react
   :collapse:


.. raw:: html
   
   <div class="autoapi-module-summary">
<span class="module-stat">2 classes</span>   </div>

.. autoapi-nested-parse::

   React agent implementations with reasoning and action loops.


   .. autolink-examples:: testhaive.agents.react
      :collapse:



.. admonition:: Submodules (1)
   :class: note

   .. toctree::
      :maxdepth: 1
      :titlesonly:

      /autoapi/testhaive/agents/react/agent/index

      
            
            

.. admonition:: Classes (2)
   :class: note

   .. autoapisummary::

      testhaive.agents.react.ReactAgent
      testhaive.agents.react.ReactConfig

            
            

.. dropdown:: :octicon:`book` Complete API Documentation
   :open:
   :class-title: sd-font-weight-bold sd-text-info
   :class-container: sd-border-info

   .. grid:: 1 2 2 3
      :gutter: 2

      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: ReactAgent(**kwargs)

            Bases: :py:obj:`testhaive.agents.simple.agent.SimpleAgent`


            ReactAgent implementing the ReAct (Reasoning and Acting) pattern.

            ReactAgent extends SimpleAgent with advanced reasoning capabilities, tool usage,
            and reflective thinking. It follows the ReAct pattern of reasoning about problems,
            planning actions, executing tools, and reflecting on results.

            The agent operates in iterative cycles:
            1. **Reasoning**: Analyze the problem and current state
            2. **Planning**: Create action plans based on reasoning
            3. **Acting**: Execute tools and actions according to plans
            4. **Observing**: Process results and outcomes
            5. **Reflecting**: Evaluate progress and adjust strategy

            .. attribute:: config

               ReactAgent configuration

            .. attribute:: thought_history

               History of all thoughts and reasoning steps

            .. attribute:: action_history

               History of all actions taken

            .. attribute:: current_reasoning_step

               Current step in reasoning process

            .. attribute:: tool_call_count

               Number of tool calls made in current session

            .. attribute:: reflection_count

               Number of reflections performed

            .. rubric:: Examples

            Basic ReactAgent usage::

                from testhaive.core.engine.config import TestLLMConfig

                # Configure LLM
                llm_config = TestLLMConfig(
                    name="react_llm",
                    model="gpt-4",
                    temperature=0.7,
                    tools=["web_search", "calculator"]
                )

                # Configure ReactAgent
                react_config = ReactConfig(
                    name="research_assistant",
                    engine=llm_config,
                    max_reasoning_steps=8,
                    enable_reflection=True
                )

                # Create and use agent
                agent = ReactAgent(name="researcher", config=react_config)
                result = agent.run("What are the main risks of artificial intelligence?")

            Advanced usage with async execution::

                async def run_research():
                    agent = ReactAgent(name="async_researcher", config=react_config)
                    result = await agent.arun("Analyze recent developments in AI safety")
                    return result

            Accessing reasoning history::

                agent = ReactAgent(name="tracker", config=react_config)
                result = agent.run("Complex research question")

                # Review reasoning process
                for thought in agent.thought_history:
                    print(f"Thought: {thought.content} (confidence: {thought.confidence})")

                # Review actions taken
                for action in agent.action_history:
                    print(f"Action: {action.description} -> {action.action_type}")

            Initialize ReactAgent with React-specific setup.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: ReactAgent
               :collapse:

            .. py:method:: _can_provide_response() -> bool

               Check if sufficient information is available to provide a response.


               .. autolink-examples:: _can_provide_response
                  :collapse:


            .. py:method:: _execute_actions(actions: List[ActionPlan]) -> List[Dict[str, Any]]

               Execute planned actions.


               .. autolink-examples:: _execute_actions
                  :collapse:


            .. py:method:: _execute_tool_call(action: ActionPlan) -> Dict[str, Any]

               Execute a tool call action.


               .. autolink-examples:: _execute_tool_call
                  :collapse:


            .. py:method:: _generate_final_response() -> str

               Generate final response based on reasoning and observations.


               .. autolink-examples:: _generate_final_response
                  :collapse:


            .. py:method:: _generate_thoughts() -> List[ThoughtProcess]

               Generate thoughts for current reasoning step.


               .. autolink-examples:: _generate_thoughts
                  :collapse:


            .. py:method:: _initialize_reasoning_session(input_text: str) -> None

               Initialize a new reasoning session.


               .. autolink-examples:: _initialize_reasoning_session
                  :collapse:


            .. py:method:: _perform_reflection() -> None

               Perform reflection on current progress.


               .. autolink-examples:: _perform_reflection
                  :collapse:


            .. py:method:: _plan_actions(thoughts: List[ThoughtProcess]) -> List[ActionPlan]

               Plan actions based on current thoughts.


               .. autolink-examples:: _plan_actions
                  :collapse:


            .. py:method:: _process_observations(results: List[Dict[str, Any]]) -> List[str]

               Process and analyze action results.


               .. autolink-examples:: _process_observations
                  :collapse:


            .. py:method:: _should_reflect() -> bool

               Determine if reflection should be performed.


               .. autolink-examples:: _should_reflect
                  :collapse:


            .. py:method:: arun(input_text: str) -> str
               :async:


               Async version of the ReactAgent reasoning and action cycle.

               :param input_text: Input query or task description

               :returns: Final response after reasoning and action cycle


               .. autolink-examples:: arun
                  :collapse:


            .. py:method:: clear_history() -> None

               Clear reasoning and action history.


               .. autolink-examples:: clear_history
                  :collapse:


            .. py:method:: get_reasoning_summary() -> Dict[str, Any]

               Get a summary of the reasoning process.

               :returns: Dictionary containing reasoning statistics and history


               .. autolink-examples:: get_reasoning_summary
                  :collapse:


            .. py:method:: run(input_text: str) -> str

               Execute ReactAgent reasoning and action cycle.

               This method implements the complete ReAct cycle:
               1. Initialize reasoning with the input
               2. Generate thoughts and analyze the problem
               3. Plan actions based on reasoning
               4. Execute actions and tools
               5. Observe and process results
               6. Reflect and adjust strategy
               7. Return final response

               :param input_text: Input query or task description

               :returns: Final response after reasoning and action cycle

               .. rubric:: Examples

               Simple query::

                   response = agent.run("What is the capital of France?")

               Complex reasoning task::

                   response = agent.run(
                       "Analyze the pros and cons of renewable energy adoption "
                       "and provide policy recommendations"
                   )


               .. autolink-examples:: run
                  :collapse:


            .. py:attribute:: _reasoning_context
               :type:  Dict[str, Any]
               :value: None



            .. py:attribute:: action_history
               :type:  List[ActionPlan]
               :value: None



            .. py:attribute:: config
               :type:  ReactConfig
               :value: None



            .. py:attribute:: current_reasoning_step
               :type:  int
               :value: None



            .. py:attribute:: reflection_count
               :type:  int
               :value: None



            .. py:attribute:: thought_history
               :type:  List[ThoughtProcess]
               :value: None



            .. py:attribute:: tool_call_count
               :type:  int
               :value: None




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: ReactConfig(/, **data: Any)

            Bases: :py:obj:`testhaive.agents.simple.agent.SimpleAgentConfig`


            Configuration for ReactAgent extending SimpleAgentConfig.

            This configuration adds React-specific settings for reasoning, action planning,
            tool management, and reflection capabilities.

            .. attribute:: reasoning_mode

               Mode for reasoning process

            .. attribute:: max_reasoning_steps

               Maximum number of reasoning steps per iteration

            .. attribute:: max_tool_calls

               Maximum number of tool calls per reasoning cycle

            .. attribute:: enable_reflection

               Whether to enable reflection after actions

            .. attribute:: reflection_frequency

               How often to perform reflection (1 = every step)

            .. attribute:: tool_timeout

               Timeout for tool calls in seconds

            .. attribute:: parallel_tool_calls

               Allow parallel tool execution

            .. attribute:: reasoning_temperature

               Temperature for reasoning steps

            .. attribute:: action_temperature

               Temperature for action selection

            .. rubric:: Examples

            Basic ReactAgent configuration::

                from testhaive.core.engine.config import TestLLMConfig

                llm_config = TestLLMConfig(
                    name="react_llm",
                    model="gpt-4",
                    temperature=0.7,
                    tools=["web_search", "calculator", "code_executor"]
                )

                react_config = ReactConfig(
                    name="research_agent",
                    engine=llm_config,
                    reasoning_mode=ReasoningMode.SEQUENTIAL,
                    max_reasoning_steps=10,
                    enable_reflection=True
                )

            Advanced configuration with parallel processing::

                react_config = ReactConfig(
                    name="advanced_agent",
                    engine=llm_config,
                    reasoning_mode=ReasoningMode.PARALLEL,
                    max_reasoning_steps=15,
                    max_tool_calls=5,
                    parallel_tool_calls=True,
                    tool_timeout=30.0,
                    reflection_frequency=3
                )

            Create a new model by parsing and validating input data from keyword arguments.

            Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
            validated to form a valid model.

            `self` is explicitly positional-only to allow `self` as a field name.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: ReactConfig
               :collapse:

            .. py:method:: validate_engine_mode(v)

               Ensure engine is configured for React mode.


               .. autolink-examples:: validate_engine_mode
                  :collapse:


            .. py:attribute:: action_temperature
               :type:  float
               :value: None



            .. py:attribute:: enable_reflection
               :type:  bool
               :value: None



            .. py:attribute:: max_reasoning_steps
               :type:  int
               :value: None



            .. py:attribute:: max_tool_calls
               :type:  int
               :value: None



            .. py:attribute:: parallel_tool_calls
               :type:  bool
               :value: None



            .. py:attribute:: reasoning_mode
               :type:  ReasoningMode
               :value: None



            .. py:attribute:: reasoning_temperature
               :type:  float
               :value: None



            .. py:attribute:: reflection_frequency
               :type:  int
               :value: None



            .. py:attribute:: tool_timeout
               :type:  float
               :value: None






----

.. admonition:: Quick Reference
   :class: tip

   .. code-block:: python

      from testhaive.agents.react import *

      # Module provides type hints for mypy compatibility
      # View source: https://github.com/haive-ai/haive

