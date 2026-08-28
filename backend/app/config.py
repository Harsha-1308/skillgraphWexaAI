"""Application configuration loaded from environment variables."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """All application settings read from environment variables."""

    # CognoDB / Neo4j connection
    cognodb_uri: str = "bolt+s://localhost:7687"
    cognodb_username: str = "cognodb"
    cognodb_password: str = ""

    # Application
    app_name: str = "SkillGraph API"
    app_version: str = "1.0.0"
    debug: bool = False

    # CORS — comma-separated list of allowed origins
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
