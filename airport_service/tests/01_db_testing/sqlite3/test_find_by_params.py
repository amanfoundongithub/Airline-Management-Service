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
        Airport(airport_id=1, name="Airport One", city="CityA", country="CountryX",
                iata=IATACode("TST"), icao=ICAOCode("TEST"), latitude=12.34, longitude=56.78,
                altitude_ft=100, timezone="UTC", active=True),
        Airport(airport_id=2, name="Airport Two", city="CityB", country="CountryY",
                iata=IATACode("ABC"), icao=ICAOCode("ABCD"), latitude=23.45, longitude=67.89,
                altitude_ft=200, timezone="UTC+1", active=False),
        Airport(airport_id=3, name="Airport Three", city="CityA", country="CountryY",
                iata=IATACode("XYZ"), icao=ICAOCode("XYZA"), latitude=1.23, longitude=4.56,
                altitude_ft=50, timezone="UTC+2", active=True)
    ]


# -----------------------------
# Test 1: Search by city only
# -----------------------------
def test_find_by_city(repo, sample_airports):
    repository = repo
    repository.save(sample_airports)

    airports = repository.find_by_params(city="CityA", country=None)
    assert len(airports) == 2
    assert all(a.city == "CityA" for a in airports)


# -----------------------------
# Test 2: Search by country only
# -----------------------------
def test_find_by_country(repo, sample_airports):
    repository = repo
    repository.save(sample_airports)

    airports = repository.find_by_params(city=None, country="CountryY")
    assert len(airports) == 2
    assert all(a.country == "CountryY" for a in airports)


# -----------------------------
# Test 3: Search by city + country
# -----------------------------
def test_find_by_city_and_country(repo, sample_airports):
    repository = repo
    repository.save(sample_airports)

    airports = repository.find_by_params(city="CityA", country="CountryY")
    assert len(airports) == 1
    assert airports[0].airport_id == 3


# -----------------------------
# Test 4: Case-insensitive search
# -----------------------------
def test_find_by_params_case_insensitive(repo, sample_airports):
    repository = repo
    repository.save(sample_airports)

    airports = repository.find_by_params(city="citya", country="countryx")
    assert len(airports) == 1
    assert airports[0].airport_id == 1


# -----------------------------
# Test 5: Limit and offset
# -----------------------------
def test_find_by_params_limit_offset(repo, sample_airports):
    repository = repo
    repository.save(sample_airports)

    airports = repository.find_by_params(city="CityA", country=None, limit=1, offset=0)
    assert len(airports) == 1

    airports2 = repository.find_by_params(city="CityA", country=None, limit=1, offset=1)
    assert len(airports2) == 1
    assert airports[0].airport_id != airports2[0].airport_id


# -----------------------------
# Test 6: No results
# -----------------------------
def test_find_by_params_no_results(repo, sample_airports):
    repository = repo
    repository.save(sample_airports)

    airports = repository.find_by_params(city="Nonexistent", country="Nowhere")
    assert airports == []
