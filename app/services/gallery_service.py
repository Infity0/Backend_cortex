from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.image import Image
from app.models.request import Request


class GalleryService:
    """Gallery service"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_gallery(self, user_id: int, limit: int = 20, offset: int = 0) -> List[dict]:
        """Get user gallery"""
        result = await self.db.execute(
            select(Image, Request)
            .join(Request, Image.REQUESTS_id == Request.id)
            .where(Image.User_id == user_id)
            .order_by(Image.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        rows = result.all()
        
        gallery = []
        for image, request in rows:
            gallery.append({
                "id": image.id,
                "image_url": image.image_url,
                "thumbnail_url": image.original_url,
                "prompt": request.input_text or '',
                "style": request.style or 'realistic',
                "is_favorite": image.is_favorite,
                "created_at": image.created_at
            })
        
        return gallery
    
    async def get_favorites(self, user_id: int) -> List[dict]:
        """Get favorite images"""
        result = await self.db.execute(
            select(Image, Request)
            .join(Request, Image.REQUESTS_id == Request.id)
            .where(
                Image.User_id == user_id,
                Image.is_favorite == True
            )
            .order_by(Image.created_at.desc())
        )
        rows = result.all()
        
        favorites = []
        for image, request in rows:
            favorites.append({
                "id": image.id,
                "image_url": image.image_url,
                "thumbnail_url": image.original_url,
                "prompt": request.input_text or '',
                "style": request.style or 'realistic',
                "is_favorite": True,
                "created_at": image.created_at
            })
        
        return favorites
    
    async def add_to_favorites(self, image_id: int, user_id: int):
        """Add image to favorites"""
        result = await self.db.execute(
            select(Image).where(
                Image.id == image_id,
                Image.User_id == user_id
            )
        )
        image = result.scalar_one_or_none()
        
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        
        image.is_favorite = True
        await self.db.commit()
        
        return {"message": "Added to favorites"}
    
    async def remove_from_favorites(self, image_id: int, user_id: int):
        """Remove image from favorites"""
        result = await self.db.execute(
            select(Image).where(
                Image.id == image_id,
                Image.User_id == user_id
            )
        )
        image = result.scalar_one_or_none()
        
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        
        image.is_favorite = False
        await self.db.commit()
        
        return {"message": "Removed from favorites"}
    
    async def delete_image(self, image_id: int, user_id: int):
        """Delete image"""
        result = await self.db.execute(
            select(Image).where(
                Image.id == image_id,
                Image.User_id == user_id
            )
        )
        image = result.scalar_one_or_none()
        
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        
        await self.db.delete(image)
        await self.db.commit()
        
        return {"message": "Image deleted successfully"}
    
    async def search(self, user_id: int, query: Optional[str] = None, style: Optional[str] = None) -> List[dict]:
        """Search in gallery"""
        conditions = [Image.User_id == user_id]
        
        if query:
            conditions.append(Request.input_text.like(f'%{query}%'))
        
        if style:
            conditions.append(Request.style == style)
        
        result = await self.db.execute(
            select(Image, Request)
            .join(Request, Image.REQUESTS_id == Request.id)
            .where(and_(*conditions))
            .order_by(Image.created_at.desc())
            .limit(50)
        )
        rows = result.all()
        
        results = []
        for image, request in rows:
            results.append({
                "id": image.id,
                "image_url": image.image_url,
                "thumbnail_url": image.original_url,
                "prompt": request.input_text or '',
                "style": request.style or 'realistic',
                "is_favorite": image.is_favorite,
                "created_at": image.created_at
            })
        
        return results
    
    async def get_user_stats(self, user_id: int):
        """Get user statistics"""
        # Total generations
        result = await self.db.execute(
            select(func.count(Request.id))
            .where(Request.User_id == user_id, Request.status == 'completed')
        )
        total_generations = result.scalar() or 0
        
        # Total tokens used
        result = await self.db.execute(
            select(func.sum(Request.tokens_used))
            .where(Request.User_id == user_id, Request.status == 'completed')
        )
        total_tokens_used = result.scalar() or 0
        
        # Style distribution
        result = await self.db.execute(
            select(Request.style, func.count(Request.id))
            .where(Request.User_id == user_id, Request.status == 'completed')
            .group_by(Request.style)
        )
        style_distribution = {row[0]: row[1] for row in result.all() if row[0]}
        
        # Favorite style
        favorite_style = max(style_distribution.items(), key=lambda x: x[1])[0] if style_distribution else None
        
        return {
            "total_generations": int(total_generations),
            "total_tokens_used": int(total_tokens_used),
            "favorite_style": favorite_style,
            "style_distribution": style_distribution
        }
