from fastapi import APIRouter, Depends
from fastapi.params import Query

# Local imports from the project
from src.api.dependencies import get_airport_service, check_access_permission
from src.application.services.airport_service import AirportService
from src.domain.airport import Airport
from src.schemas.airport import AirportCreateRequest
from src.schemas.common import SuccessMessage
from src.core.settings import runtime_settings
from src.core.logging import get_logger

# Logger
LOGGER = get_logger(__name__)

# Default values from .env
default_limit_of_results = runtime_settings.DEFAULT_LIMIT_OF_RESULTS
default_offset_of_results = runtime_settings.DEFAULT_OFFSET_OF_RESULTS

# Router for airport (admin routes)
router = APIRouter(prefix="/airport",
                   tags=["Airport Management Routes (Admin)"],
                   deprecated=False,
                   include_in_schema=True)


@router.get(
    "",
    summary =
    """
    Fetches the airport details along with their id
    """,
    description =
    """
    This route is designed to help fetch the details of the airport 
    for the admin, who wishes to see the all details of an airport
    by using the IATA/ICAO code.
    """
)
async def get_airport_route(
        code : str = Query(..., description="IATA/ICAO code"),
        user_id: str = Depends(check_access_permission("airport.view")),
        service: AirportService = Depends(get_airport_service)
) -> Airport:
    LOGGER.info(f"GET /airport/{code} received from {user_id}")
    return service.find_by_code(code, mask_details = False)



@router.post(
    "/create",
    summary=
    """
    Create an airport given the details
    """,
    description=
    """
    Use this API endpoint to create an airport. The airport will be created and the
    message will be sent to the server upon the success.
    """
)
async def create_airport_route(
        request: AirportCreateRequest,
        user_id: str = Depends(check_access_permission("airport.create")),
        service: AirportService = Depends(get_airport_service)
) -> Airport:
    LOGGER.info(f"POST /airport/{request.code} received")
    return service.create_airport(request)


@router.get(
    "/{id}",
    summary =
    """
    Fetches airport data based on ID
    """
)
async def get_airport_by_id_route(
        id: int,
        user_id: str = Depends(check_access_permission("airport.view")),
        service: AirportService = Depends(get_airport_service)
) -> Airport:
    LOGGER.info(f"GET /airport/{id} received")
    return service.find_by_id(id)


@router.delete(
    "/{id}/deactivate",
    summary=
    """
    Soft deletes an airport using its unique ID
    """,
    description=
    """
    Use this route to delete an airport by rendering it inactive, so that
    it does not delete all the API endpoints that depends on it.
    """
)
async def delete_airport_route(
        id: int,
        user_id: str = Depends(check_access_permission("airport.update")),
        service: AirportService = Depends(get_airport_service)
) -> SuccessMessage:
    LOGGER.info(f"DELETE /airport/{id} received")
    service.delete_airport(id)
    return SuccessMessage()

@router.patch(
    "/{id}/activate",
    summary=
    """
    Activates an airport by using its unique ID
    """,
    description=
    """
    Use this API to activate the airport by using its IATA/ICAO code
    """
)
async def activate_airport_route(
        id: int,
        user_id: str = Depends(check_access_permission("airport.update")),
        service: AirportService = Depends(get_airport_service)
) -> SuccessMessage:
    LOGGER.info(f"PATCH /airport/{id} received")
    service.activate_airport(id)
    return SuccessMessage()
