from src.core.settings.base import BasicEnvSettings


class ServiceSettings(BasicEnvSettings):
    """
    Settings related to service details for application
    """
    SERVICE_NAME: str
    SERVICE_DESC: str
