from sqlalchemy.orm import Session
from app.models.attempt import Attempt
from app.schemas.attempt import AttemptCreate
from typing import List, Optional
from datetime import datetime

def get_attempt(db: Session, attempt_id: int) -> Optional[Attempt]:
    """Get a single attempt by ID"""
    return db.query(Attempt).filter(Attempt.id == attempt_id).first()

def get_attempts(db: Session, skip: int = 0, limit: int = 100) -> List[Attempt]:
    """Get all attempts"""
    return db.query(Attempt).order_by(Attempt.started_at.desc()).offset(skip).limit(limit).all()

def get_attempts_by_student(db: Session, student_name: str) -> List[Attempt]:
    """Get all attempts by a student"""
    return db.query(Attempt).filter(Attempt.student_name == student_name).order_by(Attempt.started_at.desc()).all()

def create_attempt(db: Session, attempt: AttemptCreate) -> Attempt:
    """Create a new attempt"""
    db_attempt = Attempt(**attempt.model_dump())
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt

def update_attempt_stats(db: Session, attempt_id: int) -> Optional[Attempt]:
    """Update attempt statistics based on responses"""
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

def complete_attempt(db: Session, attempt_id: int) -> Optional[Attempt]:
    """Mark attempt as completed"""
    attempt = get_attempt(db, attempt_id)
    if not attempt:
        return None
    
    attempt.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(attempt)
    return attempt
