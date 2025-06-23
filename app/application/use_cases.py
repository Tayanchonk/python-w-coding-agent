"""
Use cases for employee management operations
"""
from typing import List, Optional

from app.domain.entities import Employee, Position
from app.domain.interfaces import EmployeeRepositoryInterface, PositionRepositoryInterface


class EmployeeUseCase:
    """Use case for employee operations"""

    def __init__(
        self,
        employee_repository: EmployeeRepositoryInterface,
        position_repository: PositionRepositoryInterface
    ):
        self.employee_repository = employee_repository
        self.position_repository = position_repository

    def create_employee(self, first_name: str, last_name: str, position_id: int) -> Employee:
        """Create a new employee"""
        # Validate position exists
        position = self.position_repository.get_by_id(position_id)
        if not position:
            raise ValueError(f"Position with ID {position_id} not found")
        
        employee = Employee(
            emp_id=None,
            first_name=first_name,
            last_name=last_name,
            position_id=position_id
        )
        return self.employee_repository.create(employee)

    def get_employee_by_id(self, emp_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        return self.employee_repository.get_by_id(emp_id)

    def get_all_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all employees with pagination"""
        return self.employee_repository.get_all(skip, limit)

    def update_employee(self, emp_id: int, first_name: str, last_name: str, position_id: int) -> Employee:
        """Update an existing employee"""
        # Check if employee exists
        existing_employee = self.employee_repository.get_by_id(emp_id)
        if not existing_employee:
            raise ValueError(f"Employee with ID {emp_id} not found")
        
        # Validate position exists
        position = self.position_repository.get_by_id(position_id)
        if not position:
            raise ValueError(f"Position with ID {position_id} not found")
        
        updated_employee = Employee(
            emp_id=emp_id,
            first_name=first_name,
            last_name=last_name,
            position_id=position_id
        )
        return self.employee_repository.update(updated_employee)

    def delete_employee(self, emp_id: int) -> bool:
        """Delete an employee"""
        # Check if employee exists
        existing_employee = self.employee_repository.get_by_id(emp_id)
        if not existing_employee:
            raise ValueError(f"Employee with ID {emp_id} not found")
        
        return self.employee_repository.delete(emp_id)


class PositionUseCase:
    """Use case for position operations"""

    def __init__(self, position_repository: PositionRepositoryInterface):
        self.position_repository = position_repository

    def create_position(self, position_name: str, description: Optional[str] = None) -> Position:
        """Create a new position"""
        position = Position(
            position_id=None,
            position_name=position_name,
            description=description
        )
        return self.position_repository.create(position)

    def get_position_by_id(self, position_id: int) -> Optional[Position]:
        """Get position by ID"""
        return self.position_repository.get_by_id(position_id)

    def get_all_positions(self, skip: int = 0, limit: int = 100) -> List[Position]:
        """Get all positions with pagination"""
        return self.position_repository.get_all(skip, limit)

    def update_position(self, position_id: int, position_name: str, description: Optional[str] = None) -> Position:
        """Update an existing position"""
        # Check if position exists
        existing_position = self.position_repository.get_by_id(position_id)
        if not existing_position:
            raise ValueError(f"Position with ID {position_id} not found")
        
        updated_position = Position(
            position_id=position_id,
            position_name=position_name,
            description=description
        )
        return self.position_repository.update(updated_position)

    def delete_position(self, position_id: int) -> bool:
        """Delete a position"""
        # Check if position exists
        existing_position = self.position_repository.get_by_id(position_id)
        if not existing_position:
            raise ValueError(f"Position with ID {position_id} not found")
        
        return self.position_repository.delete(position_id)