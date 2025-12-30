import pytest
import sqlite3
from pathlib import Path

from src.domain.airport import Airport
from src.domain.codes import IATACode, ICAOCode
from src.infrastructure.db.repositories import sqlite3_airport_repository


# -----------------------------
# Helper: create temp DB schema
# -----------------------------
def create_test_db(db_path: Path):
    conn = sqlite3.connect(db_path)
    conn.execute("""
    CREATE TABLE airports (
        airport_id INTEGER PRIMARY KEY,
        name TEXT,
        city TEXT,
        country TEXT,
        iata TEXT,
        icao TEXT,
        latitude REAL,
        longitude REAL,
        altitude_ft INTEGER,
        timezone TEXT,
        active INTEGER
    );
    """)
    conn.commit()
    conn.close()


# -----------------------------
# Fixture: repo + temp DB
# -----------------------------
@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "airports.db"
    create_test_db(db_path)

    # Patch get_connection in the module
    def test_get_connection():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    sqlite3_airport_repository.get_connection = test_get_connection
    repository = sqlite3_airport_repository.SQLite3AirportRepository()
    return repository, db_path


# -----------------------------
# Helper: sample airports
# -----------------------------
@pytest.fixture
def sample_airports():
    airport1 = Airport(
        airport_id=1, name="Airport One", city="CityA", country="CountryX",
        iata=IATACode("TST"), icao=ICAOCode("TEST"), latitude=12.34, longitude=56.78,
        altitude_ft=100, timezone="UTC", active=True
    )
    airport2 = Airport(
        airport_id=2, name="Airport Two", city="CityB", country="CountryY",
        iata=IATACode("ABC"), icao=ICAOCode("ABCD"), latitude=23.45, longitude=67.89,
        altitude_ft=200, timezone="UTC+1", active=False
    )
    airport3 = Airport(
        airport_id=3, name="Airport Three", city="CityC", country="CountryZ",
        iata=None, icao=None, latitude=1.23, longitude=4.56,
        altitude_ft=50, timezone="UTC+2", active=True
    )
    return [airport1, airport2, airport3]


# -----------------------------
# Test 1: Save single airport
# -----------------------------
def test_save_single_airport(repo, sample_airports):
    repository, db_path = repo
    repository.save([sample_airports[0]])

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM airports").fetchall()
    conn.close()

    assert len(rows) == 1
    row = rows[0]
    assert row["airport_id"] == 1
    assert row["active"] == 1
    assert row["iata"] == "TST"
    assert row["icao"] == "TEST"


# -----------------------------
# Test 2: Save multiple airports
# -----------------------------
def test_save_multiple_airports(repo, sample_airports):
    repository, db_path = repo
    repository.save(sample_airports)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM airports").fetchall()
    conn.close()

    assert len(rows) == 3
    ids = [row["airport_id"] for row in rows]
    assert ids == [1, 2, 3]


# -----------------------------
# Test 3: Ignore duplicates
# -----------------------------
def test_save_ignores_duplicates(repo, sample_airports):
    repository, db_path = repo
    repository.save([sample_airports[0]])
    repository.save([sample_airports[0]])  # duplicate

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM airports").fetchall()
    conn.close()

    assert len(rows) == 1


# -----------------------------
# Test 4: Airports with missing codes
# -----------------------------
def test_save_airport_missing_iata_icao(repo, sample_airports):
    repository, db_path = repo
    repository.save([sample_airports[2]])  # airport3 has None iata/icao

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM airports").fetchone()
    conn.close()

    assert row["iata"] is None
    assert row["icao"] is None


# -----------------------------
# Test 5: Active field True/False
# -----------------------------
def test_save_active_flag(repo, sample_airports):
    repository, db_path = repo
    repository.save(sample_airports[:2])  # first two airports

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM airports").fetchall()
    conn.close()

    assert rows[0]["active"] == 1
    assert rows[1]["active"] == 0


# -----------------------------
# Test 6: Insert after previous save
# -----------------------------
def test_save_additional_airport(repo, sample_airports):
    repository, db_path = repo
    repository.save([sample_airports[0]])
    repository.save([sample_airports[1]])

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM airports").fetchall()
    conn.close()

    assert len(rows) == 2
    ids = [row["airport_id"] for row in rows]
    assert set(ids) == {1, 2}


# -----------------------------
# Test 7: Save empty list does nothing
# -----------------------------
def test_save_empty_list(repo):
    repository, db_path = repo
    repository.save([])

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM airports").fetchall()
    conn.close()

    assert len(rows) == 0
