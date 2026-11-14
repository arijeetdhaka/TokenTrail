from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str = "change-this-later"
    ingest_api_key: str = ""
    frontend_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5500"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()