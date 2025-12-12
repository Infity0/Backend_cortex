from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.subscription import (
    SubscriptionPlanResponse, SubscriptionResponse,
    SubscribeRequest, CancelSubscriptionRequest
)
from app.services.subscription_service import SubscriptionService

router = APIRouter()


@router.get("/plans", response_model=List[SubscriptionPlanResponse])
async def get_plans(db: AsyncSession = Depends(get_db)):
    service = SubscriptionService(db)
    plans = await service.get_all_plans()
    return plans


@router.get("/current", response_model=SubscriptionResponse)
async def get_current_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = SubscriptionService(db)
    subscription = await service.get_current_subscription(user_id=current_user.id)
    return subscription


@router.post("/subscribe", response_model=dict)
async def subscribe(
    request: SubscribeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = SubscriptionService(db)
    result = await service.create_subscription(
        user_id=current_user.id,
        plan_id=request.plan_id,
        payment_method=request.payment_method
    )
    return result


@router.post("/cancel", response_model=dict)
async def cancel_subscription(
    request: CancelSubscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = SubscriptionService(db)
    result = await service.cancel_subscription(
        user_id=current_user.id,
        reason=request.reason
    )
    return result
