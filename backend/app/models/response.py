from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Response(Base):
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("attempts.id"), nullable=False)
    question_id = Column(Integer, nullable=False)  # No FK - questions from API
    user_answer = Column(String, nullable=False)
    confidence_level = Column(Float, nullable=False)  # 0-100
    is_correct = Column(Boolean, nullable=False)
    time_spent = Column(Integer, default=0)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Question metadata (stored for analysis since questions come from external API)
    question_text = Column(Text, nullable=True)
    category = Column(String, nullable=True, default="General")
    difficulty = Column(String, nullable=True, default="medium")
    
    # Relationships
    attempt = relationship("Attempt", back_populates="responses")
