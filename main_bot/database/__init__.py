from .user_table import db, User
from .location_table import LocationUser
from .user_images_table import UserImages
from .updown import on_start, on_shutdown

from aiogram import Dispatcher


def setup(dp: Dispatcher):
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)


__all__ = ['db',
           'User',
           'setup',
           'UserImages',
           'LocationUser']

