"""
Position controller for handling position-related endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.domain.entities import User
from app.application.use_cases import PositionUseCase
from app.infrastructure.database import get_db
from app.infrastructure.repositories import SqlAlchemyPositionRepository
from app.presentation.controllers.auth_controller import get_current_active_user
from app.presentation.models import PositionCreateRequest, PositionUpdateRequest, PositionResponse

router = APIRouter()


def get_position_use_case(db: Session = Depends(get_db)) -> PositionUseCase:
    """Dependency to get position use case"""
    position_repository = SqlAlchemyPositionRepository(db)
    return PositionUseCase(position_repository)


@router.get("/", response_model=List[PositionResponse], summary="Get all positions")
async def get_positions(
    skip: int = 0,
    limit: int = 100,
    position_use_case: PositionUseCase = Depends(get_position_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Get all positions with pagination"""
    positions = position_use_case.get_all_positions(skip, limit)
    return [
        PositionResponse(
            position_id=pos.position_id,
            position_name=pos.position_name,
            description=pos.description
        )
        for pos in positions
    ]


@router.get("/{position_id}", response_model=PositionResponse, summary="Get position by ID")
async def get_position(
    position_id: int,
    position_use_case: PositionUseCase = Depends(get_position_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Get position by ID"""
    position = position_use_case.get_position_by_id(position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    
    return PositionResponse(
        position_id=position.position_id,
        position_name=position.position_name,
        description=position.description
    )


@router.post("/", response_model=PositionResponse, summary="Create a new position")
async def create_position(
    position_data: PositionCreateRequest,
    position_use_case: PositionUseCase = Depends(get_position_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new position.
    
    - **position_name**: Name of the position
    - **description**: Optional description of the position
    """
    try:
        position = position_use_case.create_position(
            position_name=position_data.position_name,
            description=position_data.description
        )
        return PositionResponse(
            position_id=position.position_id,
            position_name=position.position_name,
            description=position.description
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{position_id}", response_model=PositionResponse, summary="Update a position")
async def update_position(
    position_id: int,
    position_data: PositionUpdateRequest,
    position_use_case: PositionUseCase = Depends(get_position_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing position"""
    try:
        position = position_use_case.update_position(
            position_id=position_id,
            position_name=position_data.position_name,
            description=position_data.description
        )
        return PositionResponse(
            position_id=position.position_id,
            position_name=position.position_name,
            description=position.description
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{position_id}", summary="Delete a position")
async def delete_position(
    position_id: int,
    position_use_case: PositionUseCase = Depends(get_position_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a position"""
    try:
        success = position_use_case.delete_position(position_id)
        if success:
            return {"message": "Position deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Position not found")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))