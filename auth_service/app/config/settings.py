from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal


# Expose only settings
__all__ = ["settings"] 

class AppSettings(BaseSettings):
    """
    This is a settings configuration for the application
    """

    ENVIRONMENT: Literal["dev", "test", "prod"] = "dev"
    SERVICE_NAME: str = "auth_service"

    DEBUG : bool = Field(default = False, validation_alias = "DEBUG_MODE")

    LOG_LEVEL : str = "info"


class MongoSettings(BaseSettings):
    """
    Defines the settings for MongoDB
    """

    uri : str = Field(validation_alias = "MONGO_URI")
    db_name : str = Field(validation_alias = "MONGO_DB_NAME")
    user_collection_name : str = Field(validation_alias = "MONGO_COLLECTION_NAME")


class SecuritySettings(BaseSettings):
    """
    Defines the settings for security params
    """

    jwt_secret_key : str = Field(validation_alias = "JWT_SECRET_KEY")
    jwt_algorithm  : str = "HS256"
    access_token_expiration_in_minutes : int = 30

    password_hash_rounds : int = 12 


class Settings(BaseSettings):
    """
    Global settings object with all configurations
    """

    app : AppSettings          = Field(default_factory = AppSettings)
    mongo: MongoSettings       = Field(default_factory = MongoSettings)
    security: SecuritySettings = Field(default_factory = SecuritySettings)

    model_config = SettingsConfigDict(
        env_file = '.env',
        env_file_encoding = 'utf-8',
        case_sensitive = True, 
        extra = 'ignore'
    )


settings = Settings() 
