# Dependency injection
from src.application.repositories.airport_repository import AirportRepository
from src.infrastructure.db.repositories.sqlite3_airport_repository import SQLite3AirportRepository


def get_airport_repository() -> AirportRepository:
    return SQLite3AirportRepository()