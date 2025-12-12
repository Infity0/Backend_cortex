from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse,
    VerifyEmailRequest, ForgotPasswordRequest, ResetPasswordRequest, RefreshTokenRequest
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    result = await service.register_user(
        email=request.email,
        password=request.password,
        username=request.username
    )
    return result


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    tokens = await service.login_user(
        email=request.email,
        password=request.password
    )
    return tokens


@router.post("/verify-email", response_model=dict)
async def verify_email(
    request: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    result = await service.verify_email(code=request.code)
    return result


@router.post("/forgot-password", response_model=dict)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    result = await service.forgot_password(email=request.email)
    return result


@router.post("/reset-password", response_model=dict)
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    result = await service.reset_password(
        token=request.token,
        new_password=request.new_password
    )
    return result


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    tokens = await service.refresh_token(refresh_token=request.refresh_token)
    return tokens


@router.post("/logout", response_model=dict)
async def logout():
    return {"message": "Successfully logged out"}
