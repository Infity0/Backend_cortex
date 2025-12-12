from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.request import Request
from app.models.image import Image
from app.services.token_service import TokenService


class GenerateService:
    
    TOKEN_COSTS = {
        'colorization': 25,
        'style': 100,
        'generation': 350
    }
    
    ALLOWED_STYLES = ['realistic', 'anime', 'painting', 'cyberpunk', 'fantasy', 'abstract']
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.token_service = TokenService(db)
    
    async def create_generation(self, user_id: int, prompt: str, style: str, request_type: str):

        if style not in self.ALLOWED_STYLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid style. Allowed: {', '.join(self.ALLOWED_STYLES)}"
            )
        
        tokens_cost = self.TOKEN_COSTS.get(request_type, 350)
        
        success = await self.token_service.deduct_tokens(user_id, tokens_cost)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Insufficient tokens"
            )
        
        new_request = Request(
            User_id=user_id,
            request_type=request_type,
            input_text=prompt,
            tokens_used=tokens_cost,
            status='pending',
            style=style,
            resolution='1024x1024'
        )
        
        self.db.add(new_request)
        await self.db.commit()
        await self.db.refresh(new_request)
        
        new_request.status = 'processing'
        await self.db.commit()
        
        return {
            "message": "Generation request created",
            "request_id": new_request.id,
            "tokens_used": tokens_cost,
            "status": "processing"
        }
    
    async def get_status(self, generation_id: int, user_id: int):
        result = await self.db.execute(
            select(Request).where(
                Request.id == generation_id,
                Request.User_id == user_id
            )
        )
        request = result.scalar_one_or_none()
        
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Generation request not found"
            )
        
        image_url = None
        thumbnail_url = None
        if request.status == 'completed':
            result = await self.db.execute(
                select(Image).where(Image.REQUESTS_id == generation_id)
            )
            image = result.scalar_one_or_none()
            if image:
                image_url = image.image_url
                thumbnail_url = image.original_url
        
        return {
            "id": request.id,
            "status": request.status,
            "prompt": request.input_text,
            "style": request.style,
            "tokens_used": request.tokens_used,
            "image_url": image_url,
            "thumbnail_url": thumbnail_url,
            "error_message": request.error_message,
            "created_at": request.created_at
        }
    
    async def delete_generation(self, generation_id: int, user_id: int):
        result = await self.db.execute(
            select(Request).where(
                Request.id == generation_id,
                Request.User_id == user_id
            )
        )
        request = result.scalar_one_or_none()
        
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Generation request not found"
            )
        
        if request.status in ['failed', 'pending']:
            await self.token_service.refund_tokens(user_id, request.tokens_used)
        
        await self.db.delete(request)
        await self.db.commit()
        
        return {"message": "Generation deleted successfully"}
    
    async def get_history(self, user_id: int) -> List[dict]:
        result = await self.db.execute(
            select(Request)
            .where(Request.User_id == user_id)
            .order_by(Request.created_at.desc())
            .limit(50)
        )
        requests = result.scalars().all()
        
        history = []
        for req in requests:
            image_url = None
            if req.status == 'completed':
                img_result = await self.db.execute(
                    select(Image).where(Image.REQUESTS_id == req.id)
                )
                image = img_result.scalar_one_or_none()
                if image:
                    image_url = image.image_url
            
            history.append({
                "id": req.id,
                "prompt": req.input_text,
                "style": req.style,
                "status": req.status,
                "image_url": image_url,
                "tokens_cost": req.tokens_used,
                "created_at": req.created_at
            })
        
        return history
