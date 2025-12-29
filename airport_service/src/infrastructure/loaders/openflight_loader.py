from src.core.settings   import openflights_settings
from src.core.exceptions import OpenFlightParseError, OpenFlightDownloadError, OpenFlightsMappingError
from src.domain.airport  import Airport
from src.domain.codes    import IATACode, ICAOCode

from pathlib           import Path
from typing            import List

import requests
import csv



class OpenFlightLoader:
    def __init__(self):
        self.url = openflights_settings.OPENFLIGHTS_URL
        self.path = Path(openflights_settings.OPENFLIGHTS_PATH)

    def load(self) -> List[Airport]:
        path = self.__ensure_file()
        rows = self.__load_rows(path)
        return self.__map_rows(rows)

    def __ensure_file(self) -> Path:
        if self.path.exists():
            return self.path
        self.path.parent.mkdir(parents = True, exist_ok = True)

        try:
            response = requests.get(self.url, timeout = 30)
            response.raise_for_status()
        except Exception as e:
            raise OpenFlightDownloadError(e)

        self.path.write_bytes(response.content)
        return self.path

    def __load_rows(self, path : Path) -> List[List[str]]:
        try:
            with path.open(encoding = "utf-8") as f:
                reader = csv.reader(f)
                return list(reader)
        except Exception as e:
            raise OpenFlightParseError(e)

    def __map_rows(self, row : List[List[str]]) -> List[Airport]:
        list_of_airports = []
        for i in row:
            list_of_airports.append(self.__map(i))
        return list_of_airports

    def __map(self, row : List[str]) -> Airport:
        try:
            return Airport(
                airport_id=int(row[0]),
                name=row[1].strip(),
                city=row[2].strip(),
                country=row[3].strip(),
                iata=self.__parse_iata(row[4]),
                icao=self.__parse_icao(row[5]),
                latitude=float(row[6]),
                longitude=float(row[7]),
                altitude_ft=int(row[8]),
                timezone=row[9],
            )
        except Exception as e:
            print(row)
            raise OpenFlightsMappingError(e)

    def __parse_iata(self, value: str):
        value = value.strip()
        try:
            return IATACode(value)
        except:
            return None

    def __parse_icao(self, value: str):
        value = value.strip()
        try:
            return ICAOCode(value)
        except:
            return None