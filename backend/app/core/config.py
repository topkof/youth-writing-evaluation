import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "青少年写作质量评测系统"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/youth_writing"
    SYNC_DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/youth_writing"
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    OSS_ENABLED: bool = False
    OSS_ACCESS_KEY_ID: Optional[str] = None
    OSS_ACCESS_KEY_SECRET: Optional[str] = None
    OSS_BUCKET: Optional[str] = None
    OSS_ENDPOINT: Optional[str] = None
    OSS_REGION: str = "oss-cn-hangzhou"
    
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    MAX_ZIP_FILES: int = 100
    MAX_ZIP_DEPTH: int = 3
    MAX_UNZIP_SIZE: int = 500 * 1024 * 1024
    
    LLM_DEFAULT_MODEL: str = "gpt-4-turbo"
    LLM_DEFAULT_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 4096
    LLM_CONTEXT_LIMIT: int = 128000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
