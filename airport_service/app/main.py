from helpers.openflight_loader import OpenFlightLoader
from mappers.openflight_mapper import OpenFlightMapper


loader = OpenFlightLoader() 
mapper = OpenFlightMapper()
print(mapper.map_rows(loader.load_rows())[-1])