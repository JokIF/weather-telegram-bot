from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from main_bot.utils.handls_keyboards import keyboard_accep_lang
from main_bot.utils import StartStates
from main_bot.init import dp, sql_router

from typing import Union

from loguru import logger


@sql_router.message(CommandStart())
async def cmd_start(message: Union[types.Message, types.CallbackQuery], locale, state: FSMContext):
    logger.debug('start now')
    await state.set_state(StartStates.start)
    await state.set_data({'start': True})
    text, reply = keyboard_accep_lang(locale)
    return await message.answer(text=text, reply_markup=reply)
