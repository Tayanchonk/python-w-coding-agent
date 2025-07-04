# Employee Management API

A Python-based CRUD API for employee management with JWT authentication built using FastAPI, SQLAlchemy, and SQLite.

## Features

- **Authentication**: JWT token-based authentication with login, register, and refresh endpoints
- **Employee Management**: Full CRUD operations for employees
- **Position Management**: Full CRUD operations for job positions
- **Database**: SQLite database with proper relationships
- **Documentation**: Auto-generated Swagger UI documentation
- **Testing**: Comprehensive test suite using pytest

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **JWT**: JSON Web Tokens for authentication
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application

## Installation

1. Clone the repository:
```bash
git clone <repository_url>
cd python-w-coding-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database with sample data:
```bash
python init_db.py
```

**Note**: If you get `ModuleNotFoundError` when running `init_db.py`, make sure you have installed all dependencies from step 2.

4. Run the application:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Schema

### Users Table
- `user_id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password` (Hashed)
- `is_active` (Boolean)

### Positions Table
- `position_id` (Primary Key)
- `position_name`
- `description` (Optional)

### Employees Table
- `emp_id` (Primary Key)
- `first_name`
- `last_name`
- `position_id` (Foreign Key to Positions)

## Sample Credentials

After running `init_db.py`, you can use these test accounts:

- **Username**: `admin`, **Password**: `admin123`
- **Username**: `manager`, **Password**: `manager123`

## API Endpoints

### Authentication

#### Register a New User
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "email": "newuser@example.com",
       "password": "newpassword"
     }'
```

**Response:**
```json
{
  "user_id": 3,
  "username": "newuser",
  "email": "newuser@example.com",
  "is_active": true
}
```

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin",
       "password": "admin123"
     }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Refresh Token
```bash
curl -X POST "http://localhost:8000/auth/refresh" \
     -H "Authorization: Bearer <refresh_token>"
```

### Employee Management

**Note**: All employee endpoints require authentication. Include the access token in the Authorization header.

#### Get All Employees
```bash
curl -X GET "http://localhost:8000/employees/" \
     -H "Authorization: Bearer <access_token>"
```

**Response:**
```json
[
  {
    "emp_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "position_id": 1,
    "position": {
      "position_id": 1,
      "position_name": "Software Engineer",
      "description": "Develops and maintains software applications"
    }
  }
]
```

#### Get Employee by ID
```bash
curl -X GET "http://localhost:8000/employees/1" \
     -H "Authorization: Bearer <access_token>"
```

#### Create New Employee
```bash
curl -X POST "http://localhost:8000/employees/" \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Alice",
       "last_name": "Brown",
       "position_id": 2
     }'
```

**Response:**
```json
{
  "emp_id": 5,
  "first_name": "Alice",
  "last_name": "Brown",
  "position_id": 2,
  "position": {
    "position_id": 2,
    "position_name": "Product Manager",
    "description": "Manages product development and strategy"
  }
}
```

#### Update Employee
```bash
curl -X PUT "http://localhost:8000/employees/1" \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Smith",
       "position_id": 2
     }'
```

#### Delete Employee
```bash
curl -X DELETE "http://localhost:8000/employees/1" \
     -H "Authorization: Bearer <access_token>"
```

**Response:**
```json
{
  "message": "Employee deleted successfully"
}
```

### Position Management

#### Get All Positions
```bash
curl -X GET "http://localhost:8000/positions/" \
     -H "Authorization: Bearer <access_token>"
```

**Response:**
```json
[
  {
    "position_id": 1,
    "position_name": "Software Engineer",
    "description": "Develops and maintains software applications"
  }
]
```

#### Get Position by ID
```bash
curl -X GET "http://localhost:8000/positions/1" \
     -H "Authorization: Bearer <access_token>"
```

#### Create New Position
```bash
curl -X POST "http://localhost:8000/positions/" \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "position_name": "UI/UX Designer",
       "description": "Designs user interfaces and experiences"
     }'
```

**Response:**
```json
{
  "position_id": 5,
  "position_name": "UI/UX Designer",
  "description": "Designs user interfaces and experiences"
}
```

#### Update Position
```bash
curl -X PUT "http://localhost:8000/positions/1" \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "position_name": "Senior Software Engineer",
       "description": "Leads software development projects"
     }'
```

#### Delete Position
```bash
curl -X DELETE "http://localhost:8000/positions/1" \
     -H "Authorization: Bearer <access_token>"
```

**Response:**
```json
{
  "message": "Position deleted successfully"
}
```

## Health Check

#### Check API Health
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy"
}
```

#### Get API Information
```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "Employee Management API",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

## Testing

Run the test suite:
```bash
python -m pytest test_api.py -v
```

## Authentication Flow

1. **Register** a new user or use existing credentials
2. **Login** to receive access and refresh tokens
3. **Use access token** in Authorization header for all protected endpoints
4. **Refresh token** when access token expires (every 30 minutes)

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (invalid authentication)
- `404`: Not Found
- `422`: Unprocessable Entity (validation errors)
- `500`: Internal Server Error

Error responses include detailed messages:
```json
{
  "detail": "Employee not found"
}
```

## Security Features

- Password hashing using bcrypt
- JWT tokens with expiration
- Token refresh mechanism
- Protected endpoints requiring authentication
- Input validation using Pydantic

## Development

For development with auto-reload:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Production Considerations

Before deploying to production:

1. Change the `SECRET_KEY` in `app/auth.py` to a secure random key
2. Use environment variables for configuration
3. Configure proper CORS settings
4. Use a production database (PostgreSQL, MySQL)
5. Set up proper logging
6. Configure HTTPS
7. Set appropriate token expiration times

## Troubleshooting

### Common Issues

#### `ModuleNotFoundError: No module named 'sqlalchemy'`
This error occurs when you try to run `init_db.py` without installing the required dependencies.

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individual packages
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart
```

#### Database initialization fails
If `init_db.py` fails to create tables or add sample data:

1. Check that all dependencies are installed
2. Ensure you have write permissions in the current directory
3. Delete the existing database file and try again:
   ```bash
   rm employee_management.db
   python init_db.py
   ```

#### Import errors when running the application
Make sure you're running the application from the project root directory and all dependencies are installed.

## License

This project is licensed under the MIT License.