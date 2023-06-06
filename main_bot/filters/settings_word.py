from aiogram.utils.i18n import gettext as __
from aiogram.filters import Filter
from aiogram import types
from loguru import logger

from main_bot.database import User


class SettingsWord(Filter):
    async def __call__(self, message: types.Message) -> bool:
        language = await User.select('language').where(
            User.id == message.from_user.id).gino.scalar()
        setting_word = __('Settings', locale=language) + "⚙"
        logger.debug(f"{setting_word}, {message.text}")
        return setting_word == message.text
