from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ResponseBase(BaseModel):
    user_answer: str
    confidence_level: float = Field(..., ge=0, le=100)
    time_spent: int = Field(default=0, ge=0)

class ResponseCreate(ResponseBase):
    attempt_id: int
    question_id: int
    correct_answer: Optional[str] = None  # For API questions validation
    # Question metadata for analysis
    question_text: Optional[str] = None
    category: Optional[str] = "General"
    difficulty: Optional[str] = "medium"

class ResponseResponse(ResponseBase):
    id: int
    attempt_id: int
    question_id: int
    is_correct: bool
    created_at: datetime
    question_text: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    
    class Config:
        from_attributes = True
