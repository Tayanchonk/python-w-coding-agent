"""
Legacy database models - now using the new UUID-based models
"""
# Import new models for backward compatibility
from app.infrastructure.database.models import UserModel as User, PositionModel as Position, EmployeeModel as Employee

# Keep the old import names for backward compatibility
__all__ = ['User', 'Position', 'Employee']