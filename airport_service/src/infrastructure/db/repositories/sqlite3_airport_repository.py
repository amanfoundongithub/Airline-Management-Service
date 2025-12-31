from typing import List

from src.application.repositories.airport_repository import AirportRepository
from src.domain.airport                              import Airport
from src.domain.codes                                import IATACode, ICAOCode
from src.infrastructure.db.connection                import get_connection


class SQLite3AirportRepository(AirportRepository):

    def save(self, airports : list[Airport]) -> None:
        with get_connection() as cursor:
            cursor.executemany("""
                INSERT OR IGNORE INTO airports VALUES(?,?,?,?,?,?,?,?,?,?,?)
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
                                   a.timezone,
                                   1 if a.active else 0
                               ) for a in airports
                           ])

    def save_one(self, a : Airport) -> Airport:
        with get_connection() as cursor:
            executor = cursor.cursor()
            executor.execute(
                """
                INSERT INTO airports (name, city, country, iata, icao,
                                      latitude, longitude, altitude_ft, timezone, active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    a.name,
                    a.city,
                    a.country,
                    a.iata.value if a.iata else None,
                    a.icao.value if a.icao else None,
                    a.latitude,
                    a.longitude,
                    a.altitude_ft,
                    a.timezone,
                    1 if a.active else 0
                )
            )
            a.airport_id = executor.lastrowid
            return a

    def find_by_code(self, code : str, mask_details : bool = False) -> Airport:
        with get_connection() as cursor:
            if mask_details:
                query = """
                SELECT *
                FROM airports
                WHERE active=1 AND (iata = ? OR icao = ?)
                """
            else:
                query = """
                SELECT *
                FROM airports
                WHERE iata = ? OR icao = ?
                """
            row = cursor.execute(query, (code.upper(), code.upper())).fetchone()
            return self._row_to_airport(row)

    def find_by_params(self,
                       city : str,
                       country : str,
                       limit : int = 50,
                       offset : int = 0) -> List[Airport]:
        with get_connection() as cursor:
            query = """
            SELECT * FROM airports WHERE active=1"""
            params = []
            if city:
                query += f""" AND city = ? COLLATE NOCASE """
                params.append(city)
            if country:
                query += f""" AND country = ? COLLATE NOCASE """
                params.append(country)

            query += f""" LIMIT ? OFFSET ?"""
            params.extend([limit, offset])

            rows = cursor.execute(query, params).fetchall()
            return [self._row_to_airport(row) for row in rows]

    def find_by_query(self,
                      q : str,
                      limit : int = 50,
                      offset : int = 0) -> List[Airport]:
        with get_connection() as cursor:
            query = """
                SELECT *
                FROM airports
                WHERE active = 1
                AND (
                    LOWER(name) LIKE LOWER(?)
                    OR LOWER(city) LIKE LOWER(?)
                    OR iata LIKE ?
                    OR icao LIKE ?
                    )
                LIMIT ? OFFSET ?"""
            search = f"%{q}%"
            params = [search, search, search, search, limit, offset]
            rows = cursor.execute(query, params).fetchall()
            return [self._row_to_airport(row) for row in rows]

    def update_status(self, id : int, status : bool) -> None:
        status_int = 1 if status else 0
        with get_connection() as cursor:
            cursor.execute("""
            UPDATE airports SET active = ? WHERE airport_id=?""",
                           (status_int, id))


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
            timezone=row["timezone"],
            active = row["active"] == 1
        )
