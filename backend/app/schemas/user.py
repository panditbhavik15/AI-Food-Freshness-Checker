"""
User / Authentication Pydantic schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """Registration request payload."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: Optional[str] = Field(None, max_length=100)


class UserLoginRequest(BaseModel):
    """Login request payload."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token pair returned on login/register."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    """Public user profile."""
    id: str
    email: str
    display_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
