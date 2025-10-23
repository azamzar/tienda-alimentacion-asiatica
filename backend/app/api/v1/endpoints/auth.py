from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user

    - **email**: Valid email address (must be unique)
    - **password**: Password (minimum 6 characters)
    - **full_name**: Optional full name

    Returns the created user (without password)
    """
    auth_service = AuthService(db)
    return auth_service.register(user_data)


@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password

    - **email**: User email
    - **password**: User password

    Returns JWT access token
    """
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


@router.post("/logout")
def logout():
    """
    Logout endpoint (client-side token deletion)

    Since we're using JWT tokens (stateless), the actual logout
    happens on the client side by deleting the token.

    This endpoint is here for completeness and future implementations
    (like token blacklisting)
    """
    return {"message": "Logout exitoso. Elimina el token del cliente."}
