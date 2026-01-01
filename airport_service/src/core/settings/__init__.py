from src.core.settings.security import SecuritySettings
from src.core.settings.service import ServiceSettings
from src.core.settings.runtime import RuntimeSettings
from src.core.settings.database import DatabaseSettings
from src.core.settings.external import OpenFlightsSettings

# Instantiate all the settings
service_settings = ServiceSettings()
runtime_settings = RuntimeSettings()
openflights_settings = OpenFlightsSettings()
database_settings = DatabaseSettings()
security_settings = SecuritySettings()