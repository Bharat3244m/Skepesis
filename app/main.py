from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError

# --- Core Imports ---
from app.config import get_settings
from app.initial_data import init_db
from app.logger import get_logger, setup_app_logging

# --- Database Imports (From your provided file) ---
# We import the existing instances instead of creating new ones
from app.database import engine, Base, SessionLocal

# --- Auth & Models ---
from app.models.user import User
from app.services.auth import decode_token

# --- Router Imports ---
from app.routers import questions, attempts, students, trivia, llm, auth

# Initialize centralized logging
setup_app_logging()
logger = get_logger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events: startup and shutdown"""
    try:
        # 1. Create Tables: Uses the 'engine' and 'Base' imported from app.database
        Base.metadata.create_all(bind=engine)
        
        # 2. Initialize Data
        init_db()
        
        logger.info("Application startup complete", extra={"app_name": settings.app_name})
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}", exc_info=True)
        raise
    yield
    # Shutdown logic (if any)
    logger.info("Application shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Smart Adaptive Learning & Education Platform",
    lifespan=lifespan
)

# --- Static Files (CSS/JS) ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# --- Auth Middleware ---
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    request.state.user = None
    token = request.cookies.get("access_token")
    
    if token:
        # Handle "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
            
        payload_email = decode_token(token)
        
        if payload_email:
            # Use the imported SessionLocal factory to create a thread-safe session
            db = SessionLocal()
            try:
                user = db.query(User).filter(User.email == payload_email).first()
                if user:
                    request.state.user = user
            except Exception as e:
                logger.error(f"Middleware Auth Error: {e}")
            finally:
                # Always close the session after the check
                db.close()
            
    response = await call_next(request)
    return response


# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request data", "errors": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )


# --- Register Routers ---
app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(attempts.router)
app.include_router(students.router)
app.include_router(trivia.router)
app.include_router(llm.router)


# --- Template Routes ---
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        # Checks for index.html, falls back to base.html if needed
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception:
        return templates.TemplateResponse("base.html", {"request": request})

@app.get("/quiz", response_class=HTMLResponse)
async def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})

@app.get("/results/{attempt_id}", response_class=HTMLResponse)
async def results(request: Request, attempt_id: int):
    return templates.TemplateResponse("results.html", {"request": request, "attempt_id": attempt_id})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/curiosity", response_class=HTMLResponse)
async def curiosity_solver(request: Request):
    return templates.TemplateResponse("curiosity.html", {"request": request})

@app.get("/attempt/{attempt_id}", response_class=HTMLResponse)
async def attempt_details(request: Request, attempt_id: int):
    return templates.TemplateResponse("attempt_details.html", {"request": request, "attempt_id": attempt_id})

@app.get("/health")
async def health():
    return {"status": "healthy", "app": settings.app_name, "version": settings.app_version}