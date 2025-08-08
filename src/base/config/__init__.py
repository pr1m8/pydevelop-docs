"""Configuration management package.

This package provides comprehensive configuration management for the application,
including system configuration, settings management, and environment handling.

Modules:
    system: System-level configuration and environment detection
    settings: Application settings using Pydantic BaseSettings

Example:
    >>> from base.config import settings, Environment
    >>>
    >>> # Access application settings
    >>> print(settings.app.app_name)
    PyAutoDoc
    >>>
    >>> # Check environment
    >>> if settings.app.environment == Environment.PROD:
    ...     print("Running in production")
"""

from .settings import (
    AppSettings,
    CacheBackend,
    CacheSettings,
    DatabaseSettings,
    DatabaseType,
    LoggingSettings,
    LogLevel,
    Settings,
    settings,
)
from .system import (
    Environment,
    SystemConfig,
    get_system_config,
)

__all__ = [
    # System config
    "Environment",
    "SystemConfig",
    "get_system_config",
    # Settings enums
    "LogLevel",
    "DatabaseType",
    "CacheBackend",
    # Settings classes
    "AppSettings",
    "DatabaseSettings",
    "CacheSettings",
    "LoggingSettings",
    "Settings",
    # Global settings instance
    "settings",
]
