from src.core.settings.base import BasicEnvSettings
from typing import Literal


class RuntimeSettings(BasicEnvSettings):
    """
    Settings for the runtime environment
    """
    SERVICE_PORT: int
    SERVICE_HOST: str
    SERVICE_ENV: Literal["dev", "stage", "prod"]

    DATA_DIRECTORY: str