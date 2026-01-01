from fastapi import APIRouter

from app.api.v1.routers.public_user_router import router as public_user_router
from app.api.v1.routers.authenticated_user_router import router as authenticated_user_router

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(public_user_router)
router.include_router(authenticated_user_router)