from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import RoleEnum

# Base Schema
class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: RoleEnum = RoleEnum.STUDENT

# Request Schemas (Input)
class RegisterRequest(UserBase):
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Response Schemas (Output)
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        # Crucial for SQLAlchemy compatibility (formerly orm_mode)
        from_attributes = True