import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    APP_NAME: str = "AI Chat Service"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered chatbot API for customer handling in fashion business."
    CONTACT: str = {
        "name": "Parvez Hossen",
        "email": "ph.cse.bd@gmail.com"
    }
    license_info = {

    }
    ENV: str = os.getenv('ENV', 'local')

    # Security
    SECRET_KEY: str

    # Database
    DATABASE_URL: str | None = None

    # LLM Model
    LLM_MODEL: str = "mistral"

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
