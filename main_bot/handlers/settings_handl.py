from aiogram import types, flags
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as __
from magic_filter import F

from main_bot.filters import SettingsWord, ContentType
from main_bot.init import dp, sql_router

from main_bot.utils.states import StartStates, SettingsStates
from main_bot.utils.handls_keyboards import KeyboardData, keyboard_selloc, keyboard_accep_loc, \
    keyboard_settings_menu, keyboard_cancle_button, \
    keyboard_choose_lang, keyboard_accep_lang
from main_bot.sevices.geopy_nominatim import DefineLoc
from main_bot.database import User, LocationUser

from collections import deque
from typing import Union

from loguru import logger


@sql_router.callback_query(KeyboardData.filter(F.action == 'no_loc'),
                           SettingsStates.setting)
@sql_router.callback_query(KeyboardData.filter(F.action == 'no_loc'),
                           StartStates.start)
@sql_router.callback_query(KeyboardData.filter(F.action == 'change_loc'),
                           SettingsStates.setting)
@sql_router.callback_query(KeyboardData.filter(F.action == 'yes_lang'),
                           StartStates.start)
async def setup_location_and_language(clback: types.CallbackQuery, state: FSMContext, user, locale):
    data = await state.get_data()
    start = data.get('start')
    result = deque()

    await user.update(language=locale).apply()
    if KeyboardData.unpack(clback.data).action == 'no_loc':
        mes_after_no = await clback.message.answer(text='try.....')
        result.appendleft(mes_after_no)
    text, reply = keyboard_selloc()
    mes_rep_but = await clback.message.answer(text=text, reply_markup=reply)
    result.appendleft(mes_rep_but)
    await state.set_state(SettingsStates.select_loc)
    if not start:
        text, reply = keyboard_cancle_button()
        mes_inl_but = await clback.message.answer(text=text, reply_markup=reply)
        result.appendleft(mes_inl_but)
        return result
    return mes_rep_but


@dp.callback_query(KeyboardData.filter(F.action == 'change_lang'),
                   SettingsStates.setting)
@dp.callback_query(KeyboardData.filter(F.action == 'no_lang'),
                   SettingsStates.setting)
@dp.callback_query(KeyboardData.filter(F.action == 'no_lang'),
                   StartStates.start)
async def choose_language(clback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text, reply = keyboard_choose_lang()
    if not data.get("start"):
        _, inline_butt = keyboard_cancle_button()
        reply.inline_keyboard.insert(0, inline_butt.inline_keyboard.pop())
    await state.set_state(SettingsStates.select_lang)
    return await clback.message.answer(text=text, reply_markup=reply)


@sql_router.message(ContentType(types.ContentType.LOCATION), SettingsStates.select_loc)
@sql_router.message(SettingsStates.select_loc)
@flags.chat_action("find_location")
async def accepting_loc(message: types.Message, user_loc: LocationUser, state: FSMContext, locale):
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
    if (await state.get_data()).get('start'):
        await state.set_state(StartStates.start)
    else:
        await state.set_state(SettingsStates.setting)

    text, reply = keyboard_accep_loc(geo_data.city)
    return await message.answer(text=text, reply_markup=reply)


@sql_router.message(SettingsWord())
@sql_router.callback_query(KeyboardData.filter(F.action == 'yes_lang'),
                           SettingsStates.setting)
@sql_router.callback_query(KeyboardData.filter(F.action == 'yes_loc'),
                           SettingsStates.setting)
@sql_router.callback_query(KeyboardData.filter(F.action == 'cancel_to_sett'),
                           SettingsStates.select_loc)
@sql_router.callback_query(KeyboardData.filter(F.action == 'cancel_to_sett'),
                           SettingsStates.select_lang)
async def settings_menu(message: Union[types.Message, types.CallbackQuery],
                        user: User,
                        user_loc: LocationUser,
                        state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.set_state(SettingsStates.setting)
    text, reply = keyboard_settings_menu(user_loc.address, user.language)
    return await message.answer(text=text, reply_markup=reply)


# ----------------------
# confirm_language always bottom

@sql_router.callback_query(SettingsStates.select_lang)
@flags.chat_action("typing")
async def confirm_language(clback: types.CallbackQuery,
                           state: FSMContext,
                           user_loc: LocationUser,
                           user: User):
    data = await state.get_data()
    locale = KeyboardData.unpack(clback.data).action
    await user.update(language=locale).apply()
    text, reply = keyboard_accep_lang(locale)
    if data.get('start'):
        await state.set_state(StartStates.start)
        return await clback.message.answer(text=text, reply_markup=reply)
    geo_data = await DefineLoc(user_loc.address, locale).define()
    await user_loc.update(address=geo_data.city).apply()
    await state.set_state(SettingsStates.setting)
    return await clback.message.answer(text=text, reply_markup=reply)
