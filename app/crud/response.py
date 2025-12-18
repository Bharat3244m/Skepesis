from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.response import Response
from app.schemas.response import ResponseCreate
from app.logger import get_logger
from typing import List, Optional

logger = get_logger(__name__)


class ResponseCRUDError(Exception):
    """Custom exception for Response CRUD operations"""
    pass


def get_response(db: Session, response_id: int) -> Optional[Response]:
    """Get a single response by ID"""
    try:
        return db.query(Response).filter(Response.id == response_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching response {response_id}: {e}")
        raise ResponseCRUDError(f"Failed to fetch response: {e}") from e


def get_responses_by_attempt(db: Session, attempt_id: int) -> List[Response]:
    """Get all responses for an attempt"""
    try:
        return db.query(Response).filter(Response.attempt_id == attempt_id).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching responses for attempt {attempt_id}: {e}")
        raise ResponseCRUDError(f"Failed to fetch responses: {e}") from e


def create_response(db: Session, response: ResponseCreate, correct_answer: Optional[str] = None) -> Response:
    """
    Create a new response and check if it's correct.
    
    Args:
        db: Database session
        response: Response data
        correct_answer: For API questions, pass the correct answer directly
    
    Raises:
        ResponseCRUDError: If database operation fails
    """
    try:
        is_correct = False
        
        # For API questions, check against provided correct answer
        if correct_answer:
            is_correct = response.user_answer.strip().lower() == correct_answer.strip().lower()
        
        # Exclude correct_answer from the data to save (it's only for validation)
        response_data = response.model_dump(exclude={'correct_answer'})
        
        # Ensure category and difficulty have defaults
        if not response_data.get('category'):
            response_data['category'] = "General"
        if not response_data.get('difficulty'):
            response_data['difficulty'] = "medium"
        
        db_response = Response(
            **response_data,
            is_correct=is_correct
        )
        db.add(db_response)
        db.commit()
        db.refresh(db_response)
        return db_response
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating response: {e}")
        raise ResponseCRUDError(f"Failed to create response: {e}") from e
