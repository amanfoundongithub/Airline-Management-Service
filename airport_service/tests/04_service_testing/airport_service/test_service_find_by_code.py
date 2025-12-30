import pytest
from unittest.mock import MagicMock, patch

from src.application.services.airport_service import AirportService
from src.core.exceptions.http import ResourceNotFoundException
from src.domain.airport import Airport
from src.domain.codes import IATACode, ICAOCode
from src.schemas.airport import AirportResponse


# ----------------- Helper Factories -----------------
def make_airport(
    airport_id=1,
    name="Indira Gandhi Airport",
    city="Delhi",
    country="India",
    iata="DEL",
    icao="VIDP",
    latitude=28.5562,
    longitude=77.1000,
    altitude_ft=777,
    timezone="Asia/Kolkata",
    active=True,
):
    return Airport(
        airport_id=airport_id,
        name=name,
        city=city,
        country=country,
        iata=IATACode(iata) if iata else None,
        icao=ICAOCode(icao) if icao else None,
        latitude=latitude,
        longitude=longitude,
        altitude_ft=altitude_ft,
        timezone=timezone,
        active=active,
    )


# ----------------- Fixtures -----------------
@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return AirportService(mock_repo)


# ----------------- Success Cases -----------------
def test_find_by_code_iata_success(service, mock_repo):
    airport = make_airport()
    mock_repo.find_by_code.return_value = airport

    response = service.find_by_code("DEL")

    assert isinstance(response, AirportResponse)
    assert response.iata.value == "DEL"
    assert response.icao.value == "VIDP"
    assert response.name == "Indira Gandhi Airport"
    mock_repo.find_by_code.assert_called_once_with("DEL")


def test_find_by_code_icao_success(service, mock_repo):
    airport = make_airport(iata=None, icao="VIDP")
    mock_repo.find_by_code.return_value = airport

    response = service.find_by_code("VIDP")

    assert response.icao.value == "VIDP"
    assert response.iata is None
    mock_repo.find_by_code.assert_called_once_with("VIDP")


def test_find_by_code_no_iata_or_icao(service, mock_repo):
    airport = make_airport(iata=None, icao=None)
    mock_repo.find_by_code.return_value = airport

    response = service.find_by_code("UNKNOWN")

    assert response.iata is None
    assert response.icao is None
    mock_repo.find_by_code.assert_called_once_with("UNKNOWN")


# ----------------- Not Found Case -----------------
def test_find_by_code_not_found(service, mock_repo):
    mock_repo.find_by_code.return_value = None

    with pytest.raises(ResourceNotFoundException) as exc:
        service.find_by_code("XXX")

    assert "XXX" in str(exc.value)
    mock_repo.find_by_code.assert_called_once_with("XXX")


# ----------------- Logging Checks -----------------
@patch("src.application.services.airport_service.get_logger")
def test_logging_info_and_warning(mock_logger, mock_repo):
    logger_instance = MagicMock()
    mock_logger.return_value = logger_instance

    # Case 1: Airport found
    airport = make_airport()
    mock_repo.find_by_code.return_value = airport
    service = AirportService(mock_repo)
    service.find_by_code("DEL")
    logger_instance.info.assert_any_call("Searching airport with code DEL")
    logger_instance.info.assert_any_call(f"Found airport with IATA/ICAO: {airport.name}")

    # Case 2: Airport not found
    mock_repo.find_by_code.return_value = None
    with pytest.raises(ResourceNotFoundException):
        service.find_by_code("XXX")
    logger_instance.info.assert_any_call("Searching airport with code XXX")
    logger_instance.warning.assert_any_call("Requested code : XXX not found.")


# ----------------- Case Insensitive -----------------
def test_find_by_code_case_insensitive(service, mock_repo):
    airport = make_airport(iata="del", icao="vidp")
    mock_repo.find_by_code.return_value = airport

    response = service.find_by_code("DEL")
    assert response.iata.value.lower() == "del"
    assert response.icao.value.lower() == "vidp"
    mock_repo.find_by_code.assert_called_once_with("DEL")
