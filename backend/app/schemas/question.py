from pydantic import BaseModel, Field
from typing import Optional

class QuestionBase(BaseModel):
    text: str
    question_type: str = "multiple_choice"
    difficulty: str = "beginner"
    category: str
    correct_answer: str
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    explanation: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    
    class Config:
        from_attributes = True

class QuestionPublic(BaseModel):
    """Public question - includes correct answer for live API questions"""
    id: int
    text: str
    question_type: str
    difficulty: str
    category: str
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_answer: Optional[str] = None  # Included for API questions validation
    
    class Config:
        from_attributes = True
