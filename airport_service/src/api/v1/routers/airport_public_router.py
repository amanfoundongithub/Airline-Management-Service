from fastapi                                  import APIRouter, Depends

# Local imports from the project
from src.api.dependencies                     import get_airport_service
from src.application.services.airport_service import AirportService
from src.schemas.airport                      import AirportResponse, AirportSearchResponse, AirportCodeValidation

# Router for airport (public routes)
router = APIRouter(prefix = "/airport",
                   tags = ["Airport (Public)"],
                   deprecated = False,
                   include_in_schema = True)


@router.get(
    "",
    summary = "Searches for airport using given parameters",
    description = "This GET request allows any user to find the airport corresponding "
    " to the provided query"
)
async def findByParamsRoute(
        city : str = None,
        country : str = None,
        limit : int = 50,
        offset : int = 0,
        service : AirportService = Depends(get_airport_service)
) -> AirportSearchResponse:
    return service.find_by_params(city, country, limit, offset)

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
    "/validate",
    summary = "Validates the airport code (ICAO/IATA)",
    description = "This GET request allows any user to validate the airport code"
)
async def validateCodeRoute(
        code : str,
        service : AirportService = Depends(get_airport_service)
) -> AirportCodeValidation:
    return service.validate_code(code)

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