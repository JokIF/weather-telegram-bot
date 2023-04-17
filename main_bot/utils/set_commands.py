from aiogram import types, Dispatcher
from main_bot.middlewares import i18n

_ = i18n.gettext


async def set_commands(dp: Dispatcher):
    command = [types.BotCommand("/menu", "Return to menu")]
    await dp.bot.set_my_commands(command)
