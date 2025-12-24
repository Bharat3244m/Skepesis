"""
Database initialization
"""
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine, Base
from app.logger import get_logger

logger = get_logger(__name__)


def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create database tables: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}", exc_info=True)
        raise
