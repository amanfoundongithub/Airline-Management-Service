from typing           import Literal, List
from pydantic import BaseModel, Field
from src.domain.codes import IATACode, ICAOCode

class AirportResponse(BaseModel):
    name: str
    city: str
    country: str

    iata: IATACode | None
    icao: ICAOCode | None

    timezone: str

class AirportSearchResponse(BaseModel):
    results : List[AirportResponse]

class AirportCodeValidation(BaseModel):
    is_valid : bool
    code_type : Literal["IATA", "ICAO"] = Field(default = "IATA")

class AirportCreateRequest(BaseModel):
    name: str
    city: str
    country: str

    iata: str
    icao: str
    timezone: str

    latitude: float
    longitude: float
    altitude_ft: int