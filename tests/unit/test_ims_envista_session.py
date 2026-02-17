"""Unit tests for session lifecycle in IMSEnvista."""

from __future__ import annotations

from typing import Any

import aiohttp
import pytest

from ims_envista import IMSEnvista
from ims_envista import ims_envista as ims_module
from ims_envista.meteo_data import StationMeteorologicalReadings

STATION_ID = 10


@pytest.mark.asyncio
async def test_lazy_session_creation_and_close() -> None:
    ims = IMSEnvista("token")

    async def fake_get(**_: Any) -> dict[str, Any]:
        return {"stationId": STATION_ID, "data": []}

    original_get = ims_module.get
    ims_module.get = fake_get
    try:
        result = await ims.get_latest_station_data(STATION_ID)
        assert isinstance(result, StationMeteorologicalReadings)
        assert result.station_id == STATION_ID
    finally:
        ims_module.get = original_get
        await ims.close()


@pytest.mark.asyncio
async def test_closed_external_session_raises() -> None:
    session = aiohttp.ClientSession()
    await session.close()
    ims = IMSEnvista("token", session=session)

    with pytest.raises(RuntimeError):
        await ims.get_latest_station_data(STATION_ID)
