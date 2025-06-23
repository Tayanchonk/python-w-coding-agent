"""
Repository interfaces for the domain layer
"""
from abc import ABC, abstractmethod
from typing import List, Optional
import uuid

from app.domain.entities.employee import User, Employee, Position


class IUserRepository(ABC):
    """User repository interface"""

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID"""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user"""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update an existing user"""
        pass

    @abstractmethod
    async def delete(self, user_id: uuid.UUID) -> bool:
        """Delete a user"""
        pass


class IEmployeeRepository(ABC):
    """Employee repository interface"""

    @abstractmethod
    async def get_by_id(self, employee_id: uuid.UUID) -> Optional[Employee]:
        """Get employee by ID"""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all employees with pagination"""
        pass

    @abstractmethod
    async def get_by_position_id(self, position_id: uuid.UUID) -> List[Employee]:
        """Get all employees in a specific position"""
        pass

    @abstractmethod
    async def create(self, employee: Employee) -> Employee:
        """Create a new employee"""
        pass

    @abstractmethod
    async def update(self, employee: Employee) -> Employee:
        """Update an existing employee"""
        pass

    @abstractmethod
    async def delete(self, employee_id: uuid.UUID) -> bool:
        """Delete an employee"""
        pass


class IPositionRepository(ABC):
    """Position repository interface"""

    @abstractmethod
    async def get_by_id(self, position_id: uuid.UUID) -> Optional[Position]:
        """Get position by ID"""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Position]:
        """Get all positions with pagination"""
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Position]:
        """Get position by name"""
        pass

    @abstractmethod
    async def create(self, position: Position) -> Position:
        """Create a new position"""
        pass

    @abstractmethod
    async def update(self, position: Position) -> Position:
        """Update an existing position"""
        pass

    @abstractmethod
    async def delete(self, position_id: uuid.UUID) -> bool:
        """Delete a position"""
        pass

    @abstractmethod
    async def has_employees(self, position_id: uuid.UUID) -> bool:
        """Check if position has any employees assigned"""
        pass