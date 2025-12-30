# Local imports
from src.infrastructure.loaders.openflight_loader import OpenFlightLoader
from src.infrastructure.db.migrate                import run_migrations
from src.api.dependencies                         import get_airport_repository
from src.core.logging.config                      import setup_logging

# Configure logger before initialization of application
setup_logging()

# Instantiate DB by running migrations
run_migrations()

# Now we will load the data of airport
loader = OpenFlightLoader()
airport_list = loader.load()

# Now ingest this data into SQL
repository = get_airport_repository()
repository.save(airport_list)