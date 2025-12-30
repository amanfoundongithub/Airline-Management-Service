from fastapi import APIRouter

from src.api.v1.routers.airport_public_router import router as airport_router

# Main router
router = APIRouter(prefix = "/api/v1")
router.include_router(airport_router)