"""
Database configuration and models for the infrastructure layer
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./employee_management.db"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


class UserModel(Base):
    """SQLAlchemy User model"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)


class PositionModel(Base):
    """SQLAlchemy Position model"""
    __tablename__ = "positions"

    position_id = Column(Integer, primary_key=True, index=True)
    position_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    # Relationship to employees
    employees = relationship("EmployeeModel", back_populates="position")


class EmployeeModel(Base):
    """SQLAlchemy Employee model"""
    __tablename__ = "employees"

    emp_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.position_id"), nullable=False)

    # Relationship to position
    position = relationship("PositionModel", back_populates="employees")


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()