"""Base tool class for testhaive framework."""

from typing import Any, Dict

from pydantic import BaseModel, Field


class BaseTool(BaseModel):
    """Base class for all tools in testhaive framework."""

    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")

    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        return {"result": "Tool executed successfully"}
