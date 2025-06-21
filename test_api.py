"""
Basic tests for the Employee Management API
"""
import pytest
import httpx
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

from app.main import app
from app.database import get_db, Base
from app.models import User, Position, Employee
from app.auth import get_password_hash
from app.utils import generate_uuid, is_valid_uuid

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    """Set up test database with sample data"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Add test user
    test_user = User(
        username="testuser",
        email="test@example.com",
        password=get_password_hash("testpass"),
        is_active=True
    )
    db.add(test_user)
    
    # Add test position
    test_position = Position(
        position_name="Test Position",
        description="A test position"
    )
    db.add(test_position)
    db.commit()
    db.refresh(test_position)  # Get the generated UUID
    
    # Add test employee using the position UUID
    test_employee = Employee(
        first_name="Test",
        last_name="Employee",
        position_id=test_position.position_id
    )
    db.add(test_employee)
    db.commit()
    db.close()
    
    yield
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        os.remove("test.db")


def get_auth_token():
    """Get authentication token for testing"""
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    return response.json()["access_token"]


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self, setup_database):
        """Test user registration"""
        response = client.post("/auth/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert is_valid_uuid(data["user_id"])
    
    def test_login(self, setup_database):
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
    
    def test_invalid_login(self, setup_database):
        """Test login with invalid credentials"""
        response = client.post("/auth/login", json={
            "username": "testuser",
            "password": "wrongpass"
        })
        assert response.status_code == 401


class TestEmployees:
    """Test employee management endpoints"""
    
    def test_get_employees(self, setup_database):
        """Test getting all employees"""
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/employees/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        # Verify that employee IDs are UUIDs
        for employee in data:
            assert is_valid_uuid(employee["emp_id"])
            assert is_valid_uuid(employee["position_id"])
    
    def test_get_employee_by_id(self, setup_database):
        """Test getting employee by ID"""
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # First get all employees to find a valid UUID
        response = client.get("/employees/", headers=headers)
        assert response.status_code == 200
        employees = response.json()
        assert len(employees) > 0
        
        emp_id = employees[0]["emp_id"]
        
        # Now get the specific employee
        response = client.get(f"/employees/{emp_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["emp_id"] == emp_id
        assert data["first_name"] == "Test"
        assert is_valid_uuid(data["emp_id"])
    
    def test_create_employee(self, setup_database):
        """Test creating a new employee"""
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # First get a valid position ID
        response = client.get("/positions/", headers=headers)
        assert response.status_code == 200
        positions = response.json()
        assert len(positions) > 0
        position_id = positions[0]["position_id"]
        
        # Create employee with valid position UUID
        response = client.post("/employees/", headers=headers, json={
            "first_name": "New",
            "last_name": "Employee",
            "position_id": position_id
        })
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "New"
        assert data["last_name"] == "Employee"
        assert is_valid_uuid(data["emp_id"])
        assert data["position_id"] == position_id
    
    def test_unauthorized_access(self, setup_database):
        """Test unauthorized access to employees"""
        response = client.get("/employees/")
        assert response.status_code == 403


class TestPositions:
    """Test position management endpoints"""
    
    def test_get_positions(self, setup_database):
        """Test getting all positions"""
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/positions/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        # Verify that position IDs are UUIDs
        for position in data:
            assert is_valid_uuid(position["position_id"])
    
    def test_create_position(self, setup_database):
        """Test creating a new position"""
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/positions/", headers=headers, json={
            "position_name": "New Position",
            "description": "A new test position"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["position_name"] == "New Position"
        assert is_valid_uuid(data["position_id"])


class TestAPIHealth:
    """Test API health and basic endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"