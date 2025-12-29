from pydantic_settings import BaseSettings, SettingsConfigDict

class BasicEnvSettings(BaseSettings):
    """
    This is a standard setting that loads all the variables
    from the .env file.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )