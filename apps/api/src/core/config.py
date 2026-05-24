from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "dev"
    database_url: str = "sqlite:///./sports_bet_copilot.db"
    redis_url: str = "redis://redis:6379/0"
    redis_result_backend: str = "redis://redis:6379/1"
    openai_api_key: str = ""
    market_api_key: str = ""
    sports_data_api_key: str = ""
    jwt_secret: str = "dev-secret"
    cors_allow_origins: list[str] = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]


settings = Settings()
