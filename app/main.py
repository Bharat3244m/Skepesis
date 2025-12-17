from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from app.routers import questions, attempts, students, trivia
from app.config import get_settings
from app.initial_data import init_db

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events: startup and shutdown"""
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: Clean up resources if needed
    pass

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Smart Adaptive Learning & Education Platform",
    lifespan=lifespan
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

# Template routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Landing page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/quiz", response_class=HTMLResponse)
async def quiz(request: Request):
    """Quiz interface"""
    return templates.TemplateResponse("quiz.html", {"request": request})

@app.get("/results/{attempt_id}", response_class=HTMLResponse)
async def results(request: Request, attempt_id: int):
    """Results and insights page"""
    return templates.TemplateResponse("results.html", {
        "request": request,
        "attempt_id": attempt_id
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Analytics dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/attempt/{attempt_id}", response_class=HTMLResponse)
async def attempt_details(request: Request, attempt_id: int):
    """Detailed attempt breakdown"""
    return templates.TemplateResponse("attempt_details.html", {
        "request": request,
        "attempt_id": attempt_id
    })

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "app": settings.app_name}
