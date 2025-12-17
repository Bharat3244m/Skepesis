from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.attempt import AttemptResponse, AttemptCreate
from app.crud import attempt as crud
from app.services.curiosity import CuriosityAnalyzer

router = APIRouter(prefix="/api/attempts", tags=["attempts"])

@router.get("/", response_model=List[AttemptResponse])
def get_attempts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all attempts"""
    return crud.get_attempts(db, skip=skip, limit=limit)

@router.get("/{attempt_id}", response_model=AttemptResponse)
def get_attempt(attempt_id: int, db: Session = Depends(get_db)):
    """Get a specific attempt"""
    attempt = crud.get_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt

@router.post("/", response_model=AttemptResponse)
def create_attempt(attempt: AttemptCreate, db: Session = Depends(get_db)):
    """Start a new learning attempt"""
    return crud.create_attempt(db, attempt)

@router.post("/{attempt_id}/complete", response_model=AttemptResponse)
def complete_attempt(attempt_id: int, db: Session = Depends(get_db)):
    """Mark attempt as complete and calculate final scores"""
    # Update stats first
    attempt = crud.update_attempt_stats(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    # Calculate curiosity score
    responses = attempt.responses
    curiosity_score = CuriosityAnalyzer.calculate_curiosity_score(responses)
    attempt.curiosity_score = curiosity_score
    
    # Mark as completed
    attempt = crud.complete_attempt(db, attempt_id)
    return attempt

@router.get("/{attempt_id}/insights")
def get_attempt_insights(attempt_id: int, db: Session = Depends(get_db)):
    """Get detailed cognitive insights for an attempt"""
    attempt = crud.get_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    responses = attempt.responses
    insights = CuriosityAnalyzer.get_cognitive_insights(responses)
    
    return {
        "attempt_id": attempt_id,
        "student_name": attempt.student_name,
        "insights": insights
    }

@router.get("/{attempt_id}/responses")
def get_attempt_responses(attempt_id: int, db: Session = Depends(get_db)):
    """Get question-by-question breakdown for an attempt"""
    attempt = crud.get_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    responses_data = []
    for response in attempt.responses:
        responses_data.append({
            "id": response.id,
            "question_id": response.question_id,
            "question_text": response.question_text or "Question not available",
            "category": response.category or "General",
            "difficulty": response.difficulty or "medium",
            "user_answer": response.user_answer,
            "is_correct": response.is_correct,
            "confidence": response.confidence_level,
            "time_taken": response.time_spent,
            "created_at": response.created_at.isoformat() if response.created_at else None
        })
    
    return {
        "attempt_id": attempt_id,
        "student_name": attempt.student_name,
        "started_at": attempt.started_at.isoformat() if attempt.started_at else None,
        "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None,
        "total_questions": attempt.total_questions,
        "correct_answers": attempt.correct_answers,
        "curiosity_score": attempt.curiosity_score,
        "average_confidence": attempt.average_confidence,
        "responses": responses_data
    }
