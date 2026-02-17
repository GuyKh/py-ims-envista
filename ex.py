"""Example script for querying IMS Envista."""

import asyncio
import os

import aiohttp

from ims_envista import IMSEnvista

# ruff: noqa: T201


STATION_ID = 22


async def main() -> None:
    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False),
        timeout=aiohttp.ClientTimeout(total=60),
    )
    try:
        ims = IMSEnvista(os.environ["IMS_TOKEN"], session)
        print(await ims.get_latest_station_data(STATION_ID))

        daily = await ims.get_daily_station_data(STATION_ID)
        for d in daily.data:
            print(d)

    finally:
        await session.close()


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
