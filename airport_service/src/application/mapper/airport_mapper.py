from typing import List

from src.domain.airport  import Airport
from src.schemas.airport import AirportResponse, AirportCodeValidation

def map_airport_to_response(airport : Airport) -> AirportResponse:
    return AirportResponse(
        name = airport.name,
        city = airport.city,
        country = airport.country,
        iata = airport.iata,
        icao = airport.icao,
        timezone = airport.timezone
    )

def map_airport_list_to_response(airports : List[Airport]) -> List[AirportResponse]:
    list_airports = []
    for airport in airports:
        list_airports.append(map_airport_to_response(airport))
    return list_airports

def _get_airport_code_type(airport : Airport, code : str) -> str:
    if airport.iata and airport.iata.value == code:
        return "IATA"
    if airport.icao and airport.icao.value == code:
        return "ICAO"
    return "NONE"

def map_airport_to_validation(airport : Airport, code : str) -> AirportCodeValidation:
    return AirportCodeValidation(
        is_valid = True,
        code_type = _get_airport_code_type(airport, code),
    )