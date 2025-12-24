from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class DifficultyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class QuestionType(str, enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False, default=QuestionType.MULTIPLE_CHOICE)
    difficulty = Column(String, nullable=False, default=DifficultyLevel.BEGINNER)
    category = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    explanation = Column(Text)
