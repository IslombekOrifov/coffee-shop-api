from enum import StrEnum


class UserStatus(StrEnum):
    """
    Enum for user status:
    - UNVERIFIED: user has not verified their email
    - VERIFIED: user has verified their email
    """
    UNVERIFIED = "unverified"
    VERIFIED = "verified"

    def __str__(self) -> str:
        return self.value


class Role(StrEnum):
    """
    Enum for user role:
    - USER:
    - ADMIN:
    """
    USER = "user"
    ADMIN = "admin"

    def __str__(self) -> str:
        return self.value

