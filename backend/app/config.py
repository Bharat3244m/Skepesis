from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "Skepesis"
    app_version: str = "1.0.0"
    debug: bool = False
    database_url: str = "sqlite:///./skepesis.db"
    secret_key: str = ""
    
    # LLM settings (abstracted from specific provider)
    # Local Ollama configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    ollama_timeout: float = 120.0  # seconds
    
    # Future cloud LLM configuration (prepared for deployment)
    llm_provider: str = "ollama"  # "ollama" | "openai" | "anthropic"
    llm_api_key: str = ""  # For cloud providers
    llm_cloud_endpoint: str = ""  # Custom endpoint for cloud

    # 
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_key_change_this_in_prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()


