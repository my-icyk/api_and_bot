from pathlib import Path

from pydantic_settings import BaseSettings
from typing import List
from urllib.parse import quote_plus


class Settings(BaseSettings):
    DEBUG: bool = True

    APP_NAME: str = "FastAPI Telegram Bot"
    PORT: int = 8005
    BOT_TOKEN: str = "YOUR_BOT_TOKEN_HERE"
    ALLOWED_CHAT_IDS: List[str] = []
    ALLOWED_IPS: List[str] = []
    DB_HOST: str = "host"
    DB_NAME: str = "name"
    DB_DRIVER: str = "ODBC Driver 17 for SQL Server"
    DB_TRUSTED_CONNECTION: str = "yes"

    class Config:
        env_file = str(Path(__file__).resolve().parent / ".env")
        case_sensitive = True

    @property
    def mssql_url(self) -> str:
        driver = quote_plus(self.DB_DRIVER)  # encode spaces
        new_driver = (
            "mssql+pyodbc:///?odbc_connect="
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={self.DB_HOST};"
            f"DATABASE={self.DB_NAME};"
            "Trusted_Connection=yes;"
        )

        # return f"mssql+pyodbc://@{self.DB_HOST}/{self.DB_NAME}?driver={driver}&trusted_connection={self.DB_TRUSTED_CONNECTION}"
        return new_driver


settings = Settings()

# print(settings.mssql_url)
#
# print(str(Path(__file__).resolve().parent / ".env"))
