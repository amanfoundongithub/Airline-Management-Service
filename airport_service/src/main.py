from fastapi           import FastAPI
from src.api.v1.router import router as v1_router
from src.core.settings import service_settings

# Initialize the FastAPI application
app = FastAPI(title = service_settings.SERVICE_NAME,
              description = service_settings.SERVICE_DESC,
              version = service_settings.SERVICE_VERSION)

# Add the router to the main application
app.include_router(v1_router)