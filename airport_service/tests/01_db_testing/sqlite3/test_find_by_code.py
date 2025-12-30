import pytest
import sqlite3
from pathlib import Path

from src.domain.airport import Airport
from src.domain.codes import IATACode, ICAOCode
from src.infrastructure.db.repositories import sqlite3_airport_repository


# -----------------------------
# Fixture: repo + temp DB
# -----------------------------
def create_airports_table(db_path):
    """Create airports table in the SQLite database."""
    with sqlite3.connect(db_path) as conn:
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

def patched_get_connection(db_path):
    """Return a SQLite connection with row_factory set to Row."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "airports.db"
    create_airports_table(db_path)

    # Patch repository connection
    sqlite3_airport_repository.get_connection = lambda: patched_get_connection(db_path)

    repository = sqlite3_airport_repository.SQLite3AirportRepository()
    return repository, db_path


# -----------------------------
# Fixture: sample airports
# -----------------------------
@pytest.fixture
def sample_airports():
    return [
        Airport(
            airport_id=1, name="Airport One", city="CityA", country="CountryX",
            iata=IATACode("TST"), icao=ICAOCode("TEST"), latitude=12.34, longitude=56.78,
            altitude_ft=100, timezone="UTC", active=True
        ),
        Airport(
            airport_id=2, name="Airport Two", city="CityB", country="CountryY",
            iata=IATACode("ABC"), icao=ICAOCode("ABCD"), latitude=23.45, longitude=67.89,
            altitude_ft=200, timezone="UTC+1", active=False
        ),
        Airport(
            airport_id=3, name="Airport Three", city="CityC", country="CountryZ",
            iata=None, icao=None, latitude=1.23, longitude=4.56,
            altitude_ft=50, timezone="UTC+2", active=True
        )
    ]


# -----------------------------
# Test 1: Find by IATA
# -----------------------------
def test_find_by_iata(repo, sample_airports):
    repository, db_path = repo
    repository.save(sample_airports)

    airport = repository.find_by_code("TST")
    assert airport is not None
    assert airport.airport_id == 1
    assert airport.name == "Airport One"


# -----------------------------
# Test 2: Find by ICAO
# -----------------------------
def test_find_by_icao(repo, sample_airports):
    repository, db_path = repo
    repository.save(sample_airports)

    airport = repository.find_by_code("ABCD")
    assert airport is not None
    assert airport.airport_id == 2
    assert airport.name == "Airport Two"


# -----------------------------
# Test 3: Case insensitive search
# -----------------------------
def test_find_by_code_case_insensitive(repo, sample_airports):
    repository, db_path = repo
    repository.save(sample_airports)

    airport = repository.find_by_code("tst")  # lowercase IATA
    assert airport is not None
    assert airport.airport_id == 1

    airport = repository.find_by_code("abcd")  # lowercase ICAO
    assert airport is not None
    assert airport.airport_id == 2


# -----------------------------
# Test 4: Code not found returns None
# -----------------------------
def test_find_by_code_not_found(repo, sample_airports):
    repository, db_path = repo
    repository.save(sample_airports)

    airport = repository.find_by_code("ZZZ")
    assert airport is None


# -----------------------------
# Test 5: Airport with no IATA/ICAO
# -----------------------------
def test_find_by_code_none_values(repo, sample_airports):
    repository, db_path = repo
    repository.save(sample_airports)

    # airport3 has None for both codes
    airport = repository.find_by_code("nonexistent")
    assert airport is None
