import pytest

from src.application.mapper.airport_mapper import (
    map_airport_to_response,
    map_airport_list_to_response,
    map_airport_to_validation
)
from src.domain.airport import Airport
from src.domain.codes import IATACode, ICAOCode
from src.schemas.airport import AirportResponse, AirportCodeValidation

# -----------------------------
# Sample Airport instances
# -----------------------------
airport_full = Airport(
    airport_id=1,
    name="Test Airport Full",
    city="CityFull",
    country="CountryFull",
    iata=IATACode("TFF"),
    icao=ICAOCode("TFFF"),
    latitude=12.345,
    longitude=67.890,
    altitude_ft=500,
    timezone="UTC+2",
    active=True
)

airport_no_codes = Airport(
    airport_id=2,
    name="Test Airport No Codes",
    city="CityNone",
    country="CountryNone",
    iata=None,
    icao=None,
    latitude=23.456,
    longitude=78.901,
    altitude_ft=1000,
    timezone="UTC-3",
    active=False
)

airport_partial_codes = Airport(
    airport_id=3,
    name="Test Airport Partial",
    city="CityPartial",
    country="CountryPartial",
    iata=IATACode("TPC"),
    icao=None,
    latitude=34.567,
    longitude=89.012,
    altitude_ft=200,
    timezone="UTC+5",
    active=True
)

# -----------------------------
# Tests for map_airport_to_response
# -----------------------------
def test_map_airport_to_response_full():
    response = map_airport_to_response(airport_full)
    assert isinstance(response, AirportResponse)
    assert response.name == airport_full.name
    assert response.city == airport_full.city
    assert response.iata.value == "TFF"
    assert response.icao.value == "TFFF"

def test_map_airport_to_response_no_codes():
    response = map_airport_to_response(airport_no_codes)
    assert response.iata is None
    assert response.icao is None

def test_map_airport_to_response_partial_codes():
    response = map_airport_to_response(airport_partial_codes)
    assert response.iata.value == "TPC"
    assert response.icao is None

# -----------------------------
# Tests for map_airport_list_to_response
# -----------------------------
def test_map_airport_list_to_response_multiple():
    airports = [airport_full, airport_no_codes, airport_partial_codes]
    responses = map_airport_list_to_response(airports)
    assert len(responses) == 3
    assert all(isinstance(r, AirportResponse) for r in responses)
    assert responses[1].name == airport_no_codes.name
    assert responses[2].iata.value == "TPC"

def test_map_airport_list_to_response_empty():
    responses = map_airport_list_to_response([])
    assert responses == []

# -----------------------------
# Tests for map_airport_to_validation
# -----------------------------
def test_map_airport_to_validation_iata_match():
    validation = map_airport_to_validation(airport_full, "TFF")
    assert isinstance(validation, AirportCodeValidation)
    assert validation.is_valid
    assert validation.code_type == "IATA"

def test_map_airport_to_validation_icao_match():
    validation = map_airport_to_validation(airport_full, "TFFF")
    assert validation.code_type == "ICAO"

def test_map_airport_to_validation_no_match():
    validation = map_airport_to_validation(airport_full, "ZZZ")
    assert validation.code_type == "NONE"

def test_map_airport_to_validation_no_codes_airport():
    validation = map_airport_to_validation(airport_no_codes, "ZZZ")
    assert validation.code_type == "NONE"

def test_map_airport_to_validation_partial_codes():
    validation_iata = map_airport_to_validation(airport_partial_codes, "TPC")
    validation_icao = map_airport_to_validation(airport_partial_codes, "ZZZ")
    assert validation_iata.code_type == "IATA"
    assert validation_icao.code_type == "NONE"

# -----------------------------
# Edge case: Airport with empty strings for codes
# -----------------------------
airport_empty_codes = Airport(
    airport_id=4,
    name="Empty Codes Airport",
    city="CityEmpty",
    country="CountryEmpty",
    iata=IATACode("") if "" else None,
    icao=ICAOCode("") if "" else None,
    latitude=0,
    longitude=0,
    altitude_ft=0,
    timezone="UTC"
)

def test_map_airport_to_validation_empty_codes():
    validation = map_airport_to_validation(airport_empty_codes, "ZZZ")
    assert validation.code_type == "NONE"

def test_map_airport_to_response_empty_codes():
    response = map_airport_to_response(airport_empty_codes)
    assert response.iata is None
    assert response.icao is None
