from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Image(Base):
    __tablename__ = "IMAGES"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    User_id = Column(Integer, ForeignKey("User.id", ondelete="CASCADE"), nullable=False)
    REQUESTS_id = Column(Integer, ForeignKey("REQUESTS.id", ondelete="SET NULL"), nullable=True)
    image_url = Column(String(255), nullable=False)
    original_url = Column(String(255), nullable=True) 
    created_at = Column(DateTime, server_default=func.now())
    
    is_favorite = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="images")
    request = relationship("Request", back_populates="images")
