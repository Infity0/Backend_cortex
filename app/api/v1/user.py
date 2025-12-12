from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserPasswordChange
from app.services.user_service import UserService

router = APIRouter()


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user profile"""
    return current_user


@router.patch("/profile", response_model=UserResponse)
async def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user profile"""
    service = UserService(db)
    updated_user = await service.update_profile(
        user_id=current_user.id,
        username=data.username
    )
    return updated_user


@router.post("/avatar", response_model=dict)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload user avatar"""
    service = UserService(db)
    result = await service.upload_avatar(
        user_id=current_user.id,
        file=file
    )
    return result


@router.patch("/password", response_model=dict)
async def change_password(
    data: UserPasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change user password"""
    service = UserService(db)
    result = await service.change_password(
        user_id=current_user.id,
        old_password=data.old_password,
        new_password=data.new_password
    )
    return result


@router.delete("/account", response_model=dict)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete user account"""
    service = UserService(db)
    result = await service.delete_account(user_id=current_user.id)
    return result
