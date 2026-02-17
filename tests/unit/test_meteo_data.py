"""Unit tests for meteorological payload parsing."""

from __future__ import annotations

from ims_envista.const import API_DATA, API_STATION_ID
from ims_envista.meteo_data import meteo_data_from_json, station_meteo_data_from_json

EXPECTED_HOUR = 13
EXPECTED_MINUTE = 5


def test_station_meteo_data_from_json_empty_data_returns_empty_readings() -> None:
    payload = {API_STATION_ID: 1, API_DATA: []}

    result = station_meteo_data_from_json(payload)

    assert result.station_id == 1
    assert result.data == []


def test_meteo_data_from_json_preserves_zero_values() -> None:
    data = {
        "datetime": "2025-01-15T12:00:00",
        "channels": [
            {"name": "Rain", "value": 0, "valid": True, "status": 1},
            {"name": "TD", "value": 0, "valid": True, "status": 1},
            {"name": "Time", "value": 0, "valid": True, "status": 1},
        ],
    }

    result = meteo_data_from_json(10, data)

    assert result.rain == 0.0
    assert result.td == 0.0
    assert result.time is not None
    assert result.time.hour == 0
    assert result.time.minute == 0


def test_meteo_data_from_json_parses_hhmm_time() -> None:
    data = {
        "datetime": "2025-01-15T12:00:00+02:00",
        "channels": [
            {"name": "Time", "value": 1305, "valid": True, "status": 1},
        ],
    }

    result = meteo_data_from_json(10, data)

    assert result.time is not None
    assert result.time.hour == EXPECTED_HOUR
    assert result.time.minute == EXPECTED_MINUTE
