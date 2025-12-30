from pathlib import Path
from src.infrastructure.db.connection import get_connection

MIGRATIONS_DIR = Path(__file__).parent / "migrations"

def run_migrations():
    conn = get_connection()
    cursor = conn.cursor()
    for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
        print(f"Running migration {sql_file.name}")
        with sql_file.open() as f:
            cursor.executescript(f.read())
    conn.commit()
    conn.close()
