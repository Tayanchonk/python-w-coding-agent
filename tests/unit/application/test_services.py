"""
Unit tests for application services
"""
import pytest
from unittest.mock import Mock, MagicMock
from datetime import timedelta

from app.application.services import AuthenticationService
from app.domain.entities import User
from app.domain.interfaces import UserRepositoryInterface


class TestAuthenticationService:
    """Test cases for AuthenticationService"""

    def setup_method(self):
        """Set up test dependencies"""
        self.mock_user_repository = Mock(spec=UserRepositoryInterface)
        self.auth_service = AuthenticationService(
            user_repository=self.mock_user_repository,
            secret_key="test-secret-key",
            algorithm="HS256",
            access_token_expire_minutes=30,
            refresh_token_expire_days=7
        )

    def test_verify_password_valid(self):
        """Test password verification with valid password"""
        # This is a known bcrypt hash for "testpassword"
        hashed = self.auth_service.get_password_hash("testpassword")
        result = self.auth_service.verify_password("testpassword", hashed)
        assert result is True

    def test_verify_password_invalid(self):
        """Test password verification with invalid password"""
        hashed = self.auth_service.get_password_hash("testpassword")
        result = self.auth_service.verify_password("wrongpassword", hashed)
        assert result is False

    def test_get_password_hash(self):
        """Test password hashing"""
        password = "testpassword"
        hashed = self.auth_service.get_password_hash(password)
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")

    def test_create_access_token(self):
        """Test access token creation"""
        data = {"sub": "testuser"}
        token = self.auth_service.create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_expiry(self):
        """Test access token creation with custom expiry"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=60)
        token = self.auth_service.create_access_token(data, expires_delta)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token(self):
        """Test refresh token creation"""
        data = {"sub": "testuser"}
        token = self.auth_service.create_refresh_token(data)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token_valid_access(self):
        """Test token verification with valid access token"""
        data = {"sub": "testuser"}
        token = self.auth_service.create_access_token(data)
        username = self.auth_service.verify_token(token, "access")
        assert username == "testuser"

    def test_verify_token_valid_refresh(self):
        """Test token verification with valid refresh token"""
        data = {"sub": "testuser"}
        token = self.auth_service.create_refresh_token(data)
        username = self.auth_service.verify_token(token, "refresh")
        assert username == "testuser"

    def test_verify_token_invalid_type(self):
        """Test token verification with wrong token type"""
        data = {"sub": "testuser"}
        token = self.auth_service.create_access_token(data)
        username = self.auth_service.verify_token(token, "refresh")
        assert username is None

    def test_verify_token_invalid_token(self):
        """Test token verification with invalid token"""
        username = self.auth_service.verify_token("invalid.token.here", "access")
        assert username is None

    def test_authenticate_user_valid(self):
        """Test user authentication with valid credentials"""
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password=self.auth_service.get_password_hash("testpassword"),
            is_active=True
        )
        self.mock_user_repository.get_by_username.return_value = user

        result = self.auth_service.authenticate_user("testuser", "testpassword")
        assert result == user
        self.mock_user_repository.get_by_username.assert_called_once_with("testuser")

    def test_authenticate_user_invalid_username(self):
        """Test user authentication with invalid username"""
        self.mock_user_repository.get_by_username.return_value = None

        result = self.auth_service.authenticate_user("invaliduser", "testpassword")
        assert result is None
        self.mock_user_repository.get_by_username.assert_called_once_with("invaliduser")

    def test_authenticate_user_invalid_password(self):
        """Test user authentication with invalid password"""
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password=self.auth_service.get_password_hash("testpassword"),
            is_active=True
        )
        self.mock_user_repository.get_by_username.return_value = user

        result = self.auth_service.authenticate_user("testuser", "wrongpassword")
        assert result is None

    def test_register_user_valid(self):
        """Test user registration with valid data"""
        self.mock_user_repository.get_by_username.return_value = None
        self.mock_user_repository.get_by_email.return_value = None
        
        created_user = User(
            user_id=1,
            username="newuser",
            email="new@example.com",
            password="hashedpassword",
            is_active=True
        )
        self.mock_user_repository.create.return_value = created_user

        result = self.auth_service.register_user("newuser", "new@example.com", "password123")
        
        assert result == created_user
        self.mock_user_repository.get_by_username.assert_called_once_with("newuser")
        self.mock_user_repository.get_by_email.assert_called_once_with("new@example.com")
        self.mock_user_repository.create.assert_called_once()

    def test_register_user_username_exists(self):
        """Test user registration with existing username"""
        existing_user = User(
            user_id=1,
            username="existinguser",
            email="existing@example.com",
            password="hashedpassword",
            is_active=True
        )
        self.mock_user_repository.get_by_username.return_value = existing_user

        with pytest.raises(ValueError, match="Username already registered"):
            self.auth_service.register_user("existinguser", "new@example.com", "password123")

    def test_register_user_email_exists(self):
        """Test user registration with existing email"""
        self.mock_user_repository.get_by_username.return_value = None
        existing_user = User(
            user_id=1,
            username="existinguser",
            email="existing@example.com",
            password="hashedpassword",
            is_active=True
        )
        self.mock_user_repository.get_by_email.return_value = existing_user

        with pytest.raises(ValueError, match="Email already registered"):
            self.auth_service.register_user("newuser", "existing@example.com", "password123")

    def test_get_user_by_username(self):
        """Test getting user by username"""
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password="hashedpassword",
            is_active=True
        )
        self.mock_user_repository.get_by_username.return_value = user

        result = self.auth_service.get_user_by_username("testuser")
        assert result == user
        self.mock_user_repository.get_by_username.assert_called_once_with("testuser")