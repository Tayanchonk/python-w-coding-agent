"""
Position management endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Position, User
from app.schemas import PositionCreate, PositionUpdate, PositionResponse
from app.auth import get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[PositionResponse], summary="Get all positions")
async def get_positions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve all positions with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    positions = db.query(Position).offset(skip).limit(limit).all()
    return positions


@router.get("/{position_id}", response_model=PositionResponse, summary="Get position by ID")
async def get_position(
    position_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a specific position by its ID.
    
    - **position_id**: The ID of the position to retrieve
    """
    position = db.query(Position).filter(Position.position_id == position_id).first()
    if position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return position


@router.post("/", response_model=PositionResponse, summary="Create a new position")
async def create_position(
    position: PositionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new position.
    
    - **position_name**: Name of the position
    - **description**: Optional description of the position
    """
    db_position = Position(
        name=position.name,
        description=position.description
    )
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position


@router.put("/{position_id}", response_model=PositionResponse, summary="Update a position")
async def update_position(
    position_id: int,
    position: PositionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing position.
    
    - **position_id**: The ID of the position to update
    - **position_name**: Name of the position
    - **description**: Optional description of the position
    """
    db_position = db.query(Position).filter(Position.position_id == position_id).first()
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    
    db_position.position_name = position.position_name
    db_position.description = position.description
    
    db.commit()
    db.refresh(db_position)
    return db_position


@router.delete("/{position_id}", summary="Delete a position")
async def delete_position(
    position_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a position by its ID.
    
    - **position_id**: The ID of the position to delete
    """
    db_position = db.query(Position).filter(Position.position_id == position_id).first()
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    
    # Check if any employees are assigned to this position
    from app.models import Employee
    employees_with_position = db.query(Employee).filter(Employee.position_id == position_id).first()
    if employees_with_position:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete position: employees are assigned to this position"
        )
    
    db.delete(db_position)
    db.commit()
    return {"message": "Position deleted successfully"}