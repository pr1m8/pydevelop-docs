from pydantic import field_validator

@field_validator("email")
def validate_email(cls, v):
    if "@" not in v:
        raise ValueError("Invalid email address")
    return v