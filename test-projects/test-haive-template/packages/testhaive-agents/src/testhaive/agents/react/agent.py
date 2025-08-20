"""ReactAgent implementation with reasoning and action capabilities.

This module provides the ReactAgent class, which implements the ReAct (Reasoning and Acting)
pattern for AI agents. ReactAgent can reason about problems, plan actions, execute tools,
and reflect on results in an iterative loop.
"""

import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field, validator
from testhaive.core.engine.config import EngineMode, TestLLMConfig
from testhaive.core.schema.base import BaseSchema
from testhaive.core.schema.state import AgentState, ExecutionStatus

from ..simple.agent import SimpleAgent, SimpleAgentConfig


class ReasoningMode(str, Enum):
    """Reasoning modes for ReactAgent.

    Attributes:
        SEQUENTIAL: Process reasoning steps sequentially
        PARALLEL: Process multiple reasoning paths in parallel
        ADAPTIVE: Adaptively choose between sequential and parallel
        TREE_SEARCH: Use tree search for complex reasoning
    """

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    ADAPTIVE = "adaptive"
    TREE_SEARCH = "tree_search"


class ActionType(str, Enum):
    """Types of actions that can be performed.

    Attributes:
        TOOL_CALL: Call an external tool
        REASONING: Perform internal reasoning
        OBSERVATION: Observe and analyze results
        REFLECTION: Reflect on progress and adjust strategy
        DECISION: Make a decision based on available information
    """

    TOOL_CALL = "tool_call"
    REASONING = "reasoning"
    OBSERVATION = "observation"
    REFLECTION = "reflection"
    DECISION = "decision"


class ReactConfig(SimpleAgentConfig):
    """Configuration for ReactAgent extending SimpleAgentConfig.

    This configuration adds React-specific settings for reasoning, action planning,
    tool management, and reflection capabilities.

    Attributes:
        reasoning_mode: Mode for reasoning process
        max_reasoning_steps: Maximum number of reasoning steps per iteration
        max_tool_calls: Maximum number of tool calls per reasoning cycle
        enable_reflection: Whether to enable reflection after actions
        reflection_frequency: How often to perform reflection (1 = every step)
        tool_timeout: Timeout for tool calls in seconds
        parallel_tool_calls: Allow parallel tool execution
        reasoning_temperature: Temperature for reasoning steps
        action_temperature: Temperature for action selection

    Examples:
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
    """

    reasoning_mode: ReasoningMode = Field(
        default=ReasoningMode.SEQUENTIAL, description="Mode for reasoning process"
    )
    max_reasoning_steps: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of reasoning steps per iteration",
    )
    max_tool_calls: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of tool calls per reasoning cycle",
    )
    enable_reflection: bool = Field(
        default=True, description="Whether to enable reflection after actions"
    )
    reflection_frequency: int = Field(
        default=3, ge=1, description="How often to perform reflection (1 = every step)"
    )
    tool_timeout: float = Field(
        default=15.0, ge=1.0, le=300.0, description="Timeout for tool calls in seconds"
    )
    parallel_tool_calls: bool = Field(
        default=False, description="Allow parallel tool execution"
    )
    reasoning_temperature: float = Field(
        default=0.3, ge=0.0, le=2.0, description="Temperature for reasoning steps"
    )
    action_temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="Temperature for action selection"
    )

    @validator("engine")
    def validate_engine_mode(cls, v):
        """Ensure engine is configured for React mode."""
        if hasattr(v, "mode") and v.mode != EngineMode.REACT:
            v.mode = EngineMode.REACT
        return v


class ThoughtProcess(BaseModel):
    """Represents a single thought or reasoning step.

    This class captures individual thoughts in the reasoning process, including
    the thought content, confidence level, dependencies, and outcomes.

    Attributes:
        thought_id: Unique identifier for this thought
        content: The actual thought content
        thought_type: Type of thought (analysis, planning, etc.)
        confidence: Confidence level in this thought (0.0-1.0)
        dependencies: Other thoughts this depends on
        timestamp: When this thought was generated
        metadata: Additional metadata about the thought

    Examples:
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
    """

    thought_id: str = Field(..., description="Unique identifier for this thought")
    content: str = Field(..., description="The actual thought content")
    thought_type: str = Field(
        default="general", description="Type of thought (analysis, planning, etc.)"
    )
    confidence: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Confidence level in this thought"
    )
    dependencies: List[str] = Field(
        default_factory=list, description="Other thoughts this depends on"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When this thought was generated"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about the thought"
    )

    def add_dependency(self, thought_id: str) -> None:
        """Add a dependency to another thought.

        Args:
            thought_id: ID of the thought this depends on
        """
        if thought_id not in self.dependencies:
            self.dependencies.append(thought_id)

    def update_confidence(self, new_confidence: float) -> None:
        """Update the confidence level for this thought.

        Args:
            new_confidence: New confidence level (0.0-1.0)
        """
        self.confidence = max(0.0, min(1.0, new_confidence))


class ActionPlan(BaseModel):
    """Represents a planned action with context and expectations.

    This class encapsulates a planned action including the action type, parameters,
    expected outcomes, success criteria, and fallback strategies.

    Attributes:
        action_id: Unique identifier for this action
        action_type: Type of action to perform
        description: Human-readable description of the action
        parameters: Parameters needed to execute the action
        expected_outcome: Expected result from the action
        success_criteria: Criteria to determine if action succeeded
        fallback_actions: Alternative actions if this fails
        priority: Priority level for action execution
        estimated_duration: Estimated time to complete action

    Examples:
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
    """

    action_id: str = Field(..., description="Unique identifier for this action")
    action_type: ActionType = Field(..., description="Type of action to perform")
    description: str = Field(
        ..., description="Human-readable description of the action"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Parameters needed to execute the action"
    )
    expected_outcome: str = Field(
        default="", description="Expected result from the action"
    )
    success_criteria: Dict[str, Any] = Field(
        default_factory=dict, description="Criteria to determine if action succeeded"
    )
    fallback_actions: List[str] = Field(
        default_factory=list, description="Alternative actions if this fails"
    )
    priority: int = Field(
        default=1, ge=1, le=10, description="Priority level for action execution"
    )
    estimated_duration: Optional[float] = Field(
        default=None, ge=0.0, description="Estimated time to complete action in seconds"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="When this action was planned"
    )

    def add_fallback(self, fallback_action: str) -> None:
        """Add a fallback action.

        Args:
            fallback_action: ID or description of fallback action
        """
        if fallback_action not in self.fallback_actions:
            self.fallback_actions.append(fallback_action)

    def evaluate_success(self, actual_outcome: Dict[str, Any]) -> bool:
        """Evaluate if the action was successful based on criteria.

        Args:
            actual_outcome: Actual outcome from action execution

        Returns:
            True if action was successful, False otherwise
        """
        if not self.success_criteria:
            return True  # No criteria means assume success

        for criterion, expected_value in self.success_criteria.items():
            actual_value = actual_outcome.get(criterion)
            if actual_value != expected_value:
                return False

        return True


class ReactAgent(SimpleAgent):
    """ReactAgent implementing the ReAct (Reasoning and Acting) pattern.

    ReactAgent extends SimpleAgent with advanced reasoning capabilities, tool usage,
    and reflective thinking. It follows the ReAct pattern of reasoning about problems,
    planning actions, executing tools, and reflecting on results.

    The agent operates in iterative cycles:
    1. **Reasoning**: Analyze the problem and current state
    2. **Planning**: Create action plans based on reasoning
    3. **Acting**: Execute tools and actions according to plans
    4. **Observing**: Process results and outcomes
    5. **Reflecting**: Evaluate progress and adjust strategy

    Attributes:
        config: ReactAgent configuration
        thought_history: History of all thoughts and reasoning steps
        action_history: History of all actions taken
        current_reasoning_step: Current step in reasoning process
        tool_call_count: Number of tool calls made in current session
        reflection_count: Number of reflections performed

    Examples:
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
    """

    config: ReactConfig = Field(..., description="ReactAgent configuration")
    thought_history: List[ThoughtProcess] = Field(
        default_factory=list, description="History of all thoughts and reasoning steps"
    )
    action_history: List[ActionPlan] = Field(
        default_factory=list, description="History of all actions taken"
    )
    current_reasoning_step: int = Field(
        default=0, description="Current step in reasoning process"
    )
    tool_call_count: int = Field(
        default=0, description="Number of tool calls made in current session"
    )
    reflection_count: int = Field(
        default=0, description="Number of reflections performed"
    )
    _reasoning_context: Dict[str, Any] = Field(
        default_factory=dict, description="Internal reasoning context"
    )

    def __init__(self, **kwargs):
        """Initialize ReactAgent with React-specific setup."""
        super().__init__(**kwargs)
        self._reasoning_context = {
            "active_thoughts": [],
            "pending_actions": [],
            "observation_buffer": [],
            "reflection_insights": [],
        }

    def run(self, input_text: str) -> str:
        """Execute ReactAgent reasoning and action cycle.

        This method implements the complete ReAct cycle:
        1. Initialize reasoning with the input
        2. Generate thoughts and analyze the problem
        3. Plan actions based on reasoning
        4. Execute actions and tools
        5. Observe and process results
        6. Reflect and adjust strategy
        7. Return final response

        Args:
            input_text: Input query or task description

        Returns:
            Final response after reasoning and action cycle

        Examples:
            Simple query::

                response = agent.run("What is the capital of France?")

            Complex reasoning task::

                response = agent.run(
                    "Analyze the pros and cons of renewable energy adoption "
                    "and provide policy recommendations"
                )
        """
        if self.config.verbose:
            print(f"[{self.name}] Starting React cycle for: {input_text}")

        # Initialize reasoning
        self._initialize_reasoning_session(input_text)

        # Main React loop
        for step in range(self.config.max_reasoning_steps):
            self.current_reasoning_step = step

            if self.config.verbose:
                print(
                    f"[{self.name}] Reasoning step {step + 1}/{self.config.max_reasoning_steps}"
                )

            # Generate thoughts
            thoughts = self._generate_thoughts()

            # Plan actions based on thoughts
            actions = self._plan_actions(thoughts)

            # Execute actions
            results = self._execute_actions(actions)

            # Observe results
            observations = self._process_observations(results)

            # Check if we should reflect
            if self._should_reflect():
                self._perform_reflection()

            # Check if we have sufficient information to respond
            if self._can_provide_response():
                break

        # Generate final response
        final_response = self._generate_final_response()

        if self.config.verbose:
            print(
                f"[{self.name}] React cycle completed. Steps: {self.current_reasoning_step + 1}"
            )

        return final_response

    async def arun(self, input_text: str) -> str:
        """Async version of the ReactAgent reasoning and action cycle.

        Args:
            input_text: Input query or task description

        Returns:
            Final response after reasoning and action cycle
        """
        # For this example, we'll simulate async behavior
        # In a real implementation, this would use async LLM calls
        return await asyncio.get_event_loop().run_in_executor(
            None, self.run, input_text
        )

    def _initialize_reasoning_session(self, input_text: str) -> None:
        """Initialize a new reasoning session."""
        self.current_reasoning_step = 0
        self.tool_call_count = 0
        self.reflection_count = 0

        # Clear context for new session
        self._reasoning_context = {
            "input": input_text,
            "active_thoughts": [],
            "pending_actions": [],
            "observation_buffer": [],
            "reflection_insights": [],
            "session_start": datetime.now(),
        }

    def _generate_thoughts(self) -> List[ThoughtProcess]:
        """Generate thoughts for current reasoning step."""
        thoughts = []

        # Simulate thought generation (in real implementation, use LLM)
        if self.current_reasoning_step == 0:
            thought = ThoughtProcess(
                thought_id=f"thought_{len(self.thought_history) + 1}",
                content=f"I need to analyze the input: {self._reasoning_context['input']}",
                thought_type="analysis",
                confidence=0.8,
            )
            thoughts.append(thought)

        # Add thoughts to history
        self.thought_history.extend(thoughts)
        self._reasoning_context["active_thoughts"].extend(thoughts)

        return thoughts

    def _plan_actions(self, thoughts: List[ThoughtProcess]) -> List[ActionPlan]:
        """Plan actions based on current thoughts."""
        actions = []

        # Simple action planning logic
        if (
            self.current_reasoning_step == 0
            and self.tool_call_count < self.config.max_tool_calls
        ):
            action = ActionPlan(
                action_id=f"action_{len(self.action_history) + 1}",
                action_type=ActionType.TOOL_CALL,
                description="Search for relevant information",
                parameters={
                    "tool": "web_search",
                    "query": self._reasoning_context["input"],
                },
                expected_outcome="Relevant search results",
            )
            actions.append(action)

        # Add actions to history
        self.action_history.extend(actions)
        self._reasoning_context["pending_actions"].extend(actions)

        return actions

    def _execute_actions(self, actions: List[ActionPlan]) -> List[Dict[str, Any]]:
        """Execute planned actions."""
        results = []

        for action in actions:
            if action.action_type == ActionType.TOOL_CALL:
                # Simulate tool call execution
                result = self._execute_tool_call(action)
                self.tool_call_count += 1
            else:
                # Simulate other action types
                result = {
                    "action_id": action.action_id,
                    "status": "completed",
                    "output": "Action completed",
                }

            results.append(result)

        return results

    def _execute_tool_call(self, action: ActionPlan) -> Dict[str, Any]:
        """Execute a tool call action."""
        # Simulate tool execution (in real implementation, call actual tools)
        tool_name = action.parameters.get("tool", "unknown")

        if tool_name == "web_search":
            return {
                "action_id": action.action_id,
                "tool": tool_name,
                "status": "success",
                "output": f"Search results for: {action.parameters.get('query', '')}",
            }
        else:
            return {
                "action_id": action.action_id,
                "tool": tool_name,
                "status": "success",
                "output": f"Tool {tool_name} executed successfully",
            }

    def _process_observations(self, results: List[Dict[str, Any]]) -> List[str]:
        """Process and analyze action results."""
        observations = []

        for result in results:
            observation = f"Observed: {result.get('output', 'No output')}"
            observations.append(observation)

        self._reasoning_context["observation_buffer"].extend(observations)
        return observations

    def _should_reflect(self) -> bool:
        """Determine if reflection should be performed."""
        if not self.config.enable_reflection:
            return False

        return (self.current_reasoning_step + 1) % self.config.reflection_frequency == 0

    def _perform_reflection(self) -> None:
        """Perform reflection on current progress."""
        self.reflection_count += 1

        # Simulate reflection process
        insight = f"Reflection {self.reflection_count}: Progress analysis at step {self.current_reasoning_step + 1}"
        self._reasoning_context["reflection_insights"].append(insight)

        if self.config.verbose:
            print(f"[{self.name}] Performing reflection: {insight}")

    def _can_provide_response(self) -> bool:
        """Check if sufficient information is available to provide a response."""
        # Simple logic: can respond after first observation
        return len(self._reasoning_context["observation_buffer"]) > 0

    def _generate_final_response(self) -> str:
        """Generate final response based on reasoning and observations."""
        observations = self._reasoning_context["observation_buffer"]

        if observations:
            return f"Based on my analysis: {observations[0]}"
        else:
            return f"I have analyzed the input: {self._reasoning_context['input']}"

    def get_reasoning_summary(self) -> Dict[str, Any]:
        """Get a summary of the reasoning process.

        Returns:
            Dictionary containing reasoning statistics and history
        """
        return {
            "total_thoughts": len(self.thought_history),
            "total_actions": len(self.action_history),
            "reasoning_steps": self.current_reasoning_step + 1,
            "tool_calls_made": self.tool_call_count,
            "reflections_performed": self.reflection_count,
            "thought_types": [t.thought_type for t in self.thought_history],
            "action_types": [a.action_type.value for a in self.action_history],
            "average_confidence": (
                sum(t.confidence for t in self.thought_history)
                / len(self.thought_history)
                if self.thought_history
                else 0
            ),
        }

    def clear_history(self) -> None:
        """Clear reasoning and action history."""
        self.thought_history.clear()
        self.action_history.clear()
        self.current_reasoning_step = 0
        self.tool_call_count = 0
        self.reflection_count = 0
        self._reasoning_context.clear()
