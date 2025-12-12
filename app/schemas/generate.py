from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GenerateImageRequest(BaseModel):
    """Generate image request schema"""
    prompt: str = Field(..., min_length=3, max_length=500, description="Text description")
    style: str = Field(..., description="Style: realistic, anime, painting, cyberpunk, fantasy, abstract")
    request_type: str = Field("generation", description="Type: colorization (25), style (100), generation (350)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "A futuristic city at sunset",
                "style": "cyberpunk",
                "request_type": "generation"
            }
        }


class GenerationStatusResponse(BaseModel):
    """Generation status response"""
    id: int
    status: str  # pending, processing, completed, failed
    prompt: str
    style: str
    tokens_used: int
    image_url: Optional[str]
    thumbnail_url: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class GenerationHistoryItem(BaseModel):
    """Generation history item"""
    id: int
    prompt: str
    style: str
    status: str
    image_url: Optional[str]
    tokens_cost: int
    created_at: datetime
    
    class Config:
        from_attributes = True
