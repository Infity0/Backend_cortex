from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.generate import (
    GenerateImageRequest, GenerationStatusResponse, GenerationHistoryItem
)
from app.services.generate_service import GenerateService

router = APIRouter()


@router.post("/image", response_model=dict)
async def create_generation(
    request: GenerateImageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new image generation request"""
    service = GenerateService(db)
    result = await service.create_generation(
        user_id=current_user.id,
        prompt=request.prompt,
        style=request.style,
        request_type=request.request_type
    )
    return result


@router.get("/status/{generation_id}", response_model=GenerationStatusResponse)
async def get_generation_status(
    generation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get generation status"""
    service = GenerateService(db)
    status = await service.get_status(
        generation_id=generation_id,
        user_id=current_user.id
    )
    return status


@router.delete("/{generation_id}", response_model=dict)
async def delete_generation(
    generation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete generation"""
    service = GenerateService(db)
    result = await service.delete_generation(
        generation_id=generation_id,
        user_id=current_user.id
    )
    return result


@router.get("/history", response_model=List[GenerationHistoryItem])
async def get_generation_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get generation history"""
    service = GenerateService(db)
    history = await service.get_history(user_id=current_user.id)
    return history
