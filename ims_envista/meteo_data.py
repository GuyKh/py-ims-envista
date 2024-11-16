"""Data Class for IMS Meteorological Readings."""

from __future__ import annotations

import datetime
import logging
import textwrap
import time
from dataclasses import dataclass, field

import pytz

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

@dataclass
class MeteorologicalData:
    """Meteorological Data."""

    station_id: int
    """Station ID"""
    datetime: datetime.datetime
    """Date and time of the data"""
    rain: float
    """Rainfall in mm"""
    ws: float
    """Wind speed in m/s"""
    ws_max: float
    """Gust wind speed in m/s"""
    wd: float
    """Wind direction in deg"""
    wd_max: float
    """Gust wind direction in deg"""
    std_wd: float
    """Standard deviation wind direction in deg"""
    td: float
    """Temperature in °C"""
    td_max: float
    """Maximum Temperature in °C"""
    td_min: float
    """Minimum Temperature in °C"""
    tg: float
    """Ground Temperature in °C"""
    tw: float
    """TW Temperature (?) in °C"""
    rh: float
    """Relative humidity in %"""
    ws_1mm: float
    """Maximum 1 minute wind speed in m/s"""
    ws_10mm: float
    """Maximum 10 minute wind speed in m/s"""
    time: datetime.time
    """Time"""
    bp: float
    """Maximum barometric pressure in mb"""
    diff_r: float
    """Distributed radiation in w/m^2"""
    grad: float
    """Global radiation in w/m^2"""
    nip: float
    """Direct radiation in w/m^2"""
    rain_1_min: float
    """Rainfall per minute in mm"""

    def _prety_print_field(self, value: float | str | None, unit: str | None) -> str:
        """Pretty Print a specific field."""
        if value:
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

tz = pytz.timezone("Asia/Jerusalem")


def _fix_datetime_offset(dt: datetime.datetime) -> tuple[datetime.datetime, bool]:
    dt = dt.replace(tzinfo=None)
    dt = tz.localize(dt)

    # Get the UTC offset in seconds
    offset_seconds = dt.utcoffset().total_seconds()

    # Create a fixed timezone with the same offset and name
    fixed_timezone = datetime.timezone(datetime.timedelta(seconds=offset_seconds), dt.tzname())

    # Replace the pytz tzinfo with the fixed timezone
    dt = dt.replace(tzinfo=fixed_timezone)

    is_dst = dt.dst() and dt.dst() != datetime.timedelta(0)
    if is_dst:
        dt = dt + datetime.timedelta(hours=1)

    return dt,is_dst


def meteo_data_from_json(station_id: int, data: dict) -> MeteorologicalData:
    """Create a MeteorologicalData object from a JSON object."""
    dt = datetime.datetime.fromisoformat(data[API_DATETIME])
    dt, is_dst = _fix_datetime_offset(dt)

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
    time_val = channel_value_dict.get(API_TIME)
    if time_val:
        time_int = int(time_val)
        if time_int <= MAX_HOUR_INT:
            t = time.strptime(str(time_int), "%M")
        else :
            t = time.strptime(str(time_int), "%H%M")
        time_val = datetime.time(t.tm_hour, t.tm_min, tzinfo=tz)
    bp = channel_value_dict.get(API_BP)
    diff_r = channel_value_dict.get(API_DIFF)
    grad = channel_value_dict.get(API_GRAD)
    nip = channel_value_dict.get(API_NIP)
    rain_1_min = channel_value_dict.get(API_RAIN_1_MIN)

    if is_dst and time_val:
        # Strange IMS logic :o
        dt = dt + datetime.timedelta(hours=1)
        time_val = time_val.replace(hour=(time_val.hour+1)%24)

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


def station_meteo_data_from_json(json: dict) -> StationMeteorologicalReadings | None:
    station_id = int(json[API_STATION_ID])
    data = json.get(API_DATA)
    if not data:
        return None
    meteo_data = [meteo_data_from_json(station_id, single_meteo_data) for single_meteo_data in data]
    return StationMeteorologicalReadings(station_id, meteo_data)
