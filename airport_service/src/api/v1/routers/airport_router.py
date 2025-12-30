from fastapi import APIRouter, Depends

from src.api.dependencies                     import get_airport_service
from src.application.services.airport_service import AirportService

# Router
router = APIRouter(prefix = "/airport", tags = ["Airport"])

# Finds an airline by IATA Code
@router.get(
    "/find_by_iata",
    summary = "Finds the airport by using IATA Code",
    description = "This GET request allows any user to find the airport corresponding "
                  "to the provided IATA Code.",
    response_description = "Airport details corresponding to the IATA Code"
)
async def findByIATARoute(iata    : str,
                          service : AirportService = Depends(get_airport_service)):
    return service.find_by_iata(iata)