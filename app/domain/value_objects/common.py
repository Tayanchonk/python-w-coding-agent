"""
Value objects for the domain layer
"""
from dataclasses import dataclass
from typing import Optional
import re
import uuid


@dataclass(frozen=True)
class Email:
    """Email value object with validation"""
    value: str

    def __post_init__(self):
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email format: {self.value}")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Username:
    """Username value object with validation"""
    value: str

    def __post_init__(self):
        if not self._is_valid_username(self.value):
            raise ValueError(f"Invalid username: {self.value}")

    @staticmethod
    def _is_valid_username(username: str) -> bool:
        """Validate username format"""
        if len(username) < 3 or len(username) > 50:
            return False
        # Allow alphanumeric characters, underscores, and hyphens
        pattern = r'^[a-zA-Z0-9_-]+$'
        return re.match(pattern, username) is not None

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class PersonName:
    """Person name value object with validation"""
    value: str

    def __post_init__(self):
        if not self._is_valid_name(self.value):
            raise ValueError(f"Invalid name: {self.value}")

    @staticmethod
    def _is_valid_name(name: str) -> bool:
        """Validate name format"""
        if len(name) < 1 or len(name) > 50:
            return False
        # Allow letters, spaces, hyphens, and apostrophes
        pattern = r"^[a-zA-Z\s\-']+$"
        return re.match(pattern, name) is not None

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class EntityId:
    """Entity ID value object"""
    value: uuid.UUID

    def __post_init__(self):
        if not isinstance(self.value, uuid.UUID):
            raise ValueError("ID must be a valid UUID")

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def generate(cls) -> 'EntityId':
        """Generate a new random EntityId"""
        return cls(uuid.uuid4())

    @classmethod
    def from_string(cls, id_str: str) -> 'EntityId':
        """Create EntityId from string"""
        try:
            return cls(uuid.UUID(id_str))
        except ValueError as e:
            raise ValueError(f"Invalid UUID string: {id_str}") from e


@dataclass(frozen=True)
class PositionName:
    """Position name value object with validation"""
    value: str

    def __post_init__(self):
        if not self._is_valid_position_name(self.value):
            raise ValueError(f"Invalid position name: {self.value}")

    @staticmethod
    def _is_valid_position_name(name: str) -> bool:
        """Validate position name format"""
        if len(name) < 1 or len(name) > 100:
            return False
        # Allow letters, numbers, spaces, hyphens, and some special characters
        pattern = r"^[a-zA-Z0-9\s\-/()&.]+$"
        return re.match(pattern, name) is not None

    def __str__(self) -> str:
        return self.value