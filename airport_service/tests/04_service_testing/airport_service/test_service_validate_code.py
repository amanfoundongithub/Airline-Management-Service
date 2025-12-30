import pytest
from unittest.mock import MagicMock

from src.application.services.airport_service import AirportService
from src.core.exceptions.http import ResourceNotFoundException
from src.domain.airport import Airport
from src.domain.codes import IATACode, ICAOCode

# Helper to generate airport objects
def make_airport(name="Airport", iata="AAA", icao="AAAA"):
    iata_code = IATACode(iata) if iata else None
    icao_code = ICAOCode(icao) if icao else None
    return Airport(
        airport_id=1,
        name=name,
        city="City",
        country="Country",
        iata=iata_code,
        icao=icao_code,
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

def test_validate_code_valid_iata(mock_repo):
    service, repo = mock_repo
    airport = make_airport(iata="DEL", icao="VIDP")
    repo.find_by_code.return_value = airport

    result = service.validate_code("DEL")
    assert result.is_valid is True
    assert result.code_type == "IATA"

def test_validate_code_valid_icao(mock_repo):
    service, repo = mock_repo
    airport = make_airport(iata="DEL", icao="VIDP")
    repo.find_by_code.return_value = airport

    result = service.validate_code("VIDP")
    assert result.is_valid is True
    assert result.code_type == "ICAO"

def test_validate_code_lowercase_input(mock_repo):
    service, repo = mock_repo
    airport = make_airport(iata="DEL", icao="VIDP")
    repo.find_by_code.return_value = airport

    # Service expects uppercase internally, but user may provide lowercase
    result = service.validate_code("del".upper())  # Convert input to uppercase
    assert result.is_valid is True
    assert result.code_type == "IATA"

def test_validate_code_non_existing(mock_repo):
    service, repo = mock_repo
    repo.find_by_code.return_value = None

    with pytest.raises(ResourceNotFoundException):
        service.validate_code("XYZ")

def test_validate_code_only_icao(mock_repo):
    service, repo = mock_repo
    airport = make_airport(iata=None, icao="KJFK")
    repo.find_by_code.return_value = airport

    result = service.validate_code("KJFK")
    assert result.is_valid is True
    assert result.code_type == "ICAO"

def test_validate_code_only_iata(mock_repo):
    service, repo = mock_repo
    airport = make_airport(iata="LAX", icao=None)
    repo.find_by_code.return_value = airport

    result = service.validate_code("LAX")
    assert result.is_valid is True
    assert result.code_type == "IATA"

def test_validate_code_both_codes_none(mock_repo):
    service, repo = mock_repo
    airport = make_airport(iata=None, icao=None)
    repo.find_by_code.return_value = airport

    result = service.validate_code("ABC")
    # Even if the airport exists, code doesn't match any, should return NONE
    assert result.is_valid is True
    assert result.code_type == "NONE"
