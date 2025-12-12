import random
import string
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from app.services.email_service import EmailService


class AuthService:
    """Authentication service"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.email_service = EmailService()
    
    async def register_user(self, email: str, password: str, username: Optional[str] = None):
        """Register new user"""
        # Check if user exists
        result = await self.db.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        # Generate verification code
        verification_code = ''.join(random.choices(string.digits, k=6))
        
        # Create user
        new_user = User(
            email=email,
            password_hash=get_password_hash(password),
            username=username,
            verification_code=verification_code,
            verification_code_expires=datetime.utcnow() + timedelta(hours=24),
            token_balance=0  # Will get tokens after subscription
        )
        
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        
        # Send verification email
        await self.email_service.send_verification_email(email, verification_code)
        
        return {
            "message": "User registered successfully. Please check your email for verification code.",
            "user_id": new_user.id
        }
    
    async def login_user(self, email: str, password: str):
        """Login user"""
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Create tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    async def verify_email(self, code: str):
        """Verify user email"""
        result = await self.db.execute(
            select(User).where(
                User.verification_code == code,
                User.verification_code_expires > datetime.utcnow()
            )
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification code"
            )
        
        user.email_verified = True
        user.verification_code = None
        user.verification_code_expires = None
        
        await self.db.commit()
        
        return {"message": "Email verified successfully"}
    
    async def forgot_password(self, email: str):
        """Send password reset email"""
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user:
            # Don't reveal if email exists
            return {"message": "If the email exists, a reset link has been sent"}
        
        # Generate reset token
        reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        user.reset_token = reset_token
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        
        await self.db.commit()
        
        # Send reset email
        await self.email_service.send_password_reset_email(email, reset_token)
        
        return {"message": "If the email exists, a reset link has been sent"}
    
    async def reset_password(self, token: str, new_password: str):
        """Reset password with token"""
        result = await self.db.execute(
            select(User).where(
                User.reset_token == token,
                User.reset_token_expires > datetime.utcnow()
            )
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        user.password_hash = get_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        
        await self.db.commit()
        
        return {"message": "Password reset successfully"}
    
    async def refresh_token(self, refresh_token: str):
        """Refresh access token"""
        payload = decode_token(refresh_token)
        
        if payload is None or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new tokens
        access_token = create_access_token(data={"sub": user_id})
        new_refresh_token = create_refresh_token(data={"sub": user_id})
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
