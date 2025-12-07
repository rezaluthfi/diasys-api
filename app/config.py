# Configuration - Load from environment variables

from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    # Security
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    
    # Token expiry
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "sqlite:///./database.db"
    
    # CORS
    CORS_ORIGINS: str = '["*"]'
    
    @property
    def cors_origins_list(self) -> List[str]:
        try:
            return json.loads(self.CORS_ORIGINS)
        except:
            return ["*"]
    
    # API Info
    API_TITLE: str = "DiaSys - Diabetes Prediction API"
    API_DESCRIPTION: str = "API Prediksi Risiko Diabetes"
    API_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
