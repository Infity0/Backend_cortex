from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class SubscriptionPlan(Base):
    """Subscription plans model"""
    __tablename__ = "SUBSCRIPTION_PLANS"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    tokens_included = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    note = Column(String(255), nullable=True)
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    """User subscriptions model"""
    __tablename__ = "SUBSCRIPTIONS"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    User_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    SUBSCRIPTION_PLANS_id = Column(Integer, ForeignKey("SUBSCRIPTION_PLANS.id"), nullable=False)
    start_date = Column(DateTime, nullable=False, server_default=func.now())
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum('active', 'inactive', 'cancelled', name='subscription_status'), default='active')
    created_at = Column(DateTime, server_default=func.now())
    
    # Auto-renewal
    auto_renew = Column(Integer, default=1)  # 1 = True, 0 = False (MySQL compatibility)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")
    transactions = relationship("Transaction", back_populates="subscription")
