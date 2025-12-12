from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.request import Request


class TokenService:
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_balance(self, user_id: int):

        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            return {"balance": 0, "total_used": 0, "percentage_remaining": 0}

        result = await self.db.execute(
            select(func.sum(Request.tokens_used))
            .where(Request.User_id == user_id, Request.status == 'completed')
        )
        total_used = result.scalar() or 0

        balance = user.token_balance
        percentage = (balance / (balance + total_used) * 100) if (balance + total_used) > 0 else 0
        
        return {
            "balance": balance,
            "total_used": int(total_used),
            "percentage_remaining": round(percentage, 2)
        }
    
    async def get_history(self, user_id: int) -> List[dict]:
        result = await self.db.execute(
            select(Request)
            .where(Request.User_id == user_id, Request.tokens_used.isnot(None))
            .order_by(Request.created_at.desc())
            .limit(50)
        )
        requests = result.scalars().all()
        
        history = []
        for req in requests:
            history.append({
                "id": req.id,
                "request_type": req.request_type or 'generation',
                "tokens_used": req.tokens_used,
                "prompt": req.input_text or '',
                "created_at": req.created_at,
                "status": req.status
            })
        
        return history
    
    async def deduct_tokens(self, user_id: int, amount: int) -> bool:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            return False
        
        if user.token_balance < amount:
            return False
        
        user.token_balance -= amount
        await self.db.commit()
        
        return True
    
    async def refund_tokens(self, user_id: int, amount: int):
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user:
            user.token_balance += amount
            await self.db.commit()
