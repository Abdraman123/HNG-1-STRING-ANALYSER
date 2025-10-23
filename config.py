"""
Configuration management for the application.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://hng_user:password@localhost:5432/string_analyzer"
    )
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # App Metadata
    APP_NAME: str = "String Analyzer API"
    APP_VERSION: str = "1.0.0"


settings = Settings()


# Validation
def validate_settings():
    """Validate required settings."""
    if "your_secure_password" in settings.DATABASE_URL or "password" in settings.DATABASE_URL:
        print("\n⚠️  WARNING: Using default database password!")
        print("Please update DATABASE_URL in .env file\n")


validate_settings()