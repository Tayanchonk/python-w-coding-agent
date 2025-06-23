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

# Create test database
TEST_DB_FD, TEST_DB_PATH = tempfile.mkstemp(suffix='.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
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
        email="testuser@example.com",
        password_hash=get_password_hash("testpass"),
        is_active=True
    )
    db.add(test_user)
    
    # Add test position
    test_position = Position(
        name="Test Position",
        description="A test position"
    )
    db.add(test_position)
    db.commit()
    
    # Add test employee
    test_employee = Employee(
        first_name="Test",
        last_name="Employee",
        position_id=test_position.id
    )
    db.add(test_employee)
    db.commit()
    db.close()
    
    yield
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    db.close()
    try:
        os.close(TEST_DB_FD)
    except Exception:
        pass
    try:
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
    except Exception:
        pass


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
    
    def test_get_employee_by_id(self, setup_database):
        """Test getting employee by ID"""
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        # ใช้ UUID ของ test_employee ที่สร้างใน setup_database
        from app.database import get_db
        db = next(override_get_db())
        employee = db.query(Employee).filter(Employee.first_name=="Test").first()
        response = client.get(f"/employees/{employee.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(employee.id)
        assert data["first_name"] == "Test"

    def test_create_employee(self, setup_database):
        """Test creating a new employee"""
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        # ต้องใช้ position_id เป็น UUID string
        from app.database import get_db
        db = next(override_get_db())
        position = db.query(Position).first()
        response = client.post("/employees/", headers=headers, json={
            "first_name": "New",
            "last_name": "Employee",
            "position_id": str(position.id)
        })
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "New"
        assert data["last_name"] == "Employee"

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
    
    def test_create_position(self, setup_database):
        """Test creating a new position"""
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/positions/", headers=headers, json={
            "name": "New Position",
            "description": "A new test position"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Position"


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