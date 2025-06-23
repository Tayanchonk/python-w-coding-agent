"""
Unit tests for application use cases
"""
import pytest
from unittest.mock import Mock

from app.application.use_cases import EmployeeUseCase, PositionUseCase
from app.domain.entities import Employee, Position
from app.domain.interfaces import EmployeeRepositoryInterface, PositionRepositoryInterface


class TestEmployeeUseCase:
    """Test cases for EmployeeUseCase"""

    def setup_method(self):
        """Set up test dependencies"""
        self.mock_employee_repository = Mock(spec=EmployeeRepositoryInterface)
        self.mock_position_repository = Mock(spec=PositionRepositoryInterface)
        self.employee_use_case = EmployeeUseCase(
            self.mock_employee_repository,
            self.mock_position_repository
        )

    def test_create_employee_valid(self):
        """Test creating employee with valid data"""
        position = Position(
            position_id=1,
            position_name="Developer",
            description="Software Developer"
        )
        self.mock_position_repository.get_by_id.return_value = position

        created_employee = Employee(
            emp_id=1,
            first_name="John",
            last_name="Doe",
            position_id=1
        )
        self.mock_employee_repository.create.return_value = created_employee

        result = self.employee_use_case.create_employee("John", "Doe", 1)

        assert result == created_employee
        self.mock_position_repository.get_by_id.assert_called_once_with(1)
        self.mock_employee_repository.create.assert_called_once()

    def test_create_employee_invalid_position(self):
        """Test creating employee with invalid position"""
        self.mock_position_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Position with ID 999 not found"):
            self.employee_use_case.create_employee("John", "Doe", 999)

    def test_get_employee_by_id(self):
        """Test getting employee by ID"""
        employee = Employee(
            emp_id=1,
            first_name="John",
            last_name="Doe",
            position_id=1
        )
        self.mock_employee_repository.get_by_id.return_value = employee

        result = self.employee_use_case.get_employee_by_id(1)

        assert result == employee
        self.mock_employee_repository.get_by_id.assert_called_once_with(1)

    def test_get_all_employees(self):
        """Test getting all employees"""
        employees = [
            Employee(emp_id=1, first_name="John", last_name="Doe", position_id=1),
            Employee(emp_id=2, first_name="Jane", last_name="Smith", position_id=2)
        ]
        self.mock_employee_repository.get_all.return_value = employees

        result = self.employee_use_case.get_all_employees(0, 100)

        assert result == employees
        self.mock_employee_repository.get_all.assert_called_once_with(0, 100)

    def test_update_employee_valid(self):
        """Test updating employee with valid data"""
        existing_employee = Employee(
            emp_id=1,
            first_name="John",
            last_name="Doe",
            position_id=1
        )
        self.mock_employee_repository.get_by_id.return_value = existing_employee

        position = Position(
            position_id=2,
            position_name="Manager",
            description="Team Manager"
        )
        self.mock_position_repository.get_by_id.return_value = position

        updated_employee = Employee(
            emp_id=1,
            first_name="John",
            last_name="Smith",
            position_id=2
        )
        self.mock_employee_repository.update.return_value = updated_employee

        result = self.employee_use_case.update_employee(1, "John", "Smith", 2)

        assert result == updated_employee
        self.mock_employee_repository.get_by_id.assert_called_once_with(1)
        self.mock_position_repository.get_by_id.assert_called_once_with(2)
        self.mock_employee_repository.update.assert_called_once()

    def test_update_employee_not_found(self):
        """Test updating non-existent employee"""
        self.mock_employee_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Employee with ID 999 not found"):
            self.employee_use_case.update_employee(999, "John", "Doe", 1)

    def test_update_employee_invalid_position(self):
        """Test updating employee with invalid position"""
        existing_employee = Employee(
            emp_id=1,
            first_name="John",
            last_name="Doe",
            position_id=1
        )
        self.mock_employee_repository.get_by_id.return_value = existing_employee
        self.mock_position_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Position with ID 999 not found"):
            self.employee_use_case.update_employee(1, "John", "Doe", 999)

    def test_delete_employee_valid(self):
        """Test deleting existing employee"""
        existing_employee = Employee(
            emp_id=1,
            first_name="John",
            last_name="Doe",
            position_id=1
        )
        self.mock_employee_repository.get_by_id.return_value = existing_employee
        self.mock_employee_repository.delete.return_value = True

        result = self.employee_use_case.delete_employee(1)

        assert result is True
        self.mock_employee_repository.get_by_id.assert_called_once_with(1)
        self.mock_employee_repository.delete.assert_called_once_with(1)

    def test_delete_employee_not_found(self):
        """Test deleting non-existent employee"""
        self.mock_employee_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Employee with ID 999 not found"):
            self.employee_use_case.delete_employee(999)


class TestPositionUseCase:
    """Test cases for PositionUseCase"""

    def setup_method(self):
        """Set up test dependencies"""
        self.mock_position_repository = Mock(spec=PositionRepositoryInterface)
        self.position_use_case = PositionUseCase(self.mock_position_repository)

    def test_create_position_valid(self):
        """Test creating position with valid data"""
        created_position = Position(
            position_id=1,
            position_name="Developer",
            description="Software Developer"
        )
        self.mock_position_repository.create.return_value = created_position

        result = self.position_use_case.create_position("Developer", "Software Developer")

        assert result == created_position
        self.mock_position_repository.create.assert_called_once()

    def test_create_position_without_description(self):
        """Test creating position without description"""
        created_position = Position(
            position_id=1,
            position_name="Developer",
            description=None
        )
        self.mock_position_repository.create.return_value = created_position

        result = self.position_use_case.create_position("Developer")

        assert result == created_position
        self.mock_position_repository.create.assert_called_once()

    def test_get_position_by_id(self):
        """Test getting position by ID"""
        position = Position(
            position_id=1,
            position_name="Developer",
            description="Software Developer"
        )
        self.mock_position_repository.get_by_id.return_value = position

        result = self.position_use_case.get_position_by_id(1)

        assert result == position
        self.mock_position_repository.get_by_id.assert_called_once_with(1)

    def test_get_all_positions(self):
        """Test getting all positions"""
        positions = [
            Position(position_id=1, position_name="Developer", description="Software Developer"),
            Position(position_id=2, position_name="Manager", description="Team Manager")
        ]
        self.mock_position_repository.get_all.return_value = positions

        result = self.position_use_case.get_all_positions(0, 100)

        assert result == positions
        self.mock_position_repository.get_all.assert_called_once_with(0, 100)

    def test_update_position_valid(self):
        """Test updating position with valid data"""
        existing_position = Position(
            position_id=1,
            position_name="Developer",
            description="Software Developer"
        )
        self.mock_position_repository.get_by_id.return_value = existing_position

        updated_position = Position(
            position_id=1,
            position_name="Senior Developer",
            description="Senior Software Developer"
        )
        self.mock_position_repository.update.return_value = updated_position

        result = self.position_use_case.update_position(1, "Senior Developer", "Senior Software Developer")

        assert result == updated_position
        self.mock_position_repository.get_by_id.assert_called_once_with(1)
        self.mock_position_repository.update.assert_called_once()

    def test_update_position_not_found(self):
        """Test updating non-existent position"""
        self.mock_position_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Position with ID 999 not found"):
            self.position_use_case.update_position(999, "Developer", "Software Developer")

    def test_delete_position_valid(self):
        """Test deleting existing position"""
        existing_position = Position(
            position_id=1,
            position_name="Developer",
            description="Software Developer"
        )
        self.mock_position_repository.get_by_id.return_value = existing_position
        self.mock_position_repository.delete.return_value = True

        result = self.position_use_case.delete_position(1)

        assert result is True
        self.mock_position_repository.get_by_id.assert_called_once_with(1)
        self.mock_position_repository.delete.assert_called_once_with(1)

    def test_delete_position_not_found(self):
        """Test deleting non-existent position"""
        self.mock_position_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Position with ID 999 not found"):
            self.position_use_case.delete_position(999)