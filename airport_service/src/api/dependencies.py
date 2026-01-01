# Dependency injection
from src.core.security import decode_jwt_token
from src.application.repositories.airport_repository               import AirportRepository
from src.application.services.airport_service                      import AirportService
from src.infrastructure.db.repositories.sqlite3_airport_repository import SQLite3AirportRepository

# Token parsing
from fastapi          import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Simple bearer
security = HTTPBearer()

def get_airport_repository() -> AirportRepository:
    return SQLite3AirportRepository()

def get_airport_service() -> AirportService:
    return AirportService(get_airport_repository())

def check_access_permission(permission : str):

    def dependency(
            credentials: HTTPAuthorizationCredentials = Depends(security),
    ) -> str:
        token = credentials.credentials
        if token is None:
            raise HTTPException(
                status_code = 401,
                detail = {
                    "message" : "Authentication credentials missing"
                }
            )
        details = decode_jwt_token(token)
        if details is None or "permissions" not in details:
            raise HTTPException(
                status_code = 401,
                detail = {
                    "message" : "Invalid/expired token"
                }
            )
        if permission not in details["permissions"]:
            raise HTTPException(
                status_code = 403,
                detail = {
                    "message" : f"The user does not have {permission} permission. Please check your permissions"
                }
            )
        return details["email"]

    return dependency