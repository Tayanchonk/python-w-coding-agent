"""
Repository implementations for data access
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities import User, Employee, Position
from app.domain.interfaces import (
    UserRepositoryInterface,
    EmployeeRepositoryInterface,
    PositionRepositoryInterface
)
from app.infrastructure.database import UserModel, EmployeeModel, PositionModel


class SqlAlchemyUserRepository(UserRepositoryInterface):
    """SQLAlchemy implementation of User repository"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        """Create a new user"""
        db_user = UserModel(
            username=user.username,
            email=user.email,
            password=user.password,
            is_active=user.is_active
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_domain(db_user)

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        db_user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        return self._to_domain(db_user) if db_user else None

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        db_user = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_domain(db_user) if db_user else None

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(db_user) if db_user else None

    def update(self, user: User) -> User:
        """Update existing user"""
        db_user = self.db.query(UserModel).filter(UserModel.user_id == user.user_id).first()
        if not db_user:
            raise ValueError(f"User with ID {user.user_id} not found")
        
        db_user.username = user.username
        db_user.email = user.email
        if user.password:
            db_user.password = user.password
        db_user.is_active = user.is_active
        
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_domain(db_user)

    def delete(self, user_id: int) -> bool:
        """Delete user by ID"""
        db_user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True

    def _to_domain(self, db_user: UserModel) -> User:
        """Convert database model to domain entity"""
        return User(
            user_id=db_user.user_id,
            username=db_user.username,
            email=db_user.email,
            password=db_user.password,
            is_active=db_user.is_active
        )


class SqlAlchemyEmployeeRepository(EmployeeRepositoryInterface):
    """SQLAlchemy implementation of Employee repository"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, employee: Employee) -> Employee:
        """Create a new employee"""
        db_employee = EmployeeModel(
            first_name=employee.first_name,
            last_name=employee.last_name,
            position_id=employee.position_id
        )
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return self._to_domain(db_employee)

    def get_by_id(self, emp_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        db_employee = self.db.query(EmployeeModel).filter(EmployeeModel.emp_id == emp_id).first()
        return self._to_domain(db_employee) if db_employee else None

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """Get all employees with pagination"""
        db_employees = self.db.query(EmployeeModel).offset(skip).limit(limit).all()
        return [self._to_domain(emp) for emp in db_employees]

    def update(self, employee: Employee) -> Employee:
        """Update existing employee"""
        db_employee = self.db.query(EmployeeModel).filter(EmployeeModel.emp_id == employee.emp_id).first()
        if not db_employee:
            raise ValueError(f"Employee with ID {employee.emp_id} not found")
        
        db_employee.first_name = employee.first_name
        db_employee.last_name = employee.last_name
        db_employee.position_id = employee.position_id
        
        self.db.commit()
        self.db.refresh(db_employee)
        return self._to_domain(db_employee)

    def delete(self, emp_id: int) -> bool:
        """Delete employee by ID"""
        db_employee = self.db.query(EmployeeModel).filter(EmployeeModel.emp_id == emp_id).first()
        if not db_employee:
            return False
        
        self.db.delete(db_employee)
        self.db.commit()
        return True

    def _to_domain(self, db_employee: EmployeeModel) -> Employee:
        """Convert database model to domain entity"""
        position = None
        if db_employee.position:
            position = Position(
                position_id=db_employee.position.position_id,
                position_name=db_employee.position.position_name,
                description=db_employee.position.description
            )
        
        return Employee(
            emp_id=db_employee.emp_id,
            first_name=db_employee.first_name,
            last_name=db_employee.last_name,
            position_id=db_employee.position_id,
            position=position
        )


class SqlAlchemyPositionRepository(PositionRepositoryInterface):
    """SQLAlchemy implementation of Position repository"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, position: Position) -> Position:
        """Create a new position"""
        db_position = PositionModel(
            position_name=position.position_name,
            description=position.description
        )
        self.db.add(db_position)
        self.db.commit()
        self.db.refresh(db_position)
        return self._to_domain(db_position)

    def get_by_id(self, position_id: int) -> Optional[Position]:
        """Get position by ID"""
        db_position = self.db.query(PositionModel).filter(PositionModel.position_id == position_id).first()
        return self._to_domain(db_position) if db_position else None

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Position]:
        """Get all positions with pagination"""
        db_positions = self.db.query(PositionModel).offset(skip).limit(limit).all()
        return [self._to_domain(pos) for pos in db_positions]

    def update(self, position: Position) -> Position:
        """Update existing position"""
        db_position = self.db.query(PositionModel).filter(PositionModel.position_id == position.position_id).first()
        if not db_position:
            raise ValueError(f"Position with ID {position.position_id} not found")
        
        db_position.position_name = position.position_name
        db_position.description = position.description
        
        self.db.commit()
        self.db.refresh(db_position)
        return self._to_domain(db_position)

    def delete(self, position_id: int) -> bool:
        """Delete position by ID"""
        db_position = self.db.query(PositionModel).filter(PositionModel.position_id == position_id).first()
        if not db_position:
            return False
        
        self.db.delete(db_position)
        self.db.commit()
        return True

    def _to_domain(self, db_position: PositionModel) -> Position:
        """Convert database model to domain entity"""
        return Position(
            position_id=db_position.position_id,
            position_name=db_position.position_name,
            description=db_position.description
        )