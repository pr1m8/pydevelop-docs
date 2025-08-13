"""Simple agent implementation (mimics SimpleAgent from haive.agents).

This module provides a basic agent implementation for testing AutoAPI organization.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from testhaive.core.engine.config import TestLLMConfig
from testhaive.core.schema.base import BaseSchema


class SimpleAgentConfig(BaseModel):
    """Configuration for SimpleAgent.

    Args:
        name: Agent name
        engine: LLM configuration
        max_iterations: Maximum execution iterations
        verbose: Enable verbose logging
    """

    name: str = Field(..., description="Agent identifier")
    engine: TestLLMConfig = Field(..., description="LLM configuration")
    max_iterations: int = Field(default=5, ge=1, description="Maximum iterations")
    verbose: bool = Field(default=False, description="Verbose logging")


class SimpleAgent(BaseModel):
    """Simple agent implementation.

    This agent provides basic functionality for testing documentation structure.
    It mimics the patterns used in haive.agents.simple.SimpleAgent.

    Args:
        name: Agent identifier
        config: Agent configuration
        state: Current agent state

    Examples:
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
    """

    name: str = Field(..., description="Agent identifier")
    config: SimpleAgentConfig = Field(..., description="Agent configuration")
    state: Optional[BaseSchema] = Field(default=None, description="Current state")
    _execution_count: int = Field(default=0, alias="execution_count")

    def run(self, input_text: str) -> str:
        """Execute the agent with input text.

        Args:
            input_text: Input text to process

        Returns:
            Processed output text
        """
        self._execution_count += 1

        if self.config.verbose:
            print(f"[{self.name}] Processing: {input_text}")

        # Simulate processing
        result = f"Processed by {self.name}: {input_text}"

        return result

    def reset(self) -> None:
        """Reset agent state."""
        self.state = None
        self._execution_count = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get agent execution statistics.

        Returns:
            Dictionary with execution stats
        """
        return {
            "name": self.name,
            "execution_count": self._execution_count,
            "has_state": self.state is not None,
            "config_summary": self.config.engine.get_summary(),
        }
