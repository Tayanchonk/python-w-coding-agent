"""
User/Authentication use cases
"""
from typing import Optional
import uuid
from datetime import datetime

from app.domain.entities.employee import User
from app.domain.interfaces.repositories import IUserRepository
from app.domain.value_objects.common import Username, Email, EntityId


class UserUseCases:
    """User business logic use cases"""

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID"""
        return await self._user_repository.get_by_id(user_id)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return await self._user_repository.get_by_username(username)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return await self._user_repository.get_by_email(email)

    async def create_user(
        self,
        username: str,
        email: str,
        password_hash: str
    ) -> User:
        """Create a new user"""
        # Validate input
        username_vo = Username(username)
        email_vo = Email(email)

        # Check if user already exists
        existing_user_by_username = await self._user_repository.get_by_username(str(username_vo))
        if existing_user_by_username:
            raise ValueError(f"Username '{username}' already exists")

        existing_user_by_email = await self._user_repository.get_by_email(str(email_vo))
        if existing_user_by_email:
            raise ValueError(f"Email '{email}' already exists")

        # Create user entity
        user = User(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            username=str(username_vo),
            email=str(email_vo),
            password_hash=password_hash,
            is_active=True
        )

        return await self._user_repository.create(user)

    async def authenticate_user(self, username: str, password_hash: str) -> Optional[User]:
        """Authenticate user with username and password hash"""
        user = await self._user_repository.get_by_username(username)
        if not user or not user.is_active:
            return None

        # In a real implementation, you would verify the password hash here
        # For now, we assume the password_hash is already verified
        return user

    async def deactivate_user(self, user_id: uuid.UUID) -> User:
        """Deactivate a user"""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        user.deactivate()
        return await self._user_repository.update(user)

    async def activate_user(self, user_id: uuid.UUID) -> User:
        """Activate a user"""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        user.activate()
        return await self._user_repository.update(user)