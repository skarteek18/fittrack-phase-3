

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

class Settings(BaseSettings):

    # Application
    APP_NAME: str = "FitTrack"
    APP_VERSION: str = "3.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./fittrack.db"

    # JWT Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"

    # Nutrition
    DEFAULT_DAILY_CALORIE_GOAL: int = 2000

    # Water Tracking
    DEFAULT_WATER_GOAL: int = 2500

    # Workout Tracking
    DEFAULT_WORKOUT_DURATION: int = 30

    # Reminder Settings
    ENABLE_REMINDERS: bool = True

    # External Integrations
    GOOGLE_FIT_ENABLED: bool = False
    APPLE_HEALTH_ENABLED: bool = False

    # Pydantic Settings Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# ==========================================
# CREATE SETTINGS INSTANCE
# ==========================================

settings = Settings()
