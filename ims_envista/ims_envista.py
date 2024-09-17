"""Module IMSEnvista getting IMS meteorological readings."""

from __future__ import annotations

import asyncio
import atexit
from typing import TYPE_CHECKING

import requests
from aiohttp import ClientSession, TraceConfig

from .commons import (
    get,
    on_request_chunk_sent_debug,
    on_request_end_debug,
    on_request_start_debug,
)
from .const import (
    API_NAME,
    API_REGION_ID,
    API_STATIONS,
    GET_ALL_REGIONS_DATA_URL,
    GET_ALL_STATIONS_DATA_URL,
    GET_DAILY_STATION_DATA_URL,
    GET_EARLIEST_STATION_DATA_URL,
    GET_LATEST_STATION_DATA_URL,
    GET_MONTHLY_STATION_DATA_BY_MONTH_URL,
    GET_MONTHLY_STATION_DATA_URL,
    GET_SPECIFIC_REGION_DATA_URL,
    GET_SPECIFIC_STATION_DATA_URL,
    GET_STATION_DATA_BY_DATE_URL,
    GET_STATION_DATA_BY_RANGE_URL,
    VARIABLES,
)
from .meteo_data import (
    StationMeteorologicalReadings,
    station_meteo_data_from_json,
)
from .station_data import RegionInfo, StationInfo, region_from_json, station_from_json

if TYPE_CHECKING:
    from datetime import date
    from uuid import UUID

    from .ims_variable import IMSVariable

# ims.gov.il does not support ipv6 yet, `requests` use ipv6 by default
# and wait for timeout before trying ipv4, so we have to disable ipv6
requests.packages.urllib3.util.connection.HAS_IPV6 = False


class IMSEnvista:
    """API Wrapper to IMS Envista."""

    def __init__(self, token: UUID | str, session: ClientSession | None = None) -> None:
        if not token:
            raise ValueError

        # Custom Logger to the session
        trace_config = TraceConfig()
        trace_config.on_request_start.append(on_request_start_debug)
        trace_config.on_request_chunk_sent.append(on_request_chunk_sent_debug)
        trace_config.on_request_end.append(on_request_end_debug)
        trace_config.freeze()

        if not session:
            session = ClientSession(trace_configs=[trace_config])
            atexit.register(self._shutdown)
        else:
            session.trace_configs.append(trace_config)

        self._session = session
        self._token = token

    def _shutdown(self) -> None:
        if not self._session.closed:
            asyncio.run(self._session.close())

    @staticmethod
    def _get_channel_id_url_part(channel_id: int) -> str:
        """Get specific Channel Id url param."""
        if channel_id:
            return "/" + str(channel_id)
        return ""

    async def get_latest_station_data(
            self, station_id: int, channel_id: int | None = None
        ) -> StationMeteorologicalReadings:
        """
        Fetch the latest station data from IMS Envista API.

        Args:
        ----
            station_id (int): IMS Station Id
            channel_id (int): [Optional] Specific Channel Id

        Returns:
        -------
            data: Current station meteorological data

        """
        get_url = GET_LATEST_STATION_DATA_URL.format(
            str(station_id), self._get_channel_id_url_part(channel_id)
        )
        return station_meteo_data_from_json(await get(get_url, self._token))

    async def get_earliest_station_data(
            self, station_id: int, channel_id: int | None = None
        ) -> StationMeteorologicalReadings:
        """
        Fetch the earliest station data from IMS Envista API.

        Args:
        ----
            station_id (int): IMS Station ID
            channel_id (int): [Optional] Specific Channel ID

        Returns:
        -------
            data: Current station meteorological data

        """
        get_url = GET_EARLIEST_STATION_DATA_URL.format(
            str(station_id), self._get_channel_id_url_part(channel_id)
        )
        return station_meteo_data_from_json(await get(get_url, self._token))

    async def get_station_data_from_date(
            self, station_id: int, date_to_query: date, channel_id: int | None = None
        ) -> StationMeteorologicalReadings:
        """
        Fetch latest station data from IMS Envista API by date.

        Args:
        ----
            station_id (int): IMS Station ID
            date_to_query (date): Selected date to query
            channel_id (int): [Optional] Specific Channel Id

        Returns:
        -------
            data: Current station meteorological data

        """
        get_url = GET_STATION_DATA_BY_DATE_URL.format(
            str(station_id),
            self._get_channel_id_url_part(channel_id),
            str(date_to_query.year),
            str(date_to_query.month),
            str(date_to_query.day),
        )
        return station_meteo_data_from_json(await get(get_url, self._token))

    async def get_station_data_by_date_range(
            self,
            station_id: int,
            from_date: date,
            to_date: date,
            channel_id: int | None = None,
        ) -> StationMeteorologicalReadings:
        """
        Fetch latest station data from IMS Envista API by date range.

        Args:
        ----
            station_id (int): IMS Station ID
            from_date (date): From date to query
            to_date (date): to date to query
            channel_id (int): [Optional] Specific Channel Id

        Returns:
        -------
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
        return station_meteo_data_from_json(await get(get_url, self._token))

    async def get_daily_station_data(
            self, station_id: int, channel_id: int | None = None
        ) -> StationMeteorologicalReadings:
        """
        Fetch the daily station data from IMS Envista API.

        Args:
        ----
            station_id (int): IMS Station ID
            channel_id (int): [Optional] Specific Channel Id

        Returns:
        -------
            data: Current station meteorological data

        """
        get_url = GET_DAILY_STATION_DATA_URL.format(
            str(station_id),
            self._get_channel_id_url_part(channel_id),
        )
        return station_meteo_data_from_json(await get(get_url, self._token))

    async def get_monthly_station_data(
            self,
            station_id: int,
            channel_id: int | None = None,
            month: str | None = None,
            year: str | None = None,
        ) -> StationMeteorologicalReadings:
        """
        Fetch monthly station data from IMS Envista API.

        Args:
        ----
            station_id (int): IMS Station ID
            channel_id (int): [Optional] Specific Channel Id
            month (str): [Optional] Specific Month in MM format (07)
            year (str):  [Optional] Specific Year in YYYY format (2020)

        Returns:
        -------
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
        return station_meteo_data_from_json(await get(get_url, self._token))

    async def get_all_stations_info(self) -> list[StationInfo]:
        """
        Fetch all stations data from IMS Envista API.

        Returns
        -------
            data: All stations data

        """
        get_url = GET_ALL_STATIONS_DATA_URL
        response = await get(get_url, self._token)
        return [station_from_json(station) for station in response]

    async def get_station_info(self, station_id: int) -> StationInfo:
        """
        Fetch station data from IMS Envista API.

        Args:
        ----
            station_id (int): IMS Station ID

        Returns:
        -------
            data: Current station data

        """
        get_url = GET_SPECIFIC_STATION_DATA_URL.format(str(station_id))
        return station_meteo_data_from_json(await get(get_url, self._token))

    async def get_all_regions_info(self) -> list[RegionInfo]:
        """
        Fetch all regions data from IMS Envista API.

        Returns
        -------
            data: All stations data

        """
        get_url = GET_ALL_REGIONS_DATA_URL
        response = await get(get_url, self._token)
        regions = []
        for region in response:
            stations = [station_from_json(station) for station in region[API_STATIONS]]
            regions.append(
                RegionInfo(region[API_REGION_ID], region[API_NAME], stations)
            )
        return regions

    async def get_region_info(self, region_id: int) -> RegionInfo:
        """
        Fetch region data from IMS Envista API.

        Args:
        ----
            region_id (int): IMS Region ID

        Returns:
        -------
            data: region data

        """
        get_url = GET_SPECIFIC_REGION_DATA_URL.format(str(region_id))
        response = await get(get_url, self._token)
        return region_from_json(response)

    def get_metrics_descriptions(self) -> list[IMSVariable]:
        """
        Return the descriptions of Meteorological Metrics collected by the stations.

        Returns
        -------
            list of IMSVariable, containing description and measuring unit

        """
        return list(VARIABLES.values())
