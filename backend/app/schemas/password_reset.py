"""
Password Reset schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field


class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr = Field(..., description="User email address")


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""
    token: str = Field(..., min_length=1, description="Password reset token")
    new_password: str = Field(..., min_length=6, description="New password (min 6 characters)")


class PasswordResetResponse(BaseModel):
    """Schema for password reset response"""
    message: str = Field(..., description="Response message")
