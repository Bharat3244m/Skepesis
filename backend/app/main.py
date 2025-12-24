from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# --- Core Imports ---
from app.config import get_settings
from app.logger import get_logger, setup_app_logging
from app.database import engine, Base

# --- Router Imports ---
from app.routers import questions, attempts, responses, trivia, llm, auth
from app.routers import quiz

# Initialize logging
setup_app_logging()
logger = get_logger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Async Table Creation
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Startup complete")
    yield
    await engine.dispose()
    logger.info("Shutdown complete")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

# --- CRITICAL: CORS Setup for Angular ---
# Angular runs on port 4200. We must explicitly allow it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # The Angular URL
    allow_credentials=True,                   # Required for Cookies/Auth
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# --- Register Routers ---
app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(attempts.router)
app.include_router(responses.router)
app.include_router(trivia.router)
app.include_router(llm.router)
app.include_router(trivia.router)
app.include_router(quiz.router)

# --- Health Check ---
@app.get("/health")
async def health():
    return {"status": "active", "mode": "api-only"}