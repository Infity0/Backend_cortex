from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.token import TokenBalanceResponse, TokenHistoryItem
from app.services.token_service import TokenService

router = APIRouter()


@router.get("/balance", response_model=TokenBalanceResponse)
async def get_token_balance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user token balance"""
    service = TokenService(db)
    balance = await service.get_balance(user_id=current_user.id)
    return balance


@router.get("/history", response_model=List[TokenHistoryItem])
async def get_token_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get token usage history"""
    service = TokenService(db)
    history = await service.get_history(user_id=current_user.id)
    return history
