from fastapi import APIRouter, Depends, status, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth import verify_password, create_access_token, get_password_hash, get_settings
from datetime import timedelta

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request, 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    # Enforce password length: min 8, max 32 (and bcrypt limit)
    if not (8 <= len(password) <= 32):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Password must be 8-32 characters long."})
    if len(password.encode("utf-8")) > 72:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Password cannot be longer than 72 bytes."})
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    response = RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email already registered"})
    # Enforce password length: min 8, max 32 (and bcrypt limit)
    if not (8 <= len(password) <= 32):
        return templates.TemplateResponse("register.html", {"request": request, "error": "Password must be 8-32 characters long."})
    if len(password.encode("utf-8")) > 72:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Password cannot be longer than 72 bytes."})
    new_user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password)
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response

@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, db: Session = Depends(get_db)):
    # The middleware (step E) ensures request.state.user is set if logged in
    user = getattr(request.state, "user", None)
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})