from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Request(Base):
    """Image generation requests model"""
    __tablename__ = "REQUESTS"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    User_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    request_type = Column(String(50), nullable=True)  # colorization, style, generation
    input_text = Column(String(500), nullable=True)  # prompt
    input_image_url = Column(String(255), nullable=True)
    tokens_used = Column(Integer, nullable=True)
    status = Column(
        Enum('pending', 'processing', 'completed', 'failed', name='request_status'),
        default='pending'
    )
    created_at = Column(DateTime, server_default=func.now())
    
    # Generation parameters
    style = Column(String(50), nullable=True)  # realistic, anime, painting, etc.
    resolution = Column(String(20), nullable=True)  # 1024x1024
    
    # Error info
    error_message = Column(String(500), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="requests")
    images = relationship("Image", back_populates="request", cascade="all, delete-orphan")
