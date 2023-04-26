from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram import types

from main_bot.init import dp

from contextlib import suppress


@dp.message_handler(state='*')
async def trash(message: types.Message):
    with suppress(MessageToDeleteNotFound):
        await message.delete()
