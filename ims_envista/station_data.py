import textwrap
from typing import List
from dataclasses import dataclass, field


@dataclass
class Location:
    latitude: float
    """Latitude"""
    longitude: float
    """Longitude"""

    def __repr__(self):
        return textwrap.dedent("""[Lat-{}/Long-{}]""").format(
            self.latitude, self.longitude
        )


def location_from_json(json: dict) -> Location:
    """Converts a JSON object to a Location object."""
    return Location(json["latitude"], json["longitude"])

@dataclass
class Monitor:
    channel_id: int
    """Channel ID"""
    name: str
    """Monitored Condition Name"""
    alias: str
    """Monitored Condition Alias"""
    active: bool
    """Is the monitored condition active"""
    type_id: int
    """Monitored Condition Type ID"""
    pollutant_id: int
    """Monitored Condition Pollutant ID"""
    units: str
    """Monitored Condition Units"""
    description: str
    """Monitored Condition Description"""
    def __repr__(self):
        return textwrap.dedent("""{}({})""").format(self.name, self.units)


def monitor_from_json(json: dict) -> Monitor:
    """Converts a JSON object to a Monitor object."""
    return Monitor(
        json["channelId"],
        json["name"],
        json["alias"],
        json["active"],
        json["typeId"],
        json["pollutantId"],
        json["units"],
        json["description"],
    )

@dataclass
class StationInfo:
    station_id: int
    """Station ID"""
    name: str
    """Station name"""
    short_name: str
    """Station short name"""
    stations_tag: str
    """Station tags"""
    location: Location
    """Station Location (Lat/Long)"""
    timebase: int
    """Timebase"""
    active: bool
    """Is the station Active"""
    owner: str
    """Station owner"""
    region_id: int
    """Region ID"""
    station_target: str
    """Station Target"""
    monitors: List['Monitor'] = field(default_factory=list)
    """List of Monitored Conditions"""

    def __repr__(self):
        return textwrap.dedent(
            """{} ({}) - Location: {}, {}ctive, Owner: {}, RegionId: {}, Monitors: {}, StationTarget: {}"""
        ).format(
            self.name,
            self.station_id,
            self.location,
            ("A" if self.active else "Ina"),
            self.owner,
            self.region_id,
            self.monitors,
            self.station_target,
        )


def station_from_json(json: dict) -> StationInfo:
    """Converts a JSON object to a Station object."""
    return StationInfo(
        json["stationId"],
        json["name"],
        json["shortName"],
        json["stationsTag"],
        location_from_json(json["location"]),
        json["timebase"],
        json["active"],
        json["owner"],
        json["regionId"],
        [monitor_from_json(monitor) for monitor in json["monitors"]],
        json["StationTarget"],
    )

@dataclass
class RegionInfo:
    region_id: int
    """Region ID"""
    name: str
    """Region Name"""
    stations: List['StationInfo'] = field(default_factory=list)
    """List of Stations in the Region"""

    def __repr__(self):
        return textwrap.dedent("""{}({}), Stations: {}""").format(
            self.name, self.region_id, self.stations
        )


def region_from_json(json: dict) -> RegionInfo:
    """Converts a JSON object to a Region object."""
    return RegionInfo(
        json["regionId"],
        json["name"],
        [station_from_json(station) for station in json["stations"]],
    )
