"""
Employee controller for handling employee-related endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.domain.entities import User
from app.application.use_cases import EmployeeUseCase
from app.infrastructure.database import get_db
from app.infrastructure.repositories import SqlAlchemyEmployeeRepository, SqlAlchemyPositionRepository
from app.presentation.controllers.auth_controller import get_current_active_user
from app.presentation.models import EmployeeCreateRequest, EmployeeUpdateRequest, EmployeeResponse

router = APIRouter()


def get_employee_use_case(db: Session = Depends(get_db)) -> EmployeeUseCase:
    """Dependency to get employee use case"""
    employee_repository = SqlAlchemyEmployeeRepository(db)
    position_repository = SqlAlchemyPositionRepository(db)
    return EmployeeUseCase(employee_repository, position_repository)


@router.get("/", response_model=List[EmployeeResponse], summary="Get all employees")
async def get_employees(
    skip: int = 0,
    limit: int = 100,
    employee_use_case: EmployeeUseCase = Depends(get_employee_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Get all employees with pagination"""
    employees = employee_use_case.get_all_employees(skip, limit)
    return [
        EmployeeResponse(
            emp_id=emp.emp_id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            position_id=emp.position_id,
            position=emp.position
        )
        for emp in employees
    ]


@router.get("/{emp_id}", response_model=EmployeeResponse, summary="Get employee by ID")
async def get_employee(
    emp_id: int,
    employee_use_case: EmployeeUseCase = Depends(get_employee_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Get employee by ID"""
    employee = employee_use_case.get_employee_by_id(emp_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return EmployeeResponse(
        emp_id=employee.emp_id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        position_id=employee.position_id,
        position=employee.position
    )


@router.post("/", response_model=EmployeeResponse, summary="Create a new employee")
async def create_employee(
    employee_data: EmployeeCreateRequest,
    employee_use_case: EmployeeUseCase = Depends(get_employee_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new employee.
    
    - **first_name**: Employee's first name
    - **last_name**: Employee's last name
    - **position_id**: ID of the position for this employee
    """
    try:
        employee = employee_use_case.create_employee(
            first_name=employee_data.first_name,
            last_name=employee_data.last_name,
            position_id=employee_data.position_id
        )
        return EmployeeResponse(
            emp_id=employee.emp_id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            position_id=employee.position_id,
            position=employee.position
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{emp_id}", response_model=EmployeeResponse, summary="Update an employee")
async def update_employee(
    emp_id: int,
    employee_data: EmployeeUpdateRequest,
    employee_use_case: EmployeeUseCase = Depends(get_employee_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing employee"""
    try:
        employee = employee_use_case.update_employee(
            emp_id=emp_id,
            first_name=employee_data.first_name,
            last_name=employee_data.last_name,
            position_id=employee_data.position_id
        )
        return EmployeeResponse(
            emp_id=employee.emp_id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            position_id=employee.position_id,
            position=employee.position
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{emp_id}", summary="Delete an employee")
async def delete_employee(
    emp_id: int,
    employee_use_case: EmployeeUseCase = Depends(get_employee_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Delete an employee"""
    try:
        success = employee_use_case.delete_employee(emp_id)
        if success:
            return {"message": "Employee deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))