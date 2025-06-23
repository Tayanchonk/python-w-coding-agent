"""
Legacy Pydantic schemas - now using UUID-based schemas for backward compatibility
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid
from datetime import datetime

# Import the new schemas
from app.infrastructure.schemas import (
    UserBase as NewUserBase,
    UserCreate as NewUserCreate, 
    UserResponse as NewUserResponse,
    Token, TokenData, LoginRequest,
    PositionBase as NewPositionBase,
    PositionCreate as NewPositionCreate,
    PositionUpdate as NewPositionUpdate,
    PositionResponse as NewPositionResponse,
    EmployeeBase as NewEmployeeBase,
    EmployeeCreate as NewEmployeeCreate,
    EmployeeUpdate as NewEmployeeUpdate,
    EmployeeResponse as NewEmployeeResponse
)

# Legacy schemas for backward compatibility
class UserBase(NewUserBase):
    pass

class UserCreate(NewUserCreate):
    pass

class UserResponse(NewUserResponse):
    # Keep legacy field name for compatibility
    user_id: uuid.UUID = Field(alias="id")
    
    class Config:
        from_attributes = True
        allow_population_by_field_name = True

class PositionBase(NewPositionBase):
    # Map legacy field name
    position_name: str = Field(alias="name")
    
    class Config:
        allow_population_by_field_name = True

class PositionCreate(NewPositionCreate):
    position_name: str = Field(alias="name")
    
    class Config:
        allow_population_by_field_name = True

class PositionUpdate(NewPositionUpdate):
    position_name: str = Field(alias="name")
    
    class Config:
        allow_population_by_field_name = True

class PositionResponse(NewPositionResponse):
    # Keep legacy field names for compatibility
    position_id: uuid.UUID = Field(alias="id")
    position_name: str = Field(alias="name")
    
    class Config:
        from_attributes = True
        allow_population_by_field_name = True

class EmployeeBase(NewEmployeeBase):
    pass

class EmployeeCreate(NewEmployeeCreate):
    pass

class EmployeeUpdate(NewEmployeeUpdate):
    pass

class EmployeeResponse(NewEmployeeResponse):
    # Keep legacy field name for compatibility
    emp_id: uuid.UUID = Field(alias="id")
    
    class Config:
        from_attributes = True
        allow_population_by_field_name = True