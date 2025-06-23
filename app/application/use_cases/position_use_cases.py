"""
Position use cases
"""
from typing import List, Optional
import uuid
from datetime import datetime

from app.domain.entities.employee import Position
from app.domain.interfaces.repositories import IPositionRepository, IEmployeeRepository
from app.domain.value_objects.common import PositionName, EntityId


class PositionUseCases:
    """Position business logic use cases"""

    def __init__(
        self,
        position_repository: IPositionRepository,
        employee_repository: IEmployeeRepository
    ):
        self._position_repository = position_repository
        self._employee_repository = employee_repository

    async def get_position_by_id(self, position_id: uuid.UUID) -> Optional[Position]:
        """Get position by ID"""
        return await self._position_repository.get_by_id(position_id)

    async def get_all_positions(self, skip: int = 0, limit: int = 100) -> List[Position]:
        """Get all positions with pagination"""
        return await self._position_repository.get_all(skip, limit)

    async def create_position(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Position:
        """Create a new position"""
        # Validate input
        name_vo = PositionName(name)

        # Check if position with same name already exists
        existing_position = await self._position_repository.get_by_name(str(name_vo))
        if existing_position:
            raise ValueError(f"Position with name '{name}' already exists")

        # Create position entity
        position = Position(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name=str(name_vo),
            description=description
        )

        return await self._position_repository.create(position)

    async def update_position(
        self,
        position_id: uuid.UUID,
        name: str,
        description: Optional[str] = None
    ) -> Position:
        """Update an existing position"""
        # Validate input
        name_vo = PositionName(name)

        # Get existing position
        position = await self._position_repository.get_by_id(position_id)
        if not position:
            raise ValueError(f"Position with ID {position_id} not found")

        # Check if another position with same name exists
        existing_position = await self._position_repository.get_by_name(str(name_vo))
        if existing_position and existing_position.id != position_id:
            raise ValueError(f"Position with name '{name}' already exists")

        # Update position
        position.update_details(str(name_vo), description)

        return await self._position_repository.update(position)

    async def delete_position(self, position_id: uuid.UUID) -> bool:
        """Delete a position"""
        position = await self._position_repository.get_by_id(position_id)
        if not position:
            raise ValueError(f"Position with ID {position_id} not found")

        # Check if any employees are assigned to this position
        has_employees = await self._position_repository.has_employees(position_id)
        if has_employees:
            raise ValueError(
                "Cannot delete position: employees are assigned to this position"
            )

        return await self._position_repository.delete(position_id)