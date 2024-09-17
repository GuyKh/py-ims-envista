"""Test IMS Envista API."""

import os
import unittest
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from aiohttp import ClientSession

from ims_envista import IMSEnvista


def to_date_time(d: date) -> datetime:
    """Convert date to datetime."""
    return datetime(d.year, d.month, d.day).astimezone()


class TestIMSEnvista(unittest.IsolatedAsyncioTestCase):
    """Test IMS Envista API."""

    async def asyncSetUp(self) -> None:
        """Do Setup."""
        self.token = os.environ.get("IMS_TOKEN")
        self.station_id = 178  # TEL AVIV COAST station
        self.region_id = 13
        self.channel_id = 7  # TD = Temperature Channel

        # Initialize the session in an async context
        self.session = ClientSession()
        self.ims = IMSEnvista(self.token, session=self.session)

    async def asyncTearDown(self) -> None:
        """Tear Down."""
        await self.session.close()


    async def test_get_all_regions_info(self) -> None:
        """Test get_all_regions_info endpoint."""
        regions = await self.ims.get_all_regions_info()

        assert regions is not None
        assert len(regions) > 0


    async def test_get_region_info(self) -> None:
        """Test get_regions_info endpoint."""
        region = await self.ims.get_region_info(self.region_id)

        assert region is not None
        assert region.region_id == self.region_id


    async def test_get_all_stations_info(self) -> None:
        """Test get_all_stations_info endpoint."""
        stations = await self.ims.get_all_stations_info()

        assert stations is not None
        assert len(stations) > 0


    async def test_get_station_info(self) -> None:
        """Test get_region_info endpoint."""
        station = await self.ims.get_station_info(self.station_id)

        assert station is not None
        assert station.station_id == self.station_id


    async def test_get_latest_station_data(self) -> None:
        """Test get_latest_station endpoint."""
        station_data = await self.ims.get_latest_station_data(self.station_id)

        assert station_data is not None
        assert station_data.station_id == self.station_id
        assert station_data.data is not None
        assert len(station_data.data) > 0
        assert station_data.data[0].td > 0


    async def test_get_latest_station_data_with_channel(self) -> None:
        """Test get_latest_station_data endpoint with channel."""
        station_data = await self.ims.get_latest_station_data(
            self.station_id, self.channel_id
        )

        assert station_data is not None
        assert station_data.station_id == self.station_id
        assert station_data.data is not None
        assert len(station_data.data) > 0
        assert station_data.data[0].td > 0


    async def test_get_earliest_station_data(self) -> None:
        """Test get_earliest_station_data endpoint."""
        station_data = await self.ims.get_earliest_station_data(self.station_id)

        assert station_data is not None
        assert station_data.station_id == self.station_id
        assert station_data.data is not None
        assert len(station_data.data) > 0
        assert station_data.data[0].td > 0


    async def test_get_earliest_station_data_with_channel(self) -> None:
        """Test get_earliest_station_data endpoint with channel."""
        station_data = await self.ims.get_earliest_station_data(
            self.station_id, self.channel_id
        )

        assert station_data is not None
        assert station_data.station_id == self.station_id
        assert station_data.data is not None
        assert len(station_data.data) > 0
        assert station_data.data[0].td > 0


    async def test_get_station_data_from_date(self) -> None:
        """Test get_station_data_from_date endpoint."""
        station_data = await self.ims.get_station_data_from_date(
            self.station_id, datetime.now(tz=ZoneInfo("Asia/Jerusalem"))
        )

        assert station_data is not None
        assert station_data.station_id == self.station_id
        assert station_data.data is not None
        assert len(station_data.data) > 0
        for station_reading in station_data.data:
            assert station_reading.datetime.date() == datetime.now(tz=ZoneInfo("Asia/Jerusalem")).date()


    async def test_get_station_data_from_date_with_channel(self) -> None:
        """Test get_station_data_from_date endpoint with channel."""
        station_data = await self.ims.get_station_data_from_date(
            self.station_id, datetime.now(tz=ZoneInfo("Asia/Jerusalem")), self.channel_id
        )

        assert station_data is not None
        assert station_data.station_id == self.station_id
        assert station_data.data is not None
        assert len(station_data.data) > 0
        for station_reading in station_data.data:
            assert station_reading.datetime.date() == datetime.now(tz=ZoneInfo("Asia/Jerusalem")).date()


    async def test_get_station_data_by_date_range(self) -> None:
        """Test get_station_data_by_date_range endpoint."""
        today = datetime.now(tz=ZoneInfo("Asia/Jerusalem"))
        yesterday = today - timedelta(days=1)
        station_data = await self.ims.get_station_data_by_date_range(
            self.station_id, from_date=yesterday, to_date=today
        )

        assert station_data is not None
        assert station_data.station_id == self.station_id
        assert station_data.data is not None
        assert len(station_data.data) > 0
        for station_reading in station_data.data:
            assert station_reading.datetime >= to_date_time(yesterday)
            assert station_reading.datetime < to_date_time(today)
            assert station_reading.td > 0


    async def test_get_station_data_by_date_range_with_channel(self) -> None:
        """Test get_station_data_by_date_range endpoint with channel."""
        today = datetime.now(tz=ZoneInfo("Asia/Jerusalem"))
        yesterday = today - timedelta(days=1)
        station_data = await self.ims.get_station_data_by_date_range(
            self.station_id,
            from_date=yesterday,
            to_date=today,
            channel_id=self.channel_id,
        )

        assert station_data is not None
        assert station_data.station_id == self.station_id
        assert station_data.data is not None
        assert len(station_data.data) > 0
        for station_reading in station_data.data:
            assert station_reading.datetime >= to_date_time(yesterday)
            assert station_reading.datetime < to_date_time(today)
            assert station_reading.td > 0


    async def test_get_monthly_station_data(self) -> None:
        """Test get_monthly_station_data endpoint."""
        year = datetime.now(tz=ZoneInfo("Asia/Jerusalem")).strftime("%Y")
        month = datetime.now(tz=ZoneInfo("Asia/Jerusalem")).strftime("%m")
        station_data = await self.ims.get_monthly_station_data(
            self.station_id, month=month, year=year
        )

        assert station_data is not None
        assert station_data.station_id == self.station_id
        assert station_data.data is not None
        assert len(station_data.data) > 0
        for station_reading in station_data.data:
            assert station_reading.datetime.date().strftime("%Y") == year
            assert station_reading.datetime.date().strftime("%m") == month
            assert station_reading.td > 0


    async def test_get_monthly_station_data_with_channel(self) -> None:
        """Test get_monthly_station_data endpoint with channel."""
        year = datetime.now(tz=ZoneInfo("Asia/Jerusalem")).strftime("%Y")
        month = datetime.now(tz=ZoneInfo("Asia/Jerusalem")).strftime("%m")
        station_data = await self.ims.get_monthly_station_data(
            self.station_id, channel_id=self.channel_id, month=month, year=year
        )

        assert station_data is not None
        assert station_data.station_id == self.station_id
        assert station_data.data is not None
        assert len(station_data.data) > 0
        for station_reading in station_data.data:
            assert station_reading.datetime.date().strftime("%m") == month
            assert station_reading.datetime.date().strftime("%Y") == year
            assert station_reading.td > 0

    def test_get_metrics_descriptions(self) -> None:
        metrics = self.ims.get_metrics_descriptions()

        assert metrics is not None
        assert len(metrics) > 0
