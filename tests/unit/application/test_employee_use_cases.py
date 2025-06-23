"""
Unit tests for employee use cases
"""
import pytest
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, Mock

from app.application.use_cases.employee_use_cases import EmployeeUseCases
from app.domain.entities.employee import Employee, Position


class TestEmployeeUseCases:
    """Test Employee use cases"""

    @pytest.fixture
    def mock_employee_repo(self):
        """Mock employee repository"""
        return AsyncMock()

    @pytest.fixture
    def mock_position_repo(self):
        """Mock position repository"""
        return AsyncMock()

    @pytest.fixture
    def employee_use_cases(self, mock_employee_repo, mock_position_repo):
        """Employee use cases instance"""
        return EmployeeUseCases(mock_employee_repo, mock_position_repo)

    @pytest.fixture
    def sample_position(self):
        """Sample position entity"""
        return Position(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name="Software Engineer",
            description="Develops software applications"
        )

    @pytest.fixture
    def sample_employee(self, sample_position):
        """Sample employee entity"""
        return Employee(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            first_name="John",
            last_name="Doe",
            position_id=sample_position.id,
            position=sample_position
        )

    @pytest.mark.asyncio
    async def test_get_employee_by_id_success(
        self, employee_use_cases, mock_employee_repo, sample_employee
    ):
        """Test successful get employee by ID"""
        mock_employee_repo.get_by_id.return_value = sample_employee
        
        result = await employee_use_cases.get_employee_by_id(sample_employee.id)
        
        assert result == sample_employee
        mock_employee_repo.get_by_id.assert_called_once_with(sample_employee.id)

    @pytest.mark.asyncio
    async def test_get_employee_by_id_not_found(
        self, employee_use_cases, mock_employee_repo
    ):
        """Test get employee by ID when not found"""
        mock_employee_repo.get_by_id.return_value = None
        
        result = await employee_use_cases.get_employee_by_id(uuid.uuid4())
        
        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_employees(
        self, employee_use_cases, mock_employee_repo, sample_employee
    ):
        """Test get all employees"""
        mock_employee_repo.get_all.return_value = [sample_employee]
        
        result = await employee_use_cases.get_all_employees(skip=0, limit=100)
        
        assert result == [sample_employee]
        mock_employee_repo.get_all.assert_called_once_with(0, 100)

    @pytest.mark.asyncio
    async def test_create_employee_success(
        self, employee_use_cases, mock_employee_repo, mock_position_repo, sample_position
    ):
        """Test successful employee creation"""
        mock_position_repo.get_by_id.return_value = sample_position
        created_employee = Employee(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            first_name="John",
            last_name="Doe",
            position_id=sample_position.id,
            position=sample_position
        )
        mock_employee_repo.create.return_value = created_employee
        
        result = await employee_use_cases.create_employee(
            first_name="John",
            last_name="Doe",
            position_id=sample_position.id
        )
        
        assert result == created_employee
        mock_position_repo.get_by_id.assert_called_once_with(sample_position.id)
        mock_employee_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_employee_invalid_first_name(
        self, employee_use_cases, mock_employee_repo, mock_position_repo
    ):
        """Test employee creation with invalid first name"""
        with pytest.raises(ValueError, match="Invalid name"):
            await employee_use_cases.create_employee(
                first_name="",
                last_name="Doe",
                position_id=uuid.uuid4()
            )

    @pytest.mark.asyncio
    async def test_create_employee_invalid_last_name(
        self, employee_use_cases, mock_employee_repo, mock_position_repo
    ):
        """Test employee creation with invalid last name"""
        with pytest.raises(ValueError, match="Invalid name"):
            await employee_use_cases.create_employee(
                first_name="John",
                last_name="123",
                position_id=uuid.uuid4()
            )

    @pytest.mark.asyncio
    async def test_create_employee_position_not_found(
        self, employee_use_cases, mock_employee_repo, mock_position_repo
    ):
        """Test employee creation when position not found"""
        position_id = uuid.uuid4()
        mock_position_repo.get_by_id.return_value = None
        
        with pytest.raises(ValueError, match=f"Position with ID {position_id} not found"):
            await employee_use_cases.create_employee(
                first_name="John",
                last_name="Doe",
                position_id=position_id
            )

    @pytest.mark.asyncio
    async def test_update_employee_success(
        self, employee_use_cases, mock_employee_repo, mock_position_repo, sample_employee, sample_position
    ):
        """Test successful employee update"""
        mock_employee_repo.get_by_id.return_value = sample_employee
        mock_position_repo.get_by_id.return_value = sample_position
        updated_employee = Employee(
            id=sample_employee.id,
            created_at=sample_employee.created_at,
            updated_at=datetime.utcnow(),
            first_name="Jane",
            last_name="Smith",
            position_id=sample_position.id,
            position=sample_position
        )
        mock_employee_repo.update.return_value = updated_employee
        
        result = await employee_use_cases.update_employee(
            employee_id=sample_employee.id,
            first_name="Jane",
            last_name="Smith",
            position_id=sample_position.id
        )
        
        assert result == updated_employee
        mock_employee_repo.get_by_id.assert_called_once_with(sample_employee.id)
        mock_position_repo.get_by_id.assert_called_once_with(sample_position.id)
        mock_employee_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_employee_not_found(
        self, employee_use_cases, mock_employee_repo, mock_position_repo
    ):
        """Test employee update when employee not found"""
        employee_id = uuid.uuid4()
        mock_employee_repo.get_by_id.return_value = None
        
        with pytest.raises(ValueError, match=f"Employee with ID {employee_id} not found"):
            await employee_use_cases.update_employee(
                employee_id=employee_id,
                first_name="John",
                last_name="Doe",
                position_id=uuid.uuid4()
            )

    @pytest.mark.asyncio
    async def test_update_employee_position_not_found(
        self, employee_use_cases, mock_employee_repo, mock_position_repo, sample_employee
    ):
        """Test employee update when position not found"""
        position_id = uuid.uuid4()
        mock_employee_repo.get_by_id.return_value = sample_employee
        mock_position_repo.get_by_id.return_value = None
        
        with pytest.raises(ValueError, match=f"Position with ID {position_id} not found"):
            await employee_use_cases.update_employee(
                employee_id=sample_employee.id,
                first_name="John",
                last_name="Doe",
                position_id=position_id
            )

    @pytest.mark.asyncio
    async def test_delete_employee_success(
        self, employee_use_cases, mock_employee_repo, sample_employee
    ):
        """Test successful employee deletion"""
        mock_employee_repo.get_by_id.return_value = sample_employee
        mock_employee_repo.delete.return_value = True
        
        result = await employee_use_cases.delete_employee(sample_employee.id)
        
        assert result is True
        mock_employee_repo.get_by_id.assert_called_once_with(sample_employee.id)
        mock_employee_repo.delete.assert_called_once_with(sample_employee.id)

    @pytest.mark.asyncio
    async def test_delete_employee_not_found(
        self, employee_use_cases, mock_employee_repo
    ):
        """Test employee deletion when employee not found"""
        employee_id = uuid.uuid4()
        mock_employee_repo.get_by_id.return_value = None
        
        with pytest.raises(ValueError, match=f"Employee with ID {employee_id} not found"):
            await employee_use_cases.delete_employee(employee_id)

    @pytest.mark.asyncio
    async def test_get_employees_by_position(
        self, employee_use_cases, mock_employee_repo, sample_employee, sample_position
    ):
        """Test get employees by position"""
        mock_employee_repo.get_by_position_id.return_value = [sample_employee]
        
        result = await employee_use_cases.get_employees_by_position(sample_position.id)
        
        assert result == [sample_employee]
        mock_employee_repo.get_by_position_id.assert_called_once_with(sample_position.id)