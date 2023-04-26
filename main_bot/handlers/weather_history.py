from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger

from main_bot.data import config
from main_bot.database import UserImages, User
from main_bot.init import dp, gismeteo
from main_bot.filters import WeatherHistoryWord
from main_bot.utils.handls_keyboards import keyboard_weather_history
from main_bot.handlers.weather_current import all_user_images
from main_bot.utils import WeatherStates
from main_bot.utils.handls_keyboards import keyboard_data
from main_bot.middlewares import i18n

__ = i18n.gettext


@dp.message_handler(WeatherHistoryWord())
async def weather_history_start(message: types.Message, user: User):
    state = Dispatcher.get_current().current_state()
    all_images = await all_user_images(user.id)
    if not all_images:
        _, inline = keyboard_weather_history(1, left=False, right=False)
        text = __("you must get request first")
        await WeatherStates.history.set()
        return await message.answer(text=text, reply_markup=inline)

    right = False if len(all_images) == 1 else True
    text, inline = keyboard_weather_history(1, right=right)
    with open(all_images[0].url, "rb") as photo:
        bot_mes = await message.answer_photo(
            photo=photo, caption=text, reply_markup=inline)
    async with state.proxy() as data:
        data["bot_mes_id"] = bot_mes.message_id
        data["page"] = 0
    await WeatherStates.history.set()
    return bot_mes


@dp.callback_query_handler(keyboard_data.filter(action="right"), state=WeatherStates.history)
@dp.callback_query_handler(keyboard_data.filter(action="left"), state=WeatherStates.history)
async def turn_page(clback: types.CallbackQuery, user: User, state: FSMContext):
    urls = await all_user_images(user.id)
    action = keyboard_data.parse(clback.data).get("action")
    async with state.proxy() as data:
        page = data["page"]
        bot_mes_id: int = data["bot_mes_id"]

    if action == "right":
        page += 1
    elif action == "left":
        page -= 1

    url = urls[page].url
    right = False if page == len(urls) - 1  else True
    left = False if page == 0 else True
    text, inline = keyboard_weather_history(page + 1, left=left, right=right)
    logger.debug(f'{list(ur.url for ur in urls)}, right: {right}, left{left}')
    with open(url, "rb") as photo:
        await dp.bot.edit_message_media(
            media=types.InputMediaPhoto(photo), reply_markup=inline, message_id=bot_mes_id, chat_id=clback.from_user.id)
    await dp.bot.edit_message_caption(
        caption=text, message_id=bot_mes_id, reply_markup=inline, chat_id=clback.from_user.id)
    async with state.proxy() as data:
        data["page"] = page
