from fastapi  import APIRouter
from datetime import datetime

# Router
router = APIRouter(tags = ["Health"])

# Basic ping
@router.get("/")
async def ping():
    return {
        "timestamp" : str(datetime.now()),
        "status" : "OK"
    }
