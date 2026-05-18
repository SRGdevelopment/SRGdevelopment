from pydantic import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    database_url: str = "sqlite:///./sports_bet_copilot.db"
    redis_url: str = "redis://redis:6379/0"
    openai_api_key: str = ""
    market_api_key: str = ""
    sports_data_api_key: str = ""
    jwt_secret: str = "dev-secret"


settings = Settings()
