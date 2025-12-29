from fastapi import APIRouter

from src.api.v1.routers.health_router import router as health_router

# Main router
router = APIRouter(prefix = "/api/v1")
router.include_router(health_router)
