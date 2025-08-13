"""TestHaive Agents - Agent implementations.

This package mimics the structure of haive.agents for testing documentation generation.
"""

from .multi.agent import MultiAgent
from .react.agent import ReactAgent
from .simple.agent import SimpleAgent

__version__ = "0.1.0"
__all__ = [
    "SimpleAgent",
    "ReactAgent",
    "MultiAgent",
]
