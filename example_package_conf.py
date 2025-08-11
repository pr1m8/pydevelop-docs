"""Example conf.py for a Haive package using haive-docs.

This shows how a submodule like haive-core can use the shared configuration.
Place this in your package's docs/source/conf.py
"""

import os
import sys
from pathlib import Path

# Add the package to the Python path
package_root = Path(__file__).parents[2]
sys.path.insert(0, str(package_root / "src"))

# Import shared Haive configuration
try:
    from haive_docs import get_haive_config

    # Get base configuration for this package
    config = get_haive_config(
        package_name="haive-core",  # Change this for each package
        package_path=str(package_root / "src"),
        is_central_hub=False,
        extra_extensions=[
            # Add package-specific extensions here
            "sphinx_autodoc_typehints",
            "sphinxcontrib.autodoc_pydantic",
        ],
    )

    # Apply configuration to globals
    globals().update(config)

    # Package-specific customizations
    html_title = f"{project} Documentation"

except ImportError:
    # Fallback to standalone configuration if haive-docs not available
    print("Warning: haive-docs not installed, using fallback configuration")

    # Minimal fallback configuration
    project = "Haive Core"
    author = "Haive Team"
    copyright = "2025, Haive Team"

    extensions = [
        "sphinx.ext.autodoc",
        "autoapi.extension",
        "sphinx.ext.napoleon",
        "myst_parser",
    ]

    html_theme = "furo"
    autoapi_dirs = [str(package_root / "src")]
    autoapi_type = "python"
