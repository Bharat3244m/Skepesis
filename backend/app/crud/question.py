import random
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.question import Question
from app.schemas.question import QuestionCreate
from app.logger import get_logger
from typing import List, Optional

logger = get_logger(__name__)


class QuestionCRUDError(Exception):
    """Custom exception for Question CRUD operations"""
    pass


def get_question(db: Session, question_id: int) -> Optional[Question]:
    """Get a single question by ID"""
    try:
        return db.query(Question).filter(Question.id == question_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching question {question_id}: {e}")
        raise QuestionCRUDError(f"Failed to fetch question: {e}") from e


def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
    """Get all questions"""
    try:
        return db.query(Question).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching questions: {e}")
        raise QuestionCRUDError(f"Failed to fetch questions: {e}") from e


def get_questions_by_category(db: Session, category: str) -> List[Question]:
    """Get questions by category"""
    try:
        return db.query(Question).filter(Question.category == category).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching questions for category {category}: {e}")
        raise QuestionCRUDError(f"Failed to fetch questions by category: {e}") from e


def get_random_questions(db: Session, limit: int = 10, category: Optional[str] = None) -> List[Question]:
    """Get random questions, optionally filtered by category"""
    try:
        query = db.query(Question)
        if category:
            query = query.filter(Question.category == category)
        
        all_questions = query.all()
        if len(all_questions) <= limit:
            return all_questions
        
        return random.sample(all_questions, limit)
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching random questions: {e}")
        raise QuestionCRUDError(f"Failed to fetch random questions: {e}") from e


def create_question(db: Session, question: QuestionCreate) -> Question:
    """Create a new question"""
    try:
        db_question = Question(**question.model_dump())
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating question: {e}")
        raise QuestionCRUDError(f"Failed to create question: {e}") from e


def get_categories(db: Session) -> List[str]:
    """Get all unique categories"""
    try:
        categories = db.query(Question.category).distinct().all()
        return [cat[0] for cat in categories]
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching categories: {e}")
        raise QuestionCRUDError(f"Failed to fetch categories: {e}") from e
