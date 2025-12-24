from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import Optional

from app.services.llm import get_llm_service, LLMService, PromptTemplate
# FIXED: Import from auth, not rbac
from app.services.auth import require_roles
from app.models.user import RoleEnum, User
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/llm", tags=["llm"])

class LLMRequest(BaseModel):
    prompt: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500

@router.post("/generate")
async def generate_text(
    request: LLMRequest,
    user: User = Depends(require_roles([RoleEnum.TEACHER, RoleEnum.STUDENT])),
    llm: LLMService = Depends(get_llm_service)
):
    """
    Direct access to LLM generation (Protected).
    Useful for testing prompts or ad-hoc analysis.
    """
    try:
        response = await llm.generate(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return {"response": response}
    except Exception as e:
        logger.error(f"LLM Generation Error: {e}")
        raise HTTPException(status_code=503, detail="AI Service unavailable")

@router.get("/health")
async def llm_health(
    llm: LLMService = Depends(get_llm_service),
    user: User = Depends(require_roles([RoleEnum.TEACHER]))
):
    """Check connectivity to the local Ollama instance"""
    is_healthy = await llm.health_check()
    if not is_healthy:
        raise HTTPException(status_code=503, detail="Ollama service is not reachable")
    return {"status": "connected", "model": llm.model}