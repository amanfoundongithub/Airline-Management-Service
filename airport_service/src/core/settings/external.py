from src.core.settings.base import BasicEnvSettings


class OpenFlightsSettings(BasicEnvSettings):
    """
    Settings related to OpenFlights to download the
    airport details for ingestion.
    """
    OPENFLIGHTS_URL: str
    OPENFLIGHTS_PATH: str