# Generic exception for all domains
class GenericHTTPException(Exception):
    status_code: int

    def __init__(self, message: str) -> None:
        super().__init__(message)