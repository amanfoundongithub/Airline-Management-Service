from fastapi  import APIRouter
from datetime import datetime

# Router
router = APIRouter(prefix = "/airport")

# Basic ping
@router.get("/iata")
async def findByIATARoute():
    return