import pytest
import sqlite3

from src.domain.airport import Airport
from src.domain.codes import IATACode, ICAOCode
from src.infrastructure.db.repositories import sqlite3_airport_repository


# =====================================================
# Fixture: Repository with temporary SQLite DB
# =====================================================
@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "airports.db"

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

    def test_get_connection():
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        return connection

    sqlite3_airport_repository.get_connection = test_get_connection
    return sqlite3_airport_repository.SQLite3AirportRepository()


# =====================================================
# Fixtures: Airport datasets
# =====================================================
@pytest.fixture
def airports_for_param_search():
    return [
        Airport(1, "Airport One", "CityA", "CountryX",
                IATACode("TST"), ICAOCode("TEST"), 12.34, 56.78, 100, "UTC", True),
        Airport(2, "Airport Two", "CityB", "CountryY",
                IATACode("ABC"), ICAOCode("ABCD"), 23.45, 67.89, 200, "UTC+1", False),
        Airport(3, "Airport Three", "CityA", "CountryY",
                IATACode("XYZ"), ICAOCode("XYZA"), 1.23, 4.56, 50, "UTC+2", True),
    ]


@pytest.fixture
def airports_for_query_search():
    return [
        Airport(1, "Alpha Airport", "CityA", "CountryX",
                IATACode("AAA"), ICAOCode("ALPA"), 12.34, 56.78, 100, "UTC", True),
        Airport(2, "Bravo Airport", "CityB", "CountryY",
                IATACode("BBB"), ICAOCode("BRAV"), 23.45, 67.89, 200, "UTC+1", False),
        Airport(3, "Charlie Airport", "CityA", "CountryY",
                IATACode("CCC"), ICAOCode("CHAR"), 1.23, 4.56, 50, "UTC+2", True),
    ]


# =====================================================
# Tests: find_by_params (city / country filters)
# =====================================================
def test_find_by_city(repo, airports_for_param_search):
    repo.save(airports_for_param_search)
    results = repo.find_by_params(city="CityA", country=None)
    assert len(results) == 2
    assert all(a.city == "CityA" for a in results)


def test_find_by_country(repo, airports_for_param_search):
    repo.save(airports_for_param_search)
    results = repo.find_by_params(city=None, country="CountryY")
    assert len(results) == 2
    assert all(a.country == "CountryY" for a in results)


def test_find_by_city_and_country(repo, airports_for_param_search):
    repo.save(airports_for_param_search)
    results = repo.find_by_params(city="CityA", country="CountryY")
    assert len(results) == 1
    assert results[0].airport_id == 3


def test_find_by_params_case_insensitive(repo, airports_for_param_search):
    repo.save(airports_for_param_search)
    results = repo.find_by_params(city="citya", country="countryx")
    assert len(results) == 1
    assert results[0].airport_id == 1


def test_find_by_params_limit_offset(repo, airports_for_param_search):
    repo.save(airports_for_param_search)

    first = repo.find_by_params(city="CityA", country=None, limit=1, offset=0)
    second = repo.find_by_params(city="CityA", country=None, limit=1, offset=1)

    assert len(first) == 1
    assert len(second) == 1
    assert first[0].airport_id != second[0].airport_id


def test_find_by_params_no_results(repo, airports_for_param_search):
    repo.save(airports_for_param_search)
    results = repo.find_by_params(city="Nowhere", country="Unknown")
    assert results == []


# =====================================================
# Tests: find_by_query (free-text search)
# =====================================================
def test_find_by_name(repo, airports_for_query_search):
    repo.save(airports_for_query_search)
    results = repo.find_by_query("Alpha")
    assert len(results) == 1
    assert results[0].name == "Alpha Airport"


def test_find_by_query_city(repo, airports_for_query_search):
    repo.save(airports_for_query_search)
    results = repo.find_by_query("CityA")
    assert len(results) == 2


def test_find_by_iata(repo, airports_for_query_search):
    repo.save(airports_for_query_search)
    results = repo.find_by_query("BBB")
    assert len(results) == 1
    assert results[0].iata.value == "BBB"


def test_find_by_icao(repo, airports_for_query_search):
    repo.save(airports_for_query_search)
    results = repo.find_by_query("CHAR")
    assert len(results) == 1
    assert results[0].icao.value == "CHAR"


def test_find_by_partial_name(repo, airports_for_query_search):
    repo.save(airports_for_query_search)
    results = repo.find_by_query("Air")
    assert len(results) == 3


def test_find_by_query_case_insensitive(repo, airports_for_query_search):
    repo.save(airports_for_query_search)
    results = repo.find_by_query("alpha airport")
    assert len(results) == 1
    assert results[0].name == "Alpha Airport"


def test_find_by_query_limit_offset(repo, airports_for_query_search):
    repo.save(airports_for_query_search)

    first = repo.find_by_query("Airport", limit=2, offset=0)
    second = repo.find_by_query("Airport", limit=2, offset=2)

    assert len(first) == 2
    assert len(second) == 1
    assert first[0].airport_id != second[0].airport_id


def test_find_by_query_no_results(repo, airports_for_query_search):
    repo.save(airports_for_query_search)
    results = repo.find_by_query("Nonexistent")
    assert results == []

# =====================================================
# Tests: find_by_code (IATA / ICAO)
# =====================================================

def test_find_by_iata_code(repo, airports_for_query_search):
    repo.save(airports_for_query_search)

    airport = repo.find_by_code("AAA")

    assert airport is not None
    assert airport.iata.value == "AAA"
    assert airport.name == "Alpha Airport"


def test_find_by_icao_code(repo, airports_for_query_search):
    repo.save(airports_for_query_search)

    airport = repo.find_by_code("CHAR")

    assert airport is not None
    assert airport.icao.value == "CHAR"
    assert airport.name == "Charlie Airport"


def test_find_by_code_case_insensitive(repo, airports_for_query_search):
    repo.save(airports_for_query_search)

    airport = repo.find_by_code("bbb")  # lowercase input

    assert airport is not None
    assert airport.iata.value == "BBB"
    assert airport.name == "Bravo Airport"


def test_find_by_code_prefers_exact_match(repo, airports_for_query_search):
    repo.save(airports_for_query_search)

    airport = repo.find_by_code("BRAV")

    assert airport is not None
    assert airport.icao.value == "BRAV"


def test_find_by_code_not_found(repo, airports_for_query_search):
    repo.save(airports_for_query_search)

    airport = repo.find_by_code("ZZZ")

    assert airport is None


def test_find_by_code_with_numeric_string(repo, airports_for_query_search):
    repo.save(airports_for_query_search)

    airport = repo.find_by_code("123")

    assert airport is None