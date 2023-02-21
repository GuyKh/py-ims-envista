import textwrap


class Location:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        """Latitude"""
        self.longitude = longitude
        """Longitude"""

    def __repr__(self):
        return textwrap.dedent("""[Lat-{}/Long-{}]""").format(
            self.latitude, self.longitude
        )


def location_from_json(json: dict) -> Location:
    """Converts a JSON object to a Location object."""
    return Location(json["latitude"], json["longitude"])


class Monitor:
    def __init__(
        self,
        channel_id: int,
        name: str,
        alias: str,
        active: bool,
        type_id: int,
        pollutant_id: int,
        units: str,
        description: str,
    ):
        self.channel_id = channel_id
        """Channel ID"""
        self.name = name
        """Monitored Condition Name"""
        self.alias = alias
        """Monitored Condition Alias"""
        self.active = active
        """Is the monitored condition active"""
        self.type_id = type_id
        """Monitored Condition Type ID"""
        self.pollutant_id = pollutant_id
        """Monitored Condition Pollutant ID"""
        self.units = units
        """Monitored Condition Units"""
        self.description = description
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


class StationInfo:
    def __init__(
        self,
        station_id: int,
        name: str,
        short_name: str,
        stations_tag: str,
        location: Location,
        timebase: int,
        active: bool,
        owner: str,
        region_id: int,
        monitors: list[Monitor],
        station_target: str,
    ):
        self.station_id = station_id
        """Station ID"""
        self.name = name
        """Station name"""
        self.short_name = short_name
        """Station short name"""
        self.stations_tag = stations_tag
        """Station tags"""
        self.location = location
        """Station Location (Lat/Long)"""
        self.timebase = timebase
        """Timebase"""
        self.active = active
        """Is the station Active"""
        self.owner = owner
        """Station owner"""
        self.region_id = region_id
        """Region ID"""
        self.monitors = monitors
        """List of Monitored Conditions"""
        self.station_target = station_target
        """Station Target"""

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


class RegionInfo:
    def __init__(
        self, region_id: int, name: str, stations: list[StationInfo] = []
    ) -> None:
        self.region_id = region_id
        """Region ID"""
        self.name = name
        """Region Name"""
        self.stations = stations
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
