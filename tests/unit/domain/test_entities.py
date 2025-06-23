"""
Unit tests for domain entities
"""
import pytest
from app.domain.entities import User, Employee, Position


class TestUser:
    """Test cases for User entity"""

    def test_user_creation_valid(self):
        """Test creating a valid user"""
        user = User(
            user_id=1,
            username="testuser",
            email="test@example.com",
            password="hashedpassword",
            is_active=True
        )
        assert user.user_id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "hashedpassword"
        assert user.is_active is True

    def test_user_creation_default_active(self):
        """Test user creation with default is_active"""
        user = User(
            user_id=None,
            username="testuser",
            email="test@example.com"
        )
        assert user.is_active is True

    def test_user_creation_invalid_empty_username(self):
        """Test user creation with empty username"""
        with pytest.raises(ValueError, match="Username and email are required"):
            User(
                user_id=None,
                username="",
                email="test@example.com"
            )

    def test_user_creation_invalid_empty_email(self):
        """Test user creation with empty email"""
        with pytest.raises(ValueError, match="Username and email are required"):
            User(
                user_id=None,
                username="testuser",
                email=""
            )


class TestEmployee:
    """Test cases for Employee entity"""

    def test_employee_creation_valid(self):
        """Test creating a valid employee"""
        employee = Employee(
            emp_id=1,
            first_name="John",
            last_name="Doe",
            position_id=1
        )
        assert employee.emp_id == 1
        assert employee.first_name == "John"
        assert employee.last_name == "Doe"
        assert employee.position_id == 1
        assert employee.position is None

    def test_employee_creation_with_position(self):
        """Test creating employee with position"""
        position = Position(
            position_id=1,
            position_name="Developer",
            description="Software Developer"
        )
        employee = Employee(
            emp_id=1,
            first_name="John",
            last_name="Doe",
            position_id=1,
            position=position
        )
        assert employee.position == position

    def test_employee_full_name_property(self):
        """Test employee full_name property"""
        employee = Employee(
            emp_id=1,
            first_name="John",
            last_name="Doe",
            position_id=1
        )
        assert employee.full_name == "John Doe"

    def test_employee_creation_invalid_empty_first_name(self):
        """Test employee creation with empty first name"""
        with pytest.raises(ValueError, match="First name and last name are required"):
            Employee(
                emp_id=None,
                first_name="",
                last_name="Doe",
                position_id=1
            )

    def test_employee_creation_invalid_empty_last_name(self):
        """Test employee creation with empty last name"""
        with pytest.raises(ValueError, match="First name and last name are required"):
            Employee(
                emp_id=None,
                first_name="John",
                last_name="",
                position_id=1
            )

    def test_employee_creation_invalid_empty_position_id(self):
        """Test employee creation with empty position_id"""
        with pytest.raises(ValueError, match="Position ID is required"):
            Employee(
                emp_id=None,
                first_name="John",
                last_name="Doe",
                position_id=0
            )


class TestPosition:
    """Test cases for Position entity"""

    def test_position_creation_valid(self):
        """Test creating a valid position"""
        position = Position(
            position_id=1,
            position_name="Developer",
            description="Software Developer"
        )
        assert position.position_id == 1
        assert position.position_name == "Developer"
        assert position.description == "Software Developer"

    def test_position_creation_without_description(self):
        """Test creating position without description"""
        position = Position(
            position_id=1,
            position_name="Developer"
        )
        assert position.position_id == 1
        assert position.position_name == "Developer"
        assert position.description is None

    def test_position_creation_invalid_empty_name(self):
        """Test position creation with empty name"""
        with pytest.raises(ValueError, match="Position name is required"):
            Position(
                position_id=None,
                position_name=""
            )