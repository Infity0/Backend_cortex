from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.gallery_service import GalleryService

router = APIRouter()


@router.get("/user")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = GalleryService(db)
    stats = await service.get_user_stats(user_id=current_user.id)
    return stats
