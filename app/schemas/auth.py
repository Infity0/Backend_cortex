from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class RegisterRequest(BaseModel):
    """Registration request schema"""
    email: EmailStr
    password: str
    username: Optional[str] = None
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if v is not None and len(v) < 2:
            raise ValueError('Username must be at least 2 characters long')
        return v


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class VerifyEmailRequest(BaseModel):
    """Email verification request"""
    code: str = Field(..., min_length=6, max_length=6)


class ForgotPasswordRequest(BaseModel):
    """Forgot password request"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request"""
    token: str
    new_password: str = Field(..., min_length=8)


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str
