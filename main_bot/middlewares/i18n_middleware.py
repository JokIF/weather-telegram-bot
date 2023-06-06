from typing import List, Optional, Dict, Any, Callable, Awaitable

from aiogram.types import TelegramObject
from aiogram.utils.i18n.middleware import I18nMiddleware as BaseI18nMiddleware
from aiogram import types
from babel import Locale

from loguru import logger

from main_bot.database import User


class I18nMiddleware(BaseI18nMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        current_locale = await self.get_locale(event=event, data=data) or self.i18n.default_locale

        data["locale"] = current_locale

        with self.i18n.context(), self.i18n.use_locale(current_locale):
            return await handler(event, data)

    async def get_locale(self, event: types.TelegramObject, data: Dict[str, Any]) -> Optional[str]:
        user: types.User = data.get("event_from_user")
        locale: Optional[Locale] = Locale(user.language_code) if user else None

        if locale and locale.language in self.i18n.locales:
            if language := await User.select('language').where(
                    User.id == user.id).gino.scalar():
                return language
            else:
                return locale.language
        return

    def setup(self, router, *events):
        for event in events:
            router.observers[event].outer_middleware.register(self)
