from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext

from main_bot.utils.handls_keyboards import keyboard_accep_lang, keyboard_data, keyboard_main_menu
from main_bot.utils import StartStates, SettingsStates, WeatherStates
from main_bot.init import dp

from typing import Union

from loguru import logger


@dp.message_handler(CommandStart())
async def cmd_start(message: Union[types.Message, types.CallbackQuery], locale):
    logger.debug('start now')
    await StartStates.start.set()
    state = Dispatcher.get_current().current_state()
    await state.set_data({'start': True})
    text, reply = keyboard_accep_lang(locale)
    return await message.answer(text=text, reply_markup=reply)
