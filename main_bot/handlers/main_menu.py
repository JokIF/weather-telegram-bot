import datetime
from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Command

from main_bot.database import User
from main_bot.init import dp
from main_bot.utils.handls_keyboards import keyboard_data, keyboard_main_menu
from main_bot.utils.states import WeatherStates, SettingsStates, StartStates
from main_bot.handlers.weather_current import all_user_images


@dp.message_handler(commands="menu", state="*")
@dp.callback_query_handler(keyboard_data.filter(action='back_main'),
                           state=(SettingsStates.setting, WeatherStates.current_weather, WeatherStates.history))
@dp.callback_query_handler(keyboard_data.filter(action='yes_loc'), state=StartStates.start)
async def main_menu(message: Union[types.CallbackQuery, types.Message], user: User, user_loc, state: FSMContext):
    if hasattr(message, "message"):
        message = message.message
    if not user_loc:
        await message.delete()
        return
    time_to_update = ""
    start = (await state.get_data()).get("start")
    await state.finish()
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
