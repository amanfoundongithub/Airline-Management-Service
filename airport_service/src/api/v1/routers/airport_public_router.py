from fastapi                                  import APIRouter, Depends
from fastapi.params                           import Query
# Local imports from the project
from src.api.dependencies                     import get_airport_service
from src.application.services.airport_service import AirportService
from src.schemas.airport                      import AirportResponse, AirportSearchResponse, AirportCodeValidation
from src.core.settings                        import runtime_settings
from src.core.logging                         import get_logger

# Logger
LOGGER = get_logger(__name__)

# Default values from .env
default_limit_of_results = runtime_settings.DEFAULT_LIMIT_OF_RESULTS
default_offset_of_results = runtime_settings.DEFAULT_OFFSET_OF_RESULTS

# Router for airport (public routes)
router = APIRouter(prefix = "/airports",
                   tags = ["Airport Query Routes (Public)"],
                   deprecated = False,
                   include_in_schema = True)


@router.get(
    "",
    summary =
    """
    Finds airport(s) based on the city & country
    """,
    description =
    f"""
    Use this route to query and find all the airports that are situated in the particular
    city or country (or both). The API will limit the result to {default_limit_of_results} and 
    sets an offset to {default_offset_of_results} by default. You can configure them manually as 
    well as part of the request.
    """
)
async def find_by_params_route(
        city    : str = Query(None, alias = "city"),
        country : str = Query(None, alias = "country"),
        limit   : int = Query(default_limit_of_results,  alias = "limit"),
        offset  : int = Query(default_offset_of_results, alias = "offset"),
        service : AirportService = Depends(get_airport_service)
) -> AirportSearchResponse:
    LOGGER.info("GET /airports received", extra = {"city": city, "country": country})
    return service.find_by_params(city, country, limit, offset)




@router.get(
    "/search",
    summary =
    """
    Fuzzy search to find the list of airports matching the given phrase.
    """,
    description =
    f"""
    Use this route to get the list of airports which corresponds to the given query 
    whether it be from the name, IATA or ICAO code. 
    The API will limit the result to {default_limit_of_results} and 
    sets an offset to {default_offset_of_results} by default. You can configure them manually as 
    well as part of the request.
    """
)
async def find_by_query_route(
        q       : str = Query(..., alias = "q"),
        limit   : int = Query(default_limit_of_results, alias = "limit"),
        offset  : int = Query(default_offset_of_results, alias = "offset"),
        service : AirportService = Depends(get_airport_service)
) -> AirportSearchResponse:
    LOGGER.info("GET /airports/search received", extra = {"q": q})
    return service.find_by_query(q, limit, offset)




@router.get(
    "/validate",
    summary =
    """
    Validate the provided ICAO/IATA code  
    """,
    description =
    f"""
    Use this route to validate the provided ICAO/IATA code. The API will
    verify and return the response, as well as the type of code that is provided.
    """
)
async def validate_code_route(
        code : str = Query(..., alias = "code"),
        service : AirportService = Depends(get_airport_service)
) -> AirportCodeValidation:
    LOGGER.info("GET /airports/validate received", extra = {"code": code})
    return service.validate_code(code)




@router.get(
    "/{code}",
    summary =
    """
    Finds the airport by using ICAO/IATA code
    """,
    description =
    """
    Use this route to find the airport by using ICAO/IATA code. The API
    will verify and return the details of the airport if found.
    """,
)
async def find_by_code_route(
        code    : str,
        service : AirportService = Depends(get_airport_service)
) -> AirportResponse:
    LOGGER.info("GET /airports/{code} received", extra = {"code": code})
    return service.find_by_code(code)