from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession # Added async support

from app.database import get_db
from app.schemas.question import QuestionPublic
from app.services.trivia_api import TriviaAPIService, TriviaAPIError
from app.logger import get_logger
# CHANGED: Import from auth, not rbac
from app.services.auth import require_roles
from app.models.user import RoleEnum, User

logger = get_logger(__name__)

router = APIRouter(prefix="/api/questions", tags=["questions"])

# OpenTDB category name to ID mapping (all 24 categories)
OPENTDB_CATEGORIES = {
    "General Knowledge": 9,
    "Entertainment: Books": 10,
    "Entertainment: Film": 11,
    "Entertainment: Music": 12,
    "Entertainment: Musicals & Theatres": 13,
    "Entertainment: Television": 14,
    "Entertainment: Video Games": 15,
    "Entertainment: Board Games": 16,
    "Science & Nature": 17,
    "Science: Computers": 18,
    "Science: Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28,
    "Entertainment: Comics": 29,
    "Science: Gadgets": 30,
    "Entertainment: Japanese Anime & Manga": 31,
    "Entertainment: Cartoon & Animations": 32,
}


@router.get("/random", response_model=List[QuestionPublic])
async def get_random_questions(
    limit: int = 10,
    category: Optional[str] = None,
    # CHANGED: require_roles expects a list now
    user: User = Depends(require_roles([RoleEnum.STUDENT, RoleEnum.TEACHER]))
):
    """
    Get random questions from Open Trivia Database API.
    """
    try:
        # Map category name to OpenTDB ID if provided
        opentdb_category = None
        if category:
            if category in OPENTDB_CATEGORIES:
                opentdb_category = OPENTDB_CATEGORIES[category]
            else:
                for cat_name, cat_id in OPENTDB_CATEGORIES.items():
                    if category.lower() in cat_name.lower() or cat_name.lower() in category.lower():
                        opentdb_category = cat_id
                        break
        
        # Async call to trivia service
        api_questions = await TriviaAPIService.fetch_questions(
            amount=limit,
            category=opentdb_category
        )
        
        if not api_questions:
            raise HTTPException(status_code=404, detail="No questions available from API")
        
        # Convert to QuestionPublic format
        return [
            QuestionPublic(
                id=idx + 1,
                text=q.text,
                question_type=q.question_type,
                difficulty=q.difficulty,
                category=q.category,
                option_a=q.option_a,
                option_b=q.option_b,
                option_c=q.option_c,
                option_d=q.option_d,
                correct_answer=q.correct_answer
            )
            for idx, q in enumerate(api_questions)
        ]
    except TriviaAPIError as e:
        logger.error(f"Trivia API error: {e}")
        raise HTTPException(status_code=503, detail="Trivia service temporarily unavailable")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching questions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch questions: {str(e)}")


@router.get("/categories", response_model=List[str])
def get_categories(user: User = Depends(require_roles([RoleEnum.STUDENT, RoleEnum.TEACHER]))):
    """Get all available categories"""
    return list(OPENTDB_CATEGORIES.keys())