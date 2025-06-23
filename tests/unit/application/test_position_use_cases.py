"""
Unit tests for position use cases
"""
import pytest
import uuid
from datetime import datetime
from unittest.mock import AsyncMock

from app.application.use_cases.position_use_cases import PositionUseCases
from app.domain.entities.employee import Position


class TestPositionUseCases:
    """Test Position use cases"""

    @pytest.fixture
    def mock_position_repo(self):
        """Mock position repository"""
        return AsyncMock()

    @pytest.fixture
    def mock_employee_repo(self):
        """Mock employee repository"""
        return AsyncMock()

    @pytest.fixture
    def position_use_cases(self, mock_position_repo, mock_employee_repo):
        """Position use cases instance"""
        return PositionUseCases(mock_position_repo, mock_employee_repo)

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

    @pytest.mark.asyncio
    async def test_get_position_by_id_success(
        self, position_use_cases, mock_position_repo, sample_position
    ):
        """Test successful get position by ID"""
        mock_position_repo.get_by_id.return_value = sample_position
        
        result = await position_use_cases.get_position_by_id(sample_position.id)
        
        assert result == sample_position
        mock_position_repo.get_by_id.assert_called_once_with(sample_position.id)

    @pytest.mark.asyncio
    async def test_get_position_by_id_not_found(
        self, position_use_cases, mock_position_repo
    ):
        """Test get position by ID when not found"""
        mock_position_repo.get_by_id.return_value = None
        
        result = await position_use_cases.get_position_by_id(uuid.uuid4())
        
        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_positions(
        self, position_use_cases, mock_position_repo, sample_position
    ):
        """Test get all positions"""
        mock_position_repo.get_all.return_value = [sample_position]
        
        result = await position_use_cases.get_all_positions(skip=0, limit=100)
        
        assert result == [sample_position]
        mock_position_repo.get_all.assert_called_once_with(0, 100)

    @pytest.mark.asyncio
    async def test_create_position_success(
        self, position_use_cases, mock_position_repo
    ):
        """Test successful position creation"""
        mock_position_repo.get_by_name.return_value = None  # No existing position
        created_position = Position(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name="Data Scientist",
            description="Analyzes data"
        )
        mock_position_repo.create.return_value = created_position
        
        result = await position_use_cases.create_position(
            name="Data Scientist",
            description="Analyzes data"
        )
        
        assert result == created_position
        mock_position_repo.get_by_name.assert_called_once_with("Data Scientist")
        mock_position_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_position_invalid_name(
        self, position_use_cases, mock_position_repo
    ):
        """Test position creation with invalid name"""
        with pytest.raises(ValueError, match="Invalid position name"):
            await position_use_cases.create_position(
                name="",  # Invalid empty name
                description="Test description"
            )

    @pytest.mark.asyncio
    async def test_create_position_already_exists(
        self, position_use_cases, mock_position_repo, sample_position
    ):
        """Test position creation when name already exists"""
        mock_position_repo.get_by_name.return_value = sample_position
        
        with pytest.raises(ValueError, match="Position with name 'Software Engineer' already exists"):
            await position_use_cases.create_position(
                name="Software Engineer",
                description="New description"
            )

    @pytest.mark.asyncio
    async def test_update_position_success(
        self, position_use_cases, mock_position_repo, sample_position
    ):
        """Test successful position update"""
        mock_position_repo.get_by_id.return_value = sample_position
        mock_position_repo.get_by_name.return_value = None  # No conflict
        updated_position = Position(
            id=sample_position.id,
            created_at=sample_position.created_at,
            updated_at=datetime.utcnow(),
            name="Senior Software Engineer",
            description="Lead developer"
        )
        mock_position_repo.update.return_value = updated_position
        
        result = await position_use_cases.update_position(
            position_id=sample_position.id,
            name="Senior Software Engineer",
            description="Lead developer"
        )
        
        assert result == updated_position
        mock_position_repo.get_by_id.assert_called_once_with(sample_position.id)
        mock_position_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_position_not_found(
        self, position_use_cases, mock_position_repo
    ):
        """Test position update when position not found"""
        position_id = uuid.uuid4()
        mock_position_repo.get_by_id.return_value = None
        
        with pytest.raises(ValueError, match=f"Position with ID {position_id} not found"):
            await position_use_cases.update_position(
                position_id=position_id,
                name="New Name",
                description="New description"
            )

    @pytest.mark.asyncio
    async def test_update_position_name_conflict(
        self, position_use_cases, mock_position_repo, sample_position
    ):
        """Test position update when name conflicts with another position"""
        another_position = Position(
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            name="Existing Position",
            description="Another position"
        )
        
        mock_position_repo.get_by_id.return_value = sample_position
        mock_position_repo.get_by_name.return_value = another_position
        
        with pytest.raises(ValueError, match="Position with name 'Existing Position' already exists"):
            await position_use_cases.update_position(
                position_id=sample_position.id,
                name="Existing Position",
                description="Updated description"
            )

    @pytest.mark.asyncio
    async def test_delete_position_success(
        self, position_use_cases, mock_position_repo, sample_position
    ):
        """Test successful position deletion"""
        mock_position_repo.get_by_id.return_value = sample_position
        mock_position_repo.has_employees.return_value = False
        mock_position_repo.delete.return_value = True
        
        result = await position_use_cases.delete_position(sample_position.id)
        
        assert result is True
        mock_position_repo.get_by_id.assert_called_once_with(sample_position.id)
        mock_position_repo.has_employees.assert_called_once_with(sample_position.id)
        mock_position_repo.delete.assert_called_once_with(sample_position.id)

    @pytest.mark.asyncio
    async def test_delete_position_not_found(
        self, position_use_cases, mock_position_repo
    ):
        """Test position deletion when position not found"""
        position_id = uuid.uuid4()
        mock_position_repo.get_by_id.return_value = None
        
        with pytest.raises(ValueError, match=f"Position with ID {position_id} not found"):
            await position_use_cases.delete_position(position_id)

    @pytest.mark.asyncio
    async def test_delete_position_has_employees(
        self, position_use_cases, mock_position_repo, sample_position
    ):
        """Test position deletion when position has employees"""
        mock_position_repo.get_by_id.return_value = sample_position
        mock_position_repo.has_employees.return_value = True
        
        with pytest.raises(ValueError, match="Cannot delete position: employees are assigned to this position"):
            await position_use_cases.delete_position(sample_position.id)