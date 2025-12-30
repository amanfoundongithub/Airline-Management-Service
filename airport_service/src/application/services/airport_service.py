from src.application.mapper.airport_mapper           import map_airport_to_response, map_airport_list_to_response, map_airport_to_validation
from src.application.repositories.airport_repository import AirportRepository
from src.core.exceptions.http                        import ResourceNotFoundException
from src.schemas.airport                             import AirportResponse, AirportSearchResponse, AirportCodeValidation
from src.core.logging                                import get_logger


class AirportService:

    def __init__(self, repository : AirportRepository):
        self._repository = repository
        self._logger = get_logger(__name__)

    def find_by_code(self, code: str) -> AirportResponse:
        self._logger.info(f"Searching airport with code {code}")
        airport = self._repository.find_by_code(code)
        if airport is None:
            self._logger.warning(f"Requested code : {code} not found.")
            raise ResourceNotFoundException(f"The requested airline with IATA/ICAO: {code} is not found.")
        self._logger.info(f"Found airport with IATA/ICAO: {airport.name}")
        return map_airport_to_response(airport)

    def find_by_query(self,
                      q : str,
                      limit : int = 50,
                      offset : int = 0) -> AirportSearchResponse:
        self._logger.info(f"Searching airport with query {q}")
        airports = self._repository.find_by_query(q, limit, offset)
        self._logger.info(f"Found {len(airports)} airports for query: {q}.")
        return AirportSearchResponse(
            results = map_airport_list_to_response(airports)
        )

    def find_by_params(self,
                       city : str,
                       country : str,
                       limit : int = 50,
                       offset : int = 0) -> AirportSearchResponse:
        self._logger.info(f"Searching airport with city={city}, country={country}")
        airports = self._repository.find_by_params(city, country, limit, offset)
        self._logger.info(f"Found {len(airports)} airports for city={city}, country={country}.")
        return AirportSearchResponse(
            results = map_airport_list_to_response(airports)
        )

    def validate_code(self, code : str) -> AirportCodeValidation:
        self._logger.info(f"Validating code {code}")
        airport = self._repository.find_by_code(code)
        if airport is None:
            self._logger.warning(f"Requested code : {code} not found.")
            raise ResourceNotFoundException(f"The requested airline with code: {code} is not found.")
        self._logger.info(f"Found airport with code: {airport.name}")
        return map_airport_to_validation(airport, code)