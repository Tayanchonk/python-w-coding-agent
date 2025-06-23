"""
Pydantic models for request/response validation in the presentation layer
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


# User models
class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


# Employee models
class EmployeeCreateRequest(BaseModel):
    first_name: str
    last_name: str
    position_id: int


class EmployeeUpdateRequest(BaseModel):
    first_name: str
    last_name: str
    position_id: int


class EmployeeResponse(BaseModel):
    emp_id: int
    first_name: str
    last_name: str
    position_id: int
    position: Optional['PositionResponse'] = None

    class Config:
        from_attributes = True


# Position models
class PositionCreateRequest(BaseModel):
    position_name: str
    description: Optional[str] = None


class PositionUpdateRequest(BaseModel):
    position_name: str
    description: Optional[str] = None


class PositionResponse(BaseModel):
    position_id: int
    position_name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Fix forward reference
EmployeeResponse.model_rebuild()