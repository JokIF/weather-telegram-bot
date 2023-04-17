from typing import Optional, Tuple, Any

from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware
from aiogram import types
from babel import Locale

from main_bot.database import User

from loguru import logger


class I18nMiddleware(BaseI18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user: Optional[types.User] = types.User.get_current()
        locale: Optional[Locale] = user.locale if user else None

        if locale and locale.language in self.locales:
            *_, data = args
            if language := await User.select('language').where(
                    User.id == user.id).gino.scalar():
                data['locale'] = language
                return language
            else:
                data['locale'] = locale.language
                return locale.language
        return self.default

