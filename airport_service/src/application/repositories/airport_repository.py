from abc    import ABC, abstractmethod
from typing import List

from src.domain.airport import Airport


class AirportRepository(ABC):

    @abstractmethod
    def save(self, airports : List[Airport]) -> None:
        pass

    @abstractmethod
    def get_by_iata(self, iata : str) -> Airport:
        pass