from fastapi import APIRouter
from datetime import datetime

from src.schemas.health import PingResponse
from src.core.settings  import service_settings

router = APIRouter(tags = ["Health"])

@router.get(
    "/ping",
    summary = "Ping",
    description = "Pings the server to know if it is up or not"
)
async def ping() -> PingResponse:
    return PingResponse(
        timestamp = datetime.now(),
        name = service_settings.SERVICE_NAME,
        status = "Running",
        version = "v1"
    )

@router.get(
    "/health",
    summary = "Health Check",
    description = "Health Check",
)
async def health_check() -> PingResponse:
    # TODO: Implement health check of DB
    pass