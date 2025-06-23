"""
Integration tests for the Clean Architecture API
"""
import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.clean_main import app
from app.infrastructure.database import Base, get_db
from app.infrastructure.database import UserModel, PositionModel, EmployeeModel
from app.application.services import AuthenticationService


# Create test database
@pytest.fixture(scope="module")
def test_db():
    """Create test database"""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp()
    database_url = f"sqlite:///{db_path}"
    
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="module")
def client(test_db):
    """Create test client"""
    return TestClient(app)


@pytest.fixture(scope="module")
def setup_test_data(test_db):
    """Set up test data"""
    db = test_db()
    
    # Create test position
    test_position = PositionModel(
        position_name="Test Position",
        description="A test position"
    )
    db.add(test_position)
    db.commit()
    
    # Create test user
    auth_service = AuthenticationService(
        user_repository=None,  # We'll use direct DB access for setup
        secret_key="test-secret-key"
    )
    hashed_password = auth_service.get_password_hash("testpass")
    test_user = UserModel(
        username="testuser",
        email="test@example.com",
        password=hashed_password,
        is_active=True
    )
    db.add(test_user)
    db.commit()
    
    # Create test employee
    test_employee = EmployeeModel(
        first_name="Test",
        last_name="Employee",
        position_id=1
    )
    db.add(test_employee)
    db.commit()
    
    db.close()
    yield
    
    # Cleanup is handled by test_db fixture


def get_auth_token(client):
    """Get authentication token for testing"""
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    return response.json()["access_token"]


class TestCleanArchitectureAPI:
    """Integration tests for Clean Architecture API"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "architecture" in data
        assert data["architecture"] == "Clean Architecture"
        assert data["version"] == "2.0.0"
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["architecture"] == "clean"
    
    def test_register_user(self, client, setup_test_data):
        """Test user registration"""
        response = client.post("/auth/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert data["is_active"] is True
    
    def test_login(self, client, setup_test_data):
        """Test user login"""
        response = client.post("/auth/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_get_employees_authenticated(self, client, setup_test_data):
        """Test getting employees with authentication"""
        token = get_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/employees/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_employees_unauthenticated(self, client, setup_test_data):
        """Test getting employees without authentication"""
        response = client.get("/employees/")
        assert response.status_code == 403
    
    def test_create_employee(self, client, setup_test_data):
        """Test creating a new employee"""
        token = get_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.post("/employees/", headers=headers, json={
            "first_name": "New",
            "last_name": "Employee",
            "position_id": 1
        })
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "New"
        assert data["last_name"] == "Employee"
        assert data["position_id"] == 1
    
    def test_get_positions(self, client, setup_test_data):
        """Test getting positions"""
        token = get_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/positions/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_create_position(self, client, setup_test_data):
        """Test creating a new position"""
        token = get_auth_token(client)
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.post("/positions/", headers=headers, json={
            "position_name": "New Position",
            "description": "A new test position"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["position_name"] == "New Position"
        assert data["description"] == "A new test position"