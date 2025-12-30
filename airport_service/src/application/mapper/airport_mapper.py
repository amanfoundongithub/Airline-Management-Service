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