from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AttemptBase(BaseModel):
    student_name: str = Field(..., min_length=1, max_length=100)

class AttemptCreate(AttemptBase):
    pass

class AttemptResponse(AttemptBase):
    id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_questions: int = 0
    correct_answers: int = 0
    average_confidence: float = 0.0
    curiosity_score: float = 0.0
    
    class Config:
        from_attributes = True
