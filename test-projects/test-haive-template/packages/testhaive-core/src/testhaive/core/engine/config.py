"""Configuration classes for testhaive.core.engine (mimics AugLLMConfig).

This module provides configuration management similar to AugLLMConfig in Haive.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EngineMode(str, Enum):
    """Engine execution modes (mimics Haive's patterns)."""

    SIMPLE = "simple"
    REACT = "react"
    MULTI_AGENT = "multi_agent"
    STREAMING = "streaming"


class TestLLMConfig(BaseModel):
    """Main LLM configuration class (mimics AugLLMConfig).

    This class mimics the complexity and patterns of AugLLMConfig.

    Args:
        name: Configuration name
        model: LLM model identifier
        mode: Engine execution mode
        temperature: Sampling temperature (0.0-2.0)
        max_tokens: Maximum output tokens
        tools: List of available tools
        system_message: System prompt
        metadata: Additional configuration metadata

    Examples:
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
    """

    name: str = Field(..., description="Configuration identifier")
    model: str = Field(default="gpt-4", description="LLM model identifier")
    mode: EngineMode = Field(default=EngineMode.SIMPLE, description="Engine mode")
    temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="Sampling temperature"
    )
    max_tokens: Optional[int] = Field(
        default=None, ge=1, description="Maximum output tokens"
    )
    tools: List[str] = Field(default_factory=list, description="Available tools")
    system_message: Optional[str] = Field(default=None, description="System prompt")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    def add_tool(self, tool_name: str) -> None:
        """Add a tool to the configuration.

        Args:
            tool_name: Name of the tool to add
        """
        if tool_name not in self.tools:
            self.tools.append(tool_name)

    def remove_tool(self, tool_name: str) -> None:
        """Remove a tool from the configuration.

        Args:
            tool_name: Name of the tool to remove
        """
        if tool_name in self.tools:
            self.tools.remove(tool_name)

    def with_tools(self, tools: List[str]) -> "TestLLMConfig":
        """Create a new config with specified tools.

        Args:
            tools: List of tool names

        Returns:
            New TestLLMConfig instance with tools
        """
        return self.model_copy(update={"tools": tools})

    def get_summary(self) -> Dict[str, Any]:
        """Get configuration summary.

        Returns:
            Dictionary containing configuration summary
        """
        return {
            "name": self.name,
            "model": self.model,
            "mode": self.mode,
            "temperature": self.temperature,
            "tool_count": len(self.tools),
            "has_system_message": bool(self.system_message),
            "has_metadata": bool(self.metadata),
        }
