import textwrap
from typing import List
from dataclasses import dataclass, field
from datetime import datetime


from .const import (
    API_RAIN,
    API_WS_MAX,
    API_WD_MAX,
    API_WS,
    API_WD,
    API_STD_WD,
    API_TD,
    API_RH,
    API_TD_MAX,
    API_TD_MIN,
    API_WS_1MM,
    API_WS_10MM,
    VARIABLES,
    API_DATETIME,
    API_CHANNELS,
    API_VALID,
    API_STATUS,
    API_NAME,
    API_VALUE,
    API_STATION_ID,
    API_DATA,
)

@dataclass
class MeteorologicalData:
    station_id: int
    """Station ID"""
    datetime: datetime
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
    rh: float
    """Relative humidity in %"""
    ws_1mm: float
    """Maximum 1 minute wind speed in m/s"""
    ws_10mm: float
    """Maximum 10 minute wind speed in m/s"""
        

    def _pretty_print(self) -> str:
        return textwrap.dedent(
            """Station: {}, Date: {}, Readings: [(TD: {}{}), (TDmax: {}{}), (TDmin: {}{}), (RH: {}{}), (Rain: {}{}), (WS: {}{}), (WSmax: {}{}), (WD: {}{}), (WDmax: {}{}),  (STDwd: {}{}), (WS1mm: {}{}), (WS10mm: {}{})]
            """
        ).format(
            self.station_id,
            self.datetime,
            self.td,
            VARIABLES[API_TD].unit,
            self.td_max,
            VARIABLES[API_TD_MAX].unit,
            self.td_min,
            VARIABLES[API_TD_MIN].unit,
            self.rh,
            VARIABLES[API_RH].unit,
            self.rain,
            VARIABLES[API_RAIN].unit,
            self.ws,
            VARIABLES[API_WS].unit,
            self.ws_max,
            VARIABLES[API_WS_MAX].unit,
            self.wd,
            VARIABLES[API_WD].unit,
            self.wd_max,
            VARIABLES[API_WD_MAX].unit,
            self.std_wd,
            VARIABLES[API_STD_WD].unit,
            self.ws_1mm,
            VARIABLES[API_WS_1MM].unit,
            self.ws_10mm,
            VARIABLES[API_WS_10MM].unit,
        )

    def __str__(self) -> str:
        return self._pretty_print()

    def __repr__(self) -> str:
        return self._pretty_print().replace("\n", " ")


@dataclass
class StationMeteorologicalReadings:
    station_id: int
    """ Station Id"""
    data: : List['MeteorologicalData'] = field(default_factory=list)
    """ List of Meteorological Data """

    def __repr__(self) -> str:
        return textwrap.dedent("""Station ({}), Data: {}""").format(
            self.station_id, self.data
        )


def meteo_data_from_json(station_id: int, data: dict) -> MeteorologicalData:
    """Create a MeteorologicalData object from a JSON object"""
    dt = datetime.fromisoformat(data[API_DATETIME])
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

    return MeteorologicalData(
        station_id,
        dt,
        rain,
        ws_max,
        wd_max,
        ws,
        wd,
        std_wd,
        td,
        rh,
        td_max,
        td_min,
        ws_1mm,
        ws_10mm,
    )


def station_meteo_data_from_json(json: dict) -> StationMeteorologicalReadings:
    station_id = int(json[API_STATION_ID])
    data = json[API_DATA]
    meteo_data = []
    for single_meteo_data in data:
        meteo_data.append(meteo_data_from_json(station_id, single_meteo_data))
    return StationMeteorologicalReadings(station_id, meteo_data)
