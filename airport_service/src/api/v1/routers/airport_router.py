from fastapi import APIRouter, Depends

from src.api.dependencies                     import get_airport_service
from src.application.services.airport_service import AirportService
from src.schemas.airport                      import AirportResponse, AirportSearchResponse

router = APIRouter(prefix = "/airport", tags = ["Airport"])

@router.get(
    "/search",
    summary = "Searches for airports with the given query",
    description = "This GET request allows any user to find the airport corresponding to "
    " to a given query."
)
async def findByQueryRoute(
        q : str,
        limit : int = 50,
        offset : int = 0,
        service : AirportService = Depends(get_airport_service)
) -> AirportSearchResponse:
    return service.find_by_query(q, limit, offset)

@router.get(
    "/{code}",
    summary = "Finds the airport by using IATA/ICAO Code",
    description = "This GET request allows any user to find the airport corresponding "
                  "to the provided IATA/ICAO Code.",
    response_description = "Airport details corresponding to the IATA/ICAO Code"
)
async def findByCodeRoute(
        code    : str,
        service : AirportService = Depends(get_airport_service)
) -> AirportResponse:
    return service.find_by_code(code)

