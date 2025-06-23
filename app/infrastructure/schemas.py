"""
Updated Pydantic schemas with UUID support for Clean Architecture
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid
from datetime import datetime


# Base schemas
class BaseResponseSchema(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(BaseResponseSchema, UserBase):
    is_active: bool


# Authentication schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Position schemas
class PositionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionResponse(BaseResponseSchema, PositionBase):
    pass


# Employee schemas
class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    position_id: uuid.UUID


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(BaseResponseSchema, EmployeeBase):
    position: Optional[PositionResponse] = None
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"