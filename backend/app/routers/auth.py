from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

from app.database import get_db
from app.models.user import User, RoleEnum
from app.schemas.user import LoginResponse, RegisterRequest, UserResponse
from app.services.auth import (
    verify_password, 
    get_password_hash,  # This was the missing function
    create_access_token,
    get_current_user
)
from app.config import get_settings
from app.logger import get_logger

router = APIRouter(prefix="/api/auth", tags=["auth"])
settings = get_settings()
logger = get_logger(__name__)

@router.post("/login", response_model=LoginResponse)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2 compatible token login. 
    Sets HttpOnly cookie for web access + returns Bearer token for API access.
    """
    try:
        # 1. Fetch User (Async)
        result = await db.execute(select(User).where(User.email == form_data.username))
        user = result.scalars().first()

        # 2. Verify Credentials
        if not user or not verify_password(form_data.password, user.hashed_password):
            # Mitigate timing attacks by always taking roughly same time (optional refinement)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 3. Create Token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role.value},
            expires_delta=access_token_expires
        )

        # 4. Set HttpOnly Cookie (Crucial for your frontend templates)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=not settings.debug,  # False in dev (HTTP), True in prod (HTTPS)
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        logger.info(f"User logged in: {user.email}")

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user.role.value
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.post("/register", response_model=UserResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new student user"""
    try:
        # 1. Check if email exists
        result = await db.execute(select(User).where(User.email == payload.email))
        if result.scalars().first():
            raise HTTPException(
                status_code=400, 
                detail="Email already registered"
            )

        # 2. Create User
        new_user = User(
            email=payload.email,
            username=payload.username,
            hashed_password=get_password_hash(payload.password),
            role=RoleEnum.STUDENT # Force role to student for public registration
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logger.info(f"New user registered: {payload.email}")
        return new_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/logout")
async def logout(response: Response):
    """Clear auth cookies"""
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user