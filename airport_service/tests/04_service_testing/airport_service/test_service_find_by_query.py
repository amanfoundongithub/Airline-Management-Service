import pytest
from unittest.mock import MagicMock

from src.application.services.airport_service import AirportService
from src.domain.airport import Airport
from src.domain.codes import IATACode, ICAOCode
from src.schemas.airport import AirportSearchResponse

# Helper to create Airport objects with valid IATA and ICAO codes
def make_airport(name: str, iata: str, icao: str) -> Airport:
    return Airport(
        airport_id=1,
        name=name,
        city="TestCity",
        country="TestCountry",
        iata=IATACode(iata),
        icao=ICAOCode(icao),
        latitude=0.0,
        longitude=0.0,
        altitude_ft=0,
        timezone="UTC",
        active=True
    )

@pytest.fixture
def mock_repo():
    repo = MagicMock()
    service = AirportService(repo)
    return service, repo

# Normal case
def test_find_by_query_normal(mock_repo):
    service, repo = mock_repo
    airports = [
        make_airport("AirportA", "AAA", "AAAA"),
        make_airport("AirportB", "AAB", "AAAB"),
    ]
    repo.find_by_query.return_value = airports

    response: AirportSearchResponse = service.find_by_query("Air")
    repo.find_by_query.assert_called_once_with("Air", 50, 0)
    assert len(response.results) == 2
    assert response.results[0].name == "AirportA"
    assert response.results[1].iata.value == "AAB"

# Test limit and offset functionality
def test_find_by_query_limit_offset(mock_repo):
    service, repo = mock_repo
    airports = [
        make_airport("AirportA", "AAA", "AAAA"),
        make_airport("AirportB", "AAB", "AAAB"),
        make_airport("AirportC", "AAC", "AAAC"),
        make_airport("AirportD", "AAD", "AAAD"),
        make_airport("AirportE", "AAE", "AAAE"),
    ]
    repo.find_by_query.return_value = airports[2:5]  # simulate slicing
    response = service.find_by_query("Air", limit=3, offset=2)
    repo.find_by_query.assert_called_once_with("Air", 3, 2)
    assert len(response.results) == 3
    assert response.results[0].name == "AirportC"
    assert response.results[-1].name == "AirportE"

# Empty result
def test_find_by_query_empty(mock_repo):
    service, repo = mock_repo
    repo.find_by_query.return_value = []

    response = service.find_by_query("Nothing")
    repo.find_by_query.assert_called_once_with("Nothing", 50, 0)
    assert response.results == []

# Case-insensitive search
def test_find_by_query_case_insensitive(mock_repo):
    service, repo = mock_repo
    airports = [
        make_airport("Delhi International", "DEL", "VIDP"),
        make_airport("Mumbai Airport", "BOM", "VABB"),
    ]
    repo.find_by_query.return_value = airports

    response = service.find_by_query("del")
    repo.find_by_query.assert_called_once_with("del", 50, 0)
    assert any(a.iata.value == "DEL" for a in response.results)

# Special characters and numbers in query
def test_find_by_query_special_chars(mock_repo):
    service, repo = mock_repo
    airports = [
        make_airport("Airport-123", "ABC", "ABCD"),
        make_airport("Airport_!@", "BDE", "BDEF"),
    ]
    repo.find_by_query.return_value = airports

    response = service.find_by_query("!@")
    repo.find_by_query.assert_called_once_with("!@", 50, 0)
    assert any("!" in a.name or "@" in a.name for a in response.results)

# Query that returns very large number of results
def test_find_by_query_many_results(mock_repo):
    service, repo = mock_repo
    airports = []

    # Generate 100 valid airports with only letters
    for i in range(100):
        iata_code = chr(65 + (i % 26)) + chr(65 + ((i // 26) % 26)) + chr(65 + ((i // 26 // 26) % 26))  # 3 letters
        icao_code = iata_code + chr(65 + ((i+5) % 26))  # 4 letters
        airports.append(make_airport(f"Airport{i}", iata_code, icao_code))

    repo.find_by_query.return_value = airports

    response = service.find_by_query("Airport")
    repo.find_by_query.assert_called_once_with("Airport", 50, 0)
    assert len(response.results) == 100
    assert response.results[0].name == "Airport0"
    assert response.results[-1].name == "Airport99"



# Repository throws exception
def test_find_by_query_repo_exception(mock_repo):
    service, repo = mock_repo
    repo.find_by_query.side_effect = Exception("DB error")

    with pytest.raises(Exception) as exc:
        service.find_by_query("Air")
    assert "DB error" in str(exc.value)

# Very long query string
def test_find_by_query_long_string(mock_repo):
    service, repo = mock_repo
    airports = [make_airport("AirportX", "XXX", "XXXX")]
    repo.find_by_query.return_value = airports

    long_query = "A" * 1000
    response = service.find_by_query(long_query)
    repo.find_by_query.assert_called_once_with(long_query, 50, 0)
    assert response.results[0].name == "AirportX"

# Limit = 0 should return empty list
def test_find_by_query_limit_zero(mock_repo):
    service, repo = mock_repo
    repo.find_by_query.return_value = []

    response = service.find_by_query("Air", limit=0)
    repo.find_by_query.assert_called_once_with("Air", 0, 0)
    assert response.results == []

# Negative offset should still call repository (repository may handle it)
def test_find_by_query_negative_offset(mock_repo):
    service, repo = mock_repo
    airports = [make_airport("AirportNeg", "NEG", "NEGA")]
    repo.find_by_query.return_value = airports

    response = service.find_by_query("Neg", offset=-5)
    repo.find_by_query.assert_called_once_with("Neg", 50, -5)
    assert response.results[0].name == "AirportNeg"
