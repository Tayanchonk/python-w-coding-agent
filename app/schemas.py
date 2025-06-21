"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from app.utils import validate_uuid


# User schemas
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    user_id: str
    is_active: bool

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        return validate_uuid(v)

    class Config:
        from_attributes = True


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
    position_name: str
    description: Optional[str] = None


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionResponse(PositionBase):
    position_id: str

    @field_validator('position_id')
    @classmethod
    def validate_position_id(cls, v):
        return validate_uuid(v)

    class Config:
        from_attributes = True


# Employee schemas
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    position_id: str

    @field_validator('position_id')
    @classmethod
    def validate_position_id(cls, v):
        return validate_uuid(v)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    emp_id: str
    position: Optional[PositionResponse] = None

    @field_validator('emp_id')
    @classmethod
    def validate_emp_id(cls, v):
        return validate_uuid(v)

    class Config:
        from_attributes = True