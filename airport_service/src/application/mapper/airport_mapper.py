from typing import List

from src.domain.airport  import Airport
from src.schemas.airport import AirportResponse

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