from typing import Optional
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse, Token
from app.repositories.user_repository import UserRepository
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


class AuthService:
    """Service for authentication and user management"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def register(self, user_data: UserCreate) -> UserResponse:
        """
        Register a new user

        Args:
            user_data: User registration data

        Returns:
            Created user

        Raises:
            HTTPException: If email already exists
        """
        # Verificar si el email ya existe
        if self.repository.email_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )

        # Hashear la contraseña
        hashed_password = get_password_hash(user_data.password)

        # Crear usuario
        user_dict = {
            "email": user_data.email,
            "hashed_password": hashed_password,
            "full_name": user_data.full_name,
            "role": UserRole.CUSTOMER,  # Por defecto todos son clientes
            "is_active": True
        }

        user = self.repository.create(user_dict)
        return UserResponse.model_validate(user)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password

        Args:
            email: User email
            password: Plain password

        Returns:
            User if credentials are valid, None otherwise
        """
        user = self.repository.get_by_email(email)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        return user

    def login(self, email: str, password: str) -> Token:
        """
        Login user and generate JWT token

        Args:
            email: User email
            password: Plain password

        Returns:
            JWT token

        Raises:
            HTTPException: If credentials are invalid
        """
        user = self.authenticate(email, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Crear token con datos del usuario
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": str(user.id),  # "sub" es el estándar JWT para user_id
                "email": user.email,
                "role": user.role.value
            },
            expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID

        Args:
            user_id: User ID

        Returns:
            User if found, None otherwise
        """
        return self.repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email

        Args:
            email: User email

        Returns:
            User if found, None otherwise
        """
        return self.repository.get_by_email(email)
