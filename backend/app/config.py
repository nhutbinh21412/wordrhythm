import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "WordRhythm: Boss Battle & Spaced Repetition"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "wordrhythm-super-secret-jwt-key-2026-secure-token")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./wordrhythm.db")

settings = Settings()
