"""
Domain entities for the Employee Management System
"""
from abc import ABC
from dataclasses import dataclass
from typing import Optional
import uuid
from datetime import datetime


@dataclass
class BaseEntity(ABC):
    """Base entity with common properties"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if self.id is None:
            self.id = uuid.uuid4()
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


@dataclass
class User(BaseEntity):
    """User domain entity"""
    username: str
    email: str
    password_hash: str
    is_active: bool = True

    def __post_init__(self):
        super().__post_init__()

    def deactivate(self) -> None:
        """Deactivate the user"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activate the user"""
        self.is_active = True
        self.updated_at = datetime.utcnow()


@dataclass
class Position(BaseEntity):
    """Position domain entity"""
    name: str
    description: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()

    def update_details(self, name: str, description: Optional[str] = None) -> None:
        """Update position details"""
        self.name = name
        self.description = description
        self.updated_at = datetime.utcnow()


@dataclass
class Employee(BaseEntity):
    """Employee domain entity"""
    first_name: str
    last_name: str
    position_id: uuid.UUID
    position: Optional[Position] = None

    def __post_init__(self):
        super().__post_init__()

    @property
    def full_name(self) -> str:
        """Get employee's full name"""
        return f"{self.first_name} {self.last_name}"

    def update_personal_info(self, first_name: str, last_name: str) -> None:
        """Update employee's personal information"""
        self.first_name = first_name
        self.last_name = last_name
        self.updated_at = datetime.utcnow()

    def change_position(self, position_id: uuid.UUID) -> None:
        """Change employee's position"""
        self.position_id = position_id
        self.updated_at = datetime.utcnow()