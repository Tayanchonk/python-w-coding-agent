"""
User repository implementation
"""
from typing import Optional
import uuid
from sqlalchemy.orm import Session

from app.domain.entities.employee import User
from app.domain.interfaces.repositories import IUserRepository
from app.infrastructure.database.models import UserModel


class UserRepository(IUserRepository):
    """SQLAlchemy implementation of user repository"""

    def __init__(self, db_session: Session):
        self._db = db_session

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID"""
        db_user = (
            self._db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )
        if not db_user:
            return None
        return self._to_domain_entity(db_user)

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        db_user = (
            self._db.query(UserModel)
            .filter(UserModel.username == username)
            .first()
        )
        if not db_user:
            return None
        return self._to_domain_entity(db_user)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        db_user = (
            self._db.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )
        if not db_user:
            return None
        return self._to_domain_entity(db_user)

    async def create(self, user: User) -> User:
        """Create a new user"""
        db_user = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)
        return self._to_domain_entity(db_user)

    async def update(self, user: User) -> User:
        """Update an existing user"""
        db_user = (
            self._db.query(UserModel)
            .filter(UserModel.id == user.id)
            .first()
        )
        if not db_user:
            raise ValueError(f"User with ID {user.id} not found")

        db_user.username = user.username
        db_user.email = user.email
        db_user.password_hash = user.password_hash
        db_user.is_active = user.is_active
        db_user.updated_at = user.updated_at

        self._db.commit()
        self._db.refresh(db_user)
        return self._to_domain_entity(db_user)

    async def delete(self, user_id: uuid.UUID) -> bool:
        """Delete a user"""
        db_user = (
            self._db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )
        if not db_user:
            return False

        self._db.delete(db_user)
        self._db.commit()
        return True

    def _to_domain_entity(self, db_user: UserModel) -> User:
        """Convert database model to domain entity"""
        return User(
            id=db_user.id,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password_hash,
            is_active=db_user.is_active
        )