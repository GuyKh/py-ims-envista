""" """

import os
import unittest
from datetime import date, datetime, timedelta

from ims_envista import IMSEnvista
from tests import *


def to_date_time(d: date) -> datetime:
    """Convert date to datetime"""
    return datetime(d.year, d.month, d.day).astimezone()


class TestIMSEnvista(unittest.TestCase):
    def setUp(self):
        """Setup"""
        # Load test data
        self.ims = IMSEnvista(os.environ.get("IMS_TOKEN"))
        self.station_id = 178  # TEL AVIV COAST station
        self.region_id = 13
        self.channel_id = 7  # TD = Temperature Channel

    def tearDown(self):
        """Tear Down"""
        self.ims.close()

    def test_get_all_regions_info(self):
        """Test get_all_regions_info endpoint"""
        regions = self.ims.get_all_regions_info()

        self.assertIsNotNone(regions)
        self.assertGreater(len(regions), 0)

    def test_get_region_info(self):
        """Test get_regions_info endpoint"""
        region = self.ims.get_region_info(self.region_id)

        self.assertIsNotNone(region)
        self.assertEqual(region.region_id, self.region_id)

    def test_get_all_stations_info(self):
        """Test get_all_stations_info endpoint"""
        stations = self.ims.get_all_stations_info()

        self.assertIsNotNone(stations)
        self.assertGreater(len(stations), 0)

    def test_get_station_info(self):
        """Test get_region_info endpoint"""
        station = self.ims.get_station_info(self.station_id)

        self.assertIsNotNone(station)
        self.assertEqual(station.station_id, self.station_id)

    def test_get_latest_station_data(self):
        """Test get_latest_station endpoint"""
        station_data = self.ims.get_latest_station_data(self.station_id)

        self.assertIsNotNone(station_data)
        self.assertEqual(station_data.station_id, self.station_id)
        self.assertIsNotNone(station_data.data)
        self.assertGreater(len(station_data.data), 0)
        self.assertGreater(station_data.data[0].td, 0)

    def test_get_latest_station_data_with_channel(self):
        """Test get_latest_station_data endpoint with channel"""
        station_data = self.ims.get_latest_station_data(
            self.station_id, self.channel_id
        )

        self.assertIsNotNone(station_data)
        self.assertEqual(station_data.station_id, self.station_id)
        self.assertIsNotNone(station_data.data)
        self.assertGreater(len(station_data.data), 0)
        self.assertGreater(station_data.data[0].td, 0)

    def test_get_earliest_station_data(self):
        """Test get_earliest_station_data endpoint"""
        station_data = self.ims.get_earliest_station_data(self.station_id)

        self.assertIsNotNone(station_data)
        self.assertEqual(station_data.station_id, self.station_id)
        self.assertIsNotNone(station_data.data)
        self.assertGreater(len(station_data.data), 0)
        self.assertGreater(station_data.data[0].td, 0)

    def test_get_earliest_station_data_with_channel(self):
        """Test get_earliest_station_data endpoint with channel"""
        station_data = self.ims.get_earliest_station_data(
            self.station_id, self.channel_id
        )

        self.assertIsNotNone(station_data)
        self.assertEqual(station_data.station_id, self.station_id)
        self.assertIsNotNone(station_data.data)
        self.assertGreater(len(station_data.data), 0)
        self.assertGreater(station_data.data[0].td, 0)

    def test_get_station_data_from_date(self):
        """Test get_station_data_from_date endpoint"""
        station_data = self.ims.get_station_data_from_date(
            self.station_id, date.today()
        )

        self.assertIsNotNone(station_data)
        self.assertEqual(station_data.station_id, self.station_id)
        self.assertIsNotNone(station_data.data)
        self.assertGreater(len(station_data.data), 0)
        for station_reading in station_data.data:
            self.assertEqual(station_reading.datetime.date(), date.today())

    def test_get_station_data_from_date_with_channel(self):
        """Test get_station_data_from_date endpoint with channel"""
        station_data = self.ims.get_station_data_from_date(
            self.station_id, date.today(), self.channel_id
        )

        self.assertIsNotNone(station_data)
        self.assertEqual(station_data.station_id, self.station_id)
        self.assertIsNotNone(station_data.data)
        self.assertGreater(len(station_data.data), 0)
        for station_reading in station_data.data:
            self.assertEqual(station_reading.datetime.date(), date.today())

    def test_get_station_data_by_date_range(self):
        """Test get_station_data_by_date_range endpoint"""
        today = date.today()
        yesterday = today - timedelta(days=1)
        station_data = self.ims.get_station_data_by_date_range(
            self.station_id, from_date=yesterday, to_date=today
        )

        self.assertIsNotNone(station_data)
        self.assertEqual(station_data.station_id, self.station_id)
        self.assertIsNotNone(station_data.data)
        self.assertGreater(len(station_data.data), 0)
        for station_reading in station_data.data:
            self.assertGreaterEqual(station_reading.datetime, to_date_time(yesterday))
            self.assertLess(station_reading.datetime, to_date_time(today))
            self.assertGreater(station_reading.td, 0)

    def test_get_station_data_by_date_range_with_channel(self):
        """Test get_station_data_by_date_range endpoint with channel"""
        today = date.today()
        yesterday = today - timedelta(days=1)
        station_data = self.ims.get_station_data_by_date_range(
            self.station_id,
            from_date=yesterday,
            to_date=today,
            channel_id=self.channel_id,
        )

        self.assertIsNotNone(station_data)
        self.assertEqual(station_data.station_id, self.station_id)
        self.assertIsNotNone(station_data.data)
        self.assertGreater(len(station_data.data), 0)
        for station_reading in station_data.data:
            self.assertGreaterEqual(station_reading.datetime, to_date_time(yesterday))
            self.assertLess(station_reading.datetime, to_date_time(today))
            self.assertGreater(station_reading.td, 0)

    def test_get_monthly_station_data(self):
        """Test get_monthly_station_data endpoint"""
        year = date.today().strftime("%Y")
        month = date.today().strftime("%m")
        station_data = self.ims.get_monthly_station_data(
            self.station_id, month=month, year=year
        )

        self.assertIsNotNone(station_data)
        self.assertEqual(station_data.station_id, self.station_id)
        self.assertIsNotNone(station_data.data)
        self.assertGreater(len(station_data.data), 0)
        for station_reading in station_data.data:
            self.assertEqual(station_reading.datetime.date().strftime("%Y"), year)
            self.assertEqual(station_reading.datetime.date().strftime("%m"), month)
            self.assertGreater(station_reading.td, 0)

    def test_get_monthly_station_data_with_channel(self):
        """Test get_monthly_station_data endpoint with channel"""
        year = date.today().strftime("%Y")
        month = date.today().strftime("%m")
        station_data = self.ims.get_monthly_station_data(
            self.station_id, channel_id=self.channel_id, month=month, year=year
        )

        self.assertIsNotNone(station_data)
        self.assertEqual(station_data.station_id, self.station_id)
        self.assertIsNotNone(station_data.data)
        self.assertGreater(len(station_data.data), 0)
        for station_reading in station_data.data:
            self.assertEqual(station_reading.datetime.date().strftime("%m"), month)
            self.assertEqual(station_reading.datetime.date().strftime("%Y"), year)
            self.assertGreater(station_reading.td, 0)

    def test_get_metrics_descriptions(self):
        metrics = self.ims.get_metrics_descriptions()

        self.assertIsNotNone(metrics)
        self.assertGreater(len(metrics), 0)
