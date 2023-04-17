from .user_table import db, User
from .location_table import LocationUser
from .user_images_table import UserImages
from .updown import on_start, on_shutdown


from aiogram.utils.executor import Executor


def setup(exec: Executor):
    exec.on_startup(on_start)
    exec.on_shutdown(on_shutdown)


__all__ = ['db',
           'User',
           'setup',
           'UserImages',
           'LocationUser']

