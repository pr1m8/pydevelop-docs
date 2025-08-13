"""Meta-schema classes for advanced state management."""

from typing import Any, Dict, List, Optional, Type

from pydantic import Field

from .base import StateSchema


class MetaStateSchema(StateSchema):
    """Meta-state schema for complex state projections."""

    agent_states: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Agent states storage"
    )

    def __init__(self, **kwargs):
        kwargs.setdefault("state_type", "meta_state")
        super().__init__(**kwargs)


class StateProjection(StateSchema):
    """State projection for filtered views."""

    source_state_id: str = Field(..., description="Source state ID")
    projection_fields: List[str] = Field(default_factory=list)


class StateTransfer(StateSchema):
    """State transfer configuration."""

    transfer_rules: Dict[str, str] = Field(default_factory=dict)
    source_agent: str = Field(..., description="Source agent name")
    target_agent: str = Field(..., description="Target agent name")
