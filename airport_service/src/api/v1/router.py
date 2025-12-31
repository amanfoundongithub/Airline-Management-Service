from fastapi import APIRouter

from src.api.v1.routers.airport_public_router import router as airport_public_router
from src.api.v1.routers.airport_admin_router  import router as airport_admin_router
# Main router
router = APIRouter(prefix = "/api/v1")
router.include_router(airport_public_router)
router.include_router(airport_admin_router)