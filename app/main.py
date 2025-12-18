from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.routers import questions, attempts, students, trivia, llm
from app.config import get_settings
from app.initial_data import init_db
from app.logger import get_logger, setup_app_logging

# Initialize centralized logging
setup_app_logging()
logger = get_logger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events: startup and shutdown"""
    # Startup: Initialize database
    try:
        init_db()
        logger.info("Application startup complete", extra={"app_name": settings.app_name})
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}", exc_info=True)
        raise
    yield
    # Shutdown: Clean up resources if needed
    logger.info("Application shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Smart Adaptive Learning & Education Platform",
    lifespan=lifespan
)


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with user-friendly messages"""
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Invalid request data",
            "errors": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(questions.router)
app.include_router(attempts.router)
app.include_router(students.router)
app.include_router(trivia.router)
app.include_router(llm.router)

# Template routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Landing page"""
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        raise HTTPException(status_code=500, detail="Failed to load page")


@app.get("/quiz", response_class=HTMLResponse)
async def quiz(request: Request):
    """Quiz interface"""
    try:
        return templates.TemplateResponse("quiz.html", {"request": request})
    except Exception as e:
        logger.error(f"Error rendering quiz page: {e}")
        raise HTTPException(status_code=500, detail="Failed to load page")


@app.get("/results/{attempt_id}", response_class=HTMLResponse)
async def results(request: Request, attempt_id: int):
    """Results and insights page"""
    try:
        return templates.TemplateResponse("results.html", {
            "request": request,
            "attempt_id": attempt_id
        })
    except Exception as e:
        logger.error(f"Error rendering results page for attempt {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to load page")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Analytics dashboard"""
    try:
        return templates.TemplateResponse("dashboard.html", {"request": request})
    except Exception as e:
        logger.error(f"Error rendering dashboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to load page")


@app.get("/curiosity", response_class=HTMLResponse)
async def curiosity_solver(request: Request):
    """Curiosity Solver - analytical question exploration"""
    try:
        return templates.TemplateResponse("curiosity.html", {"request": request})
    except Exception as e:
        logger.error(f"Error rendering curiosity solver: {e}")
        raise HTTPException(status_code=500, detail="Failed to load page")


@app.get("/attempt/{attempt_id}", response_class=HTMLResponse)
async def attempt_details(request: Request, attempt_id: int):
    """Detailed attempt breakdown"""
    try:
        return templates.TemplateResponse("attempt_details.html", {
            "request": request,
            "attempt_id": attempt_id
        })
    except Exception as e:
        logger.error(f"Error rendering attempt details for {attempt_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to load page")


@app.get("/health")
async def health():
    """Health check endpoint"""
    try:
        return {"status": "healthy", "app": settings.app_name, "version": settings.app_version}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )
