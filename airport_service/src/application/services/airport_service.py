from src.application.mapper.airport_mapper           import map_airport_to_response, map_airport_list_to_response
from src.application.repositories.airport_repository import AirportRepository
from src.core.exceptions.http                        import ResourceNotFoundException
from src.schemas.airport                             import AirportResponse, AirportSearchResponse


class AirportService:

    def __init__(self, repository : AirportRepository):
        self._repository = repository

    def find_by_code(self, code: str) -> AirportResponse:
        try:
            airport = self._repository.find_by_code(code)
            if airport is None:
                raise ResourceNotFoundException(f"The requested airline with IATA/ICAO: {code} is not found.")
            return map_airport_to_response(airport)
        except Exception as e:
            raise e

    def find_by_query(self,
                      q : str,
                      limit : int = 50,
                      offset : int = 0) -> AirportSearchResponse:
        try:
            airports = self._repository.find_by_query(q, limit, offset)
            return AirportSearchResponse(
                results = map_airport_list_to_response(airports)
            )
        except Exception as e:
            raise e

    def find_by_params(self,
                       city : str,
                       country : str,
                       limit : int = 50,
                       offset : int = 0) -> AirportSearchResponse:
        try:
            airports = self._repository.find_by_params(city, country, limit, offset)
            return AirportSearchResponse(
                results = map_airport_list_to_response(airports)
            )
        except Exception as e:
            raise e