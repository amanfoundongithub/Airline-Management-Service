import pytest
import sqlite3
from src.domain.airport import Airport
from src.domain.codes import IATACode, ICAOCode
from src.infrastructure.db.repositories import sqlite3_airport_repository

# -----------------------------
# Fixture: repo + temp DB
# -----------------------------
@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "airports.db"

    # Create table
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

    # Patch get_connection in the module
    def test_get_connection():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    sqlite3_airport_repository.get_connection = test_get_connection
    repository = sqlite3_airport_repository.SQLite3AirportRepository()
    return repository


# -----------------------------
# Fixture: sample airports
# -----------------------------
@pytest.fixture
def sample_airports():
    return [
        Airport(airport_id=1, name="Alpha Airport", city="CityA", country="CountryX",
                iata=IATACode("AAA"), icao=ICAOCode("ALPA"), latitude=12.34, longitude=56.78,
                altitude_ft=100, timezone="UTC", active=True),
        Airport(airport_id=2, name="Bravo Airport", city="CityB", country="CountryY",
                iata=IATACode("BBB"), icao=ICAOCode("BRAV"), latitude=23.45, longitude=67.89,
                altitude_ft=200, timezone="UTC+1", active=False),
        Airport(airport_id=3, name="Charlie Airport", city="CityA", country="CountryY",
                iata=IATACode("CCC"), icao=ICAOCode("CHAR"), latitude=1.23, longitude=4.56,
                altitude_ft=50, timezone="UTC+2", active=True)
    ]


# -----------------------------
# Test 1: Search by name
# -----------------------------
def test_find_by_name(repo, sample_airports):
    repo.save(sample_airports)
    results = repo.find_by_query("Alpha")
    assert len(results) == 1
    assert results[0].name == "Alpha Airport"


# -----------------------------
# Test 2: Search by city
# -----------------------------
def test_find_by_city(repo, sample_airports):
    repo.save(sample_airports)
    results = repo.find_by_query("CityA")
    assert len(results) == 2
    assert all(r.city == "CityA" for r in results)


# -----------------------------
# Test 3: Search by IATA code
# -----------------------------
def test_find_by_iata(repo, sample_airports):
    repo.save(sample_airports)
    results = repo.find_by_query("BBB")
    assert len(results) == 1
    assert results[0].iata.value == "BBB"


# -----------------------------
# Test 4: Search by ICAO code
# -----------------------------
def test_find_by_icao(repo, sample_airports):
    repo.save(sample_airports)
    results = repo.find_by_query("CHAR")
    assert len(results) == 1
    assert results[0].icao.value == "CHAR"


# -----------------------------
# Test 5: Partial/fuzzy match
# -----------------------------
def test_find_by_partial_name(repo, sample_airports):
    repo.save(sample_airports)
    results = repo.find_by_query("Air")
    assert len(results) == 3  # All airport names contain 'Air'


# -----------------------------
# Test 6: Case-insensitive search
# -----------------------------
def test_find_by_case_insensitive(repo, sample_airports):
    repo.save(sample_airports)
    results = repo.find_by_query("alpha airport".lower())
    assert len(results) == 1
    assert results[0].name == "Alpha Airport"


# -----------------------------
# Test 7: Limit and offset
# -----------------------------
def test_find_by_query_limit_offset(repo, sample_airports):
    repo.save(sample_airports)
    results = repo.find_by_query("Airport", limit=2, offset=0)
    assert len(results) == 2

    results2 = repo.find_by_query("Airport", limit=2, offset=2)
    assert len(results2) == 1
    assert results[0].airport_id != results2[0].airport_id


# -----------------------------
# Test 8: No results
# -----------------------------
def test_find_by_query_no_results(repo, sample_airports):
    repo.save(sample_airports)
    results = repo.find_by_query("Nonexistent")
    assert results == []
