from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram import types

from typing import Dict, Any, List, Union

from loguru import logger

from main_bot.database import User, LocationUser


class SqlMiddleware(BaseMiddleware):
    async def __call__(self, 
                       handler, 
                       event: Union[types.Message, types.CallbackQuery], 
                       data: Dict[str, Any]):
        logger.debug(f"{event}, {type(event)}")
        user: User = await User.query.where(User.id == event.from_user.id).gino.first()
        if user is None:
            user: User = await User.create(id=event.from_user.id,
                                           first_name=event.from_user.first_name,
                                           last_name=event.from_user.last_name)
        user_loc: LocationUser = await LocationUser.query.where(
            LocationUser.user_id == event.from_user.id).gino.first()
        data['user'] = user
        data['user_loc'] = user_loc
        logger.debug(f"here {user}\n{data}")
        return await handler(event, data)

    def setup(self, router, *events):
        for event in events:
            router.observers[event].outer_middleware.register(self)
