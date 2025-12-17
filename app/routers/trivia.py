from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.question import QuestionResponse
from app.services.trivia_api import TriviaAPIService
from app.crud import question as crud

router = APIRouter(prefix="/api/trivia", tags=["trivia"])

@router.get("/categories")
async def get_trivia_categories():
    """Get available categories from Open Trivia Database"""
    try:
        categories = await TriviaAPIService.get_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/import", response_model=List[QuestionResponse])
async def import_questions(
    amount: int = Query(10, ge=1, le=50, description="Number of questions to import"),
    category: Optional[int] = Query(None, description="Category ID from Open Trivia DB"),
    difficulty: Optional[str] = Query(None, regex="^(easy|medium|hard)$", description="Difficulty level"),
    db: Session = Depends(get_db)
):
    """
    Import questions from Open Trivia Database
    
    - **amount**: Number of questions (1-50)
    - **category**: Category ID (optional, get list from /trivia/categories)
    - **difficulty**: easy, medium, or hard (optional)
    """
    try:
        # Fetch questions from API
        questions_data = await TriviaAPIService.fetch_questions(
            amount=amount,
            category=category,
            difficulty=difficulty
        )
        
        if not questions_data:
            raise HTTPException(status_code=404, detail="No questions returned from API")
        
        # Save to database
        created_questions = []
        for question_data in questions_data:
            db_question = crud.create_question(db, question_data)
            created_questions.append(db_question)
        
        return created_questions
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import questions: {str(e)}")

@router.get("/preview")
async def preview_questions(
    amount: int = Query(5, ge=1, le=10, description="Number of questions to preview"),
    category: Optional[int] = Query(None, description="Category ID"),
    difficulty: Optional[str] = Query(None, regex="^(easy|medium|hard)$")
):
    """
    Preview questions from Open Trivia Database without saving
    
    - **amount**: Number of questions (1-10 for preview)
    - **category**: Category ID (optional)
    - **difficulty**: easy, medium, or hard (optional)
    """
    try:
        questions = await TriviaAPIService.fetch_questions(
            amount=amount,
            category=category,
            difficulty=difficulty
        )
        
        return {
            "count": len(questions),
            "questions": [q.model_dump() for q in questions]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
