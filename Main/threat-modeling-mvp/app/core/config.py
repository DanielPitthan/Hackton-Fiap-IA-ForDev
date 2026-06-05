from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "threat-modeling-mvp"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Vision model
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    VISION_MODEL_PROVIDER: str = "anthropic"
    VISION_MODEL_NAME: str = "claude-3-5-sonnet-20241022"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/threat_modeling.db"

    # Storage
    UPLOAD_DIR: str = "./data/raw"
    PROCESSED_DIR: str = "./data/processed"
    REPORTS_DIR: str = "./reports"
    MAX_UPLOAD_SIZE_MB: int = 20

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Security
    SECRET_KEY: str = "change-me"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
