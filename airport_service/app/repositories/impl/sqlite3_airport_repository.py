from repositories.airport_repository import AirportRepository
from domain.airport                  import Airport
from domain.value_objects            import IATACode, ICAOCode
from db.connection                   import connectToSQLiteDB

class SQLite3AirportRepository(AirportRepository):

    def save_many(self, airports : list[Airport]) -> None:
        with connectToSQLiteDB() as cursor:
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
        with connectToSQLiteDB() as cursor:
            row = cursor.execute("""
                SELECT * FROM airports WHERE iata=?
                                """, (iata.upper(),)).fetchone()
            return self._row_to_airport(row) 
            
    
    def _row_to_airport(self, row : list) -> Airport:
        if not row: 
            return None
        
        return Airport(
            airport_id = row["airport_id"],
            name = row["name"],
            city = row["city"],
            country = row["country"],
            iata = IATACode(row["iata"]) if row["iata"] else None,
            icao = ICAOCode(row["icao"]) if row["icao"] else None, 
            latitude = row["latitude"],
            longitude = row["longitude"],
            altitude_ft = row["altitude_ft"],
            timezone = row["timezone"]
        )