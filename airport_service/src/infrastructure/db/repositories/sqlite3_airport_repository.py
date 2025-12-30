from src.application.repositories.airport_repository import AirportRepository
from src.domain.airport                              import Airport
from src.domain.codes                                import IATACode, ICAOCode
from src.infrastructure.db.connection import get_connection


class SQLite3AirportRepository(AirportRepository):

    def save(self, airports : list[Airport]) -> None:
        with get_connection() as cursor:
            cursor.executemany("""
                INSERT OR IGNORE INTO airports VALUES(?,?,?,?,?,?,?,?,?,?)
                           """, [
                               (
                                   a.airport_id,
                                   a.name,
                                   a.city,
                                   a.country,
                                   a.iata.value if a.iata else None,
                                   a.icao.value if a.icao else None,
                                   a.latitude,
                                   a.longitude,
                                   a.altitude_ft,
                                   a.timezone
                               ) for a in airports
                           ])

    def get_by_iata(self, iata : str) -> Airport:
        with get_connection() as cursor:
            row = cursor.execute("""
                                 SELECT *
                                 FROM airports
                                 WHERE iata = ?
                                 """, (iata.upper(),)).fetchone()
            return self._row_to_airport(row)

    def _row_to_airport(self, row) -> Airport:
        if not row:
            return None

        return Airport(
            airport_id=row["airport_id"],
            name=row["name"],
            city=row["city"],
            country=row["country"],
            iata=IATACode(row["iata"]) if row["iata"] else None,
            icao=ICAOCode(row["icao"]) if row["icao"] else None,
            latitude=row["latitude"],
            longitude=row["longitude"],
            altitude_ft=row["altitude_ft"],
            timezone=row["timezone"]
        )
