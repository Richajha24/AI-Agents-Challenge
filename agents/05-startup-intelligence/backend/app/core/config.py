from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for Startup Intelligence."""

    app_name: str = "Startup Intelligence Agent"
    database_url: str = "sqlite:///./startup_intelligence.db"
    ai_provider: str = "openai"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    claude_model: str = "claude-sonnet-4-20250514"
    gemini_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
