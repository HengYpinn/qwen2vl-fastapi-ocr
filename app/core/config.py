"""Application configuration."""

import os
from typing import Set
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings."""
    
    # File storage
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: Set[str] = {".jpg", ".jpeg", ".png", ".pdf"}
    
    # Database
    mongo_uri: str = "mongodb://localhost:27017/"
    database_name: str = "document_ocr_db"
    collection_name: str = "documents"
    
    # API
    api_title: str = "Document OCR API"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # Logging
    log_level: str = "INFO"
    
    @field_validator("upload_dir")
    @classmethod
    def create_upload_dir(cls, v):
        """Ensure upload directory exists."""
        os.makedirs(v, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
