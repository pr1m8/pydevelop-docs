"""Application settings and configuration.

This module provides settings management using Pydantic v2,
supporting environment variables and configuration files.
"""

import json
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..enums import Environment


class LogLevel(str, Enum):
    """Logging level enumeration."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DatabaseType(str, Enum):
    """Supported database types."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"


class CacheBackend(str, Enum):
    """Supported cache backends."""

    MEMORY = "memory"
    REDIS = "redis"
    MEMCACHED = "memcached"


class AppSettings(BaseSettings):
    """Main application settings.

    Loads configuration from environment variables and .env files.
    All settings can be overridden via environment variables with
    the ``APP_`` prefix.

    Attributes:
        app_name: Application name
        app_version: Application version
        debug: Debug mode flag
        environment: Current environment
        secret_key: Application secret key
        allowed_hosts: List of allowed hosts
        cors_origins: List of allowed CORS origins
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="APP_",
    )

    # Application settings
    app_name: str = Field(default="PyAutoDoc")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)
    environment: Environment = Field(default=Environment.DEV)

    # Security
    secret_key: SecretStr = Field(default=SecretStr("dev-secret-key"))
    allowed_hosts: List[str] = Field(default=["localhost", "127.0.0.1"])
    cors_origins: List[str] = Field(default=["http://localhost:3000"])

    # API settings
    api_prefix: str = Field(default="/api/v1")
    api_title: str = Field(default="PyAutoDoc API")
    api_docs_enabled: bool = Field(default=True)

    @field_validator("allowed_hosts", "cors_origins", mode="before")
    @classmethod
    def parse_list_env_var(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v

    @field_validator("debug")
    @classmethod
    def validate_debug(cls, v, info):
        """Ensure debug is False in production."""
        if info.data.get("environment") == Environment.PROD and v:
            raise ValueError("Debug mode cannot be enabled in production")
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == Environment.PROD

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == Environment.DEV


class DatabaseSettings(BaseSettings):
    """Database configuration settings.

    Supports multiple database backends with connection pooling
    and performance tuning options.
    """

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_")

    # Connection settings
    db_type: DatabaseType = Field(default=DatabaseType.SQLITE)
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=5432)
    db_name: str = Field(default="pyautodoc")
    db_user: Optional[str] = Field(default=None)
    db_password: Optional[SecretStr] = Field(default=None)

    # Connection pool settings
    db_pool_size: int = Field(default=10, ge=1, le=100)
    db_pool_timeout: int = Field(default=30, ge=1)
    db_pool_recycle: int = Field(default=3600, ge=60)

    # SQLite specific
    db_sqlite_path: Path = Field(default=Path("data/app.db"))

    @property
    def connection_string(self) -> str:
        """Generate database connection string."""
        if self.db_type == DatabaseType.SQLITE:
            return f"sqlite:///{self.db_sqlite_path}"

        auth = ""
        if self.db_user and self.db_password:
            auth = f"{self.db_user}:{self.db_password.get_secret_value()}@"

        return f"{self.db_type}://{auth}{self.db_host}:{self.db_port}/{self.db_name}"

    @field_validator("db_sqlite_path")
    @classmethod
    def ensure_sqlite_dir_exists(cls, v: Path) -> Path:
        """Ensure SQLite database directory exists."""
        v.parent.mkdir(parents=True, exist_ok=True)
        return v


class CacheSettings(BaseSettings):
    """Cache configuration settings.

    Configures caching backend and behavior for performance optimization.
    """

    model_config = SettingsConfigDict(env_file=".env", env_prefix="CACHE_")

    cache_backend: CacheBackend = Field(default=CacheBackend.MEMORY)
    cache_ttl: int = Field(default=300, ge=0)  # seconds
    cache_key_prefix: str = Field(default="pyautodoc:")

    # Redis specific
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0, ge=0, le=15)
    redis_password: Optional[SecretStr] = Field(default=None)

    # Memory cache specific
    memory_cache_max_size: int = Field(default=1000, ge=1)

    @property
    def redis_url(self) -> str:
        """Generate Redis connection URL."""
        auth = ""
        if self.redis_password:
            auth = f":{self.redis_password.get_secret_value()}@"
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"


class LoggingSettings(BaseSettings):
    """Logging configuration settings.

    Configures application logging behavior including levels,
    formats, and output destinations.
    """

    model_config = SettingsConfigDict(env_file=".env", env_prefix="LOG_")

    log_level: LogLevel = Field(default=LogLevel.INFO)
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    log_date_format: str = Field(default="%Y-%m-%d %H:%M:%S")

    # File logging
    log_to_file: bool = Field(default=False)
    log_file_path: Path = Field(default=Path("logs/app.log"))
    log_file_max_bytes: int = Field(default=10485760)  # 10MB
    log_file_backup_count: int = Field(default=5)

    # Structured logging
    log_json_format: bool = Field(default=False)

    # Log filtering
    log_exclude_paths: Set[str] = Field(default={"/health", "/metrics", "/static"})

    @field_validator("log_exclude_paths", mode="before")
    @classmethod
    def parse_set_env_var(cls, v):
        if isinstance(v, str):
            return set(x.strip() for x in v.split(","))
        return v

    @field_validator("log_file_path")
    @classmethod
    def ensure_log_dir_exists(cls, v: Path) -> Path:
        """Ensure log directory exists."""
        v.parent.mkdir(parents=True, exist_ok=True)
        return v


class Settings(BaseModel):
    """Combined application settings.

    Aggregates all setting groups into a single configuration object.
    This is the main settings class that should be used throughout
    the application.

    Attributes:
        app: Application-specific settings
        database: Database configuration
        cache: Cache configuration
        logging: Logging configuration
    """

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    # Feature flags
    features: Dict[str, bool] = Field(
        default_factory=lambda: {
            "new_ui": False,
            "beta_api": False,
            "analytics": True,
        }
    )

    @field_validator("features", mode="before")
    @classmethod
    def parse_features(cls, v):
        if isinstance(v, str):
            return json.loads(v) if v else {}
        return v

    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature flag is enabled."""
        return self.features.get(feature_name, False)

    def to_dict(self, exclude_secrets: bool = True) -> Dict[str, Any]:
        """Convert settings to dictionary.

        Args:
            exclude_secrets: Whether to exclude secret values

        Returns:
            Settings as dictionary
        """
        data = self.model_dump()

        if exclude_secrets:
            # Recursively mask secret values
            def mask_secrets(obj):
                if isinstance(obj, dict):
                    return {
                        k: mask_secrets(v) if not k.endswith("password") else "***"
                        for k, v in obj.items()
                    }
                return obj

            data = mask_secrets(data)

        return data


# Create global settings instance
settings = Settings()
