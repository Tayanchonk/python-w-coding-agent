"""
Unit tests for database configuration
"""
import pytest
from unittest.mock import patch, MagicMock

from app.database import get_db


class TestDatabase:
    """Test database configuration and utilities"""

    @patch('app.database.SessionLocal')
    def test_get_db_success(self, mock_session_local):
        """Test successful database session creation and cleanup"""
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        # Convert generator to list to test it
        db_generator = get_db()
        db_sessions = list(db_generator)
        
        # Should yield one session
        assert len(db_sessions) == 1
        assert db_sessions[0] == mock_db
        
        # Session should be closed after use
        mock_db.close.assert_called_once()

    @patch('app.database.SessionLocal')
    def test_get_db_exception_handling(self, mock_session_local):
        """Test database session cleanup on exception"""
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        db_generator = get_db()
        
        # Simulate an exception during database operation
        try:
            next(db_generator)
            # Simulate exception
            db_generator.throw(Exception("Database error"))
        except Exception:
            pass
        
        # Session should still be closed despite exception
        mock_db.close.assert_called_once()