from src.application.mapper.airport_mapper           import map_airport_to_response
from src.application.repositories.airport_repository import AirportRepository
from src.core.exceptions.http                        import ResourceNotFoundException
from src.schemas.airport                             import AirportResponse


class AirportService:

    def __init__(self, repository : AirportRepository):
        self._repository = repository

    def find_by_iata(self, iata: str) -> AirportResponse:
        try:
            airport = self._repository.get_by_iata(iata)
            if airport is None:
                raise ResourceNotFoundException(f"The requested airline with IATA: {iata} is not found.")
            return map_airport_to_response(airport)
        except Exception as e:
            raise e