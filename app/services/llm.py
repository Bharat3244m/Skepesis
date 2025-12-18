"""
LLM Service - Ollama Integration
Centralized module for all LLM interactions via local Ollama instance.
Implements strict guardrails for analytical, structured outputs.
Optimized for low-latency, reliable responses on consumer GPUs.
"""
import httpx
import re
import asyncio
import hashlib
import time
from typing import Optional
from enum import Enum
from dataclasses import dataclass, field
from collections import OrderedDict
from pydantic import BaseModel
from app.config import get_settings
from app.logger import get_logger

logger = get_logger(__name__)

settings = get_settings()


# =============================================================================
# PERFORMANCE CONSTANTS
# =============================================================================

# Connection settings
CONNECT_TIMEOUT = 5.0      # Fast fail if Ollama unreachable
READ_TIMEOUT = 90.0        # Allow time for generation
POOL_CONNECTIONS = 10      # Connection pool size
POOL_KEEPALIVE = 30        # Keep connections alive (seconds)

# Rate limiting (protect GPU from concurrent heavy loads)
MAX_CONCURRENT_REQUESTS = 2  # Max parallel LLM calls
REQUEST_QUEUE_TIMEOUT = 30.0  # Max wait time in queue

# Caching
CACHE_MAX_SIZE = 100       # Max cached responses
CACHE_TTL = 300            # Cache entry TTL (5 minutes)

# Response limits
MAX_RESPONSE_LENGTH = 2000  # Truncate responses beyond this (chars)
TRUNCATION_SUFFIX = "\n\n[Response truncated]"


# =============================================================================
# PROMPT GUARDRAILS & TEMPLATES
# =============================================================================

class PromptTemplate(str, Enum):
    """
    Predefined prompt templates aligned with Skepesis cognitive analysis.
    
    These templates ensure outputs feel like analytical insights,
    not chatbot responses or tutoring sessions.
    """
    
    # Core system prompt - enforces Skepesis cognitive analysis tone
    SYSTEM_BASE = """You are the analytical engine of Skepesis, a metacognitive learning platform.

YOUR ROLE:
You provide cognitive analysis - objective observations about thinking patterns, knowledge gaps, and learning calibration. You are NOT a tutor, coach, or assistant.

VOICE:
- Clinical and observational, like a diagnostic report
- Third-person perspective when discussing the learner
- Present findings as data points, not advice
- Neutral and non-judgmental

OUTPUT STYLE:
- Brief, scannable bullet points
- Single short paragraphs for conclusions
- No greetings, sign-offs, or pleasantries
- No questions back to the user
- No encouragement or motivation

FORBIDDEN:
- "Great job", "Well done", "Keep it up"
- "You should", "I recommend", "Try to"
- "Let me explain", "Here's what I think"
- Emojis, exclamation marks, casual language
- Rhetorical questions or engagement hooks

REMEMBER: You generate insight cards, not conversations."""

    # ==========================================================================
    # SKEPESIS DOMAIN-SPECIFIC TEMPLATES
    # ==========================================================================
    
    # Performance pattern analysis (for dashboard insights)
    PATTERN_ANALYSIS = """Analyze this learning performance data:

{prompt}

Provide a cognitive pattern observation:
- Primary pattern identified (one line)
- Supporting evidence (2 bullet points)
- Calibration note (one line)

Keep total response under 80 words."""

    # Confidence calibration assessment
    CALIBRATION_CHECK = """Assess confidence calibration from this data:

{prompt}

Report:
- Calibration status: [well-calibrated | overconfident | underconfident]
- Evidence (2 bullet points)
- Pattern implication (one line)

Keep total response under 60 words."""

    # Knowledge gap identification
    GAP_IDENTIFICATION = """Identify knowledge gaps from this quiz performance:

{prompt}

List:
- Primary gap area
- Secondary gap (if evident)
- Confidence-accuracy mismatch (if any)

Keep total response under 50 words."""

    # Thinking speed observation
    THINKING_ANALYSIS = """Analyze response timing patterns:

{prompt}

Observe:
- Thinking style: [quick/moderate/deliberate]
- Consistency note
- Speed-accuracy relationship

Keep total response under 50 words."""

    # Session summary (for results page)
    SESSION_SUMMARY = """Summarize this quiz session:

{prompt}

Provide:
- Performance snapshot (one line)
- Notable pattern (one line)  
- Calibration observation (one line)

Keep total response under 40 words."""

    # Insight card (for dashboard display)
    INSIGHT_CARD = """Generate a single learning insight from:

{prompt}

Format as one insight card:
- Observation title (3-5 words)
- Supporting detail (one sentence)

Keep total response under 25 words."""

    # ==========================================================================
    # GENERAL ANALYTICAL TEMPLATES  
    # ==========================================================================
    
    ANALYZE = """Analyze the following:

{prompt}

Provide:
- Key observations (2-3 points)
- Gaps or assumptions noted
- Conclusion (1-2 sentences)

Keep response concise."""

    EVALUATE = """Evaluate this:

{prompt}

Assess:
- Reasoning accuracy
- Logical gaps
- Brief verdict

Keep response under 60 words."""

    EXPLAIN = """Explain:

{prompt}

Structure:
- Core definition (1 sentence)
- Key components
- Common misconception (if any)

Keep response under 80 words."""


# Response length presets for different UI contexts
class ResponseLength(str, Enum):
    """Preset response lengths for UI components."""
    CARD = "card"          # ~25 words - dashboard insight cards
    COMPACT = "compact"    # ~50 words - inline insights
    STANDARD = "standard"  # ~80 words - detail panels
    FULL = "full"          # ~150 words - full analysis

RESPONSE_LENGTH_TOKENS = {
    ResponseLength.CARD: 50,
    ResponseLength.COMPACT: 100,
    ResponseLength.STANDARD: 150,
    ResponseLength.FULL: 300,
}


class PromptValidationError(Exception):
    """Raised when a prompt fails validation."""
    pass


class LLMError(Exception):
    """Custom exception for LLM service errors"""
    pass


class LLMRequest(BaseModel):
    """Request schema for LLM generation"""
    prompt: str
    system: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None


class LLMResponse(BaseModel):
    """Response schema from LLM generation"""
    response: str
    model: str
    done: bool


# =============================================================================
# GUARDRAIL CONSTANTS
# =============================================================================

# Hard limits
MAX_PROMPT_LENGTH = 4000
MAX_OUTPUT_TOKENS = 512
MIN_PROMPT_LENGTH = 10
DEFAULT_TEMPERATURE = 0.3  # Lower for more deterministic analytical output

# Patterns for input sanitization
INJECTION_PATTERNS = [
    r"ignore\s+(previous|above|all)\s+instructions",
    r"disregard\s+(previous|above|all)",
    r"forget\s+(everything|all|previous)",
    r"you\s+are\s+now",
    r"act\s+as\s+if",
    r"pretend\s+(to\s+be|you)",
    r"new\s+instructions:",
    r"system\s*:\s*",
]

# Vague/open-ended prompt indicators
VAGUE_PATTERNS = [
    r"^(hi|hello|hey)[\s!.]*$",
    r"^what\s+do\s+you\s+think\??$",
    r"^tell\s+me\s+(something|anything)",
    r"^(help|help\s+me)[\s!.]*$",
    r"^(idk|dunno|not\s+sure)",
]


# =============================================================================
# CACHING INFRASTRUCTURE
# =============================================================================

@dataclass
class CacheEntry:
    """A cached LLM response with metadata."""
    response: str
    created_at: float
    hit_count: int = 0


class LRUCache:
    """
    Simple LRU cache with TTL for LLM responses.
    Thread-safe for async usage.
    """
    
    def __init__(self, max_size: int = CACHE_MAX_SIZE, ttl: float = CACHE_TTL):
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._max_size = max_size
        self._ttl = ttl
        self._lock = asyncio.Lock()
        self._hits = 0
        self._misses = 0
    
    @staticmethod
    def _make_key(prompt: str, system: str, temperature: float, max_tokens: int) -> str:
        """Generate a cache key from request parameters."""
        content = f"{prompt}|{system}|{temperature}|{max_tokens}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    async def get(self, key: str) -> Optional[str]:
        """Get cached response if valid."""
        async with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            
            entry = self._cache[key]
            
            # Check TTL
            if time.time() - entry.created_at > self._ttl:
                del self._cache[key]
                self._misses += 1
                return None
            
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            entry.hit_count += 1
            self._hits += 1
            
            logger.debug(f"Cache hit", extra={"key": key, "hits": entry.hit_count})
            return entry.response
    
    async def set(self, key: str, response: str) -> None:
        """Store response in cache."""
        async with self._lock:
            # Evict oldest if at capacity
            while len(self._cache) >= self._max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                logger.debug(f"Cache eviction", extra={"evicted_key": oldest_key})
            
            self._cache[key] = CacheEntry(
                response=response,
                created_at=time.time()
            )
    
    async def clear(self) -> None:
        """Clear all cached entries."""
        async with self._lock:
            self._cache.clear()
            logger.info("Cache cleared")
    
    def stats(self) -> dict:
        """Return cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0
        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate_percent": round(hit_rate, 1)
        }


# Global cache instance
_response_cache = LRUCache()


class LLMService:
    """
    Service to interact with local Ollama instance.
    
    All LLM calls are centralized here to:
    - Keep Ollama details hidden from frontend
    - Provide consistent error handling
    - Enable easy model/endpoint changes
    - Enforce strict prompt guardrails
    
    Performance optimizations:
    - Persistent HTTP connection pool
    - In-memory response caching
    - Concurrency limiting for GPU protection
    - Granular timeouts for fast failure
    """
    
    # Class-level semaphore for rate limiting across all instances
    _request_semaphore: Optional[asyncio.Semaphore] = None
    _http_client: Optional[httpx.AsyncClient] = None
    
    def __init__(
        self,
        base_url: str = None,
        model: str = None,
        timeout: float = None
    ):
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_model
        self.timeout = timeout or settings.ollama_timeout
        self.generate_endpoint = f"{self.base_url}/api/generate"
        self._cache = _response_cache
    
    @classmethod
    def _get_semaphore(cls) -> asyncio.Semaphore:
        """Get or create the request semaphore."""
        if cls._request_semaphore is None:
            cls._request_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        return cls._request_semaphore
    
    @classmethod
    async def _get_client(cls, base_url: str) -> httpx.AsyncClient:
        """
        Get or create a persistent HTTP client with connection pooling.
        Reuses connections for better performance.
        """
        if cls._http_client is None or cls._http_client.is_closed:
            cls._http_client = httpx.AsyncClient(
                base_url=base_url,
                timeout=httpx.Timeout(
                    connect=CONNECT_TIMEOUT,
                    read=READ_TIMEOUT,
                    write=10.0,
                    pool=5.0
                ),
                limits=httpx.Limits(
                    max_connections=POOL_CONNECTIONS,
                    max_keepalive_connections=POOL_CONNECTIONS,
                    keepalive_expiry=POOL_KEEPALIVE
                )
            )
        return cls._http_client
    
    @classmethod
    async def close_client(cls) -> None:
        """Close the HTTP client. Call on app shutdown."""
        if cls._http_client and not cls._http_client.is_closed:
            await cls._http_client.aclose()
            cls._http_client = None
            logger.info("HTTP client closed")
    
    # =========================================================================
    # INPUT VALIDATION & SANITIZATION
    # =========================================================================
    
    def validate_prompt(self, prompt: str) -> None:
        """
        Validate prompt against guardrails.
        
        Args:
            prompt: Raw user prompt
            
        Raises:
            PromptValidationError: If prompt fails validation
        """
        if not prompt or not prompt.strip():
            raise PromptValidationError("Prompt cannot be empty.")
        
        prompt_clean = prompt.strip()
        
        # Length checks
        if len(prompt_clean) < MIN_PROMPT_LENGTH:
            raise PromptValidationError(
                f"Prompt too short. Minimum {MIN_PROMPT_LENGTH} characters required."
            )
        
        if len(prompt_clean) > MAX_PROMPT_LENGTH:
            raise PromptValidationError(
                f"Prompt exceeds maximum length of {MAX_PROMPT_LENGTH} characters."
            )
        
        # Check for vague/open-ended prompts
        prompt_lower = prompt_clean.lower()
        for pattern in VAGUE_PATTERNS:
            if re.match(pattern, prompt_lower):
                raise PromptValidationError(
                    "Prompt is too vague. Please provide a specific question or task."
                )
    
    def sanitize_input(self, text: str) -> str:
        """
        Sanitize user input to prevent prompt injection.
        
        Args:
            text: Raw user input
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        sanitized = text.strip()
        
        # Remove potential injection attempts
        text_lower = sanitized.lower()
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                logger.warning("Potential prompt injection detected", extra={
                    "pattern": pattern,
                    "input_preview": text[:100]
                })
                # Remove the injection attempt
                sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
        
        # Normalize whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        return sanitized
    
    def build_prompt(
        self,
        prompt: str,
        template: Optional[PromptTemplate] = None
    ) -> tuple[str, str]:
        """
        Build a structured prompt with system instruction.
        
        Args:
            prompt: User's input prompt
            template: Optional template for structured tasks
            
        Returns:
            Tuple of (system_prompt, formatted_prompt)
        """
        system = PromptTemplate.SYSTEM_BASE.value
        
        if template and template != PromptTemplate.SYSTEM_BASE:
            formatted_prompt = template.value.format(prompt=prompt)
        else:
            formatted_prompt = prompt
        
        return system, formatted_prompt
    
    # =========================================================================
    # OUTPUT PROCESSING
    # =========================================================================
    
    def _clean_response(
        self,
        response: str,
        strip_markdown: bool = True,
        max_length: int = MAX_RESPONSE_LENGTH
    ) -> str:
        """
        Clean, normalize, and truncate the model response.
        
        Args:
            response: Raw response from model
            strip_markdown: Whether to remove markdown formatting
            max_length: Maximum response length (chars)
            
        Returns:
            Cleaned response string
        """
        if not response:
            return ""
        
        cleaned = response.strip()
        
        # Normalize line breaks
        cleaned = cleaned.replace("\r\n", "\n")
        
        # Remove common LLM pleasantries
        pleasantry_patterns = [
            r"^(Sure|Certainly|Of course|Absolutely)[,!.]?\s*",
            r"^I('d| would) be happy to\s+",
            r"^(Great|Good|Excellent) question[!.]?\s*",
            r"^Let me\s+",
            r"^Here's\s+",
            r"\n*(I hope this helps|Let me know if)[^.]*[.!]?\s*$",
            r"\n*Feel free to[^.]*[.!]?\s*$",
        ]
        
        for pattern in pleasantry_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
        
        # Strip markdown if requested
        if strip_markdown:
            cleaned = self._strip_markdown(cleaned)
        
        # Remove excessive blank lines
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        cleaned = cleaned.strip()
        
        # Truncate if too long (preserve sentence boundaries)
        if len(cleaned) > max_length:
            cleaned = self._truncate_safely(cleaned, max_length)
        
        return cleaned
    
    def _truncate_safely(self, text: str, max_length: int) -> str:
        """
        Truncate text at a safe boundary (sentence or paragraph).
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            
        Returns:
            Truncated text with indicator
        """
        if len(text) <= max_length:
            return text
        
        # Reserve space for truncation suffix
        effective_max = max_length - len(TRUNCATION_SUFFIX)
        
        # Try to cut at paragraph break
        truncated = text[:effective_max]
        last_para = truncated.rfind('\n\n')
        if last_para > effective_max * 0.5:  # At least half the content
            return truncated[:last_para].strip() + TRUNCATION_SUFFIX
        
        # Try to cut at sentence boundary
        sentence_ends = [
            truncated.rfind('. '),
            truncated.rfind('.\n'),
            truncated.rfind('? '),
            truncated.rfind('?\n'),
            truncated.rfind('! '),
            truncated.rfind('!\n'),
        ]
        last_sentence = max(sentence_ends)
        if last_sentence > effective_max * 0.5:
            return truncated[:last_sentence + 1].strip() + TRUNCATION_SUFFIX
        
        # Fall back to word boundary
        last_space = truncated.rfind(' ')
        if last_space > effective_max * 0.7:
            return truncated[:last_space].strip() + TRUNCATION_SUFFIX
        
        # Hard cut as last resort
        return truncated.strip() + TRUNCATION_SUFFIX
    
    def _strip_markdown(self, text: str) -> str:
        """
        Remove markdown formatting from text.
        
        Args:
            text: Text potentially containing markdown
            
        Returns:
            Plain text without markdown
        """
        # Remove code blocks but keep content
        text = re.sub(r'```[\w]*\n?', '', text)
        
        # Remove inline code backticks
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # Remove bold/italic markers
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        
        # Remove headers but keep text
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        
        # Remove horizontal rules
        text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
        
        # Clean up link syntax [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        return text
    
    # =========================================================================
    # CORE GENERATION
    # =========================================================================
    
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        template: Optional[PromptTemplate] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = MAX_OUTPUT_TOKENS,
        strip_markdown: bool = True,
        validate: bool = True,
        use_cache: bool = True
    ) -> str:
        """
        Generate a response from the LLM with guardrails.
        
        Args:
            prompt: The user prompt/question
            system: Optional custom system prompt (overrides default)
            template: Optional structured template
            temperature: Creativity control (0.0-1.0), default 0.3
            max_tokens: Maximum tokens in response, default 512
            strip_markdown: Remove markdown from output, default True
            validate: Whether to validate prompt, default True
            use_cache: Whether to use response caching, default True
            
        Returns:
            Cleaned model response text
            
        Raises:
            PromptValidationError: If prompt fails validation
            LLMError: If generation fails or times out
        """
        start_time = time.time()
        
        # Validate input
        if validate:
            self.validate_prompt(prompt)
        
        # Sanitize input
        sanitized_prompt = self.sanitize_input(prompt)
        
        # Build structured prompt
        if system is None:
            system, formatted_prompt = self.build_prompt(sanitized_prompt, template)
        else:
            formatted_prompt = sanitized_prompt
        
        # Enforce hard token limit
        effective_max_tokens = min(max_tokens, MAX_OUTPUT_TOKENS)
        
        # Check cache first
        cache_key = None
        if use_cache:
            cache_key = LRUCache._make_key(
                formatted_prompt, system, temperature, effective_max_tokens
            )
            cached_response = await self._cache.get(cache_key)
            if cached_response is not None:
                logger.info("Returning cached LLM response", extra={
                    "cache_key": cache_key,
                    "latency_ms": round((time.time() - start_time) * 1000)
                })
                return cached_response
        
        # Acquire semaphore for rate limiting
        semaphore = self._get_semaphore()
        try:
            acquired = await asyncio.wait_for(
                semaphore.acquire(),
                timeout=REQUEST_QUEUE_TIMEOUT
            )
        except asyncio.TimeoutError:
            logger.warning("Request queued too long, rejecting", extra={
                "queue_timeout": REQUEST_QUEUE_TIMEOUT
            })
            raise LLMError("Service busy. Please try again shortly.")
        
        try:
            response = await self._execute_generation(
                formatted_prompt=formatted_prompt,
                system=system,
                temperature=temperature,
                max_tokens=effective_max_tokens,
                strip_markdown=strip_markdown,
                start_time=start_time,
                cache_key=cache_key
            )
            return response
        finally:
            semaphore.release()
    
    async def _execute_generation(
        self,
        formatted_prompt: str,
        system: str,
        temperature: float,
        max_tokens: int,
        strip_markdown: bool,
        start_time: float,
        cache_key: Optional[str]
    ) -> str:
        """Execute the actual LLM generation request."""
        payload = {
            "model": self.model,
            "prompt": formatted_prompt,
            "system": system,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        logger.debug(f"LLM request to {self.model}", extra={
            "prompt_length": len(formatted_prompt),
            "temperature": temperature,
            "max_tokens": max_tokens
        })
        
        try:
            client = await self._get_client(self.base_url)
            response = await client.post(
                "/api/generate",
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract only the response field (discard metadata)
            raw_response = data.get("response", "")
            cleaned_response = self._clean_response(raw_response, strip_markdown)
            
            latency_ms = round((time.time() - start_time) * 1000)
            logger.info("LLM generation successful", extra={
                "model": self.model,
                "response_length": len(cleaned_response),
                "latency_ms": latency_ms
            })
            
            # Cache the response
            if cache_key:
                await self._cache.set(cache_key, cleaned_response)
            
            return cleaned_response
            
        except httpx.TimeoutException as e:
            latency_ms = round((time.time() - start_time) * 1000)
            logger.error("LLM request timed out", extra={
                "timeout_type": type(e).__name__,
                "latency_ms": latency_ms
            })
            raise LLMError("Request timed out. The model may be overloaded.")
        
        except httpx.ConnectError:
            logger.error("Cannot connect to Ollama service")
            raise LLMError("LLM service unavailable.")
        
        except httpx.HTTPStatusError as e:
            logger.error(f"LLM HTTP error: {e.response.status_code}")
            raise LLMError(f"Service error: {e.response.status_code}")
        
        except Exception as e:
            logger.error(f"Unexpected LLM error: {e}", exc_info=True)
            raise LLMError("An unexpected error occurred.")
    
    async def health_check(self) -> bool:
        """
        Check if Ollama service is available.
        Uses fast connect timeout for quick feedback.
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=CONNECT_TIMEOUT) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.warning(f"LLM health check failed: {e}")
            return False
    
    def cache_stats(self) -> dict:
        """Return cache statistics for monitoring."""
        return self._cache.stats()
    
    async def clear_cache(self) -> None:
        """Clear the response cache."""
        await self._cache.clear()


# Singleton instance for reuse
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """
    Get or create the LLM service instance.
    
    Returns:
        LLMService singleton instance
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
