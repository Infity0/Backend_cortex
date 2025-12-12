from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Transaction(Base):
    """Transactions/Payments model"""
    __tablename__ = "TRANSACTIONS"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    User_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    SUBSCRIPTIONS_id = Column(Integer, ForeignKey("SUBSCRIPTIONS.id", ondelete="SET NULL"), nullable=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=True)
    date = Column(DateTime, server_default=func.now())
    
    # Payment status
    status = Column(String(20), default='pending')  # pending, succeeded, failed
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    subscription = relationship("Subscription", back_populates="transactions")
