from src.application.repositories.airport_repository import AirportRepository
from src.domain.airport import Airport


class AirportService:

    def __init__(self, repository : AirportRepository):
        self._repository = repository

    def find_by_iata(self, iata: str) -> Airport:
        return self._repository.get_by_iata(iata)