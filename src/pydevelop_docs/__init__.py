"""Haive Documentation System - Shared Configuration and Themes.

Universal documentation tools for Python projects with full PyAutoDoc configuration.
"""

__version__ = "0.1.0"
__author__ = "Haive Team"
__email__ = "team@haive.ai"

# Export main configuration functions
from .config import get_central_hub_config, get_haive_config

# Export builders (if available)
try:
    from .builders import (
        BaseDocumentationBuilder,
        CustomConfigBuilder,
        MonorepoBuilder,
        SinglePackageBuilder,
        get_builder,
    )

    __all__ = [
        "get_haive_config",
        "get_central_hub_config",
        "BaseDocumentationBuilder",
        "SinglePackageBuilder",
        "MonorepoBuilder",
        "CustomConfigBuilder",
        "get_builder",
    ]
except ImportError:
    # CLI dependencies might not be installed
    __all__ = ["get_haive_config", "get_central_hub_config"]
