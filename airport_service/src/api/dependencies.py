# Dependency injection
from pyexpat.errors import messages

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

def try_admin_login(
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
    if token != "admin":
        raise HTTPException(
            status_code = 403,
            detail = {
                "message" : "Unauthorized access detected"
            }
        )
    return token