from abc                import ABC, abstractmethod
from typing             import List
from src.domain.airport import Airport


class AirportRepository(ABC):

    @abstractmethod
    def save(self,
             airports : List[Airport]) -> None:
        pass

    @abstractmethod
    def save_one(self, airport : Airport) -> Airport:
        pass

    @abstractmethod
    def find_by_code(self,
                     code : str,
                     mask_details : bool = False) -> Airport:
        pass

    @abstractmethod
    def find_by_params(self,
                       city : str,
                       country : str,
                       limit : int = 50,
                       offset : int = 0) -> List[Airport]:
        pass

    @abstractmethod
    def find_by_query(self,
                      q : str,
                      limit : int = 50,
                      offset : int = 0) -> List[Airport]:
        pass

    @abstractmethod
    def update_status(self, id : int, status : bool) -> None:
        pass