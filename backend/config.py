from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MASTER_DB: str
    ASYNC_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
