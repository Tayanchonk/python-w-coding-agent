"""
Position repository implementation
"""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.domain.entities.employee import Position
from app.domain.interfaces.repositories import IPositionRepository
from app.infrastructure.database.models import PositionModel, EmployeeModel


class PositionRepository(IPositionRepository):
    """SQLAlchemy implementation of position repository"""

    def __init__(self, db_session: Session):
        self._db = db_session

    async def get_by_id(self, position_id: uuid.UUID) -> Optional[Position]:
        """Get position by ID"""
        db_position = (
            self._db.query(PositionModel)
            .filter(PositionModel.id == position_id)
            .first()
        )
        if not db_position:
            return None
        return self._to_domain_entity(db_position)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Position]:
        """Get all positions with pagination"""
        db_positions = (
            self._db.query(PositionModel)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(pos) for pos in db_positions]

    async def get_by_name(self, name: str) -> Optional[Position]:
        """Get position by name"""
        db_position = (
            self._db.query(PositionModel)
            .filter(PositionModel.name == name)
            .first()
        )
        if not db_position:
            return None
        return self._to_domain_entity(db_position)

    async def create(self, position: Position) -> Position:
        """Create a new position"""
        db_position = PositionModel(
            id=position.id,
            name=position.name,
            description=position.description,
            created_at=position.created_at,
            updated_at=position.updated_at
        )
        self._db.add(db_position)
        self._db.commit()
        self._db.refresh(db_position)
        return self._to_domain_entity(db_position)

    async def update(self, position: Position) -> Position:
        """Update an existing position"""
        db_position = (
            self._db.query(PositionModel)
            .filter(PositionModel.id == position.id)
            .first()
        )
        if not db_position:
            raise ValueError(f"Position with ID {position.id} not found")

        db_position.name = position.name
        db_position.description = position.description
        db_position.updated_at = position.updated_at

        self._db.commit()
        self._db.refresh(db_position)
        return self._to_domain_entity(db_position)

    async def delete(self, position_id: uuid.UUID) -> bool:
        """Delete a position"""
        db_position = (
            self._db.query(PositionModel)
            .filter(PositionModel.id == position_id)
            .first()
        )
        if not db_position:
            return False

        self._db.delete(db_position)
        self._db.commit()
        return True

    async def has_employees(self, position_id: uuid.UUID) -> bool:
        """Check if position has any employees assigned"""
        employee_count = (
            self._db.query(EmployeeModel)
            .filter(EmployeeModel.position_id == position_id)
            .count()
        )
        return employee_count > 0

    def _to_domain_entity(self, db_position: PositionModel) -> Position:
        """Convert database model to domain entity"""
        return Position(
            id=db_position.id,
            created_at=db_position.created_at,
            updated_at=db_position.updated_at,
            name=db_position.name,
            description=db_position.description
        )