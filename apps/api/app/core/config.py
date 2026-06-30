"""Application configuration management."""
from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = Field(default="CareerOS API", description="Application name")
    app_env: str = Field(default="development", description="Application environment")
    debug: bool = Field(default=False, description="Debug mode")
    demo_mode: bool = Field(default=False, description="Demo mode with seeded data")
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")

    # Server
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=4, description="Number of workers")

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./careeros.db",
        description="Database connection URL"
    )
    database_pool_size: int = Field(default=20, description="Database pool size")
    database_max_overflow: int = Field(default=10, description="Database max overflow")

    # Supabase
    supabase_url: str = Field(default="", description="Supabase URL")
    supabase_anon_key: str = Field(default="", description="Supabase anonymous key")
    supabase_service_role_key: str = Field(default="", description="Supabase service role key")

    # JWT
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for JWT"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration")
    refresh_token_expire_days: int = Field(default=7, description="Refresh token expiration")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000"], description="CORS allowed origins"
    )

    # Lemma SDK
    lemma_api_key: str = Field(default="", description="Lemma API key")
    lemma_environment: str = Field(default="development", description="Lemma environment")

    # OpenAI / OpenRouter
    careeros_api_key: str = Field(default="", env="CAREEROS_API_KEY", description="CareerOS API key for AI services")
    openai_api_key_fallback: str = Field(default="", env="OPENAI_API_KEY", description="Fallback OpenAI API key")
    use_openrouter: bool = Field(default=True, description="Use OpenRouter instead of direct OpenAI")
    
    @property
    def openai_api_key(self) -> str:
        """Get the API key, preferring CAREEROS_API_KEY over OPENAI_API_KEY."""
        return self.careeros_api_key or self.openai_api_key_fallback

    # Logging
    log_level: str = Field(default="INFO", description="Log level")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.strip("[]").split(",")]
        return v

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
