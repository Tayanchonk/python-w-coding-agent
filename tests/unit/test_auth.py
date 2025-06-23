"""
Unit tests for auth module
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from app.auth import (
    verify_password, get_password_hash, create_access_token, 
    create_refresh_token, get_user_by_username, get_user_by_email,
    create_user, authenticate_user
)
from app.models import User


class TestAuthHelpers:
    """Test authentication helper functions"""

    def test_password_hashing_and_verification(self):
        """Test password hashing and verification"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False

    def test_create_access_token(self):
        """Test access token creation"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_expiry(self):
        """Test access token creation with custom expiry"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)
        
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token(self):
        """Test refresh token creation"""
        data = {"sub": "testuser"}
        token = create_refresh_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token_with_expiry(self):
        """Test refresh token creation with custom expiry"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(days=1)
        token = create_refresh_token(data, expires_delta)
        
        assert isinstance(token, str)
        assert len(token) > 0


class TestDatabaseHelpers:
    """Test database helper functions"""

    @patch('app.auth.User')
    def test_get_user_by_username(self, mock_user):
        """Test getting user by username"""
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_user_instance = MagicMock()
        mock_filter.first.return_value = mock_user_instance
        
        result = get_user_by_username(mock_db, "testuser")
        
        mock_db.query.assert_called_once_with(mock_user)
        assert result == mock_user_instance

    @patch('app.auth.User')
    def test_get_user_by_email(self, mock_user):
        """Test getting user by email"""
        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_user_instance = MagicMock()
        mock_filter.first.return_value = mock_user_instance
        
        result = get_user_by_email(mock_db, "test@example.com")
        
        mock_db.query.assert_called_once_with(mock_user)
        assert result == mock_user_instance

    @patch('app.auth.get_password_hash')
    @patch('app.auth.User')
    def test_create_user(self, mock_user_class, mock_get_password_hash):
        """Test user creation"""
        mock_db = MagicMock()
        mock_get_password_hash.return_value = "hashed_password"
        mock_user_instance = MagicMock()
        mock_user_class.return_value = mock_user_instance
        
        from app.schemas import UserCreate
        user_data = UserCreate(
            username="testuser",
            email="test@example.com", 
            password="password123"
        )
        
        result = create_user(mock_db, user_data)
        
        mock_get_password_hash.assert_called_once_with("password123")
        mock_user_class.assert_called_once_with(
            username="testuser",
            email="test@example.com",
            password="hashed_password"  # The legacy field name used in the actual implementation
        )
        mock_db.add.assert_called_once_with(mock_user_instance)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(mock_user_instance)
        assert result == mock_user_instance

    @patch('app.auth.verify_password')
    @patch('app.auth.get_user_by_username')
    def test_authenticate_user_success(self, mock_get_user, mock_verify):
        """Test successful user authentication"""
        mock_db = MagicMock()
        mock_user = MagicMock()
        mock_user.password = "hashed_password"  # Legacy field name
        mock_get_user.return_value = mock_user
        mock_verify.return_value = True
        
        result = authenticate_user(mock_db, "testuser", "password123")
        
        mock_get_user.assert_called_once_with(mock_db, "testuser")
        mock_verify.assert_called_once_with("password123", "hashed_password")
        assert result == mock_user

    @patch('app.auth.get_user_by_username')
    def test_authenticate_user_not_found(self, mock_get_user):
        """Test user authentication when user not found"""
        mock_db = MagicMock()
        mock_get_user.return_value = None
        
        result = authenticate_user(mock_db, "nonexistent", "password123")
        
        mock_get_user.assert_called_once_with(mock_db, "nonexistent")
        assert result is False

    @patch('app.auth.verify_password')
    @patch('app.auth.get_user_by_username')
    def test_authenticate_user_wrong_password(self, mock_get_user, mock_verify):
        """Test user authentication with wrong password"""
        mock_db = MagicMock()
        mock_user = MagicMock()
        mock_user.password = "hashed_password"  # Legacy field name
        mock_get_user.return_value = mock_user
        mock_verify.return_value = False
        
        result = authenticate_user(mock_db, "testuser", "wrongpassword")
        
        mock_get_user.assert_called_once_with(mock_db, "testuser")
        mock_verify.assert_called_once_with("wrongpassword", "hashed_password")
        assert result is False