testhaive.agents.react.agent
============================

.. py:module:: testhaive.agents.react.agent

ReactAgent implementation with reasoning and action capabilities.

This module provides the ReactAgent class, which implements the ReAct (Reasoning and Acting)
pattern for AI agents. ReactAgent can reason about problems, plan actions, execute tools,
and reflect on results in an iterative loop.


.. autolink-examples:: testhaive.agents.react.agent
   :collapse:


.. raw:: html
   
   <div class="autoapi-module-summary">
<span class="module-stat">6 classes</span>   </div>

.. autoapi-nested-parse::

   ReactAgent implementation with reasoning and action capabilities.

   This module provides the ReactAgent class, which implements the ReAct (Reasoning and Acting)
   pattern for AI agents. ReactAgent can reason about problems, plan actions, execute tools,
   and reflect on results in an iterative loop.


   .. autolink-examples:: testhaive.agents.react.agent
      :collapse:


      
            
            

.. admonition:: Classes (6)
   :class: note

   .. autoapisummary::

      testhaive.agents.react.agent.ActionPlan
      testhaive.agents.react.agent.ActionType
      testhaive.agents.react.agent.ReactAgent
      testhaive.agents.react.agent.ReactConfig
      testhaive.agents.react.agent.ReasoningMode
      testhaive.agents.react.agent.ThoughtProcess

            
            

.. dropdown:: :octicon:`book` Complete API Documentation
   :open:
   :class-title: sd-font-weight-bold sd-text-info
   :class-container: sd-border-info

   .. grid:: 1 2 2 3
      :gutter: 2

      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: ActionPlan(/, **data: Any)

            Bases: :py:obj:`pydantic.BaseModel`


            Represents a planned action with context and expectations.

            This class encapsulates a planned action including the action type, parameters,
            expected outcomes, success criteria, and fallback strategies.

            .. attribute:: action_id

               Unique identifier for this action

            .. attribute:: action_type

               Type of action to perform

            .. attribute:: description

               Human-readable description of the action

            .. attribute:: parameters

               Parameters needed to execute the action

            .. attribute:: expected_outcome

               Expected result from the action

            .. attribute:: success_criteria

               Criteria to determine if action succeeded

            .. attribute:: fallback_actions

               Alternative actions if this fails

            .. attribute:: priority

               Priority level for action execution

            .. attribute:: estimated_duration

               Estimated time to complete action

            .. rubric:: Examples

            Creating an action plan::

                action = ActionPlan(
                    action_id="search_001",
                    action_type=ActionType.TOOL_CALL,
                    description="Search for recent AI safety research",
                    parameters={"tool": "web_search", "query": "AI safety 2024"},
                    expected_outcome="List of recent research papers"
                )

            Complex action with fallbacks::

                action = ActionPlan(
                    action_id="analysis_001",
                    action_type=ActionType.REASONING,
                    description="Analyze search results for key themes",
                    parameters={"method": "thematic_analysis", "min_themes": 3},
                    success_criteria={"themes_found": 3, "confidence": 0.7},
                    fallback_actions=["manual_review", "simplified_analysis"],
                    priority=1
                )

            Create a new model by parsing and validating input data from keyword arguments.

            Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
            validated to form a valid model.

            `self` is explicitly positional-only to allow `self` as a field name.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: ActionPlan
               :collapse:

            .. py:method:: add_fallback(fallback_action: str) -> None

               Add a fallback action.

               :param fallback_action: ID or description of fallback action


               .. autolink-examples:: add_fallback
                  :collapse:


            .. py:method:: evaluate_success(actual_outcome: Dict[str, Any]) -> bool

               Evaluate if the action was successful based on criteria.

               :param actual_outcome: Actual outcome from action execution

               :returns: True if action was successful, False otherwise


               .. autolink-examples:: evaluate_success
                  :collapse:


            .. py:attribute:: action_id
               :type:  str
               :value: None



            .. py:attribute:: action_type
               :type:  ActionType
               :value: None



            .. py:attribute:: description
               :type:  str
               :value: None



            .. py:attribute:: estimated_duration
               :type:  Optional[float]
               :value: None



            .. py:attribute:: expected_outcome
               :type:  str
               :value: None



            .. py:attribute:: fallback_actions
               :type:  List[str]
               :value: None



            .. py:attribute:: parameters
               :type:  Dict[str, Any]
               :value: None



            .. py:attribute:: priority
               :type:  int
               :value: None



            .. py:attribute:: success_criteria
               :type:  Dict[str, Any]
               :value: None



            .. py:attribute:: timestamp
               :type:  datetime.datetime
               :value: None




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: ActionType

            Bases: :py:obj:`str`, :py:obj:`enum.Enum`


            Types of actions that can be performed.

            .. attribute:: TOOL_CALL

               Call an external tool

            .. attribute:: REASONING

               Perform internal reasoning

            .. attribute:: OBSERVATION

               Observe and analyze results

            .. attribute:: REFLECTION

               Reflect on progress and adjust strategy

            .. attribute:: DECISION

               Make a decision based on available information

            Initialize self.  See help(type(self)) for accurate signature.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: ActionType
               :collapse:

            .. py:attribute:: DECISION
               :value: 'decision'



            .. py:attribute:: OBSERVATION
               :value: 'observation'



            .. py:attribute:: REASONING
               :value: 'reasoning'



            .. py:attribute:: REFLECTION
               :value: 'reflection'



            .. py:attribute:: TOOL_CALL
               :value: 'tool_call'




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




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: ReasoningMode

            Bases: :py:obj:`str`, :py:obj:`enum.Enum`


            Reasoning modes for ReactAgent.

            .. attribute:: SEQUENTIAL

               Process reasoning steps sequentially

            .. attribute:: PARALLEL

               Process multiple reasoning paths in parallel

            .. attribute:: ADAPTIVE

               Adaptively choose between sequential and parallel

            .. attribute:: TREE_SEARCH

               Use tree search for complex reasoning

            Initialize self.  See help(type(self)) for accurate signature.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: ReasoningMode
               :collapse:

            .. py:attribute:: ADAPTIVE
               :value: 'adaptive'



            .. py:attribute:: PARALLEL
               :value: 'parallel'



            .. py:attribute:: SEQUENTIAL
               :value: 'sequential'



            .. py:attribute:: TREE_SEARCH
               :value: 'tree_search'




      .. grid-item-card:: 
         :class-card: sd-border-0 sd-shadow-sm
         :class-title: sd-text-center sd-font-weight-bold

.. py:class:: ThoughtProcess(/, **data: Any)

            Bases: :py:obj:`pydantic.BaseModel`


            Represents a single thought or reasoning step.

            This class captures individual thoughts in the reasoning process, including
            the thought content, confidence level, dependencies, and outcomes.

            .. attribute:: thought_id

               Unique identifier for this thought

            .. attribute:: content

               The actual thought content

            .. attribute:: thought_type

               Type of thought (analysis, planning, etc.)

            .. attribute:: confidence

               Confidence level in this thought (0.0-1.0)

            .. attribute:: dependencies

               Other thoughts this depends on

            .. attribute:: timestamp

               When this thought was generated

            .. attribute:: metadata

               Additional metadata about the thought

            .. rubric:: Examples

            Creating a thought process::

                thought = ThoughtProcess(
                    thought_id="thought_001",
                    content="I need to search for information about AI safety",
                    thought_type="analysis",
                    confidence=0.8
                )

            Linking thoughts::

                dependent_thought = ThoughtProcess(
                    thought_id="thought_002",
                    content="Based on the search results, I should analyze the key risks",
                    thought_type="planning",
                    dependencies=["thought_001"]
                )

            Create a new model by parsing and validating input data from keyword arguments.

            Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
            validated to form a valid model.

            `self` is explicitly positional-only to allow `self` as a field name.


            .. autolink-examples:: __init__
               :collapse:


            .. autolink-examples:: ThoughtProcess
               :collapse:

            .. py:method:: add_dependency(thought_id: str) -> None

               Add a dependency to another thought.

               :param thought_id: ID of the thought this depends on


               .. autolink-examples:: add_dependency
                  :collapse:


            .. py:method:: update_confidence(new_confidence: float) -> None

               Update the confidence level for this thought.

               :param new_confidence: New confidence level (0.0-1.0)


               .. autolink-examples:: update_confidence
                  :collapse:


            .. py:attribute:: confidence
               :type:  float
               :value: None



            .. py:attribute:: content
               :type:  str
               :value: None



            .. py:attribute:: dependencies
               :type:  List[str]
               :value: None



            .. py:attribute:: metadata
               :type:  Dict[str, Any]
               :value: None



            .. py:attribute:: thought_id
               :type:  str
               :value: None



            .. py:attribute:: thought_type
               :type:  str
               :value: None



            .. py:attribute:: timestamp
               :type:  datetime.datetime
               :value: None






----

.. admonition:: Quick Reference
   :class: tip

   .. code-block:: python

      from testhaive.agents.react.agent import *

      # Module provides type hints for mypy compatibility
      # View source: https://github.com/haive-ai/haive

