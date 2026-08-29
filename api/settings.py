"""Environment settings for Remi.

The app reads these values from `.env` or the shell. Keeping them here makes the
rest of the code independent from where the project is running: local Python,
Docker, or a small server.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration values needed by PostgreSQL and Redis."""

    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int = 5432  # PostgreSQL default port.

    REDIS_PORT: int = 6379  # Redis default port.
    REDIS_HOST: str
    REDIS_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
