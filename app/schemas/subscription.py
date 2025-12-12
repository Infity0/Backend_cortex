from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class SubscriptionPlanResponse(BaseModel):
    """Subscription plan response schema"""
    id: int
    name: str
    price: Decimal
    tokens_included: int
    duration_days: int
    description: Optional[str]
    note: Optional[str]
    
    class Config:
        from_attributes = True


class SubscriptionResponse(BaseModel):
    """Subscription response schema"""
    id: int
    plan_name: str
    status: str
    start_date: datetime
    end_date: datetime
    auto_renew: bool
    tokens_total: int
    tokens_remaining: int
    
    class Config:
        from_attributes = True


class SubscribeRequest(BaseModel):
    """Subscribe to plan request"""
    plan_id: int = Field(..., description="Subscription plan ID")
    payment_method: Optional[str] = Field("card", description="Payment method")


class CancelSubscriptionRequest(BaseModel):
    """Cancel subscription request"""
    reason: Optional[str] = Field(None, max_length=500)
