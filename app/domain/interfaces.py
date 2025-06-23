"""
Repository interfaces defining contracts for data access
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import User, Employee, Position


class UserRepositoryInterface(ABC):
    """Interface for user data access"""

    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user"""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Update existing user"""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete user by ID"""
        pass


class EmployeeRepositoryInterface(ABC):
    """Interface for employee data access"""

    @abstractmethod
    def create(self, employee: Employee) -> Employee:
        """Create a new employee"""
        pass

    @abstractmethod
    def get_by_id(self, emp_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all employees with pagination"""
        pass

    @abstractmethod
    def update(self, employee: Employee) -> Employee:
        """Update existing employee"""
        pass

    @abstractmethod
    def delete(self, emp_id: int) -> bool:
        """Delete employee by ID"""
        pass


class PositionRepositoryInterface(ABC):
    """Interface for position data access"""

    @abstractmethod
    def create(self, position: Position) -> Position:
        """Create a new position"""
        pass

    @abstractmethod
    def get_by_id(self, position_id: int) -> Optional[Position]:
        """Get position by ID"""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Position]:
        """Get all positions with pagination"""
        pass

    @abstractmethod
    def update(self, position: Position) -> Position:
        """Update existing position"""
        pass

    @abstractmethod
    def delete(self, position_id: int) -> bool:
        """Delete position by ID"""
        pass