from aiogram.utils.i18n import gettext as __
from aiogram.fsm.context import FSMContext
from aiogram import types, Dispatcher, Bot
from loguru import logger
from magic_filter import F

from main_bot.database import User
from main_bot.init import dp, sql_router
from main_bot.filters import WeatherHistoryWord
from main_bot.utils.handls_keyboards import keyboard_weather_history
from main_bot.handlers.weather_current import all_user_images
from main_bot.utils import WeatherStates
from main_bot.utils.handls_keyboards import KeyboardData


@sql_router.message(WeatherHistoryWord())
async def weather_history_start(message: types.Message, user: User, state: FSMContext):
    all_images = await all_user_images(user.id)
    if not all_images:
        _, inline = keyboard_weather_history(1, left=False, right=False)
        text = __("you must get request first")
        await WeatherStates.history.set()
        return await message.answer(text=text, reply_markup=inline)

    right = False if len(all_images) == 1 else True
    text, inline = keyboard_weather_history(1, right=right)
    url: str = all_images[0].url
    photo = types.BufferedInputFile.from_file(url, "photo_weather")
    bot_mes = await message.answer_photo(
        photo=photo, caption=text, reply_markup=inline)
    state_data = {"bot_mes_id": bot_mes.message_id,
                  "page": 0}
    await state.set_data(state_data)
    await state.set_state(WeatherStates.history)
    return bot_mes


@sql_router.callback_query(KeyboardData.filter(F.action == "right"), WeatherStates.history)
@sql_router.callback_query(KeyboardData.filter(F.action == "left"), WeatherStates.history)
async def turn_page(clback: types.CallbackQuery, user: User, state: FSMContext, bot: Bot):
    urls = await all_user_images(user.id)
    action = KeyboardData.unpack(clback.data).action
    bot_mes_id, page = (await state.get_data()).values()

    if action == "right":
        page += 1
    elif action == "left":
        page -= 1

    url = urls[page].url
    right = page != len(urls) - 1
    left = page != 0
    text, inline = keyboard_weather_history(page + 1, left=left, right=right)
    logger.debug(f'{list(ur.url for ur in urls)}, right: {right}, left{left}')
    photo = types.BufferedInputFile.from_file(url, "weather_photo")
    await bot.edit_message_media(
        media=types.InputMediaPhoto(media=photo), reply_markup=inline, message_id=bot_mes_id, chat_id=clback.from_user.id)
    await bot.edit_message_caption(
        caption=text, message_id=bot_mes_id, reply_markup=inline, chat_id=clback.from_user.id)
    await state.update_data({"page": page})
