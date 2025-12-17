from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question import QuestionCreate
from typing import List, Optional
import random

def get_question(db: Session, question_id: int) -> Optional[Question]:
    """Get a single question by ID"""
    return db.query(Question).filter(Question.id == question_id).first()

def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
    """Get all questions"""
    return db.query(Question).offset(skip).limit(limit).all()

def get_questions_by_category(db: Session, category: str) -> List[Question]:
    """Get questions by category"""
    return db.query(Question).filter(Question.category == category).all()

def get_random_questions(db: Session, limit: int = 10, category: Optional[str] = None) -> List[Question]:
    """Get random questions, optionally filtered by category"""
    query = db.query(Question)
    if category:
        query = query.filter(Question.category == category)
    
    all_questions = query.all()
    if len(all_questions) <= limit:
        return all_questions
    
    return random.sample(all_questions, limit)

def create_question(db: Session, question: QuestionCreate) -> Question:
    """Create a new question"""
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_categories(db: Session) -> List[str]:
    """Get all unique categories"""
    categories = db.query(Question.category).distinct().all()
    return [cat[0] for cat in categories]
