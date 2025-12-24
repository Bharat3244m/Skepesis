from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.attempt import Attempt
from app.schemas.attempt import AttemptCreate
from app.logger import get_logger
from typing import List, Optional
from datetime import datetime

logger = get_logger(__name__)


class AttemptCRUDError(Exception):
    """Custom exception for Attempt CRUD operations"""
    pass


def get_attempt(db: Session, attempt_id: int) -> Optional[Attempt]:
    """Get a single attempt by ID"""
    try:
        return db.query(Attempt).filter(Attempt.id == attempt_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching attempt {attempt_id}: {e}")
        raise AttemptCRUDError(f"Failed to fetch attempt: {e}") from e


def get_attempts(db: Session, skip: int = 0, limit: int = 100) -> List[Attempt]:
    """Get all attempts"""
    try:
        return db.query(Attempt).order_by(Attempt.started_at.desc()).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching attempts: {e}")
        raise AttemptCRUDError(f"Failed to fetch attempts: {e}") from e


def get_attempts_by_student(db: Session, student_name: str) -> List[Attempt]:
    """Get all attempts by a student"""
    try:
        return db.query(Attempt).filter(Attempt.student_name == student_name).order_by(Attempt.started_at.desc()).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching attempts for student {student_name}: {e}")
        raise AttemptCRUDError(f"Failed to fetch student attempts: {e}") from e


def create_attempt(db: Session, attempt: AttemptCreate) -> Attempt:
    """Create a new attempt"""
    try:
        db_attempt = Attempt(**attempt.model_dump())
        db.add(db_attempt)
        db.commit()
        db.refresh(db_attempt)
        return db_attempt
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating attempt: {e}")
        raise AttemptCRUDError(f"Failed to create attempt: {e}") from e


def update_attempt_stats(db: Session, attempt_id: int) -> Optional[Attempt]:
    """Update attempt statistics based on responses"""
    try:
        attempt = get_attempt(db, attempt_id)
        if not attempt:
            return None
        
        responses = attempt.responses
        if not responses:
            return attempt
        
        attempt.total_questions = len(responses)
        attempt.correct_answers = sum(1 for r in responses if r.is_correct)
        attempt.average_confidence = sum(r.confidence_level for r in responses) / len(responses)
        
        db.commit()
        db.refresh(attempt)
        return attempt
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating attempt stats for {attempt_id}: {e}")
        raise AttemptCRUDError(f"Failed to update attempt stats: {e}") from e


def complete_attempt(db: Session, attempt_id: int) -> Optional[Attempt]:
    """Mark attempt as completed"""
    try:
        attempt = get_attempt(db, attempt_id)
        if not attempt:
            return None
        
        attempt.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(attempt)
        return attempt
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error completing attempt {attempt_id}: {e}")
        raise AttemptCRUDError(f"Failed to complete attempt: {e}") from e
