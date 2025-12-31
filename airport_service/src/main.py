from fastapi                   import FastAPI

from src.api.exception_handler import generic_exception_handler
from src.api.v1.router         import router as v1_router
from src.api.health_router     import router as health_router
from src.core.exceptions.http  import GenericHTTPException
from src.core.settings         import service_settings
from src.bootstrap             import bootstrap

# Initialize the FastAPI application
app = FastAPI(title = service_settings.SERVICE_NAME,
              description = service_settings.SERVICE_DESC,
              version = service_settings.SERVICE_VERSION)

app.add_event_handler("startup", bootstrap)
# Add exception handler for generic use
app.add_exception_handler(GenericHTTPException, generic_exception_handler)

# Add the router to the main application
app.include_router(health_router)
app.include_router(v1_router)

