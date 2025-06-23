# Employee Management API - Clean Architecture

This is a modern FastAPI-based Employee Management API that follows Clean Architecture principles, providing a clear separation of concerns and high testability.

## Architecture Overview

The application is structured according to Clean Architecture principles with the following layers:

### 1. Domain Layer (Core Business Logic)
- **Entities**: Core business objects (`User`, `Employee`, `Position`)
- **Interfaces**: Repository contracts and abstractions
- **Business Rules**: Domain validation and business logic

### 2. Application Layer
- **Use Cases**: Application-specific business rules
- **Services**: Application services for complex operations
- **Business Logic**: Orchestration of domain entities

### 3. Infrastructure Layer
- **Database**: SQLAlchemy models and database configuration
- **Repositories**: Data access implementations
- **External Services**: External API integrations

### 4. Presentation Layer
- **Controllers**: FastAPI route handlers
- **Models**: Request/response Pydantic models
- **Serialization**: Data transformation for API responses

## Features

- **Clean Architecture**: Proper separation of concerns with dependency inversion
- **Authentication**: JWT token-based authentication with login, register, and refresh endpoints
- **Employee Management**: Full CRUD operations for employees
- **Position Management**: Full CRUD operations for job positions
- **Database**: SQLite database with proper relationships
- **Documentation**: Auto-generated Swagger UI documentation
- **Testing**: Comprehensive unit and integration tests with coverage reporting
- **Type Safety**: Full type hints throughout the codebase

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **JWT**: JSON Web Tokens for authentication
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application
- **Pytest**: Testing framework with coverage support

## Project Structure

```
app/
├── domain/                    # Domain layer (business entities and rules)
│   ├── entities.py           # Domain entities
│   └── interfaces.py         # Repository interfaces
├── application/              # Application layer (use cases and services)
│   ├── services.py          # Application services
│   └── use_cases.py         # Use case implementations
├── infrastructure/          # Infrastructure layer (data access)
│   ├── database.py         # Database configuration and models
│   └── repositories.py     # Repository implementations
├── presentation/           # Presentation layer (API controllers)
│   ├── controllers/        # FastAPI controllers
│   │   ├── auth_controller.py
│   │   ├── employee_controller.py
│   │   └── position_controller.py
│   └── models.py          # Request/response models
└── clean_main.py          # Application entry point

tests/
├── unit/                  # Unit tests
│   ├── domain/           # Domain layer tests
│   └── application/      # Application layer tests
└── integration/          # Integration tests
```

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd python-w-coding-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python -m app.clean_main
   # OR
   uvicorn app.clean_main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing

### Run all tests:
```bash
python -m pytest tests/ -v
```

### Run unit tests only:
```bash
python -m pytest tests/unit/ -v
```

### Run integration tests only:
```bash
python -m pytest tests/integration/ -v
```

### Run tests with coverage:
```bash
python -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html
```

### View coverage report:
After running tests with coverage, open `htmlcov/index.html` in your browser.

## API Endpoints

### Authentication

#### Register a New User
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "newuser", "email": "user@example.com", "password": "password123"}'
```

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "newuser", "password": "password123"}'
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
     -d '{"first_name": "John", "last_name": "Doe", "position_id": 1}'
```

#### Update Employee
```bash
curl -X PUT "http://localhost:8000/employees/1" \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{"first_name": "John", "last_name": "Smith", "position_id": 2}'
```

#### Delete Employee
```bash
curl -X DELETE "http://localhost:8000/employees/1" \
     -H "Authorization: Bearer <access_token>"
```

### Position Management

#### Get All Positions
```bash
curl -X GET "http://localhost:8000/positions/" \
     -H "Authorization: Bearer <access_token>"
```

#### Create New Position
```bash
curl -X POST "http://localhost:8000/positions/" \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{"position_name": "Software Engineer", "description": "Develops software applications"}'
```

## Health Check

#### Check API Health
```bash
curl -X GET "http://localhost:8000/health"
```

#### Get API Information
```bash
curl -X GET "http://localhost:8000/"
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
- Clean Architecture for better security boundaries

## Development

### Running with Auto-reload
```bash
uvicorn app.clean_main:app --reload --host 0.0.0.0 --port 8000
```

### Code Quality
The codebase follows Clean Architecture principles:
- **Domain entities** contain business logic and validation
- **Use cases** orchestrate business operations
- **Repositories** abstract data access
- **Controllers** handle HTTP concerns only
- **Dependency injection** for loose coupling
- **Interface segregation** for testability

### Testing Strategy
- **Unit Tests**: Test individual components in isolation with mocks
- **Integration Tests**: Test the full application stack
- **Coverage**: Maintain high test coverage for business logic
- **Mocking**: Proper mocking of dependencies for unit tests

## Migration from Legacy Code

The original FastAPI code has been preserved in the original files. The new Clean Architecture implementation is in:
- `app/clean_main.py` - New application entry point
- `app/domain/` - Domain layer
- `app/application/` - Application layer  
- `app/infrastructure/` - Infrastructure layer
- `app/presentation/` - Presentation layer

Both implementations can coexist during migration.

## Contributing

1. Follow Clean Architecture principles
2. Write tests for new features
3. Maintain type hints
4. Update documentation
5. Ensure test coverage remains high

## License

This project is licensed under the MIT License.