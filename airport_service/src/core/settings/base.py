from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file for base settings
load_dotenv(find_dotenv())

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