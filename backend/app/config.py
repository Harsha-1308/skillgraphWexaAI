"""Application configuration loaded from environment variables."""
import os
from pathlib import Path
from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Robustly find and load .env from current directory, backend directory, or project root
_backend_dir = Path(__file__).resolve().parent.parent
_root_dir = _backend_dir.parent
for env_path in [
    Path.cwd() / ".env",
    _backend_dir / ".env",
    _root_dir / ".env",
]:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
        break


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

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()

