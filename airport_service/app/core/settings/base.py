from pydantic_settings import BaseSettings, SettingsConfigDict


class BasicEnvSettings(BaseSettings):
    """
    Basic settings to load .env variables
    """
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )

