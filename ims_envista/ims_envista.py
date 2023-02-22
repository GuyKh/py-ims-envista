"""Module IMSEnvista getting IMS meteorological readings."""
import json
from typing import Optional

from datetime import datetime, date
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from loguru import logger
from urllib3 import Retry

from .const import (
    GET_LATEST_STATION_DATA_URL,
    GET_EARLIEST_STATION_DATA_URL,
    GET_STATION_DATA_BY_DATE_URL,
    GET_SPECIFIC_STATION_DATA_URL,
    GET_ALL_STATIONS_DATA_URL,
    GET_ALL_REGIONS_DATA_URL,
    API_REGION_ID,
    API_NAME,
    API_STATIONS,
    GET_SPECIFIC_REGION_DATA_URL,
    GET_DAILY_STATION_DATA_URL,
    GET_MONTHLY_STATION_DATA_URL,
    GET_MONTHLY_STATION_DATA_BY_MONTH_URL,
    GET_STATION_DATA_BY_RANGE_URL,
)
from .meteo_data import (
    MeteorologicalData,
    station_meteo_data_from_json,
    StationMeteorologicalReadings,
)
from .station_data import StationInfo, station_from_json, region_from_json, RegionInfo

# ims.gov.il does not support ipv6 yet, `requests` use ipv6 by default
# and wait for timeout before trying ipv4, so we have to disable ipv6
requests.packages.urllib3.util.connection.HAS_IPV6 = False

def createSession():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class IMSEnvista:
    """API Wrapper to IMS Envista"""

    def __init__(self, token: str):
        if not token:
            raise ValueError

        self.token = token
        self.session = createSession()

    @staticmethod
    def _get_channel_id_url_part(channel_id: int) -> str:
        """get specific Channel Id url param"""
        if channel_id:
            return "/" + str(channel_id)
        return ""

    def _get_ims_url(self, url: str) -> Optional[dict]:
        """Fetches data from IMS url

        Args:
            url (str): IMS Station ID

        Returns:
            data: Current station meteorological data
        """
        logger.debug(f"Fetching data from: {url}")
        try:
            response = self.session.get(
                url,
                headers={
                    "Accept": "application/vnd.github.v3.text-match+json",
                    "Authorization": f"ApiToken {self.token}",
                },
                timeout=10,
            )

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
            return json.loads(response.text)
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")  # Python 3.6
            return None
        except Exception as err:
            logger.error(f"Other error occurred: {err}")  # Python 3.6
            return None

    def close(self):
        self.session.close()

    def get_latest_station_data(
        self, station_id: int, channel_id: int = None
    ) -> StationMeteorologicalReadings:
        """Fetches the latest station data from IMS Envista API

        Args:
            station_id (int): IMS Station Id
            channel_id (int): [Optional] Specific Channel Id

        Returns:
            data: Current station meteorological data
        """
        get_url = GET_LATEST_STATION_DATA_URL.format(
            str(station_id), self._get_channel_id_url_part(channel_id)
        )
        return station_meteo_data_from_json(self._get_ims_url(get_url))

    def get_earliest_station_data(
        self, station_id: int, channel_id: int = None
    ) -> StationMeteorologicalReadings:
        """Fetches the earliest station data from IMS Envista API

        Args:
            station_id (int): IMS Station ID
            channel_id (int): [Optional] Specific Channel ID

        Returns:
            data: Current station meteorological data
        """
        get_url = GET_EARLIEST_STATION_DATA_URL.format(
            str(station_id), self._get_channel_id_url_part(channel_id)
        )
        return station_meteo_data_from_json(self._get_ims_url(get_url))

    def get_station_data_from_date(
        self, station_id: int, date_to_query: date, channel_id: int = None
    ) -> StationMeteorologicalReadings:
        """Fetches latest station data from IMS Envista API by date

        Args:
            station_id (int): IMS Station ID
            date_to_query (datetime): Selected date to query
            channel_id (int): [Optional] Specific Channel Id

        Returns:
            data: Current station meteorological data
        """
        get_url = GET_STATION_DATA_BY_DATE_URL.format(
            str(station_id),
            self._get_channel_id_url_part(channel_id),
            str(date_to_query.year),
            str(date_to_query.month),
            str(date_to_query.day),
        )
        return station_meteo_data_from_json(self._get_ims_url(get_url))

    def get_station_data_by_date_range(
        self,
        station_id: int,
        from_date: date,
        to_date: date,
        channel_id: int = None,
    ) -> StationMeteorologicalReadings:
        """Fetches latest station data from IMS Envista API by date range

        Args:
            station_id (int): IMS Station ID
            from_date (datetime): From date to query
            to_date (datetime): to date to query
            channel_id (int): [Optional] Specific Channel Id

        Returns:
            data: Current station meteorological data
        """
        get_url = GET_STATION_DATA_BY_RANGE_URL.format(
            str(station_id),
            self._get_channel_id_url_part(channel_id),
            str(from_date.strftime("%Y")),
            str(from_date.strftime("%m")),
            str(from_date.strftime("%d")),
            str(to_date.strftime("%Y")),
            str(to_date.strftime("%m")),
            str(to_date.strftime("%d")),
        )
        return station_meteo_data_from_json(self._get_ims_url(get_url))

    def get_daily_station_data(
        self, station_id: int, channel_id: int = None
    ) -> StationMeteorologicalReadings:
        """Fetches the daily station data from IMS Envista API

        Args:
            station_id (int): IMS Station ID
            channel_id (int): [Optional] Specific Channel Id

        Returns:
            data: Current station meteorological data
        """
        get_url = GET_DAILY_STATION_DATA_URL.format(
            str(station_id),
            self._get_channel_id_url_part(channel_id),
        )
        return station_meteo_data_from_json(self._get_ims_url(get_url))

    def get_monthly_station_data(
        self,
        station_id: int,
        channel_id: int = None,
        month: str = None,
        year: str = None,
    ) -> StationMeteorologicalReadings:
        """Fetches monthly station data from IMS Envista API

        Args:
            station_id (int): IMS Station ID
            channel_id (int): [Optional] Specific Channel Id
            month (str): [Optional] Specific Month in MM format (07)
            year (str):  [Optional] Specific Year in YYYY format (2020)

        Returns:
            data: Current station meteorological data
        """

        if not month or not year:
            get_url = GET_MONTHLY_STATION_DATA_URL.format(
                str(station_id), self._get_channel_id_url_part(channel_id)
            )
        else:
            get_url = GET_MONTHLY_STATION_DATA_BY_MONTH_URL.format(
                str(station_id), self._get_channel_id_url_part(channel_id), year, month
            )
        return station_meteo_data_from_json(self._get_ims_url(get_url))

    def get_all_stations_info(self) -> list[StationInfo]:
        """Fetches all stations data from IMS Envista API

        Returns:
            data: All stations data
        """
        get_url = GET_ALL_STATIONS_DATA_URL
        response = self._get_ims_url(get_url)
        stations = []
        for station in response:
            stations.append(station_from_json(station))
        return stations

    def get_station_info(self, station_id: int) -> StationInfo:
        """Fetches station data from IMS Envista API

        Args:
            station_id (int): IMS Station ID

        Returns:
            data: Current station data
        """
        get_url = GET_SPECIFIC_STATION_DATA_URL.format(str(station_id))
        return station_from_json(self._get_ims_url(get_url))

    def get_all_regions_info(self) -> list[RegionInfo]:
        """Fetches all regions data from IMS Envista API

        Returns:
            data: All stations data
        """
        get_url = GET_ALL_REGIONS_DATA_URL
        response = self._get_ims_url(get_url)
        regions = []
        for region in response:
            stations = []
            for station in region[API_STATIONS]:
                stations.append(station_from_json(station))

            regions.append(
                RegionInfo(region[API_REGION_ID], region[API_NAME], stations)
            )
        return regions

    def get_region_info(self, region_id: int) -> RegionInfo:
        """Fetches region data from IMS Envista API

        Args:
            region_id (int): IMS Region ID

        Returns:
            data: region data
        """
        get_url = GET_SPECIFIC_REGION_DATA_URL.format(str(region_id))
        response = self._get_ims_url(get_url)
        return region_from_json(response)
