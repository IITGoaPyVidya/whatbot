import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # WhatsApp Configuration
    whatsapp_business_account_id: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_token: str = ""
    whatsapp_webhook_token: str = "verify_token"

    # LLM API Keys
    google_api_key: str = ""
    groq_api_key: str = ""

    # Groq Model (free tier)
    groq_model: str = "llama3-8b-8192"

    # Google Gemini Model
    gemini_model: str = "gemini-1.5-flash"

    # Application Settings
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # Rate Limiting
    rate_limit_requests: int = 30
    rate_limit_window: int = 60  # seconds

    # Session Management
    session_ttl: int = 3600  # 1 hour in seconds
    max_history_length: int = 10  # max messages to keep per session

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
