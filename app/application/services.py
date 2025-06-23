"""
Authentication service for handling auth-related business logic
"""
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.domain.entities import User
from app.domain.interfaces import UserRepositoryInterface


class AuthenticationService:
    """Service for handling authentication operations"""

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7
    ):
        self.user_repository = user_repository
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str, token_type: str = "access") -> Optional[str]:
        """Verify JWT token and return username if valid"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            token_type_claim: str = payload.get("type")
            
            if username is None or token_type_claim != token_type:
                return None
            return username
        except JWTError:
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = self.user_repository.get_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        return user

    def register_user(self, username: str, email: str, password: str) -> User:
        """Register a new user"""
        # Check if user already exists
        if self.user_repository.get_by_username(username):
            raise ValueError("Username already registered")
        if self.user_repository.get_by_email(email):
            raise ValueError("Email already registered")
        
        # Create new user with hashed password
        hashed_password = self.get_password_hash(password)
        user = User(
            user_id=None,
            username=username,
            email=email,
            password=hashed_password
        )
        return self.user_repository.create(user)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.user_repository.get_by_username(username)