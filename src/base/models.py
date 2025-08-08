from datetime import datetime
from typing import Any, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    computed_field,
    field_validator,
    model_validator,
)

from .enums import UserRole


class User(BaseModel):
    """Represents an individual user account in the system.

    This model captures identifying and authorization data for users,
    including support for metadata, validation, and computed fields.

    Attributes:
        id (int): Unique identifier (positive integer).
        name (str): Full display name, automatically title-cased and validated.
        email (EmailStr): Valid email address for login and communication.
        role (UserRole): Access role (e.g., admin, member, guest).
        is_active (bool): Indicates whether the user account is enabled.
        created_at (datetime): Timestamp for when the account was created.
        updated_at (Optional[datetime]): Timestamp of the most recent profile update.
        metadata (dict): Arbitrary key-value metadata for advanced configuration.

    Computed Fields:
        username (str): Local part of the user's email (before @).
        domain (str): Domain part of the user's email (after @).
        email_verified (bool): Whether the email uses a verified domain.
        profile_url (str): Canonical URL path to the user's profile.
    """

    id: int = Field(
        ...,
        gt=0,
        description="Internal unique identifier for the user (positive integer).",
        json_schema_extra={"example": 123},
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z\s\.\'-]+$",
        description="User's full name. Must use letters, spaces, and punctuation.",
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address. Must be unique.",
        examples=["jane.doe@example.com"],
    )
    role: UserRole = Field(
        default=UserRole.MEMBER,
        description="Access role that determines user permissions.",
    )
    is_active: bool = Field(
        default=True, description="True if the account is active and usable."
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when the user account was created.",
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="UTC timestamp of last update. Optional."
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Arbitrary JSON-serializable metadata."
    )

    @field_validator("name")
    @classmethod
    def strip_and_title_case(cls, name: str) -> str:
        """Ensure the name is clean and title-cased.

        Args:
            name: Raw name string.

        Returns:
            A stripped and title-cased name string.
        """
        return name.strip().title()

    @model_validator(mode="after")
    def validate_admin_email(self) -> "User":
        """Ensure admins use a company email domain.

        Raises:
            ValueError: If admin has a non-company email address.

        Returns:
            User: The validated user model.
        """
        if self.role == UserRole.ADMIN and not self.email.endswith("@company.com"):
            raise ValueError("Admins must use a @company.com email address.")
        return self

    @computed_field
    @property
    def username(self) -> str:
        """Username extracted from the local part of the email.

        Returns:
            str: The part of the email before '@'.
        """
        return self.email.split("@")[0]

    @computed_field
    @property
    def domain(self) -> str:
        """Email domain (after '@').

        Returns:
            str: The domain of the email.
        """
        return self.email.split("@")[-1]

    @computed_field
    @property
    def email_verified(self) -> bool:
        """Check if the email is from an approved/verified domain.

        Returns:
            bool: True if domain is 'company.com', otherwise False.
        """
        return self.domain == "company.com"

    @computed_field
    @property
    def profile_url(self) -> str:
        """Canonical profile URL for the user.

        Returns:
            str: A URL path like '/users/jane.doe'.
        """
        return f"/users/{self.username.lower().replace('.', '-')}"

    def get_profile_url(self) -> str:
        """Canonical profile URL for the user.

        Returns:
            str: A URL path like '/users/jane.doe'.
        """
        return f"/users/{self.username.lower().replace('.', '-')}"
