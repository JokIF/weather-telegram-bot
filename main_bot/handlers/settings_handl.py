from aiogram import types
from aiogram.dispatcher import FSMContext

from main_bot.filters import SettingsWord

from main_bot.init import dp

from main_bot.utils.states import StartStates, SettingsStates
from main_bot.utils.handls_keyboards import keyboard_data, keyboard_selloc, keyboard_accep_loc, \
    keyboard_settings_menu, keyboard_cancle_button, \
    keyboard_choose_lang, keyboard_accep_lang
from main_bot.sevices.geopy_nominatim import DefineLoc
from main_bot.database import User, LocationUser
from main_bot.middlewares import i18n

from collections import deque
from typing import Union

from loguru import logger


__ = i18n.gettext


@dp.callback_query_handler(keyboard_data.filter(action='no_loc'),
                           state=(SettingsStates.setting,
                                  StartStates.start))
@dp.callback_query_handler(keyboard_data.filter(action='change_loc'),
                           state=SettingsStates.setting)
@dp.callback_query_handler(keyboard_data.filter(action='yes_lang'),
                           state=StartStates.start)
async def setup_location_and_language(clback: types.CallbackQuery, state: FSMContext, user: User, locale):
    await SettingsStates.select_loc.set()
    data = await state.get_data()
    start = data.get('start')
    result = deque()

    await user.update(language=locale).apply()

    if keyboard_data.parse(clback.data).get('action') == 'no_loc':
        mes_after_no = await clback.message.answer(text='try.....')
        result.appendleft(mes_after_no)
    text, reply = keyboard_selloc()
    mes_rep_but = await clback.message.answer(text=text, reply_markup=reply)
    result.appendleft(mes_rep_but)
    logger.debug(f'{start}, {type(start)}')
    if not start:
        text, reply = keyboard_cancle_button()
        mes_inl_but = await clback.message.answer(text=text, reply_markup=reply)
        result.appendleft(mes_inl_but)
        return result
    return mes_rep_but


@dp.callback_query_handler(keyboard_data.filter(action='change_lang'),
                           state=SettingsStates.setting)
@dp.callback_query_handler(keyboard_data.filter(action='no_lang'),
                           state=(SettingsStates.setting,
                                  StartStates.start))
async def choose_language(clback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.debug(data)
    await SettingsStates.select_lang.set()
    text, reply = keyboard_choose_lang()
    if not data.get("start"):
        _, inline_butt = keyboard_cancle_button()
        reply.insert(inline_butt.inline_keyboard.pop().pop())
    return await clback.message.answer(text=text, reply_markup=reply)


@dp.message_handler(content_types=['location'], state=SettingsStates.select_loc)
@dp.message_handler(state=SettingsStates.select_loc)
async def accepting_loc(message: types.Message, user_loc: LocationUser, state: FSMContext, locale):
    await message.answer_chat_action(types.ChatActions.FIND_LOCATION)
    geo_data = await DefineLoc([message.location.latitude, message.location.longitude]
                               if message.location else message.text, locale).define()

    if user_loc:
        await user_loc.update(address=geo_data.city,
                              lat=geo_data.lat,
                              lon=geo_data.lon).apply()
    elif user_loc is None:
        await LocationUser.create(user_id=message.from_user.id,
                                  address=geo_data.city,
                                  lat=geo_data.lat,
                                  lon=geo_data.lon)
    if await state.get_data('start'):
        await StartStates.start.set()
    else:
        await SettingsStates.setting.set()

    text, reply = keyboard_accep_loc(geo_data.city)
    return await message.answer(text=text, reply_markup=reply)


@dp.message_handler(SettingsWord())
@dp.callback_query_handler(keyboard_data.filter(action='yes_lang'),
                           state=SettingsStates.setting)
@dp.callback_query_handler(keyboard_data.filter(action='yes_loc'),
                           state=SettingsStates.setting)
@dp.callback_query_handler(keyboard_data.filter(action='cancel_to_sett'),
                           state=(SettingsStates.select_loc,
                                  SettingsStates.select_lang))
async def settings_menu(message: Union[types.Message, types.CallbackQuery],
                        user: User,
                        user_loc: LocationUser):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await SettingsStates.setting.set()
    text, reply = keyboard_settings_menu(user_loc.address, user.language)
    return await message.answer(text=text, reply_markup=reply)


# ----------------------
# confirm_language always bottom

@dp.callback_query_handler(state=SettingsStates.select_lang)
async def confirm_language(clback: types.CallbackQuery,
                           state: FSMContext,
                           user_loc: LocationUser,
                           user: User):

    await clback.message.answer_chat_action(types.ChatActions.TYPING)
    data = await state.get_data()
    locale = keyboard_data.parse(clback.data).get("action")
    await user.update(language=locale).apply()
    text, reply = keyboard_accep_lang(locale)
    if data.get('start'):
        await StartStates.start.set()
        return await clback.message.answer(text=text, reply_markup=reply)
    geo_data = await DefineLoc(user_loc.address, locale).define()
    await user_loc.update(address=geo_data.city).apply()
    await SettingsStates.setting.set()
    return await clback.message.answer(text=text, reply_markup=reply)
