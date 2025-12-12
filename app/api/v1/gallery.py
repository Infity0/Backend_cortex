from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.gallery import ImageResponse, GallerySearchRequest
from app.services.gallery_service import GalleryService

router = APIRouter()


@router.get("", response_model=List[ImageResponse])
async def get_gallery(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user gallery images"""
    service = GalleryService(db)
    images = await service.get_gallery(
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )
    return images


@router.get("/favorites", response_model=List[ImageResponse])
async def get_favorites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get favorite images"""
    service = GalleryService(db)
    favorites = await service.get_favorites(user_id=current_user.id)
    return favorites


@router.post("/{image_id}/favorite", response_model=dict)
async def add_to_favorites(
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add image to favorites"""
    service = GalleryService(db)
    result = await service.add_to_favorites(
        image_id=image_id,
        user_id=current_user.id
    )
    return result


@router.delete("/{image_id}/favorite", response_model=dict)
async def remove_from_favorites(
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove image from favorites"""
    service = GalleryService(db)
    result = await service.remove_from_favorites(
        image_id=image_id,
        user_id=current_user.id
    )
    return result


@router.delete("/{image_id}", response_model=dict)
async def delete_image(
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete image"""
    service = GalleryService(db)
    result = await service.delete_image(
        image_id=image_id,
        user_id=current_user.id
    )
    return result


@router.get("/search", response_model=List[ImageResponse])
async def search_gallery(
    query: Optional[str] = Query(None),
    style: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search in gallery"""
    service = GalleryService(db)
    results = await service.search(
        user_id=current_user.id,
        query=query,
        style=style
    )
    return results
