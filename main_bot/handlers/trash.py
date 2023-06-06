from aiogram.exceptions import TelegramNotFound
from aiogram import types
from loguru import logger

from main_bot.init import trash_router

from contextlib import suppress


@trash_router.message()
async def trash(message: types.Message):
    logger.debug("here")
    with suppress(TelegramNotFound):
        await message.delete()
