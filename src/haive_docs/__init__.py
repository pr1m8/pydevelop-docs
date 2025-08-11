"""Haive Documentation System - Shared Configuration and Themes."""

__version__ = "0.1.0"
__author__ = "Haive Team"

# Export main configuration functions
from .config import get_central_hub_config, get_haive_config

__all__ = ["get_haive_config", "get_central_hub_config"]
