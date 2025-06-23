"""
Unit tests for user use cases
"""
import pytest
import uuid
from datetime import datetime
from unittest.mock import AsyncMock

from app.application.use_cases.user_use_cases import UserUseCases
from app.domain.entities.employee import User


class TestUserUseCases:
    """Test User use cases"""

    @pytest.fixture
    def mock_user_repo(self):
        """Mock user repository"""
        return AsyncMock()

    @pytest.fixture
    def user_use_cases(self, mock_user_repo):
        """User use cases instance"""
        return UserUseCases(mock_user_repo)

    @pytest.fixture
    def sample_user(self):
        """Sample user entity"""
        return User(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            is_active=True
        )

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(
        self, user_use_cases, mock_user_repo, sample_user
    ):
        """Test successful get user by ID"""
        mock_user_repo.get_by_id.return_value = sample_user
        
        result = await user_use_cases.get_user_by_id(sample_user.id)
        
        assert result == sample_user
        mock_user_repo.get_by_id.assert_called_once_with(sample_user.id)

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(
        self, user_use_cases, mock_user_repo
    ):
        """Test get user by ID when not found"""
        mock_user_repo.get_by_id.return_value = None
        
        result = await user_use_cases.get_user_by_id(uuid.uuid4())
        
        assert result is None

    @pytest.mark.asyncio
    async def test_get_user_by_username_success(
        self, user_use_cases, mock_user_repo, sample_user
    ):
        """Test successful get user by username"""
        mock_user_repo.get_by_username.return_value = sample_user
        
        result = await user_use_cases.get_user_by_username("testuser")
        
        assert result == sample_user
        mock_user_repo.get_by_username.assert_called_once_with("testuser")

    @pytest.mark.asyncio
    async def test_get_user_by_email_success(
        self, user_use_cases, mock_user_repo, sample_user
    ):
        """Test successful get user by email"""
        mock_user_repo.get_by_email.return_value = sample_user
        
        result = await user_use_cases.get_user_by_email("test@example.com")
        
        assert result == sample_user
        mock_user_repo.get_by_email.assert_called_once_with("test@example.com")

    @pytest.mark.asyncio
    async def test_create_user_success(
        self, user_use_cases, mock_user_repo
    ):
        """Test successful user creation"""
        mock_user_repo.get_by_username.return_value = None  # No existing user
        mock_user_repo.get_by_email.return_value = None  # No existing email
        created_user = User(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            username="newuser",
            email="new@example.com",
            password_hash="hashed_password",
            is_active=True
        )
        mock_user_repo.create.return_value = created_user
        
        result = await user_use_cases.create_user(
            username="newuser",
            email="new@example.com",
            password_hash="hashed_password"
        )
        
        assert result == created_user
        mock_user_repo.get_by_username.assert_called_once_with("newuser")
        mock_user_repo.get_by_email.assert_called_once_with("new@example.com")
        mock_user_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_invalid_username(
        self, user_use_cases, mock_user_repo
    ):
        """Test user creation with invalid username"""
        with pytest.raises(ValueError, match="Invalid username"):
            await user_use_cases.create_user(
                username="ab",  # Too short
                email="test@example.com",
                password_hash="hashed_password"
            )

    @pytest.mark.asyncio
    async def test_create_user_invalid_email(
        self, user_use_cases, mock_user_repo
    ):
        """Test user creation with invalid email"""
        with pytest.raises(ValueError, match="Invalid email format"):
            await user_use_cases.create_user(
                username="testuser",
                email="invalid-email",
                password_hash="hashed_password"
            )

    @pytest.mark.asyncio
    async def test_create_user_username_exists(
        self, user_use_cases, mock_user_repo, sample_user
    ):
        """Test user creation when username already exists"""
        mock_user_repo.get_by_username.return_value = sample_user
        
        with pytest.raises(ValueError, match="Username 'testuser' already exists"):
            await user_use_cases.create_user(
                username="testuser",
                email="new@example.com",
                password_hash="hashed_password"
            )

    @pytest.mark.asyncio
    async def test_create_user_email_exists(
        self, user_use_cases, mock_user_repo, sample_user
    ):
        """Test user creation when email already exists"""
        mock_user_repo.get_by_username.return_value = None  # Username is available
        mock_user_repo.get_by_email.return_value = sample_user  # Email exists
        
        with pytest.raises(ValueError, match="Email 'test@example.com' already exists"):
            await user_use_cases.create_user(
                username="newuser",
                email="test@example.com",
                password_hash="hashed_password"
            )

    @pytest.mark.asyncio
    async def test_authenticate_user_success(
        self, user_use_cases, mock_user_repo, sample_user
    ):
        """Test successful user authentication"""
        mock_user_repo.get_by_username.return_value = sample_user
        
        result = await user_use_cases.authenticate_user("testuser", "hashed_password")
        
        assert result == sample_user
        mock_user_repo.get_by_username.assert_called_once_with("testuser")

    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(
        self, user_use_cases, mock_user_repo
    ):
        """Test user authentication when user not found"""
        mock_user_repo.get_by_username.return_value = None
        
        result = await user_use_cases.authenticate_user("nonexistent", "password")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_authenticate_user_inactive(
        self, user_use_cases, mock_user_repo, sample_user
    ):
        """Test user authentication when user is inactive"""
        sample_user.is_active = False
        mock_user_repo.get_by_username.return_value = sample_user
        
        result = await user_use_cases.authenticate_user("testuser", "password")
        
        assert result is None

    @pytest.mark.asyncio
    async def test_deactivate_user_success(
        self, user_use_cases, mock_user_repo, sample_user
    ):
        """Test successful user deactivation"""
        mock_user_repo.get_by_id.return_value = sample_user
        deactivated_user = User(
            id=sample_user.id,
            created_at=sample_user.created_at,
            updated_at=datetime.utcnow(),
            username=sample_user.username,
            email=sample_user.email,
            password_hash=sample_user.password_hash,
            is_active=False
        )
        mock_user_repo.update.return_value = deactivated_user
        
        result = await user_use_cases.deactivate_user(sample_user.id)
        
        assert result == deactivated_user
        mock_user_repo.get_by_id.assert_called_once_with(sample_user.id)
        mock_user_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_deactivate_user_not_found(
        self, user_use_cases, mock_user_repo
    ):
        """Test user deactivation when user not found"""
        user_id = uuid.uuid4()
        mock_user_repo.get_by_id.return_value = None
        
        with pytest.raises(ValueError, match=f"User with ID {user_id} not found"):
            await user_use_cases.deactivate_user(user_id)

    @pytest.mark.asyncio
    async def test_activate_user_success(
        self, user_use_cases, mock_user_repo, sample_user
    ):
        """Test successful user activation"""
        sample_user.is_active = False  # Start as inactive
        mock_user_repo.get_by_id.return_value = sample_user
        activated_user = User(
            id=sample_user.id,
            created_at=sample_user.created_at,
            updated_at=datetime.utcnow(),
            username=sample_user.username,
            email=sample_user.email,
            password_hash=sample_user.password_hash,
            is_active=True
        )
        mock_user_repo.update.return_value = activated_user
        
        result = await user_use_cases.activate_user(sample_user.id)
        
        assert result == activated_user
        mock_user_repo.get_by_id.assert_called_once_with(sample_user.id)
        mock_user_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_activate_user_not_found(
        self, user_use_cases, mock_user_repo
    ):
        """Test user activation when user not found"""
        user_id = uuid.uuid4()
        mock_user_repo.get_by_id.return_value = None
        
        with pytest.raises(ValueError, match=f"User with ID {user_id} not found"):
            await user_use_cases.activate_user(user_id)