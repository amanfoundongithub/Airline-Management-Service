from src.core.settings.base import BasicEnvSettings

class SecuritySettings(BasicEnvSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM : str = 'HS256'