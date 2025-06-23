"""
Unit tests for infrastructure schemas
"""
import pytest
import uuid
from datetime import datetime

from app.infrastructure.schemas import (
    UserCreate, UserResponse, 
    PositionCreate, PositionResponse,
    EmployeeCreate, EmployeeResponse,
    Token, LoginRequest
)


class TestSchemas:
    """Test infrastructure schemas"""

    def test_user_create_schema(self):
        """Test UserCreate schema validation"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        user = UserCreate(**user_data)
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "password123"

    def test_user_create_schema_invalid_email(self):
        """Test UserCreate schema with invalid email"""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "password123"
        }
        with pytest.raises(ValueError):
            UserCreate(**user_data)

    def test_user_create_schema_short_username(self):
        """Test UserCreate schema with short username"""
        user_data = {
            "username": "ab",  # Too short
            "email": "test@example.com",
            "password": "password123"
        }
        with pytest.raises(ValueError):
            UserCreate(**user_data)

    def test_user_create_schema_short_password(self):
        """Test UserCreate schema with short password"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"  # Too short
        }
        with pytest.raises(ValueError):
            UserCreate(**user_data)

    def test_user_response_schema(self):
        """Test UserResponse schema"""
        user_id = uuid.uuid4()
        now = datetime.utcnow()
        
        user_data = {
            "id": user_id,
            "created_at": now,
            "updated_at": now,
            "username": "testuser",
            "email": "test@example.com",
            "is_active": True
        }
        user = UserResponse(**user_data)
        
        assert user.id == user_id
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_active is True

    def test_position_create_schema(self):
        """Test PositionCreate schema validation"""
        position_data = {
            "name": "Software Engineer",
            "description": "Develops software"
        }
        position = PositionCreate(**position_data)
        
        assert position.name == "Software Engineer"
        assert position.description == "Develops software"

    def test_position_create_schema_empty_name(self):
        """Test PositionCreate schema with empty name"""
        position_data = {
            "name": "",  # Empty name
            "description": "Test description"
        }
        with pytest.raises(ValueError):
            PositionCreate(**position_data)

    def test_position_create_schema_long_name(self):
        """Test PositionCreate schema with too long name"""
        position_data = {
            "name": "a" * 101,  # Too long
            "description": "Test description"
        }
        with pytest.raises(ValueError):
            PositionCreate(**position_data)

    def test_position_response_schema(self):
        """Test PositionResponse schema"""
        position_id = uuid.uuid4()
        now = datetime.utcnow()
        
        position_data = {
            "id": position_id,
            "created_at": now,
            "updated_at": now,
            "name": "Software Engineer",
            "description": "Develops software"
        }
        position = PositionResponse(**position_data)
        
        assert position.id == position_id
        assert position.name == "Software Engineer"
        assert position.description == "Develops software"

    def test_employee_create_schema(self):
        """Test EmployeeCreate schema validation"""
        position_id = uuid.uuid4()
        employee_data = {
            "first_name": "John",
            "last_name": "Doe",
            "position_id": position_id
        }
        employee = EmployeeCreate(**employee_data)
        
        assert employee.first_name == "John"
        assert employee.last_name == "Doe"
        assert employee.position_id == position_id

    def test_employee_create_schema_empty_name(self):
        """Test EmployeeCreate schema with empty first name"""
        employee_data = {
            "first_name": "",  # Empty name
            "last_name": "Doe",
            "position_id": uuid.uuid4()
        }
        with pytest.raises(ValueError):
            EmployeeCreate(**employee_data)

    def test_employee_response_schema(self):
        """Test EmployeeResponse schema"""
        employee_id = uuid.uuid4()
        position_id = uuid.uuid4()
        now = datetime.utcnow()
        
        position_data = {
            "id": position_id,
            "created_at": now,
            "updated_at": now,
            "name": "Software Engineer",
            "description": "Develops software"
        }
        
        employee_data = {
            "id": employee_id,
            "created_at": now,
            "updated_at": now,
            "first_name": "John",
            "last_name": "Doe",
            "position_id": position_id,
            "position": position_data
        }
        employee = EmployeeResponse(**employee_data)
        
        assert employee.id == employee_id
        assert employee.first_name == "John"
        assert employee.last_name == "Doe"
        assert employee.position_id == position_id
        assert employee.position is not None
        assert employee.position.name == "Software Engineer"

    def test_employee_response_schema_without_position(self):
        """Test EmployeeResponse schema without position"""
        employee_id = uuid.uuid4()
        position_id = uuid.uuid4()
        now = datetime.utcnow()
        
        employee_data = {
            "id": employee_id,
            "created_at": now,
            "updated_at": now,
            "first_name": "John",
            "last_name": "Doe",
            "position_id": position_id,
            "position": None
        }
        employee = EmployeeResponse(**employee_data)
        
        assert employee.id == employee_id
        assert employee.position is None

    def test_token_schema(self):
        """Test Token schema"""
        token_data = {
            "access_token": "access_token_value",
            "refresh_token": "refresh_token_value",
            "token_type": "bearer"
        }
        token = Token(**token_data)
        
        assert token.access_token == "access_token_value"
        assert token.refresh_token == "refresh_token_value"
        assert token.token_type == "bearer"

    def test_login_request_schema(self):
        """Test LoginRequest schema"""
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login = LoginRequest(**login_data)
        
        assert login.username == "testuser"
        assert login.password == "password123"