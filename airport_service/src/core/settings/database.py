from src.core.settings.base import BasicEnvSettings

class DatabaseSettings(BasicEnvSettings):
    """
    Settings related to database connection and operations
    """
    SQLITE_DB_PATH : str