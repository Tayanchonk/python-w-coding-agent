"""
Authentication controller for handling auth-related endpoints
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.domain.entities import User
from app.application.services import AuthenticationService
from app.infrastructure.database import get_db
from app.infrastructure.repositories import SqlAlchemyUserRepository
from app.presentation.models import UserCreateRequest, UserResponse, LoginRequest, Token

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

router = APIRouter()
security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_db)) -> AuthenticationService:
    """Dependency to get authentication service"""
    user_repository = SqlAlchemyUserRepository(db)
    return AuthenticationService(
        user_repository=user_repository,
        secret_key=SECRET_KEY,
        access_token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days=REFRESH_TOKEN_EXPIRE_DAYS
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> User:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = auth_service.verify_token(credentials.credentials, "access")
    if username is None:
        raise credentials_exception
    
    user = auth_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/register", response_model=UserResponse, summary="Register a new user")
async def register(
    user_data: UserCreateRequest,
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """
    Register a new user with username, email, and password.
    
    - **username**: Unique username
    - **email**: Unique email address
    - **password**: Password for the account
    """
    try:
        user = auth_service.register_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        return UserResponse(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token, summary="Login and get tokens")
async def login(
    login_data: LoginRequest,
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """
    Login with username and password to get access and refresh tokens.
    
    - **username**: Your username
    - **password**: Your password
    """
    user = auth_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = auth_service.create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token, summary="Refresh access token")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """
    Refresh access token using a valid refresh token.
    
    - **Authorization**: Bearer {refresh_token}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = auth_service.verify_token(credentials.credentials, "refresh")
    if username is None:
        raise credentials_exception
    
    user = auth_service.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = auth_service.create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )