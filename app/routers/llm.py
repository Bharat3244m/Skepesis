"""
LLM Router - Cognitive Analysis API
Provides analytical insights for Skepesis learning platform.
Frontend communicates only with these endpoints - no LLM internals exposed.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from app.services.llm import (
    get_llm_service,
    LLMError,
    PromptValidationError,
    PromptTemplate,
    ResponseLength,
    RESPONSE_LENGTH_TOKENS,
    MAX_PROMPT_LENGTH,
    LRUCache
)
from app.logger import get_logger
import time

logger = get_logger(__name__)

router = APIRouter(prefix="/api/insights", tags=["insights"])


# =============================================================================
# SKEPESIS DOMAIN TASK TYPES
# =============================================================================

class InsightType(str, Enum):
    """
    Cognitive analysis types aligned with Skepesis features.
    These map to specific UI components and use cases.
    """
    # Dashboard insights
    PATTERN = "pattern"           # Learning pattern analysis
    CALIBRATION = "calibration"   # Confidence calibration check
    GAP = "gap"                   # Knowledge gap identification
    THINKING = "thinking"         # Thinking speed analysis
    
    # Results & summaries
    SUMMARY = "summary"           # Session summary
    CARD = "card"                 # Single insight card
    
    # General analysis
    ANALYZE = "analyze"           # General analysis
    EVALUATE = "evaluate"         # Evaluation
    EXPLAIN = "explain"           # Explanation


# Map insight types to templates and default lengths
INSIGHT_CONFIG = {
    InsightType.PATTERN: {
        "template": PromptTemplate.PATTERN_ANALYSIS,
        "length": ResponseLength.STANDARD,
        "description": "Learning pattern observation"
    },
    InsightType.CALIBRATION: {
        "template": PromptTemplate.CALIBRATION_CHECK,
        "length": ResponseLength.COMPACT,
        "description": "Confidence calibration assessment"
    },
    InsightType.GAP: {
        "template": PromptTemplate.GAP_IDENTIFICATION,
        "length": ResponseLength.COMPACT,
        "description": "Knowledge gap identification"
    },
    InsightType.THINKING: {
        "template": PromptTemplate.THINKING_ANALYSIS,
        "length": ResponseLength.COMPACT,
        "description": "Thinking speed analysis"
    },
    InsightType.SUMMARY: {
        "template": PromptTemplate.SESSION_SUMMARY,
        "length": ResponseLength.COMPACT,
        "description": "Quiz session summary"
    },
    InsightType.CARD: {
        "template": PromptTemplate.INSIGHT_CARD,
        "length": ResponseLength.CARD,
        "description": "Dashboard insight card"
    },
    InsightType.ANALYZE: {
        "template": PromptTemplate.ANALYZE,
        "length": ResponseLength.STANDARD,
        "description": "General analysis"
    },
    InsightType.EVALUATE: {
        "template": PromptTemplate.EVALUATE,
        "length": ResponseLength.COMPACT,
        "description": "Evaluation assessment"
    },
    InsightType.EXPLAIN: {
        "template": PromptTemplate.EXPLAIN,
        "length": ResponseLength.STANDARD,
        "description": "Concept explanation"
    },
}


# =============================================================================
# REQUEST/RESPONSE MODELS (No LLM internals exposed)
# =============================================================================

class InsightRequest(BaseModel):
    """Request for cognitive insight generation."""
    data: str = Field(
        ...,
        min_length=10,
        max_length=MAX_PROMPT_LENGTH,
        description="Learning data or context to analyze"
    )
    type: InsightType = Field(
        InsightType.ANALYZE,
        description="Type of cognitive insight"
    )
    length: Optional[ResponseLength] = Field(
        None,
        description="Response length (auto-selected if not specified)"
    )
    bypass_cache: bool = Field(
        False,
        description="Force fresh analysis"
    )


class InsightResponse(BaseModel):
    """Cognitive insight response - clean, frontend-ready."""
    insight: str = Field(..., description="The analytical insight")
    type: str = Field(..., description="Insight type")
    
    class Config:
        # Hide implementation details
        json_schema_extra = {
            "example": {
                "insight": "Pattern: Deliberate thinking style observed. Response times exceed 30s on medium-difficulty items. Accuracy correlates with extended consideration.",
                "type": "pattern"
            }
        }


class ServiceStatus(BaseModel):
    """Service health status."""
    status: str
    ready: bool


class InsightTypeInfo(BaseModel):
    """Information about an insight type."""
    type: str
    description: str
    typical_length: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post("/generate", response_model=InsightResponse)
async def generate_insight(request: InsightRequest):
    """
    Generate a cognitive insight from learning data.
    
    This endpoint analyzes learning patterns, calibration, gaps, and more.
    Response format is optimized for Skepesis UI components.
    """
    start_time = time.time()
    
    config = INSIGHT_CONFIG.get(request.type)
    if not config:
        raise HTTPException(status_code=400, detail="Invalid insight type")
    
    # Use requested length or default for insight type
    length = request.length or config["length"]
    max_tokens = RESPONSE_LENGTH_TOKENS.get(length, 150)
    
    logger.info("Insight request", extra={
        "type": request.type.value,
        "length": length.value,
        "data_length": len(request.data)
    })
    
    try:
        llm = get_llm_service()
        
        insight = await llm.generate(
            prompt=request.data,
            template=config["template"],
            max_tokens=max_tokens,
            use_cache=not request.bypass_cache
        )
        
        logger.info("Insight generated", extra={
            "type": request.type.value,
            "latency_ms": round((time.time() - start_time) * 1000)
        })
        
        return InsightResponse(
            insight=insight,
            type=request.type.value
        )
    
    except PromptValidationError as e:
        logger.warning(f"Validation failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except LLMError as e:
        logger.warning(f"Insight generation failed: {e}")
        raise HTTPException(status_code=503, detail="Analysis temporarily unavailable")
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal error")


@router.get("/types", response_model=List[InsightTypeInfo])
async def list_insight_types():
    """
    List available insight types for UI feature discovery.
    """
    return [
        InsightTypeInfo(
            type=insight_type.value,
            description=config["description"],
            typical_length=config["length"].value
        )
        for insight_type, config in INSIGHT_CONFIG.items()
    ]


@router.get("/status", response_model=ServiceStatus)
async def check_status():
    """
    Check if cognitive analysis is available.
    Used by frontend to gracefully enable/disable features.
    """
    llm = get_llm_service()
    is_ready = await llm.health_check()
    
    return ServiceStatus(
        status="ready" if is_ready else "unavailable",
        ready=is_ready
    )


@router.post("/cache/clear")
async def clear_insight_cache():
    """Clear cached insights. Use when model behavior needs refresh."""
    llm = get_llm_service()
    await llm.clear_cache()
    return {"cleared": True}
