from aiogram.utils.i18n import gettext as __
from aiogram.filters import BaseFilter
from aiogram import types

from main_bot.database import User


class WeatherCurrentWord(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        language = await User.select('language').where(
            User.id == message.from_user.id).gino.scalar()
        return __('current weather', locale=language) + '🌤' == message.text
