from src.core.settings import database_settings
import sqlite3

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(database_settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn