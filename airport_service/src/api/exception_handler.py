from fastapi                  import Request
from fastapi.responses        import JSONResponse

from src.core.exceptions.http import GenericHTTPException

# Generic handler for all kinds of exceptions
def generic_exception_handler(request : Request, exception : GenericHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code = exception.status_code,
        content = {
            "error" : exception.__class__.__name__,
            "message" : str(exception)
        }
    )
