from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from app.models.user import UserRole


# Schema base con campos comunes
class UserBase(BaseModel):
    """Base User schema with common fields"""
    email: EmailStr
    full_name: Optional[str] = None


# Schema para crear usuario (registro)
class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")


# Schema para actualizar usuario
class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)
    is_active: Optional[bool] = None


# Schema para respuesta (sin password)
class UserResponse(UserBase):
    """Schema for user response (without password)"""
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Antes era orm_mode en Pydantic v1


# Schema para login
class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


# Schema para token de autenticación
class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"


# Schema para datos dentro del token
class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
