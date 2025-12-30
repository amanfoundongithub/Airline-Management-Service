# Local imports
from src.infrastructure.loaders.openflight_loader import OpenFlightLoader
from src.infrastructure.db.migrate                import run_migrations
from src.api.dependencies                         import get_airport_repository
from src.core.logging.config                      import setup_logging

print("[INFO] Starting the application...\n")

# Configure logger before initialization of application
print("[INFO] Setting up logging...")
setup_logging()
print("[INFO] Logger set up COMPLETED!\n")

# Instantiate DB by running migrations
print("[INFO] Setting up database...")
run_migrations()
print("[INFO] database set up COMPLETED!\n")

# Now we will load the data of airport
loader = OpenFlightLoader()
airport_list = loader.load()

# Now ingest this data into SQL
repository = get_airport_repository()
repository.save(airport_list)