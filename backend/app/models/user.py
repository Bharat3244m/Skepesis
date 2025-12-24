from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SqlEnum
import enum
from sqlalchemy.sql import func
from app.database import Base

class RoleEnum(str, enum.Enum):
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(SqlEnum(RoleEnum, name="role_enum", native_enum=False), nullable=False, default=RoleEnum.STUDENT)