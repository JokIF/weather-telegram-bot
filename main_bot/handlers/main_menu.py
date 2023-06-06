import datetime
from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters import Command
from magic_filter import F

from main_bot.database import User
from main_bot.init import dp, sql_router
from main_bot.utils.handls_keyboards import KeyboardData, keyboard_main_menu
from main_bot.utils.states import WeatherStates, SettingsStates, StartStates
from main_bot.handlers.weather_current import all_user_images


@sql_router.callback_query(KeyboardData.filter(F.action == 'back_main'),
                           SettingsStates.setting)
@sql_router.callback_query(KeyboardData.filter(F.action == 'back_main'),
                           WeatherStates.history)
@sql_router.callback_query(KeyboardData.filter(F.action == 'back_main'),
                           WeatherStates.current_weather)
@sql_router.message(Command("menu"))
@sql_router.callback_query(KeyboardData.filter(F.action == 'yes_loc'),
                           StartStates.start)
async def main_menu(message: Union[types.CallbackQuery, types.Message], user: User, user_loc, state: FSMContext):
    if hasattr(message, "message"):
        message = message.message
    if not user_loc:
        await message.delete()
        return
    time_to_update = ""
    start = (await state.get_data()).get("start")
    await state.clear()
    all_images = await all_user_images(user.id)
    available_requests = list(image for image in all_images
                              if (datetime.datetime.utcnow() - image.create_at).days != 0)
    if len(all_images) < 4:
        tickets = 4 - len(all_images)
        available_requests = True
    else:
        tickets = len(available_requests)
    if not available_requests:
        time_to_update = str(all_images[-1].create_at - datetime.datetime.utcnow())
        time_to_update = time_to_update.split(",")[-1] if "," in time_to_update else time_to_update
    text, reply = keyboard_main_menu(tickets, time_to_update, start)
    return await message.answer(text=text, reply_markup=reply)
