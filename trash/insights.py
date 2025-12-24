# app/routers/insights.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.learning_session_service import LearningSessionService
from app.services.rbac import require_roles
from app.models.user import RoleEnum

router = APIRouter(prefix="/api/insights", tags=["insights"])


@router.get("/{attempt_id}")
async def generate_insights(
    attempt_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles(RoleEnum.TEACHER))
):
    return {
        "insight": await LearningSessionService.generate_insights(db, attempt_id)
    }
