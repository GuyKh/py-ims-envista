"""Constant for ims-envista."""

from .ims_variable import IMSVariable

ENVISTA_STATIONS_URL = "https://api.ims.gov.il/v1/envista/stations"
ENVISTA_REGIONS_URL = "https://api.ims.gov.il/v1/envista/regions"

GET_ALL_STATIONS_DATA_URL = ENVISTA_STATIONS_URL
GET_ALL_REGIONS_DATA_URL = ENVISTA_REGIONS_URL
GET_SPECIFIC_STATION_DATA_URL = ENVISTA_STATIONS_URL + "/{}"
GET_SPECIFIC_REGION_DATA_URL = ENVISTA_REGIONS_URL + "/{}"
GET_LATEST_STATION_DATA_URL = ENVISTA_STATIONS_URL + "/{}/data/{}/latest"
GET_EARLIEST_STATION_DATA_URL = ENVISTA_STATIONS_URL + "/{}/data/{}/earliest"
GET_DAILY_STATION_DATA_URL = ENVISTA_STATIONS_URL + "/{}/data/{}/daily"
GET_STATION_DATA_BY_DATE_URL = GET_DAILY_STATION_DATA_URL + "/{}/{}/{}"

GET_MONTHLY_STATION_DATA_URL = ENVISTA_STATIONS_URL + "/{}/data{}/monthly"
GET_MONTHLY_STATION_DATA_BY_MONTH_URL = GET_MONTHLY_STATION_DATA_URL + "/{}/{}"
GET_STATION_DATA_BY_RANGE_URL = (
    ENVISTA_STATIONS_URL + "/{}/data{}?from={}/{}/{}&to={}/{}/{}"
)

API_BP = "BP"
API_DIFF = "Diff"
API_GRAD = "Grad"
API_NIP = "NIP"
API_RAIN = "Rain"
API_RAIN_1_MIN = "Rain_1_min"
API_WS_MAX = "WSmax"
API_WD_MAX = "WDmax"
API_WS = "WS"
API_WD = "WD"
API_TG = "WD"
API_STD_WD = "STDwd"
API_TD = "TD"
API_RH = "RH"
API_TD_MAX = "TDmax"
API_TD_MIN = "TDmin"
API_WS_1MM = "WS1mm"
API_WS_10MM = "Ws10mm"
API_TIME = "Time"
API_REGION_ID = "regionId"
API_NAME = "name"
API_STATIONS = "stations"
API_DATETIME = "datetime"
API_CHANNELS = "channels"
API_VALID = "valid"
API_STATUS = "status"
API_VALUE = "value"
API_STATION_ID = "stationId"
API_DATA = "data"

VARIABLES = {
    API_BP: IMSVariable("BP", "hPa", "Average pressure at station level"),
    API_DIFF: IMSVariable("Diff", "w/m²", "Diffused radiation"),
    API_GRAD: IMSVariable("Grad", "w/m²", "Global radiation"),
    API_NIP: IMSVariable("NIP", "w/m²", "Direct radiation"),
    API_RAIN: IMSVariable("Rain", "mm", "Rainfall"),
    API_RH: IMSVariable("RH", "%", "Relative humidity"),
    API_STD_WD: IMSVariable("STDwd", "deg", "Standard deviation wind direction"),
    API_TD: IMSVariable("TD", "°C", "Temperature"),
    API_TD_MAX: IMSVariable(
        "TDMax",
        "°C",
        "Maximum temperature",
    ),
    API_TD_MIN: IMSVariable("TDmin", "°C", "Minimum temperature"),
    API_TG: IMSVariable("TG", "°C", "Grass minimum temperature"),
    API_WD: IMSVariable("WD", "deg", "Wind direction"),
    API_WD_MAX: IMSVariable("WDmax", "deg", "Gust wind direction"),
    API_WS: IMSVariable("WS", "m/s", "Wind speed"),
    API_WS_10MM: IMSVariable("Ws10mm", "m/s", "Maximum 10 minutes wind speed"),
    API_TIME: IMSVariable("Time", "hhmm", "end time of Ws10mm"),
    API_WS_1MM: IMSVariable("WS1mm", "m/s", "Maximum 1 minute wind speed"),
    API_WS_MAX: IMSVariable("WSmax", "m/s", "Gust wind speed"),
    API_RAIN_1_MIN: IMSVariable("Rain_1_min", "mm", "Rainfall per minute"),
}
