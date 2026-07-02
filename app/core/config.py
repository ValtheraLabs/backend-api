from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Valthera Backend API"
    app_env: str = "local"
    api_v1_prefix: str = "/v1"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    ai_engine_base_url: str = "http://127.0.0.1:8001"
    ai_engine_timeout_seconds: float = 5.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
