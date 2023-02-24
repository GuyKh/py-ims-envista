# IMS Envista
==========================

*ims_envista*  is an unofficial IMS (Israel Meteorological Service) python API wrapper for Envista service.

## Features supported

* Get latest meteorological readings from IMS Envista
* Get measurement data by region, station and date range.
* Get Daily and Monthly readings by measurement station.

## Installing

```bash
pip3 install --upgrade ims-envista
```

## Working with the API

weatheril can be configured to retrive forecast information for specific location. when initiating the library you must set the location id and language (Currently only he and en are supported)

### Getting an IMS Token
You can read about the API and about how to get a token [here](https://ims.gov.il/en/ObservationDataAPI) - signing terms of use, etc.

```python
from ims_envista import IMSEnvista

# Create IMS object with Token
ims = IMSEnvista("2cc57fb1-cda5-4965-af12-b397e5b8eb32")

# Get JERUSALEM stations for getting an id
[station for station in ims.get_all_stations_info() if station.name.startswith("JERUSALEM")]
> [JERUSALEM GIVAT RAM(22) - Location: [Lat - 31.771 / Long - 35.197], Active, Owner: ims, RegionId: 7, Monitors: [
    Rain(mm), WSmax(m / sec), WDmax(deg), WS(m / sec), WD(deg), STDwd(deg), TD(degC), RH( %), TDmax(degC), TDmin(
    degC), Grad(w / m2), DiffR(w / m2), WS1mm(m / sec), Ws10mm(m / sec), Time(hhmm), NIP(
    w / m2)], StationTarget:, JERUSALEM
CENTRE(23) - Location: [Lat - 31.781 / Long - 35.222], Active, Owner: ims, RegionId: 7, Monitors: [Rain(mm),
                                                                                                   WSmax(m / sec),
                                                                                                   WDmax(deg),
                                                                                                   WS(m / sec), WD(deg),
                                                                                                   STDwd(deg), TD(degC),
                                                                                                   TDmax(degC),
                                                                                                   TDmin(degC),
                                                                                                   WS1mm(m / sec),
                                                                                                   Ws10mm(m / sec),
                                                                                                   Time(hhmm), BP(mb),
                                                                                                   RH( %)], StationTarget:, JERUSALEM
CENTRE_1m(248) - Location: [Lat - 31.7806 / Long - 35.2217], Active, Owner: ims, RegionId: 7, Monitors: [Rain_1_min(mm),
                                                                                                         Rain_Corr(
                                                                                                             mm)], StationTarget:, JERUSALEM
GIVAT
RAM_1m(249) - Location: [Lat - 31.7704 / Long - 35.1973], Active, Owner: ims, RegionId: 7, Monitors: [Rain_1_min(mm),
                                                                                                      Rain_Corr(
                                                                                                          mm)], StationTarget:]

# Get latest data by a station id
ims.get_latest_station_data(23)
> Station(23), Data: [Station: 23, Date: 2023 - 02 - 21
12: 00:00 + 02: 00, Readings: [(TD: 17.6°C), (TDmax: 17.8°C), (TDmin: 17.5°C), (RH: 58.0 %), (Rain: 0.0mm),
                               (WS: 2.8m / s), (WSmax: 3.7m / s), (WD: 285.0deg), (WDmax: 289.0deg), (STDwd: 10.5deg),
                               (WS1mm: 3.4m / s), (WS10mm: 2.9m / s)]]
```

## Methods

| Method  | Description  | Parameters  | Returns  |
|--- |--- |--- |--- |
| get_latest_station_data  | Get Latest Station Readings  | station_id: int, <br>(optional) channel_id: int  | [StationMeteorologicalReadings](./ims_envista/meteo_data.py)  |
| get_earliest_station_data  | Get Earliest Station Readings  | station_id: int, <br>(optional) channel_id: int  | [StationMeteorologicalReadings](./ims_envista/meteo_data.py)  |
| get_station_data_from_date  | Get Station Reading from a specific date  | station_id: int, <br>date: datetime, <br>(optional) channel_id: int  | [StationMeteorologicalReadings](./ims_envista/meteo_data.py)  |
| get_station_data_by_date_range  | Get Station Readings from a date range  | station_id: int, <br>from_date: datetime, <br>to_date: datetime, <br>(optional) channel_id: int  | [StationMeteorologicalReadings](./ims_envista/meteo_data.py)  |
| get_daily_station_data  | Get Daily Station Readings  | station_id: int, <br>(optional) channel_id: int  | [StationMeteorologicalReadings](./ims_envista/meteo_data.py)  |
| get_monthly_station_data  | Get Monthly Station Readings  | station_id: int, <br>(optional) channel_id: int, <br>(optional) month: str, [e.g. 03]<br>(optional) year: str [e.g. 2020]  | [StationMeteorologicalReadings](./ims_envista/meteo_data.py)  |
| get_all_stations_data  | Get Station Info of all stations  |   | list[[Station](./ims_envista/station_data.py)]  |
| get_station_data  | Get Station Info by station_id  | station_id: int  | [Station](./ims_envista/station_data.py)  |
| get_all_regions_data  | Get Region Info of all regions  |   | list[[Region](./ims_envista/station_data.py)]  |
| get_region_info  | Get Region Info by region_id  | station_id: int  | [Region](./ims_envista/station_data.py)  |
| get_metric_descriptions  | Get Station Measurements Description  |   | list[IMSVariable](./ims_envista/ims_variable.py)  |

## Local Development

### Clone from Github

Clone the repo from GitHub

```
git clone git@github.com:GuyKh/ims-envista.git
```

### Requirements

Package requirements are handled using pip. To install them do

```
pip install -r requirements.txt
```

### Local Installation

To install locally:

```
python setup.py install
```

## Tests

Testing is set up using [pytest](http://pytest.org) and coverage is handled
with the pytest-cov plugin.

Run your tests with ```py.test``` in the root directory.

Coverage is ran by default and is set in the ```pytest.ini``` file.
To see an html output of coverage open ```htmlcov/index.html``` after running the tests.
