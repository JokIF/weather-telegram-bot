from aiogram import types
from loguru import logger

from main_bot.sevices.geopy_nominatim import NoGeoException
from main_bot.init import dp

#
# @dp.errors(exception=NoGeoException)
# async def no_geo_exception(update: types.Update, exc: NoGeoException):
#     logger.exception(f'{exc.__class__.__name__} from\nuser:{update.message.from_user.id}\n'
#                      f'chat:{update.message.chat.id}')
#     return await update.message.answer(text='You may have misspelled the city name. Try again')
