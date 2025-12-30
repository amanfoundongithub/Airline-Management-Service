from pathlib import Path

from src.core.settings import database_settings
import sqlite3

def get_connection() -> sqlite3.Connection:
    # Make the path if it ain't there
    db_path = Path(database_settings.SQLITE_DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(database_settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn