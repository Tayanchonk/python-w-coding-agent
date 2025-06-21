"""
Database models for the Employee Management API
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)


class Position(Base):
    """Position model"""
    __tablename__ = "positions"

    position_id = Column(Integer, primary_key=True, index=True)
    position_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    # Relationship to employees
    employees = relationship("Employee", back_populates="position")


class Employee(Base):
    """Employee model"""
    __tablename__ = "employees"

    emp_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.position_id"), nullable=False)

    # Relationship to position
    position = relationship("Position", back_populates="employees")