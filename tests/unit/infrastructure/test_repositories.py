"""
Unit tests for repository implementations with mocked database
"""
import pytest
import uuid
from datetime import datetime
from unittest.mock import MagicMock, patch

from app.infrastructure.repositories.employee_repository import EmployeeRepository
from app.infrastructure.repositories.position_repository import PositionRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.database.models import EmployeeModel, PositionModel, UserModel
from app.domain.entities.employee import Employee, Position, User


class TestEmployeeRepository:
    """Test Employee repository implementation"""

    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        return MagicMock()

    @pytest.fixture
    def employee_repo(self, mock_db):
        """Employee repository instance"""
        return EmployeeRepository(mock_db)

    @pytest.fixture
    def mock_employee_model(self):
        """Mock employee database model"""
        position_model = MagicMock()
        position_model.id = uuid.uuid4()
        position_model.name = "Software Engineer"
        position_model.description = "Develops software"
        position_model.created_at = datetime.utcnow()
        position_model.updated_at = datetime.utcnow()
        
        model = MagicMock()
        model.id = uuid.uuid4()
        model.first_name = "John"
        model.last_name = "Doe"
        model.position_id = position_model.id
        model.created_at = datetime.utcnow()
        model.updated_at = datetime.utcnow()
        model.position = position_model
        return model

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, employee_repo, mock_db, mock_employee_model):
        """Test successful get employee by ID"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_options = MagicMock()
        mock_query.options.return_value = mock_options
        mock_filter = MagicMock()
        mock_options.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_employee_model
        
        result = await employee_repo.get_by_id(mock_employee_model.id)
        
        assert result is not None
        assert result.id == mock_employee_model.id
        assert result.first_name == "John"
        assert result.last_name == "Doe"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, employee_repo, mock_db):
        """Test get employee by ID when not found"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_options = MagicMock()
        mock_query.options.return_value = mock_options
        mock_filter = MagicMock()
        mock_options.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        result = await employee_repo.get_by_id(uuid.uuid4())
        
        assert result is None

    @pytest.mark.asyncio
    async def test_get_all(self, employee_repo, mock_db, mock_employee_model):
        """Test get all employees"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_options = MagicMock()
        mock_query.options.return_value = mock_options
        mock_offset = MagicMock()
        mock_options.offset.return_value = mock_offset
        mock_limit = MagicMock()
        mock_offset.limit.return_value = mock_limit
        mock_limit.all.return_value = [mock_employee_model]
        
        result = await employee_repo.get_all(skip=0, limit=100)
        
        assert len(result) == 1
        assert result[0].first_name == "John"

    @pytest.mark.asyncio
    async def test_create_employee(self, employee_repo, mock_db, mock_employee_model):
        """Test employee creation"""
        employee = Employee(
            id=mock_employee_model.id,
            created_at=mock_employee_model.created_at,
            updated_at=mock_employee_model.updated_at,
            first_name="John",
            last_name="Doe",
            position_id=mock_employee_model.position_id
        )
        
        # Mock the database operations
        mock_db.add = MagicMock()
        mock_db.commit = MagicMock()
        mock_db.refresh = MagicMock()
        
        # Mock the query for loading relationships
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_options = MagicMock()
        mock_query.options.return_value = mock_options
        mock_filter = MagicMock()
        mock_options.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_employee_model
        
        result = await employee_repo.create(employee)
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        assert result.first_name == "John"


class TestPositionRepository:
    """Test Position repository implementation"""

    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        return MagicMock()

    @pytest.fixture
    def position_repo(self, mock_db):
        """Position repository instance"""
        return PositionRepository(mock_db)

    @pytest.fixture
    def mock_position_model(self):
        """Mock position database model"""
        model = MagicMock()
        model.id = uuid.uuid4()
        model.name = "Software Engineer"
        model.description = "Develops software"
        model.created_at = datetime.utcnow()
        model.updated_at = datetime.utcnow()
        return model

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, position_repo, mock_db, mock_position_model):
        """Test successful get position by ID"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_position_model
        
        result = await position_repo.get_by_id(mock_position_model.id)
        
        assert result is not None
        assert result.id == mock_position_model.id
        assert result.name == "Software Engineer"

    @pytest.mark.asyncio
    async def test_get_by_name_success(self, position_repo, mock_db, mock_position_model):
        """Test successful get position by name"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_position_model
        
        result = await position_repo.get_by_name("Software Engineer")
        
        assert result is not None
        assert result.name == "Software Engineer"

    @pytest.mark.asyncio
    async def test_has_employees_true(self, position_repo, mock_db):
        """Test has_employees returns True when employees exist"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_filter.count.return_value = 5  # Has employees
        
        result = await position_repo.has_employees(uuid.uuid4())
        
        assert result is True

    @pytest.mark.asyncio
    async def test_has_employees_false(self, position_repo, mock_db):
        """Test has_employees returns False when no employees exist"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_filter.count.return_value = 0  # No employees
        
        result = await position_repo.has_employees(uuid.uuid4())
        
        assert result is False


class TestUserRepository:
    """Test User repository implementation"""

    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        return MagicMock()

    @pytest.fixture
    def user_repo(self, mock_db):
        """User repository instance"""
        return UserRepository(mock_db)

    @pytest.fixture
    def mock_user_model(self):
        """Mock user database model"""
        model = MagicMock()
        model.id = uuid.uuid4()
        model.username = "testuser"
        model.email = "test@example.com"
        model.password_hash = "hashed_password"
        model.is_active = True
        model.created_at = datetime.utcnow()
        model.updated_at = datetime.utcnow()
        return model

    @pytest.mark.asyncio
    async def test_get_by_username_success(self, user_repo, mock_db, mock_user_model):
        """Test successful get user by username"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_user_model
        
        result = await user_repo.get_by_username("testuser")
        
        assert result is not None
        assert result.username == "testuser"
        assert result.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_by_email_success(self, user_repo, mock_db, mock_user_model):
        """Test successful get user by email"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_user_model
        
        result = await user_repo.get_by_email("test@example.com")
        
        assert result is not None
        assert result.username == "testuser"
        assert result.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_delete_user_success(self, user_repo, mock_db, mock_user_model):
        """Test successful user deletion"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_user_model
        
        mock_db.delete = MagicMock()
        mock_db.commit = MagicMock()
        
        result = await user_repo.delete(mock_user_model.id)
        
        assert result is True
        mock_db.delete.assert_called_once_with(mock_user_model)
        mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, user_repo, mock_db):
        """Test user deletion when user not found"""
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        result = await user_repo.delete(uuid.uuid4())
        
        assert result is False