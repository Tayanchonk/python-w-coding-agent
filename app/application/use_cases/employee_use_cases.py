"""
Employee use cases
"""
from typing import List, Optional
import uuid
from datetime import datetime

from app.domain.entities.employee import Employee, Position
from app.domain.interfaces.repositories import IEmployeeRepository, IPositionRepository
from app.domain.value_objects.common import PersonName, EntityId


class EmployeeUseCases:
    """Employee business logic use cases"""

    def __init__(
        self,
        employee_repository: IEmployeeRepository,
        position_repository: IPositionRepository
    ):
        self._employee_repository = employee_repository
        self._position_repository = position_repository

    async def get_employee_by_id(self, employee_id: uuid.UUID) -> Optional[Employee]:
        """Get employee by ID"""
        return await self._employee_repository.get_by_id(employee_id)

    async def get_all_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all employees with pagination"""
        return await self._employee_repository.get_all(skip, limit)

    async def create_employee(
        self,
        first_name: str,
        last_name: str,
        position_id: uuid.UUID
    ) -> Employee:
        """Create a new employee"""
        # Validate input
        first_name_vo = PersonName(first_name)
        last_name_vo = PersonName(last_name)
        position_id_vo = EntityId(position_id)

        # Verify position exists
        position = await self._position_repository.get_by_id(position_id)
        if not position:
            raise ValueError(f"Position with ID {position_id} not found")

        # Create employee entity
        employee = Employee(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            first_name=str(first_name_vo),
            last_name=str(last_name_vo),
            position_id=position_id_vo.value,
            position=position
        )

        return await self._employee_repository.create(employee)

    async def update_employee(
        self,
        employee_id: uuid.UUID,
        first_name: str,
        last_name: str,
        position_id: uuid.UUID
    ) -> Employee:
        """Update an existing employee"""
        # Validate input
        first_name_vo = PersonName(first_name)
        last_name_vo = PersonName(last_name)
        position_id_vo = EntityId(position_id)

        # Get existing employee
        employee = await self._employee_repository.get_by_id(employee_id)
        if not employee:
            raise ValueError(f"Employee with ID {employee_id} not found")

        # Verify position exists
        position = await self._position_repository.get_by_id(position_id)
        if not position:
            raise ValueError(f"Position with ID {position_id} not found")

        # Update employee
        employee.update_personal_info(str(first_name_vo), str(last_name_vo))
        employee.change_position(position_id_vo.value)
        employee.position = position

        return await self._employee_repository.update(employee)

    async def delete_employee(self, employee_id: uuid.UUID) -> bool:
        """Delete an employee"""
        employee = await self._employee_repository.get_by_id(employee_id)
        if not employee:
            raise ValueError(f"Employee with ID {employee_id} not found")

        return await self._employee_repository.delete(employee_id)

    async def get_employees_by_position(self, position_id: uuid.UUID) -> List[Employee]:
        """Get all employees in a specific position"""
        return await self._employee_repository.get_by_position_id(position_id)