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

    # Security & JWT
    SECRET_KEY: str = "change-this-secret-key-in-production-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutos (más seguro)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 días

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60  # Requests por minuto (general)
    RATE_LIMIT_AUTH_PER_MINUTE: int = 5  # Login attempts por minuto
    RATE_LIMIT_REGISTER_PER_HOUR: int = 3  # Register attempts por hora

    # Email Configuration
    EMAIL_ENABLED: bool = True
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@tienda-asiatica.com"
    EMAIL_FROM_NAME: str = "Tienda Alimentación Asiática"
    EMAIL_USE_TLS: bool = True
    EMAIL_USE_SSL: bool = False

    # Frontend URL (for email links)
    FRONTEND_URL: str = "http://localhost:5173"

    # Password Reset
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 30

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
