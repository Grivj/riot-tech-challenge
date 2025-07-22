from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Riot Tech Challenge"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Take Home Tech Challenge for riot"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
