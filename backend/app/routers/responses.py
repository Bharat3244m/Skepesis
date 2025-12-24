from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.response import ResponseCreate, ResponseResponse
from app.services.learning_session_service import LearningSessionService
from app.services.auth import require_roles
from app.models.user import User, RoleEnum
from app.logger import get_logger

# Initialize Logger
logger = get_logger(__name__)

router = APIRouter(prefix="/api/responses", tags=["responses"])

@router.post("/", response_model=ResponseResponse)
async def submit_response(
    payload: ResponseCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles([RoleEnum.STUDENT]))
):
    """
    Submit a single answer to a question.
    - Calculates correctness immediately
    - Updates attempt statistics asynchronously
    """
    try:
        # We enforce that the logged-in student owns the attempt in the Service layer
        # or we trust the attempt_id provided (since we don't have attempt ownership check here yet).
        # ideally, the Service should verify attempt ownership.
        
        response = await LearningSessionService.submit_response(
            db=db,
            attempt_id=payload.attempt_id,
            payload=payload
        )
        return response
        
    except ValueError as e:
        # Handle specific business logic errors (e.g., attempt closed)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error submitting response: {e}")
        raise HTTPException(status_code=500, detail="Failed to save response")

@router.get("/attempt/{attempt_id}", response_model=List[ResponseResponse])
async def get_responses_by_attempt(
    attempt_id: int, 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles([RoleEnum.STUDENT, RoleEnum.TEACHER, RoleEnum.PARENT]))
):
    """
    Get the full history of answers for a specific attempt.
    """
    try:
        # Reuse the service method (you need to ensure this method exists in Service or call CRUD directly)
        # For now, we will call the Service to keep the router clean.
        responses = await LearningSessionService.get_responses_for_attempt(db, attempt_id)
        
        if not responses:
             # Returning empty list is better than 404 if the attempt just has no answers yet
            return []
            
        return responses
        
    except Exception as e:
        logger.error(f"Failed to fetch responses for attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch responses")