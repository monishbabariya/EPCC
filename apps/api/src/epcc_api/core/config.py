"""Application settings loaded from environment.

Sourced from `.env.local` in dev, real environment vars in prod.
See `.env.example` at the repo root for the full key list.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.local", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    env: str = Field(default="dev", alias="EPCC_ENV")
    api_host: str = Field(default="0.0.0.0", alias="EPCC_API_HOST")
    api_port: int = Field(default=8000, alias="EPCC_API_PORT")
    api_log_level: str = Field(default="info", alias="EPCC_API_LOG_LEVEL")
    cors_origins_raw: str = Field(default="http://localhost:5173", alias="EPCC_API_CORS_ORIGINS")

    database_url: str = Field(
        default="postgresql+asyncpg://epcc:epcc_dev_password@localhost:5432/epcc",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    celery_broker_url: str = Field(
        default="redis://localhost:6379/1", alias="CELERY_BROKER_URL"
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/2", alias="CELERY_RESULT_BACKEND"
    )

    minio_endpoint: str = Field(default="http://localhost:9000", alias="MINIO_ENDPOINT")
    minio_access_key: str = Field(default="minio", alias="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="miniopassword", alias="MINIO_SECRET_KEY")
    minio_bucket_photos: str = Field(default="epcc-photos", alias="MINIO_BUCKET_PHOTOS")
    minio_bucket_documents: str = Field(default="epcc-documents", alias="MINIO_BUCKET_DOCUMENTS")
    minio_bucket_exports: str = Field(default="epcc-exports", alias="MINIO_BUCKET_EXPORTS")

    keycloak_url: str = Field(default="http://localhost:8080", alias="KEYCLOAK_URL")
    keycloak_realm: str = Field(default="epcc", alias="KEYCLOAK_REALM")
    keycloak_client_id: str = Field(default="epcc-api", alias="KEYCLOAK_CLIENT_ID")
    keycloak_client_secret: str = Field(
        default="dev-client-secret-change-me", alias="KEYCLOAK_CLIENT_SECRET"
    )

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origins_raw.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
