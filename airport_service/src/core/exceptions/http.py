
# Generic exception for all domains
# Corresponds to internal server error
class DomainError(Exception):
    status_code = 500
    def __init__(self, message : str) -> None:
        super().__init__(message)

