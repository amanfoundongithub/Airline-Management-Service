from fastapi                                  import APIRouter, Depends
from fastapi.params                           import Query

# Local imports from the project
from src.api.dependencies                     import get_airport_service, try_admin_login
from src.application.services.airport_service import AirportService
from src.domain.airport                       import Airport
from src.schemas.airport                      import AirportCreateRequest
from src.core.settings                        import runtime_settings
from src.core.logging                         import get_logger

# Logger
LOGGER = get_logger(__name__)

# Default values from .env
default_limit_of_results = runtime_settings.DEFAULT_LIMIT_OF_RESULTS
default_offset_of_results = runtime_settings.DEFAULT_OFFSET_OF_RESULTS

# Router for airport (admin routes)
router = APIRouter(prefix = "/airport",
                   tags = ["Airport Management Routes (Admin)"],
                   deprecated = False,
                   include_in_schema = True)

@router.post(
    "/create",
    summary =
    """
    Create an airport given the details
    """,
    description =
    """
    Use this API endpoint to create an airport. The airport will be created and the
    message will be sent to the server upon the success.
    """
)
async def create_airport_route(
        request : AirportCreateRequest,
        user_id : str = Depends(try_admin_login),
        service : AirportService = Depends(get_airport_service)
) -> Airport:
    return service.create_airport(request)