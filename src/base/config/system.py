from pydantic import BaseModel, Field
from base.enums import Environment

class SystemConfig(BaseModel):
    env: Environment
    debug: bool = False
    log_level: str = Field(default="INFO", pattern="DEBUG|INFO|WARNING|ERROR")