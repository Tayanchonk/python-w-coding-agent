"""
Employee API endpoints using Clean Architecture
"""
from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.employee_use_cases import EmployeeUseCases
from app.infrastructure.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.infrastructure.repositories.employee_repository import EmployeeRepository
from app.infrastructure.repositories.position_repository import PositionRepository
from app.database import get_db
from app.auth import get_current_active_user
from app.models import User
from sqlalchemy.orm import Session


router = APIRouter()


def get_employee_use_cases(db: Session = Depends(get_db)) -> EmployeeUseCases:
    """Dependency to get employee use cases"""
    employee_repo = EmployeeRepository(db)
    position_repo = PositionRepository(db)
    return EmployeeUseCases(employee_repo, position_repo)


@router.get("/", response_model=List[EmployeeResponse], summary="Get all employees")
async def get_employees(
    skip: int = 0,
    limit: int = 100,
    employee_use_cases: EmployeeUseCases = Depends(get_employee_use_cases),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve all employees with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    try:
        employees = await employee_use_cases.get_all_employees(skip, limit)
        return [_to_response_schema(emp) for emp in employees]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{employee_id}", response_model=EmployeeResponse, summary="Get employee by ID")
async def get_employee(
    employee_id: uuid.UUID,
    employee_use_cases: EmployeeUseCases = Depends(get_employee_use_cases),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a specific employee by their ID.
    
    - **employee_id**: The UUID of the employee to retrieve
    """
    try:
        employee = await employee_use_cases.get_employee_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return _to_response_schema(employee)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=EmployeeResponse, summary="Create a new employee")
async def create_employee(
    employee_data: EmployeeCreate,
    employee_use_cases: EmployeeUseCases = Depends(get_employee_use_cases),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new employee.
    
    - **first_name**: Employee's first name
    - **last_name**: Employee's last name
    - **position_id**: UUID of the position for this employee
    """
    try:
        employee = await employee_use_cases.create_employee(
            first_name=employee_data.first_name,
            last_name=employee_data.last_name,
            position_id=employee_data.position_id
        )
        return _to_response_schema(employee)
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{employee_id}", response_model=EmployeeResponse, summary="Update an employee")
async def update_employee(
    employee_id: uuid.UUID,
    employee_data: EmployeeUpdate,
    employee_use_cases: EmployeeUseCases = Depends(get_employee_use_cases),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing employee.
    
    - **employee_id**: The UUID of the employee to update
    - **first_name**: Employee's first name
    - **last_name**: Employee's last name
    - **position_id**: UUID of the position for this employee
    """
    try:
        employee = await employee_use_cases.update_employee(
            employee_id=employee_id,
            first_name=employee_data.first_name,
            last_name=employee_data.last_name,
            position_id=employee_data.position_id
        )
        return _to_response_schema(employee)
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{employee_id}", summary="Delete an employee")
async def delete_employee(
    employee_id: uuid.UUID,
    employee_use_cases: EmployeeUseCases = Depends(get_employee_use_cases),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete an employee by their ID.
    
    - **employee_id**: The UUID of the employee to delete
    """
    try:
        success = await employee_use_cases.delete_employee(employee_id)
        if not success:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"message": "Employee deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _to_response_schema(employee) -> EmployeeResponse:
    """Convert domain entity to response schema"""
    position_response = None
    if employee.position:
        position_response = {
            "id": employee.position.id,
            "created_at": employee.position.created_at,
            "updated_at": employee.position.updated_at,
            "name": employee.position.name,
            "description": employee.position.description
        }
    
    return EmployeeResponse(
        id=employee.id,
        created_at=employee.created_at,
        updated_at=employee.updated_at,
        first_name=employee.first_name,
        last_name=employee.last_name,
        position_id=employee.position_id,
        position=position_response
    )