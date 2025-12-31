# Local imports
from src.infrastructure.loaders.openflight_loader import OpenFlightLoader
from src.infrastructure.db.migrate                import run_migrations
from src.api.dependencies                         import get_airport_repository


def bootstrap():
    run_migrations()

    loader = OpenFlightLoader()
    airport_list = loader.load()

    repository = get_airport_repository()
    repository.save(airport_list)