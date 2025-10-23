from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.services.auth_service import AuthService


def get_db() -> Generator:
    """
    Dependency function that yields a database session.
    The session is automatically closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Configuración de seguridad HTTP Bearer
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token

    Args:
        credentials: HTTP Bearer credentials with JWT token
        db: Database session

    Returns:
        Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials

    # Decodificar token
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extraer user_id del token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Obtener usuario de la base de datos
    auth_service = AuthService(db)
    user = auth_service.get_user_by_id(int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    return user


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to verify current user is an admin

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if they are admin

    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )

    return current_user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to optionally get current user (doesn't raise exception if no token)

    Args:
        credentials: HTTP Bearer credentials (optional)
        db: Database session

    Returns:
        Current user if authenticated, None otherwise
    """
    if not credentials:
        return None

    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None
