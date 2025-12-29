from dataclasses import dataclass
from domain.value_objects import IATACode, ICAOCode


@dataclass
class Airport:
    airport_id: int
    name: str
    city: str
    country: str

    iata: IATACode | None
    icao: ICAOCode | None

    latitude: float
    longitude: float
    altitude_ft: int
    timezone: str