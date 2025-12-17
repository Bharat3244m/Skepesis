from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.response import ResponseResponse, ResponseCreate
from app.crud import response as response_crud
from app.crud import attempt as attempt_crud

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
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/attempt/{attempt_id}", response_model=List[ResponseResponse])
def get_responses_by_attempt(attempt_id: int, db: Session = Depends(get_db)):
    """Get all responses for an attempt"""
    return response_crud.get_responses_by_attempt(db, attempt_id)
