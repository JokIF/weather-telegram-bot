from aiogram.utils.i18n import gettext as __
from aiogram import Bot, types


async def set_commands(bot: Bot):
    command = [types.BotCommand("/menu", "Return to menu")]
    await bot.set_my_commands(command)
#old