"""
Employee management endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee, User
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.auth import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[EmployeeResponse], summary="Get all employees")
async def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve all employees with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees


@router.get("/{emp_id}", response_model=EmployeeResponse, summary="Get employee by ID")
async def get_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a specific employee by their ID.
    
    - **emp_id**: The ID of the employee to retrieve
    """
    employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.post("/", response_model=EmployeeResponse, summary="Create a new employee")
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new employee.
    
    - **first_name**: Employee's first name
    - **last_name**: Employee's last name
    - **position_id**: ID of the position for this employee
    """
    # Check if position exists
    from app.models import Position
    position = db.query(Position).filter(Position.position_id == employee.position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    db_employee = Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        position_id=employee.position_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.put("/{emp_id}", response_model=EmployeeResponse, summary="Update an employee")
async def update_employee(
    emp_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing employee.
    
    - **emp_id**: The ID of the employee to update
    - **first_name**: Employee's first name
    - **last_name**: Employee's last name
    - **position_id**: ID of the position for this employee
    """
    db_employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check if position exists
    from app.models import Position
    position = db.query(Position).filter(Position.position_id == employee.position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    db_employee.first_name = employee.first_name
    db_employee.last_name = employee.last_name
    db_employee.position_id = employee.position_id
    
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.delete("/{emp_id}", summary="Delete an employee")
async def delete_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete an employee by their ID.
    
    - **emp_id**: The ID of the employee to delete
    """
    db_employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return {"message": "Employee deleted successfully"}