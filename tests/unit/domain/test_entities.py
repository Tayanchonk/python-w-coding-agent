"""
Unit tests for domain entities
"""
import pytest
import uuid
from datetime import datetime

from app.domain.entities.employee import User, Employee, Position


class TestUser:
    """Test User entity"""

    def test_user_creation(self):
        """Test user creation with valid data"""
        user_id = uuid.uuid4()
        now = datetime.utcnow()
        
        user = User(
            id=user_id,
            created_at=now,
            updated_at=now,
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            is_active=True
        )
        
        assert user.id == user_id
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password_hash == "hashed_password"
        assert user.is_active is True

    def test_user_creation_with_defaults(self):
        """Test user creation with auto-generated values"""
        user = User(
            id=None,
            created_at=None,
            updated_at=None,
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password"
        )
        
        assert isinstance(user.id, uuid.UUID)
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
        assert user.is_active is True

    def test_user_deactivate(self):
        """Test user deactivation"""
        user = User(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            is_active=True
        )
        
        original_updated_at = user.updated_at
        user.deactivate()
        
        assert user.is_active is False
        assert user.updated_at > original_updated_at

    def test_user_activate(self):
        """Test user activation"""
        user = User(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            is_active=False
        )
        
        original_updated_at = user.updated_at
        user.activate()
        
        assert user.is_active is True
        assert user.updated_at > original_updated_at


class TestPosition:
    """Test Position entity"""

    def test_position_creation(self):
        """Test position creation with valid data"""
        position_id = uuid.uuid4()
        now = datetime.utcnow()
        
        position = Position(
            id=position_id,
            created_at=now,
            updated_at=now,
            name="Software Engineer",
            description="Develops software applications"
        )
        
        assert position.id == position_id
        assert position.name == "Software Engineer"
        assert position.description == "Develops software applications"

    def test_position_update_details(self):
        """Test position details update"""
        position = Position(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name="Developer",
            description="Original description"
        )
        
        original_updated_at = position.updated_at
        position.update_details("Senior Developer", "Updated description")
        
        assert position.name == "Senior Developer"
        assert position.description == "Updated description"
        assert position.updated_at > original_updated_at


class TestEmployee:
    """Test Employee entity"""

    def test_employee_creation(self):
        """Test employee creation with valid data"""
        employee_id = uuid.uuid4()
        position_id = uuid.uuid4()
        now = datetime.utcnow()
        
        employee = Employee(
            id=employee_id,
            created_at=now,
            updated_at=now,
            first_name="John",
            last_name="Doe",
            position_id=position_id
        )
        
        assert employee.id == employee_id
        assert employee.first_name == "John"
        assert employee.last_name == "Doe"
        assert employee.position_id == position_id

    def test_employee_full_name(self):
        """Test employee full name property"""
        employee = Employee(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            first_name="John",
            last_name="Doe",
            position_id=uuid.uuid4()
        )
        
        assert employee.full_name == "John Doe"

    def test_employee_update_personal_info(self):
        """Test employee personal info update"""
        employee = Employee(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            first_name="John",
            last_name="Doe",
            position_id=uuid.uuid4()
        )
        
        original_updated_at = employee.updated_at
        employee.update_personal_info("Jane", "Smith")
        
        assert employee.first_name == "Jane"
        assert employee.last_name == "Smith"
        assert employee.full_name == "Jane Smith"
        assert employee.updated_at > original_updated_at

    def test_employee_change_position(self):
        """Test employee position change"""
        original_position_id = uuid.uuid4()
        new_position_id = uuid.uuid4()
        
        employee = Employee(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            first_name="John",
            last_name="Doe",
            position_id=original_position_id
        )
        
        original_updated_at = employee.updated_at
        employee.change_position(new_position_id)
        
        assert employee.position_id == new_position_id
        assert employee.updated_at > original_updated_at

    def test_employee_with_position(self):
        """Test employee with position relationship"""
        position = Position(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name="Software Engineer",
            description="Develops software"
        )
        
        employee = Employee(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            first_name="John",
            last_name="Doe",
            position_id=position.id,
            position=position
        )
        
        assert employee.position == position
        assert employee.position.name == "Software Engineer"