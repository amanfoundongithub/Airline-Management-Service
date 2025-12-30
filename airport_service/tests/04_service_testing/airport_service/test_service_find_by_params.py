import pytest
from unittest.mock import MagicMock
from src.application.services.airport_service import AirportService
from src.domain.airport import Airport
from src.domain.codes import IATACode, ICAOCode
from src.schemas.airport import AirportSearchResponse

# -----------------------------
# Helper function to create Airport
# -----------------------------
def make_airport(name: str, iata: str, icao: str, city="CityX", country="CountryY"):
    assert len(iata) == 3 and iata.isalpha(), "IATA code must be 3 letters"
    assert len(icao) == 4 and icao.isalpha(), "ICAO code must be 4 letters"
    return Airport(
        airport_id=1,
        name=name,
        city=city,
        country=country,
        iata=IATACode(iata),
        icao=ICAOCode(icao),
        latitude=0.0,
        longitude=0.0,
        altitude_ft=0,
        timezone="UTC",
        active=True
    )

# -----------------------------
# Fixture for service with mocked repository
# -----------------------------
@pytest.fixture
def mock_repo():
    repo = MagicMock()
    service = AirportService(repo)
    return service, repo

# -----------------------------
# Tests for find_by_params
# -----------------------------
def test_find_by_params_city_only(mock_repo):
    service, repo = mock_repo
    airport1 = make_airport("Airport1", "AAA", "AAAA", city="Delhi")
    airport2 = make_airport("Airport2", "AAB", "AAAB", city="Delhi")
    repo.find_by_params.return_value = [airport1, airport2]

    response: AirportSearchResponse = service.find_by_params(city="Delhi", country=None)

    repo.find_by_params.assert_called_once_with("Delhi", None, 50, 0)
    assert len(response.results) == 2
    assert all(a.city == "Delhi" for a in response.results)

def test_find_by_params_country_only(mock_repo):
    service, repo = mock_repo
    airport = make_airport("Airport3", "AAC", "AAAC", country="India")
    repo.find_by_params.return_value = [airport]

    response: AirportSearchResponse = service.find_by_params(city=None, country="India")

    repo.find_by_params.assert_called_once_with(None, "India", 50, 0)
    assert len(response.results) == 1
    assert response.results[0].country == "India"

def test_find_by_params_city_and_country(mock_repo):
    service, repo = mock_repo
    airport = make_airport("Airport4", "AAD", "AAAD", city="Mumbai", country="India")
    repo.find_by_params.return_value = [airport]

    response: AirportSearchResponse = service.find_by_params(city="Mumbai", country="India")

    repo.find_by_params.assert_called_once_with("Mumbai", "India", 50, 0)
    assert len(response.results) == 1
    a = response.results[0]
    assert a.city == "Mumbai"
    assert a.country == "India"

def test_find_by_params_no_results(mock_repo):
    service, repo = mock_repo
    repo.find_by_params.return_value = []

    response: AirportSearchResponse = service.find_by_params(city="Nowhere", country="Noland")

    repo.find_by_params.assert_called_once_with("Nowhere", "Noland", 50, 0)
    assert len(response.results) == 0

import string

def letter_code(n, length):
    # Generate a simple repeating letter code e.g., 'AAA', 'AAB', 'AAC'
    letters = string.ascii_uppercase
    code = ""
    for i in range(length):
        code += letters[(n + i) % len(letters)]
    return code

def test_find_by_params_limit_offset(mock_repo):
    service, repo = mock_repo
    airports = [make_airport(f"Airport{i}", letter_code(i, 3), letter_code(i, 4)) for i in range(10)]
    repo.find_by_params.return_value = airports[2:7]

    response: AirportSearchResponse = service.find_by_params(city="TestCity", country="TestCountry", limit=5, offset=2)

    repo.find_by_params.assert_called_once_with("TestCity", "TestCountry", 5, 2)
    assert len(response.results) == 5
    assert response.results[0].name == "Airport2"
    assert response.results[-1].name == "Airport6"

def test_find_by_params_case_insensitive(mock_repo):
    service, repo = mock_repo
    airport = make_airport("AirportX", "AAX", "AAAX", city="Delhi", country="India")
    repo.find_by_params.return_value = [airport]

    response: AirportSearchResponse = service.find_by_params(city="delhi", country="india")

    repo.find_by_params.assert_called_once_with("delhi", "india", 50, 0)
    assert len(response.results) == 1
    assert response.results[0].city.lower() == "delhi"
    assert response.results[0].country.lower() == "india"
