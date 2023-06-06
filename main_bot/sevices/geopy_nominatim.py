from dataclasses import dataclass

import tenacity

from geopy import Location, Nominatim
from geopy.adapters import AioHTTPAdapter
from geopy.exc import GeocoderTimedOut

from functools import singledispatchmethod
from typing import Optional, Union
import logging

from loguru import logger

from main_bot import config


class NoGeoException(Exception):
    pass


class DefineLoc:
    def __init__(self, location: Union[str, list], language):
        self.location = None
        self.location_user = location
        self.language = language
        self.lat: Optional[int] = None
        self.lon = None

    async def define(self):
        async with Nominatim(
                user_agent='SQLWeatherBot',
                adapter_factory=AioHTTPAdapter
        ) as geolocator:
            logger.debug('DefineLoc.define')
            try:
                self.location = await self._geo_rev(
                    self.location_user, geolocator)
            except GeocoderTimedOut:
                logger.exception(GeocoderTimedOut)
                raise
        return self._GeoData(self.get_city, self.lat, self.lon)

    @singledispatchmethod
    async def _geo_rev(self, location_user, geolocator: Nominatim):
        raise ValueError('Invalid data')

    @_geo_rev.register
    @tenacity.retry(retry=tenacity.retry_if_exception_type(GeocoderTimedOut),
                    wait=tenacity.wait_fixed(config.WAIT_TIME),
                    before=tenacity.before_log(logger, logging.DEBUG))
    async def _(self, location_user: str, geolocator: Nominatim):
        logger.debug('str')
        loc: Location = await geolocator.geocode(
            location_user, language=self.language)
        if loc is None:
            raise NoGeoException
        list_loc = [loc.latitude, loc.longitude]
        return await self._geo_rev(list_loc, geolocator)

    @_geo_rev.register
    @tenacity.retry(retry=tenacity.retry_if_exception_type(GeocoderTimedOut),
                    wait=tenacity.wait_fixed(config.WAIT_TIME),
                    before=tenacity.before_log(logger, logging.DEBUG))
    async def _(self, location_user: list, geolocator: Nominatim):
        self.lat, self.lon = location_user
        loc = await geolocator.reverse(
            location_user, language=self.language)
        if loc is None:
            raise NoGeoException
        return loc

    @property
    def get_city(self):
        logger.debug(self.location.raw["address"])
        return self.location.raw['address'].get('city') \
               or self.location.raw['address'].get('town') \
               or self.location.raw["address"].get("county") \
               or self.location.raw["address"].get("state") \
               or self.location.raw["address"].get("country")

    @dataclass
    class _GeoData:
        city: str
        lat: int
        lon: int
