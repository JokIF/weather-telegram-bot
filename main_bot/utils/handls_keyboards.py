from aiogram.filters.callback_data import CallbackData
from aiogram.utils.i18n import gettext as _
from aiogram import types
from babel import Locale
from loguru import logger

from main_bot.utils.formating import u, b, i


class KeyboardData(CallbackData, prefix="my"):
    action: str


def keyboard_accep_lang(locale):
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=_('Yes', locale=locale),
                                       callback_data=KeyboardData(action='yes_lang').pack()),

            types.InlineKeyboardButton(text=_('No', locale=locale),
                                       callback_data=KeyboardData(action='no_lang').pack())
        ]
    ])
    logger.debug(f'{locale} {type(locale)}')
    logger.debug(Locale('en').languages[locale].lower())
    text = _('i18n is your language?(i18n){locale}:flag:', locale=locale)
    logger.debug(text)
    text = text.format(locale=locale)
    return text, inline


def keyboard_choose_lang():
    inline = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            types.InlineKeyboardButton(text='Русский🇷🇺',
                                       callback_data=KeyboardData(action='ru').pack()),

            types.InlineKeyboardButton(text='English🇺🇸',
                                       callback_data=KeyboardData(action='en').pack())
        ]
    ])

    text = _('Choose your language') + '💬'

    return text, inline


def keyboard_selloc():
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            types.KeyboardButton(text=_('get my location'), request_location=True)
        ]
    ])

    text = _('enter your location') + "📍"

    return text, reply


def keyboard_cancle_button():
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=_('cancel'),
                                       callback_data=KeyboardData(action='cancel_to_sett').pack())
        ]
    ])

    text = _('or go back to setting') + '⚙'

    return text, inline


def keyboard_accep_loc(location: str):
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=_('Yes'),
                                       callback_data=KeyboardData(action='yes_loc').pack()),
            types.InlineKeyboardButton(text=_('No'),
                                       callback_data=KeyboardData(action='no_loc').pack())
        ]
    ])

    text = _('is correct location?') + f' {location}' + '🏰'

    return text, inline


def keyboard_main_menu(tickets, time_, start=False):
    reply = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
        [
            types.KeyboardButton(text=_('Current weather') + '🌤')
        ],
        [
            types.KeyboardButton(text=_('requests history') + '🗄'),
            types.KeyboardButton(text=_('Settings') + '⚙')
        ]
    ])

    text = _('<b>Tickets</b> available') + ": " + str(tickets) + " 🎟\n"
    if time_ and not tickets:
        text = text + _("Remaining to update <b>ticket</b>") + f": {time_.split('.')[0]} ⏰\n"

    if start:
        text = text + "\n" + i(_("you can request weather for tickets")) + "\n"\
               + i(_("1 ticket = 1 request")) if start else text

    return text, reply


def keyboard_settings_menu(address: str, language: str):
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=_('Change location') + "🏰",
                                       callback_data=KeyboardData(action='change_loc').pack()),
            types.InlineKeyboardButton(text=_('Change language') + "🗣",
                                       callback_data=KeyboardData(action='change_lang').pack())
        ],
        [
            types.InlineKeyboardButton(text="↩",
                                       callback_data=KeyboardData(action='back_main').pack())
        ]
    ])

    text = _('your address:') + b(f' {address}') + "📍\n" \
           + _('your language') + b(' {language}').format(language=Locale(language).language_name) + "💬"

    return text, inline


def keyboard_weather_current():
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=_("menu"),
                                       callback_data=KeyboardData(action='back_main').pack())
        ]
    ])

    text = _('into the history')

    return text, inline


def keyboard_weather_current_cancel():
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=_('okay'),
                                       callback_data=KeyboardData(action='back_main').pack())
        ]
    ])

    text = _("your <b>tickets</b> are over") + "😢"

    return text, inline


def keyboard_weather_history(page, left=False, right=True):
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [],
        [
            types.InlineKeyboardButton(text=_('back'),
                                       callback_data=KeyboardData(action='back_main').pack())
        ]
    ])

    if left:
        button_left = types.InlineKeyboardButton(text='<<',
                                                 callback_data=KeyboardData(action='left').pack())
        inline.inline_keyboard[0].append(button_left)
    if right:
        button_right = types.InlineKeyboardButton(text='>>',
                                                  callback_data=KeyboardData(action='right').pack())
        inline.inline_keyboard[0].append(button_right)

    text = "📃" + _('Page') + f' {page}'

    return text, inline
