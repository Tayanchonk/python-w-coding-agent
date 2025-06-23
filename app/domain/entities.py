"""
Domain entities representing core business objects
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """User domain entity"""
    user_id: Optional[int]
    username: str
    email: str
    password: Optional[str] = None  # Only set during creation/password change
    is_active: bool = True

    def __post_init__(self):
        if not self.username or not self.email:
            raise ValueError("Username and email are required")


@dataclass
class Position:
    """Position domain entity"""
    position_id: Optional[int]
    position_name: str
    description: Optional[str] = None

    def __post_init__(self):
        if not self.position_name:
            raise ValueError("Position name is required")


@dataclass
class Employee:
    """Employee domain entity"""
    emp_id: Optional[int]
    first_name: str
    last_name: str
    position_id: int
    position: Optional[Position] = None

    def __post_init__(self):
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name are required")
        if not self.position_id:
            raise ValueError("Position ID is required")

    @property
    def full_name(self) -> str:
        """Get employee's full name"""
        return f"{self.first_name} {self.last_name}"