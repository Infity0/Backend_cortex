from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    username: Optional[str] = Field(None, min_length=2, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=100)


class UserPasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    id: int
    username: Optional[str]
    avatar_url: Optional[str]
    email_verified: bool
    created_at: datetime
    token_balance: int
    is_active: bool
    
    class Config:
        from_attributes = True


class UserProfile(UserResponse):
    pass
