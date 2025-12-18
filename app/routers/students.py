from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.response import ResponseResponse, ResponseCreate
from app.crud import response as response_crud
from app.crud import attempt as attempt_crud
from app.crud.response import ResponseCRUDError
from app.crud.attempt import AttemptCRUDError
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/responses", tags=["responses"])


@router.post("/", response_model=ResponseResponse)
def create_response(response: ResponseCreate, db: Session = Depends(get_db)):
    """Submit a response to a question"""
    try:
        db_response = response_crud.create_response(
            db, 
            response,
            correct_answer=response.correct_answer
        )
        
        # Update attempt stats
        attempt_crud.update_attempt_stats(db, response.attempt_id)
        
        return db_response
    except ResponseCRUDError as e:
        logger.error(f"Failed to create response: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit response")
    except AttemptCRUDError as e:
        logger.error(f"Failed to update attempt stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to update attempt statistics")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating response: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/attempt/{attempt_id}", response_model=List[ResponseResponse])
def get_responses_by_attempt(attempt_id: int, db: Session = Depends(get_db)):
    """Get all responses for an attempt"""
    try:
        return response_crud.get_responses_by_attempt(db, attempt_id)
    except ResponseCRUDError as e:
        logger.error(f"Failed to fetch responses for attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch responses")
