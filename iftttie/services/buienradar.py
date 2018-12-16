from __future__ import annotations

from asyncio import sleep
from datetime import timedelta
from typing import AsyncIterator

from aiohttp import ClientSession, web
from loguru import logger

from iftttie.dataclasses_ import Update
from iftttie.enums import ValueKind
from iftttie.services.base import BaseService

url = 'https://api.buienradar.nl/data/public/2.0/jsonfeed'
keys = (
    ('airpressure', 'air_pressure', ValueKind.RAW),
    ('feeltemperature', 'feel_temperature', ValueKind.TEMPERATURE),
    ('groundtemperature', 'ground_temperature', ValueKind.TEMPERATURE),
    ('humidity', 'humidity', ValueKind.HUMIDITY),
    ('temperature', 'temperature', ValueKind.TEMPERATURE),
    ('winddirection', 'wind_direction', ValueKind.RAW),
    ('windspeed', 'windspeed', ValueKind.RAW),
    ('windspeedBft', 'windspeed_bft', ValueKind.RAW),
)


class Buienradar(BaseService):
    def __init__(self, station_id: int, interval=timedelta(seconds=300.0)):
        self.station_id = station_id
        self.interval = interval.total_seconds()

    async def yield_updates(self, app: web.Application) -> AsyncIterator[Update]:
        session: ClientSession = app['client_session']
        while True:
            async with session.get(url) as response:  # type ClientResponse
                feed = await response.json()
            for measurement in feed['actual']['stationmeasurements']:
                if measurement['stationid'] == self.station_id:
                    for source_key, target_key, kind in keys:
                        yield Update(
                            key=f'buienradar:{self.station_id}:{target_key}',
                            value=measurement[source_key],
                            kind=kind,
                        )
                    break
            else:
                logger.error('Station {station_id} is not found.', station_id=self.station_id)
            await sleep(self.interval)

    def __str__(self) -> str:
        return f'{Buienradar.__name__}(station_id={self.station_id!r})'