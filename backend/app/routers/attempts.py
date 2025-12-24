from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.database import get_db
from app.models.user import User, RoleEnum
from app.models.attempt import Attempt
from app.schemas.attempt import AttemptResponse, AttemptCreate
from app.services.learning_session_service import LearningSessionService
from app.services.auth import require_roles
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/attempts", tags=["attempts"])

def _check_ownership(attempt: Attempt, user: User):
    """
    Verifies that the current user owns the attempt.
    Teachers can view all attempts.
    """
    if user.role == RoleEnum.TEACHER:
        return
    
    # Compare emails or IDs depending on your User model structure.
    # Assuming student_name stores the email/username as per your previous code
    if attempt.student_name != user.email:
        raise HTTPException(status_code=403, detail="Not authorized to access this attempt")

@router.get("/", response_model=List[AttemptResponse])
async def get_attempts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles([RoleEnum.STUDENT, RoleEnum.TEACHER]))
):
    """Get all attempts (filtered by user role)"""
    try:
        query = select(Attempt).offset(skip).limit(limit)
        
        # If student, filter only their attempts
        if user.role == RoleEnum.STUDENT:
            query = query.where(Attempt.student_name == user.email)
            
        result = await db.execute(query)
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Failed to fetch attempts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{attempt_id}", response_model=AttemptResponse)
async def get_attempt(
    attempt_id: int, 
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(require_roles([RoleEnum.STUDENT, RoleEnum.TEACHER]))
):
    """Get a specific attempt details"""
    try:
        # Eager load responses to avoid async lazy load errors
        query = select(Attempt).options(selectinload(Attempt.responses)).where(Attempt.id == attempt_id)
        result = await db.execute(query)
        attempt = result.scalars().first()
        
        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")
            
        _check_ownership(attempt, user)
        return attempt
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch attempt")

@router.post("/", response_model=AttemptResponse)
async def create_attempt(
    attempt_data: AttemptCreate, # Assuming you have a schema, otherwise usage is implied
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(require_roles([RoleEnum.STUDENT]))
):
    """Start a new learning attempt"""
    try:
        # Delegate to the Async Service
        return await LearningSessionService.start_attempt(db, user.email)
    except Exception as e:
        logger.error(f"Failed to create attempt: {e}")
        raise HTTPException(status_code=500, detail="Failed to create attempt")

@router.post("/{attempt_id}/complete")
async def complete_attempt(
    attempt_id: int, 
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(require_roles([RoleEnum.STUDENT]))
):
    """
    Mark attempt as complete and trigger final scoring.
    """
    try:
        # 1. Fetch
        query = select(Attempt).options(selectinload(Attempt.responses)).where(Attempt.id == attempt_id)
        result = await db.execute(query)
        attempt = result.scalars().first()
        
        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")
        _check_ownership(attempt, user)
        
        # 2. Delegate Business Logic to Service (which should be async now)
        # Note: You need to add this method to your LearningSessionService as shown below
        updated_attempt = await LearningSessionService.complete_attempt(db, attempt)
        
        return updated_attempt
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error completing attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to complete attempt")

@router.get("/{attempt_id}/insights")
async def get_attempt_insights(
    attempt_id: int, 
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(require_roles([RoleEnum.TEACHER, RoleEnum.STUDENT]))
):
    """
    Get AI-generated cognitive insights.
    """
    try:
        # Permission check first
        query = select(Attempt).where(Attempt.id == attempt_id)
        result = await db.execute(query)
        attempt = result.scalars().first()
        
        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")
        _check_ownership(attempt, user)

        # Call the LLM Service
        insights_text = await LearningSessionService.generate_insights(db, attempt_id)
        
        return {
            "attempt_id": attempt_id,
            "student_name": attempt.student_name,
            "ai_insights": insights_text
        }
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate insights")