from pydantic         import BaseModel
from src.domain.codes import IATACode, ICAOCode

class AirportResponse(BaseModel):
    name: str
    city: str
    country: str

    iata: IATACode | None
    icao: ICAOCode | None

    timezone: str
