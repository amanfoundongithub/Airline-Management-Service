import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from src.infrastructure.loaders.openflight_loader import OpenFlightLoader
from src.core.exceptions import OpenFlightDownloadError, OpenFlightParseError, OpenFlightsMappingError
from src.domain.airport import Airport
from src.domain.codes import IATACode, ICAOCode


# -----------------------------
# Sample CSV data
# -----------------------------
SAMPLE_CSV = """1,Airport A,CityA,CountryA,AAA,AAAA,12.34,56.78,100,UTC
2,Airport B,CityB,CountryB,BBB,BBBB,23.45,67.89,200,UTC+1
3,Airport C,CityC,CountryC,,,34.56,78.90,50,UTC+2
"""


# -----------------------------
# Test: successful load from existing file
# -----------------------------
@patch("pathlib.Path.exists", return_value=True)
@patch("pathlib.Path.open", new_callable=mock_open, read_data=SAMPLE_CSV)
def test_load_existing_file(mock_file, mock_exists):
    loader = OpenFlightLoader()
    airports = loader.load()

    assert len(airports) == 3
    assert isinstance(airports[0], Airport)
    assert airports[0].iata.value == "AAA"
    assert airports[0].icao.value == "AAAA"
    # airport without IATA/ICAO
    assert airports[2].iata is None
    assert airports[2].icao is None


# -----------------------------
# Test: download file if not exists
# -----------------------------
@patch("pathlib.Path.exists", return_value=False)
@patch("requests.get")
@patch("pathlib.Path.write_bytes")
def test_download_file(mock_write, mock_requests, mock_exists):
    mock_response = MagicMock()
    mock_response.content = b"some,csv,data"
    mock_response.raise_for_status = MagicMock()
    mock_requests.return_value = mock_response

    loader = OpenFlightLoader()
    path = loader._OpenFlightLoader__ensure_file()  # call private method
    mock_requests.assert_called_once_with(loader.url, timeout=30)
    mock_write.assert_called_once_with(b"some,csv,data")
    assert isinstance(path, Path)


# -----------------------------
# Test: download error
# -----------------------------
@patch("pathlib.Path.exists", return_value=False)
@patch("requests.get", side_effect=Exception("network error"))
def test_download_error(mock_requests, mock_exists):
    loader = OpenFlightLoader()
    with pytest.raises(OpenFlightDownloadError):
        loader._OpenFlightLoader__ensure_file()


# -----------------------------
# Test: CSV parse error
# -----------------------------
@patch("pathlib.Path.exists", return_value=True)
@patch("pathlib.Path.open", side_effect=Exception("bad file"))
def test_parse_error(mock_open, mock_exists):
    loader = OpenFlightLoader()
    with pytest.raises(OpenFlightParseError):
        loader._OpenFlightLoader__load_rows(Path("dummy.csv"))


# -----------------------------
# Test: mapping error
# -----------------------------
def test_mapping_error():
    loader = OpenFlightLoader()
    bad_row = ["not_an_int", "Airport", "City", "Country", "AAA", "AAAA", "12.34", "56.78", "100", "UTC"]
    with pytest.raises(OpenFlightsMappingError):
        loader._OpenFlightLoader__map(bad_row)


# -----------------------------
# Test: parse IATA/ICAO edge cases
# -----------------------------
def test_parse_iata_icao_none():
    loader = OpenFlightLoader()
    # empty strings
    assert loader._OpenFlightLoader__parse_iata("") is None
    assert loader._OpenFlightLoader__parse_icao("") is None
    # valid
    assert loader._OpenFlightLoader__parse_iata("AAA").value == "AAA"
    assert loader._OpenFlightLoader__parse_icao("AAAA").value == "AAAA"
