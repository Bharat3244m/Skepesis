from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import get_settings
from app.database import get_db
from app.models.user import User, RoleEnum
from app.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)

# Security Contexts
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

# --- Core Utilities ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash using bcrypt"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
    )

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    # Ensure password is not too long for bcrypt (72 bytes limit)
    if len(password.encode('utf-8')) > 72:
        raise ValueError("Password is too long (max 72 bytes)")
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# --- Dependencies ---
async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Validates token from Cookie OR Header and returns the User object.
    """
    # 1. Extract Token (Cookie priority to support your frontend templates)
    if not token:
        token = request.cookies.get("access_token")
        if token and token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # 2. Decode & Find User
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        # Async Query
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# --- RBAC Factory ---
def require_roles(allowed_roles: List[RoleEnum]):
    """
    Dependency to enforce role-based access control.
    Usage: @router.get("/", dependencies=[Depends(require_roles([RoleEnum.TEACHER]))])
    """
    async def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles:
            logger.warning(f"Access denied for user {user.email} (Role: {user.role}). Required: {allowed_roles}")
            raise HTTPException(
                status_code=403, 
                detail=f"Access forbidden. Required roles: {[r.value for r in allowed_roles]}"
            )
        return user
    return role_checker