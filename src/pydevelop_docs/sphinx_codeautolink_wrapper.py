"""
Wrapper for sphinx-codeautolink to handle Python 3.10 union type issues gracefully.

This module provides a fallback mechanism when sphinx-codeautolink encounters
the new union type syntax (X | Y) introduced in Python 3.10.
"""

import warnings
from typing import Any, Dict


def setup(app):
    """Setup sphinx-codeautolink with error handling."""
    try:
        # Try to import and setup sphinx-codeautolink
        import sphinx_codeautolink

        # Store original setup
        original_setup = sphinx_codeautolink.setup

        # Wrap the original setup with error handling
        def safe_setup(app):
            try:
                return original_setup(app)
            except Exception as e:
                if "unsupported operand type" in str(e) and "NoneType" in str(e):
                    warnings.warn(
                        "sphinx-codeautolink disabled due to Python 3.10 union type syntax. "
                        "Code examples will not be automatically linked. "
                        "Consider using Union[X, Y] syntax instead of X | Y.",
                        category=UserWarning,
                    )
                    # Return valid extension metadata without failing
                    return {
                        "version": "0.1.0",
                        "parallel_read_safe": True,
                        "parallel_write_safe": True,
                    }
                else:
                    # Re-raise other exceptions
                    raise

        # Use the safe setup
        return safe_setup(app)

    except ImportError:
        # sphinx-codeautolink not installed
        warnings.warn(
            "sphinx-codeautolink not available. Code examples will not be automatically linked.",
            category=UserWarning,
        )
        return {
            "version": "0.1.0",
            "parallel_read_safe": True,
            "parallel_write_safe": True,
        }


def get_codeautolink_config() -> Dict[str, Any]:
    """Get configuration for sphinx-codeautolink with fallback options."""
    return {
        # Try to use sphinx-codeautolink, but don't fail if it has issues
        "codeautolink_global_preface": "",
        "codeautolink_custom_blocks": {},
        "codeautolink_concat_default": True,
        # Add configuration to handle union types better
        "codeautolink_warn_on_missing_inventory": False,
        "codeautolink_warn_on_failed_resolve": False,
    }
