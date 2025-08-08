"""User management models and enums.

This module provides data structures and enumerations for representing users
and their roles within the system. It includes the core `User` model and the
`UserRole` enum used to control access and behavior across different parts of
the application.

Modules:
    models: Defines the `User` Pydantic model with validation and serialization.
    enums: Provides the `UserRole` and related enumerations used throughout the app.

Examples:
    >>> from myapp.users import User, UserRole
    >>> user = User(id=1, name="Alice", email="alice@company.com", role=UserRole.ADMIN)
    >>> print(user.name)
    Alice
"""

from .enums import UserRole
from .models import User
