from domain.airport       import Airport
from domain.value_objects import IATACode, ICAOCode
from mappers.exceptions   import OpenFlightsMappingError


class OpenFlightMapper:

    def __init__(self):
        pass 

    def map_rows(self, row : list[list[str]]) -> list[Airport]:
        list_of_airports = []
        for i in row:
            list_of_airports.append(self.map(i))
        return list_of_airports

    def map(self, row : list[str]) -> Airport:
        try:
            return Airport(
                airport_id=int(row[0]),
                name=row[1].strip(),
                city=row[2].strip(),
                country=row[3].strip(),
                iata=self._parse_iata(row[4]),
                icao=self._parse_icao(row[5]),
                latitude=float(row[6]),
                longitude=float(row[7]),
                altitude_ft=int(row[8]),
                timezone=row[9],
            )
        except Exception as e:
            print(row) 
            raise OpenFlightsMappingError(e)
    
    def _parse_iata(self, value : str):
        value = value.strip()
        try:
            return IATACode(value)
        except:
            return None
    
    def _parse_icao(self, value : str):
        value = value.strip()
        try:
            return ICAOCode(value) 
        except:
            return None 
    
        
