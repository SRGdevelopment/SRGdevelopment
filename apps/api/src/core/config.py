from pydantic import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    app_vertical: str = "sports"
    database_url: str = ""
    redis_url: str = "redis://redis:6379/0"
    openai_api_key: str = ""
    market_api_key: str = ""
    sports_data_api_key: str = ""
    jwt_secret: str = "dev-secret"

    @property
    def resolved_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return f"sqlite:///./{self.app_vertical}_copilot.db"


settings = Settings()
