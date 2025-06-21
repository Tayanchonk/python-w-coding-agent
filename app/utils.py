"""
Utility functions for the Employee Management API
"""
import uuid
from typing import Union


def generate_uuid() -> str:
    """Generate a new UUID4 as string"""
    return str(uuid.uuid4())


def is_valid_uuid(uuid_string: Union[str, None]) -> bool:
    """Check if a string is a valid UUID"""
    if not uuid_string:
        return False
    try:
        uuid.UUID(uuid_string)
        return True
    except (ValueError, TypeError):
        return False


def validate_uuid(uuid_string: str) -> str:
    """Validate and return UUID string, raise ValueError if invalid"""
    if not is_valid_uuid(uuid_string):
        raise ValueError(f"Invalid UUID format: {uuid_string}")
    return uuid_string