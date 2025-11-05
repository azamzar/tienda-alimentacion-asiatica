from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.refresh_token import TokenResponse, RefreshTokenRequest
from app.services.auth_service import AuthService
from app.models.user import User
from app.core.rate_limiter import rate_limiter
from app.config.settings import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user

    - **email**: Valid email address (must be unique)
    - **password**: Password (minimum 6 characters)
    - **full_name**: Optional full name

    Returns the created user (without password)

    Rate Limit: 3 requests per hour
    """
    # Rate limiting: 3 registros por hora
    client_ip = rate_limiter.get_client_ip(request)
    endpoint = f"{request.method}:{request.url.path}"

    if rate_limiter.is_rate_limited(
        client_ip, endpoint, settings.RATE_LIMIT_REGISTER_PER_HOUR, 3600
    ):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Demasiados intentos de registro. Límite: {settings.RATE_LIMIT_REGISTER_PER_HOUR} por hora.",
            headers={
                "Retry-After": "3600",
                "X-RateLimit-Limit": str(settings.RATE_LIMIT_REGISTER_PER_HOUR),
                "X-RateLimit-Window": "3600"
            }
        )

    auth_service = AuthService(db)
    return auth_service.register(user_data)


@router.post("/login", response_model=TokenResponse)
def login(
    request: Request,
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password

    - **email**: User email
    - **password**: User password

    Returns JWT access token and refresh token

    Rate Limit: 5 requests per minute
    """
    # Rate limiting: 5 intentos de login por minuto
    client_ip = rate_limiter.get_client_ip(request)
    endpoint = f"{request.method}:{request.url.path}"

    if rate_limiter.is_rate_limited(
        client_ip, endpoint, settings.RATE_LIMIT_AUTH_PER_MINUTE, 60
    ):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Demasiados intentos de login. Límite: {settings.RATE_LIMIT_AUTH_PER_MINUTE} por minuto.",
            headers={
                "Retry-After": "60",
                "X-RateLimit-Limit": str(settings.RATE_LIMIT_AUTH_PER_MINUTE),
                "X-RateLimit-Window": "60"
            }
        )

    auth_service = AuthService(db)
    return auth_service.login(user_credentials.email, user_credentials.password)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information

    Requires: Bearer token in Authorization header

    Returns current user details
    """
    return UserResponse.model_validate(current_user)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token

    - **refresh_token**: Valid refresh token

    Returns new access token and refresh token (token rotation)
    """
    auth_service = AuthService(db)
    return auth_service.refresh_access_token(refresh_request.refresh_token)


@router.post("/logout")
def logout(
    refresh_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Logout endpoint - revokes the refresh token

    - **refresh_token**: Refresh token to revoke

    Client should also delete tokens from storage
    """
    auth_service = AuthService(db)
    success = auth_service.logout(refresh_request.refresh_token)

    if success:
        return {"message": "Logout exitoso. Token revocado."}
    else:
        return {"message": "Token no encontrado o ya revocado."}


@router.post("/logout-all")
def logout_all_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout from all sessions - revokes all user's refresh tokens

    Requires: Bearer token in Authorization header

    Useful for security purposes (e.g., password changed, account compromised)
    """
    auth_service = AuthService(db)
    count = auth_service.logout_all_sessions(current_user.id)

    return {"message": f"Logout exitoso. {count} sesiones cerradas."}
