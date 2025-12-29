from helpers.openflight_loader import OpenFlightLoader
from mappers.openflight_mapper import OpenFlightMapper
from db.schema import createAirportTable
from repositories.impl.sqlite3_airport_repository import SQLite3AirportRepository


loader = OpenFlightLoader() 
mapper = OpenFlightMapper()
createAirportTable()

repository = SQLite3AirportRepository()
repository.save_many(mapper.map_rows(loader.load_rows()))
print(repository.get_by_iata("BOM"))