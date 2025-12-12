from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ImageResponse(BaseModel):
    id: int
    image_url: str
    thumbnail_url: Optional[str]
    prompt: str
    style: str
    is_favorite: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class GallerySearchRequest(BaseModel):
    query: Optional[str] = None
    style: Optional[str] = None
    favorites_only: bool = False
    limit: int = 20
    offset: int = 0
