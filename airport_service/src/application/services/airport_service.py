from src.application.repositories.airport_repository import AirportRepository
from src.core.exceptions.http import ResourceNotFoundException
from src.domain.airport import Airport


class AirportService:

    def __init__(self, repository : AirportRepository):
        self._repository = repository

    def find_by_iata(self, iata: str) -> Airport:
        try:
            airport = self._repository.get_by_iata(iata)
            if airport is None:
                raise ResourceNotFoundException(f"The requested airline with IATA: {iata} is not found.")
            return airport
        except Exception as e:
            raise e