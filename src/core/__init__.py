"""Core functionality module.

This package provides the core business logic, data structures,
and utilities for the application. It includes exception handling,
data models, services, and various utility functions.

Modules:
    exceptions: Custom exception hierarchy
    data_structures: Core data structures using dataclasses
    services: Service layer implementations
    utils: Utility functions and helpers

Example:
    >>> from core import Task, TaskService, Priority
    >>> from core.utils import generate_id, Timer
    >>>
    >>> # Create a new task
    >>> task = Task(
    ...     id=generate_id("task"),
    ...     title="Complete documentation",
    ...     priority=Priority.HIGH
    ... )
"""

# Version
__version__ = "0.1.0"

# Data structures
from .data_structures import (
    Point,
    Priority,
    Result,
    Status,
    Task,
)

# Core exceptions
from .exceptions import (
    AuthenticationError,
    ConfigurationError,
    CoreException,
    NotFoundError,
    ProcessingError,
    ValidationError,
)

# Services
from .services import (
    InMemoryTaskRepository,
    MetricsCollector,
    Repository,
    TaskService,
    retry,
)

# Utilities
from .utils import (
    RateLimiter,
    Timer,
    batch,
    deep_merge,
    find_files,
    format_bytes,
    generate_id,
    hash_password,
    memoize,
    parse_size,
    safe_json_loads,
    slugify,
    timedelta_to_human,
    truncate_string,
    validate_email,
)

# Define public API
__all__ = [
    # Version
    "__version__",
    # Exceptions
    "CoreException",
    "ValidationError",
    "ProcessingError",
    "ConfigurationError",
    "AuthenticationError",
    "NotFoundError",
    # Data structures
    "Priority",
    "Status",
    "Point",
    "Task",
    "Result",
    # Services
    "Repository",
    "InMemoryTaskRepository",
    "TaskService",
    "MetricsCollector",
    "retry",
    # Utilities
    "generate_id",
    "slugify",
    "hash_password",
    "timedelta_to_human",
    "parse_size",
    "format_bytes",
    "Timer",
    "memoize",
    "validate_email",
    "deep_merge",
    "batch",
    "safe_json_loads",
    "truncate_string",
    "find_files",
    "RateLimiter",
]
