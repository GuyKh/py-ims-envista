"""Data Class for IMS Meteorological Readings."""

from __future__ import annotations

import datetime
import logging
import textwrap
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo

from .const import (
    API_BP,
    API_CHANNELS,
    API_DATA,
    API_DATETIME,
    API_DIFF,
    API_GRAD,
    API_NAME,
    API_NIP,
    API_RAIN,
    API_RAIN_1_MIN,
    API_RH,
    API_STATION_ID,
    API_STATUS,
    API_STD_WD,
    API_TD,
    API_TD_MAX,
    API_TD_MIN,
    API_TG,
    API_TIME,
    API_TW,
    API_VALID,
    API_VALUE,
    API_WD,
    API_WD_MAX,
    API_WS,
    API_WS_1MM,
    API_WS_10MM,
    API_WS_MAX,
    VARIABLES,
)

_LOGGER = logging.getLogger(__name__)
MAX_HOUR_INT = 60
MAX_CLOCK_HOUR = 23
MAX_CLOCK_MINUTE = 59
TZ = ZoneInfo("Asia/Jerusalem")

@dataclass
class MeteorologicalData:
    """Meteorological Data."""

    station_id: int
    """Station ID"""
    datetime: datetime.datetime
    """Date and time of the data"""
    rain: float | None
    """Rainfall in mm"""
    ws: float | None
    """Wind speed in m/s"""
    ws_max: float | None
    """Gust wind speed in m/s"""
    wd: float | None
    """Wind direction in deg"""
    wd_max: float | None
    """Gust wind direction in deg"""
    std_wd: float | None
    """Standard deviation wind direction in deg"""
    td: float | None
    """Temperature in °C"""
    td_max: float | None
    """Maximum Temperature in °C"""
    td_min: float | None
    """Minimum Temperature in °C"""
    tg: float | None
    """Ground Temperature in °C"""
    tw: float | None
    """TW Temperature (?) in °C"""
    rh: float | None
    """Relative humidity in %"""
    ws_1mm: float | None
    """Maximum 1 minute wind speed in m/s"""
    ws_10mm: float | None
    """Maximum 10 minute wind speed in m/s"""
    time: datetime.time | None
    """Time"""
    bp: float | None
    """Maximum barometric pressure in mb"""
    diff_r: float | None
    """Distributed radiation in w/m^2"""
    grad: float | None
    """Global radiation in w/m^2"""
    nip: float | None
    """Direct radiation in w/m^2"""
    rain_1_min: float | None
    """Rainfall per minute in mm"""

    def _prety_print_field(self, value: float | str | None, unit: str | None) -> str:
        """Pretty Print a specific field."""
        if value is not None:
            return f"{value!s}{unit if unit else ''}"
        return "None"

    def _pretty_print(self) -> str:
        """Pretty Print."""
        return (
                f"StationID: {self._prety_print_field(self.station_id, None)}, "
                f"Date: {self._prety_print_field(self.datetime, None)}, "
                f"Readings: ["
                f"(TD: {self._prety_print_field(self.td, VARIABLES[API_TD].unit)}), "
                f"(TDmax: {self._prety_print_field(self.td_max, VARIABLES[API_TD_MAX].unit)}), "
                f"(TDmin: {self._prety_print_field(self.td_min, VARIABLES[API_TD_MIN].unit)}), "
                f"(TG: {self._prety_print_field(self.tg, VARIABLES[API_TG].unit)}), "
                f"(RH: {self._prety_print_field(self.rh, VARIABLES[API_RH].unit)}), "
                f"(Rain: {self._prety_print_field(self.rain, VARIABLES[API_RAIN].unit)}), "
                f"(WS: {self._prety_print_field(self.ws, VARIABLES[API_WS].unit)}), "
                f"(WSmax: {self._prety_print_field(self.ws_max, VARIABLES[API_WS_MAX].unit)}), "
                f"(WD: {self._prety_print_field(self.wd, VARIABLES[API_WD].unit)}), "
                f"(WDmax: {self._prety_print_field(self.wd_max, VARIABLES[API_WD_MAX].unit)}), "
                f"(STDwd: {self._prety_print_field(self.std_wd, VARIABLES[API_STD_WD].unit)}), "
                f"(WS1mm: {self._prety_print_field(self.ws_1mm, VARIABLES[API_WS_1MM].unit)}), "
                f"(WS10mm: {self._prety_print_field(self.ws_10mm, VARIABLES[API_WS_10MM].unit)}), "
                f"(Time: {self._prety_print_field(self.time.strftime('%H:%M') if self.time else None, VARIABLES[API_TIME].unit)})]"
            )

    def __str__(self) -> str:
        return self._pretty_print()

    def __repr__(self) -> str:
        return self._pretty_print().replace("\n", " ")


@dataclass
class StationMeteorologicalReadings:
    """Station Meteorological Readings."""

    station_id: int
    """ Station Id"""
    data: list[MeteorologicalData] = field(default_factory=list)
    """ List of Meteorological Data """

    def __repr__(self) -> str:
        return textwrap.dedent("""Station ({}), Data: {}""").format(
            self.station_id, self.data
        )

def _fix_datetime_offset(dt: datetime.datetime) -> datetime.datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=TZ)
    return dt.astimezone(TZ)


def _parse_time_value(raw_time: float | None) -> datetime.time | None:
    if raw_time is None:
        return None

    time_int = int(raw_time)
    if time_int <= MAX_HOUR_INT:
        return datetime.time(0, time_int, tzinfo=TZ)

    time_str = f"{time_int:04d}"
    hour = int(time_str[:2])
    minute = int(time_str[2:])
    if hour > MAX_CLOCK_HOUR or minute > MAX_CLOCK_MINUTE:
        _LOGGER.debug("Invalid API time format: %s", raw_time)
        return None

    return datetime.time(hour, minute, tzinfo=TZ)


def meteo_data_from_json(station_id: int, data: dict) -> MeteorologicalData:
    """Create a MeteorologicalData object from a JSON object."""
    dt = datetime.datetime.fromisoformat(data[API_DATETIME])
    dt = _fix_datetime_offset(dt)

    channel_value_dict = {}
    for channel_value in data[API_CHANNELS]:
        if channel_value[API_VALID] is True and channel_value[API_STATUS] == 1:
            channel_value_dict[channel_value[API_NAME]] = float(
                channel_value[API_VALUE]
            )

    rain = channel_value_dict.get(API_RAIN)
    ws_max = channel_value_dict.get(API_WS_MAX)
    wd_max = channel_value_dict.get(API_WD_MAX)
    ws = channel_value_dict.get(API_WS)
    wd = channel_value_dict.get(API_WD)
    std_wd = channel_value_dict.get(API_STD_WD)
    td = channel_value_dict.get(API_TD)
    rh = channel_value_dict.get(API_RH)
    td_max = channel_value_dict.get(API_TD_MAX)
    td_min = channel_value_dict.get(API_TD_MIN)
    ws_1mm = channel_value_dict.get(API_WS_1MM)
    ws_10mm = channel_value_dict.get(API_WS_10MM)
    tg = channel_value_dict.get(API_TG)
    tw = channel_value_dict.get(API_TW)
    time_val = _parse_time_value(channel_value_dict.get(API_TIME))
    bp = channel_value_dict.get(API_BP)
    diff_r = channel_value_dict.get(API_DIFF)
    grad = channel_value_dict.get(API_GRAD)
    nip = channel_value_dict.get(API_NIP)
    rain_1_min = channel_value_dict.get(API_RAIN_1_MIN)

    return MeteorologicalData(
        station_id=station_id,
        datetime=dt,
        rain=rain,
        ws=ws,
        ws_max=ws_max,
        wd=wd,
        wd_max=wd_max,
        std_wd=std_wd,
        td=td,
        td_max=td_max,
        td_min=td_min,
        tg=tg,
        tw=tw,
        rh=rh,
        ws_1mm=ws_1mm,
        ws_10mm=ws_10mm,
        time=time_val,
        bp=bp,
        diff_r=diff_r,
        grad=grad,
        nip=nip,
        rain_1_min=rain_1_min
    )


def station_meteo_data_from_json(json: dict) -> StationMeteorologicalReadings:
    station_id = int(json[API_STATION_ID])
    data = json.get(API_DATA) or []
    meteo_data = [meteo_data_from_json(station_id, single_meteo_data) for single_meteo_data in data]
    return StationMeteorologicalReadings(station_id, meteo_data)
