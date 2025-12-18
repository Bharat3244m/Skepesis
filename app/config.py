from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "Skepesis"
    app_version: str = "1.0.0"
    debug: bool = False
    database_url: str = "sqlite:///./skepesis.db"
    secret_key: str = ""
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
