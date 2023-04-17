from aiogram import types
from aiogram.utils.callback_data import CallbackData
from babel import Locale
from loguru import logger

from main_bot.utils.formating import u, b, i
from main_bot.middlewares import i18n

_ = i18n.gettext

keyboard_data = CallbackData('main', 'action')


def keyboard_accep_lang(locale):
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=_('Yes', locale=locale),
                                       callback_data=keyboard_data.new('yes_lang')),

            types.InlineKeyboardButton(text=_('No', locale=locale),
                                       callback_data=keyboard_data.new('no_lang'))
        ]
    ])
    logger.debug(f'{locale} {type(locale)}')

    text = _('i18n is your language?(i18n){locale}:flag:', locale=locale).format(
        locale=Locale('en').languages[locale].lower())

    return text, inline


def keyboard_choose_lang():
    inline = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            types.InlineKeyboardButton(text='Русский🇷🇺',
                                       callback_data=keyboard_data.new('ru')),

            types.InlineKeyboardButton(text='English🇺🇸',
                                       callback_data=keyboard_data.new('en'))
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
                                       callback_data=keyboard_data.new('cancel_to_sett'))
        ]
    ])

    text = _('or go back to setting') + '⚙'

    return text, inline


def keyboard_accep_loc(location: str):
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=_('Yes'),
                                       callback_data=keyboard_data.new('yes_loc')),
            types.InlineKeyboardButton(text=_('No'),
                                       callback_data=keyboard_data.new('no_loc'))
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
                                       callback_data=keyboard_data.new('change_loc')),
            types.InlineKeyboardButton(text=_('Change language') + "🗣",
                                       callback_data=keyboard_data.new('change_lang'))
        ],
        [
            types.InlineKeyboardButton(text="↩",
                                       callback_data=keyboard_data.new('back_main'))
        ]
    ])

    text = _('your address:') + b(f' {address}') + "📍\n" \
           + _('your language') + b(' {language}').format(language=Locale(language).language_name) + "💬"

    return text, inline


def keyboard_weather_current():
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=_("menu"),
                                       callback_data=keyboard_data.new('back_main'))
        ]
    ])

    text = _('into the history')

    return text, inline


def keyboard_weather_current_cancel():
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text=_('okay'),
                                       callback_data=keyboard_data.new('back_main'))
        ]
    ])

    text = _("your <b>tickets</b> are over") + "😢"

    return text, inline


def keyboard_weather_history(page, left=False, right=True):
    inline = types.InlineKeyboardMarkup(inline_keyboard=[
        [],
        [
            types.InlineKeyboardButton(text=_('back'),
                                       callback_data=keyboard_data.new('back_main'))
        ]
    ])

    if left:
        button_left = types.InlineKeyboardButton(text='<<',
                                                 callback_data=keyboard_data.new('left'))
        inline.inline_keyboard[0].append(button_left)
    if right:
        button_right = types.InlineKeyboardButton(text='>>',
                                                  callback_data=keyboard_data.new('right'))
        inline.inline_keyboard[0].append(button_right)

    text = "📃" + _('Page') + f' {page}'

    return text, inline
