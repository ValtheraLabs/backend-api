from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default="local", alias="APP_ENV")
    app_name: str = Field(default="Valthera Backend API", alias="APP_NAME")
    app_version: str = Field(default="0.2.0", alias="APP_VERSION")
    host: str = Field(default="127.0.0.1", alias="HOST")
    port: int = Field(default=8000, alias="PORT", ge=1, le=65535)

    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    ai_engine_base_url: str = Field(
        default="http://localhost:8001",
        alias="AI_ENGINE_BASE_URL",
    )
    ai_engine_timeout_seconds: float = Field(
        default=5.0,
        alias="AI_ENGINE_TIMEOUT_SECONDS",
        gt=0,
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    database_url: str = Field(default="sqlite:///./valthera.db", alias="DATABASE_URL")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    quote_cache_ttl: int = Field(default=10, alias="QUOTE_CACHE_TTL", ge=0)
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        alias="CORS_ORIGINS",
    )
    rate_limit_requests: int = Field(default=120, alias="RATE_LIMIT_REQUESTS", ge=1)
    rate_limit_window_seconds: int = Field(
        default=60,
        alias="RATE_LIMIT_WINDOW_SECONDS",
        ge=1,
    )

    zerox_api_key: str = Field(default="", alias="ZEROX_API_KEY")
    oneinch_api_key: str = Field(default="", alias="ONEINCH_API_KEY")
    web3_rpc_url_1: str = Field(
        default="https://eth-mainnet.g.alchemy.com/v2/demo",
        alias="WEB3_RPC_URL_1",
    )
    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]


settings = Settings()
