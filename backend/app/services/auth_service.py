from typing import Optional
from datetime import timedelta, datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import secrets

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse
from app.schemas.refresh_token import TokenResponse, RefreshTokenRequest
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.password_reset_token_repository import PasswordResetTokenRepository
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_refresh_token
)
from app.config.settings import settings
from app.utils.email_service import email_service


class AuthService:
    """Service for authentication and user management"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
        self.refresh_token_repository = RefreshTokenRepository(db)
        self.password_reset_repository = PasswordResetTokenRepository(db)

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

        # Send welcome email
        try:
            email_service.send_welcome_email(
                to_email=user.email,
                user_name=user.full_name or user.email.split("@")[0]
            )
        except Exception as e:
            # Log error but don't fail the registration
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")

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

    def login(self, email: str, password: str) -> TokenResponse:
        """
        Login user and generate JWT tokens (access + refresh)

        Args:
            email: User email
            password: Plain password

        Returns:
            TokenResponse with access_token and refresh_token

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

        # Crear access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.value
            },
            expires_delta=access_token_expires
        )

        # Crear refresh token
        refresh_token = create_refresh_token(
            data={
                "sub": str(user.id),
                "email": user.email
            }
        )

        # Guardar refresh token en la base de datos
        refresh_token_expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self.refresh_token_repository.create_refresh_token(
            token=refresh_token,
            user_id=user.id,
            expires_at=refresh_token_expires
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

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

    def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """
        Genera un nuevo access token usando un refresh token válido

        Args:
            refresh_token: Refresh token JWT

        Returns:
            TokenResponse con nuevo access_token y refresh_token

        Raises:
            HTTPException: Si el refresh token es inválido o expirado
        """
        # Decodificar y validar el refresh token
        payload = decode_refresh_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verificar que el token existe en la base de datos y es válido
        db_token = self.refresh_token_repository.get_by_token(refresh_token)
        if not db_token or not db_token.is_valid():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido o revocado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Obtener usuario
        user_id = int(payload.get("sub"))
        user = self.repository.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o inactivo",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Revocar el refresh token antiguo (rotación de tokens)
        self.refresh_token_repository.revoke_token(refresh_token)

        # Crear nuevo access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.value
            },
            expires_delta=access_token_expires
        )

        # Crear nuevo refresh token
        new_refresh_token = create_refresh_token(
            data={
                "sub": str(user.id),
                "email": user.email
            }
        )

        # Guardar nuevo refresh token en la base de datos
        refresh_token_expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self.refresh_token_repository.create_refresh_token(
            token=new_refresh_token,
            user_id=user.id,
            expires_at=refresh_token_expires
        )

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

    def logout(self, refresh_token: str) -> bool:
        """
        Revoca un refresh token (logout de una sesión específica)

        Args:
            refresh_token: Refresh token a revocar

        Returns:
            True si se revocó exitosamente
        """
        return self.refresh_token_repository.revoke_token(refresh_token)

    def logout_all_sessions(self, user_id: int) -> int:
        """
        Revoca todos los refresh tokens de un usuario (logout de todas las sesiones)

        Args:
            user_id: ID del usuario

        Returns:
            Número de tokens revocados
        """
        return self.refresh_token_repository.revoke_all_user_tokens(user_id)

    def request_password_reset(self, email: str) -> bool:
        """
        Request password reset by email.
        Generates a token and sends email with reset link.

        Args:
            email: User email address

        Returns:
            True if request was processed (always returns True for security)

        Note:
            Always returns True even if email doesn't exist to prevent email enumeration
        """
        # Get user by email
        user = self.repository.get_by_email(email)

        # Si el usuario no existe, retornar True sin enviar email (seguridad)
        # Esto previene que atacantes puedan enumerar emails válidos
        if not user or not user.is_active:
            return True

        # Delete any existing tokens for this user
        self.password_reset_repository.delete_user_tokens(user.id)

        # Generate secure random token (32 bytes = 64 hex chars)
        reset_token = secrets.token_urlsafe(32)

        # Calculate expiration time
        expires_at = datetime.utcnow() + timedelta(
            minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
        )

        # Save token to database
        token_data = {
            "user_id": user.id,
            "token": reset_token,
            "expires_at": expires_at,
            "used": False
        }
        self.password_reset_repository.create(token_data)

        # Send password reset email
        email_service.send_password_reset_email(
            to_email=user.email,
            reset_token=reset_token,
            user_name=user.full_name
        )

        return True

    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Reset password using a valid token.

        Args:
            token: Password reset token
            new_password: New password (plain text)

        Returns:
            True if password was reset successfully

        Raises:
            HTTPException: If token is invalid, expired, or already used
        """
        # Get valid token from database
        reset_token = self.password_reset_repository.get_valid_token(token)

        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token de recuperación inválido o expirado"
            )

        # Get user
        user = self.repository.get_by_id(reset_token.user_id)

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        # Hash new password
        hashed_password = get_password_hash(new_password)

        # Update user password
        user.hashed_password = hashed_password
        self.db.commit()

        # Mark token as used
        self.password_reset_repository.mark_as_used(reset_token.id)

        # Revoke all refresh tokens (logout all sessions for security)
        self.refresh_token_repository.revoke_all_user_tokens(user.id)

        return True
