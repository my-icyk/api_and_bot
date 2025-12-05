from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Telegram Bot"
    PORT: int = 8005
    DATABASE_URL: str = "sqlite:///./app.db"
    BOT_TOKEN: str = "YOUR_BOT_TOKEN_HERE"
    ALLOWED_CHAT_IDS: List[str] = []
    ALLOWED_IPS: List[str] = []

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
