"""
Seed database with initial data
Run: python -m scripts.seed_db
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_maker
from app.models.subscription import SubscriptionPlan


async def seed_subscription_plans():
    async with async_session_maker() as session:
        from sqlalchemy import select
        result = await session.execute(select(SubscriptionPlan))
        existing = result.scalars().first()
        
        if existing:
            print("Subscription plans already exist. Skipping...")
            return
        
        plans = [
            SubscriptionPlan(
                name="Sirdar",
                price=0.00,
                tokens_included=1000,
                duration_days=3,
                description="Trial plan",
                note="Free 3-day trial with 1000 tokens"
            ),
            SubscriptionPlan(
                name="Expert",
                price=1500.00,
                tokens_included=24000,
                duration_days=30,
                description="Advanced plan",
                note="1500 RUB/month with 24000 tokens"
            ),
            SubscriptionPlan(
                name="Lord",
                price=12000.00,
                tokens_included=999999,
                duration_days=365,
                description="Professional plan",
                note="12000 RUB/year with unlimited tokens"
            )
        ]
        
        session.add_all(plans)
        await session.commit()
        
        print("✓ Subscription plans created successfully!")


async def main():
    print("Seeding database...")
    await seed_subscription_plans()
    print("✓ Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(main())
