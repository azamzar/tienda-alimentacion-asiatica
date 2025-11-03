from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses Pydantic Settings for validation and type safety.
    """
    # Application
    APP_NAME: str = "Tienda Alimentación Asiática API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # File uploads
    UPLOAD_DIR: Path = Path("uploads")
    PRODUCTS_UPLOAD_DIR: Path = Path("uploads/products")
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB

    # Database
    POSTGRES_USER: str = "tienda_user"
    POSTGRES_PASSWORD: str = "tienda_password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "tienda_asiatica"
    DATABASE_URL: Optional[str] = None

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 300  # 5 minutes default

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
    ]

    # API
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def get_database_url(self) -> str:
        """Construct database URL from components"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


# Create a global settings instance
settings = Settings()
