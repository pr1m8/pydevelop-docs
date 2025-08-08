from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

class Environment(str, Enum):
    DEV = "development"
    STAGING = "staging"
    PROD = "production"