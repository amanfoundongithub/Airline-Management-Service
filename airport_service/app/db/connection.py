import sqlite3
from core.settings import database_settings

def connectToSQLiteDB():
    connection = sqlite3.connect(database_settings.SQLITE_DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
