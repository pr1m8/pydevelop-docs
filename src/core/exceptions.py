"""Custom exceptions for the core module.

This module defines the exception hierarchy used throughout the application
for error handling and reporting.
"""

from typing import Any, Dict, Optional


class CoreException(Exception):
    """Base exception for all core module errors.

    All exceptions in the core module should inherit from this class
    to maintain a consistent exception hierarchy.

    Attributes:
        message: Human-readable error description.
        error_code: Optional error code for programmatic handling.
        context: Additional context information about the error.
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}

    def __str__(self) -> str:
        """Return a formatted error message."""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ValidationError(CoreException):
    """Raised when data validation fails.

    This exception is used when input data doesn't meet the required
    constraints or format specifications.

    Example:
        >>> raise ValidationError("Invalid email format", error_code="VAL001")
    """

    pass


class ProcessingError(CoreException):
    """Raised when data processing operations fail.

    This exception indicates failures during data transformation,
    calculation, or other processing operations.
    """

    pass


class ConfigurationError(CoreException):
    """Raised when configuration is invalid or missing.

    Used for errors related to application configuration,
    environment variables, or settings files.
    """

    pass


class AuthenticationError(CoreException):
    """Raised when authentication fails.

    Indicates failures in user authentication, token validation,
    or permission checks.
    """

    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, error_code="AUTH001", **kwargs)


class NotFoundError(CoreException):
    """Raised when a requested resource is not found.

    Used when database queries, file operations, or API calls
    fail to find the requested resource.
    """

    def __init__(self, resource_type: str, resource_id: Any, **kwargs):
        message = f"{resource_type} with id '{resource_id}' not found"
        super().__init__(message, error_code="NF404", **kwargs)
        self.resource_type = resource_type
        self.resource_id = resource_id
