from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.attempt import AttemptResponse, AttemptCreate
from app.crud import attempt as crud
from app.crud.attempt import AttemptCRUDError
from app.services.curiosity import CuriosityAnalyzer
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/attempts", tags=["attempts"])


@router.get("/", response_model=List[AttemptResponse])
def get_attempts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all attempts"""
    try:
        return crud.get_attempts(db, skip=skip, limit=limit)
    except AttemptCRUDError as e:
        logger.error(f"Failed to fetch attempts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch attempts")


@router.get("/{attempt_id}", response_model=AttemptResponse)
def get_attempt(attempt_id: int, db: Session = Depends(get_db)):
    """Get a specific attempt"""
    try:
        attempt = crud.get_attempt(db, attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")
        return attempt
    except AttemptCRUDError as e:
        logger.error(f"Failed to fetch attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch attempt")


@router.post("/", response_model=AttemptResponse)
def create_attempt(attempt: AttemptCreate, db: Session = Depends(get_db)):
    """Start a new learning attempt"""
    try:
        return crud.create_attempt(db, attempt)
    except AttemptCRUDError as e:
        logger.error(f"Failed to create attempt: {e}")
        raise HTTPException(status_code=500, detail="Failed to create attempt")


@router.post("/{attempt_id}/complete", response_model=AttemptResponse)
def complete_attempt(attempt_id: int, db: Session = Depends(get_db)):
    """Mark attempt as complete and calculate final scores"""
    try:
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
    except AttemptCRUDError as e:
        logger.error(f"Failed to complete attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to complete attempt")
    except Exception as e:
        logger.error(f"Unexpected error completing attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/{attempt_id}/insights")
def get_attempt_insights(attempt_id: int, db: Session = Depends(get_db)):
    """Get detailed cognitive insights for an attempt"""
    try:
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
    except AttemptCRUDError as e:
        logger.error(f"Failed to fetch insights for attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch attempt insights")
    except Exception as e:
        logger.error(f"Error generating insights for attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate insights")


@router.get("/{attempt_id}/responses")
def get_attempt_responses(attempt_id: int, db: Session = Depends(get_db)):
    """Get question-by-question breakdown for an attempt"""
    try:
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
    except AttemptCRUDError as e:
        logger.error(f"Failed to fetch responses for attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch attempt responses")
    except Exception as e:
        logger.error(f"Error processing responses for attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process responses")
