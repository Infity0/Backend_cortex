from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subscription import SubscriptionPlan, Subscription
from app.models.user import User
from app.models.transaction import Transaction


class SubscriptionService:
    """Subscription service"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_plans(self) -> List[SubscriptionPlan]:
        """Get all subscription plans"""
        result = await self.db.execute(select(SubscriptionPlan))
        plans = result.scalars().all()
        return list(plans)
    
    async def get_current_subscription(self, user_id: int):
        """Get current active subscription"""
        result = await self.db.execute(
            select(Subscription, SubscriptionPlan, User)
            .join(SubscriptionPlan, Subscription.SUBSCRIPTION_PLANS_id == SubscriptionPlan.id)
            .join(User, Subscription.User_id == User.id)
            .where(
                Subscription.User_id == user_id,
                Subscription.status == 'active',
                Subscription.end_date > datetime.utcnow()
            )
            .order_by(Subscription.end_date.desc())
        )
        row = result.first()
        
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active subscription found"
            )
        
        subscription, plan, user = row
        
        return {
            "id": subscription.id,
            "plan_name": plan.name,
            "status": subscription.status,
            "start_date": subscription.start_date,
            "end_date": subscription.end_date,
            "auto_renew": bool(subscription.auto_renew),
            "tokens_total": plan.tokens_included,
            "tokens_remaining": user.token_balance
        }
    
    async def create_subscription(self, user_id: int, plan_id: int, payment_method: str):
        """Create new subscription"""
        # Get plan
        result = await self.db.execute(select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id))
        plan = result.scalar_one_or_none()
        
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription plan not found"
            )
        
        # Get user
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check for existing active subscription
        result = await self.db.execute(
            select(Subscription).where(
                Subscription.User_id == user_id,
                Subscription.status == 'active',
                Subscription.end_date > datetime.utcnow()
            )
        )
        existing_sub = result.scalar_one_or_none()
        
        if existing_sub:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already has an active subscription"
            )
        
        # Create subscription
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=plan.duration_days)
        
        new_subscription = Subscription(
            User_id=user_id,
            SUBSCRIPTION_PLANS_id=plan_id,
            start_date=start_date,
            end_date=end_date,
            status='active',
            auto_renew=1
        )
        
        self.db.add(new_subscription)
        await self.db.flush()
        
        # Create transaction (mock payment)
        transaction = Transaction(
            User_id=user_id,
            SUBSCRIPTIONS_id=new_subscription.id,
            amount=plan.price,
            payment_method=payment_method,
            status='succeeded'
        )
        
        self.db.add(transaction)
        
        # Update user tokens
        user.token_balance = plan.tokens_included
        
        await self.db.commit()
        
        return {
            "message": "Subscription created successfully",
            "subscription_id": new_subscription.id,
            "tokens_added": plan.tokens_included
        }
    
    async def cancel_subscription(self, user_id: int, reason: Optional[str] = None):
        """Cancel subscription"""
        result = await self.db.execute(
            select(Subscription).where(
                Subscription.User_id == user_id,
                Subscription.status == 'active'
            ).order_by(Subscription.end_date.desc())
        )
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active subscription found"
            )
        
        # Disable auto-renewal
        subscription.auto_renew = 0
        subscription.status = 'cancelled'
        
        await self.db.commit()
        
        return {
            "message": "Subscription cancelled. Access will remain until the end of the billing period.",
            "end_date": subscription.end_date
        }
