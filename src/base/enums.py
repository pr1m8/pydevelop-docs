from enum import Enum


class UserRole(str, Enum):
    """Defines the set of roles a user can have within the system.

    Attributes:
        ADMIN: Full administrative privileges.
        MEMBER: Standard authenticated user with limited permissions.
        GUEST: Unauthenticated or read-only access.
    """

    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"

    @classmethod
    def list(cls) -> list[str]:
        """Return a list of all role values."""
        return [role.value for role in cls]


class Environment(str, Enum):
    """Defines the environment in which the application is running.

    Attributes:
        DEV: Local development environment.
        STAGING: Pre-production testing environment.
        PROD: Live production environment.
    """

    DEV = "development"
    STAGING = "staging"
    PROD = "production"

    @classmethod
    def list(cls) -> list[str]:
        """Return a list of all environment values."""
        return [env.value for env in cls]
