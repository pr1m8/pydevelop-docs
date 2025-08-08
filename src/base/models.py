from pydantic import BaseModel, Field
from typing import Optional
from .enums import UserRole

class User(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole = UserRole.MEMBER
    is_active: bool = True