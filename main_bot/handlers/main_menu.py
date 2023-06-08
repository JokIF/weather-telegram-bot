import datetime
from typing import Union, List

from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters import Command
from magic_filter import F

from main_bot.database import User, LocationUser
from main_bot.init import dp, sql_router, token_router
from main_bot.utils.handls_keyboards import KeyboardData, keyboard_main_menu
from main_bot.utils.states import WeatherStates, SettingsStates, StartStates
from main_bot.handlers.weather_current import all_user_images


@token_router.callback_query(KeyboardData.filter(F.action == 'back_main'),
                             SettingsStates.setting)
@token_router.callback_query(KeyboardData.filter(F.action == 'back_main'),
                             WeatherStates.history)
@token_router.callback_query(KeyboardData.filter(F.action == 'back_main'),
                             WeatherStates.current_weather)
@token_router.message(Command("menu"))
@token_router.callback_query(KeyboardData.filter(F.action == 'yes_loc'),
                             StartStates.start)
async def main_menu(message: Union[types.CallbackQuery, types.Message],
                    user_loc: LocationUser,
                    available_tickets: int,
                    all_tickets,
                    state: FSMContext):
    if hasattr(message, "message"):
        message = message.message
    if not user_loc:
        await message.delete()
        return
    time_to_update = ""
    start = (await state.get_data()).get("start")
    await state.clear()

    if not available_tickets:
        time_to_update = str(all_tickets[-1].create_at - datetime.datetime.utcnow())
        time_to_update = time_to_update.split(",")[-1] if "," in time_to_update else time_to_update
    text, reply = keyboard_main_menu(available_tickets, time_to_update, start)
    return await message.answer(text=text, reply_markup=reply)
