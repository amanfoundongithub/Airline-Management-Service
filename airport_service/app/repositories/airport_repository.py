from domain.airport import Airport

from abc import ABC, abstractmethod

class AirportRepository(ABC):
    
    @abstractmethod
    def save_many(self, airports : list[Airport]) -> None:
        pass 

    @abstractmethod
    def get_by_iata(self, iata : str) -> Airport:
        pass