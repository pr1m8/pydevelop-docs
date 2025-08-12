"""PyDevelop Documentation Tools.

Universal Python documentation generator with 40+ Sphinx extensions pre-configured.
Turn any Python project into beautiful documentation with zero configuration.

Features:
    - 🎯 Zero Configuration: Works out-of-the-box with any Python project
    - 📦 Universal Support: Single packages, monorepos, any structure
    - 🎨 Beautiful Themes: Pre-configured Furo theme with dark mode
    - 🔧 40+ Extensions: Complete extension suite included
    - ⚡ Smart Detection: Automatically detects project structure
    - 🚀 Interactive CLI: Guided setup with rich terminal UI

Quick Start:
    1. Install: pip install pydevelop-docs
    2. Initialize: pydevelop-docs init
    3. Build: pydevelop-docs build

    Your documentation is ready at docs/build/html/index.html!

Example:
    Basic usage in your project's docs/source/conf.py:

    >>> from pydevelop_docs.config import get_haive_config
    >>> config = get_haive_config(
    ...     package_name=\"my-package\",
    ...     package_path=\"../../src\"
    ... )
    >>> globals().update(config)
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
