from pydantic import BaseModel
from datetime import datetime


class RefreshTokenBase(BaseModel):
    """Base schema for refresh token"""
    pass


class RefreshTokenCreate(RefreshTokenBase):
    """Schema for creating a refresh token"""
    token: str
    user_id: int
    expires_at: datetime


class RefreshTokenResponse(RefreshTokenBase):
    """Schema for refresh token response"""
    id: int
    token: str
    user_id: int
    is_revoked: bool
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for token response (login/refresh)"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str
