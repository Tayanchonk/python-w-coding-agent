"""
Employee repository implementation
"""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session, joinedload

from app.domain.entities.employee import Employee, Position
from app.domain.interfaces.repositories import IEmployeeRepository
from app.infrastructure.database.models import EmployeeModel, PositionModel


class EmployeeRepository(IEmployeeRepository):
    """SQLAlchemy implementation of employee repository"""

    def __init__(self, db_session: Session):
        self._db = db_session

    async def get_by_id(self, employee_id: uuid.UUID) -> Optional[Employee]:
        """Get employee by ID"""
        db_employee = (
            self._db.query(EmployeeModel)
            .options(joinedload(EmployeeModel.position))
            .filter(EmployeeModel.id == employee_id)
            .first()
        )
        if not db_employee:
            return None
        return self._to_domain_entity(db_employee)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all employees with pagination"""
        db_employees = (
            self._db.query(EmployeeModel)
            .options(joinedload(EmployeeModel.position))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain_entity(emp) for emp in db_employees]

    async def get_by_position_id(self, position_id: uuid.UUID) -> List[Employee]:
        """Get all employees in a specific position"""
        db_employees = (
            self._db.query(EmployeeModel)
            .options(joinedload(EmployeeModel.position))
            .filter(EmployeeModel.position_id == position_id)
            .all()
        )
        return [self._to_domain_entity(emp) for emp in db_employees]

    async def create(self, employee: Employee) -> Employee:
        """Create a new employee"""
        db_employee = EmployeeModel(
            id=employee.id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            position_id=employee.position_id,
            created_at=employee.created_at,
            updated_at=employee.updated_at
        )
        self._db.add(db_employee)
        self._db.commit()
        self._db.refresh(db_employee)
        
        # Load the position relationship
        db_employee = (
            self._db.query(EmployeeModel)
            .options(joinedload(EmployeeModel.position))
            .filter(EmployeeModel.id == db_employee.id)
            .first()
        )
        return self._to_domain_entity(db_employee)

    async def update(self, employee: Employee) -> Employee:
        """Update an existing employee"""
        db_employee = (
            self._db.query(EmployeeModel)
            .filter(EmployeeModel.id == employee.id)
            .first()
        )
        if not db_employee:
            raise ValueError(f"Employee with ID {employee.id} not found")

        db_employee.first_name = employee.first_name
        db_employee.last_name = employee.last_name
        db_employee.position_id = employee.position_id
        db_employee.updated_at = employee.updated_at

        self._db.commit()
        self._db.refresh(db_employee)
        
        # Load the position relationship
        db_employee = (
            self._db.query(EmployeeModel)
            .options(joinedload(EmployeeModel.position))
            .filter(EmployeeModel.id == db_employee.id)
            .first()
        )
        return self._to_domain_entity(db_employee)

    async def delete(self, employee_id: uuid.UUID) -> bool:
        """Delete an employee"""
        db_employee = (
            self._db.query(EmployeeModel)
            .filter(EmployeeModel.id == employee_id)
            .first()
        )
        if not db_employee:
            return False

        self._db.delete(db_employee)
        self._db.commit()
        return True

    def _to_domain_entity(self, db_employee: EmployeeModel) -> Employee:
        """Convert database model to domain entity"""
        position = None
        if db_employee.position:
            position = Position(
                id=db_employee.position.id,
                created_at=db_employee.position.created_at,
                updated_at=db_employee.position.updated_at,
                name=db_employee.position.name,
                description=db_employee.position.description
            )

        return Employee(
            id=db_employee.id,
            created_at=db_employee.created_at,
            updated_at=db_employee.updated_at,
            first_name=db_employee.first_name,
            last_name=db_employee.last_name,
            position_id=db_employee.position_id,
            position=position
        )