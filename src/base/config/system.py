from pydantic import BaseModel, Field

from ..enums import Environment


class SystemConfig(BaseModel):
    env: Environment
    debug: bool = False
    log_level: str = Field(default="INFO", pattern="DEBUG|INFO|WARNING|ERROR")


def get_system_config() -> SystemConfig:
    """Get system configuration."""
    return SystemConfig(env=Environment.DEV)
