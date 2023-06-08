import datetime
from typing import Dict, Any

from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from loguru import logger

from sqlalchemy.sql.expression import desc
from main_bot.database import UserImages, User


async def all_user_images(user_id: int):
    desc_obj = desc(UserImages.create_at)
    return await UserImages.query.where(
        UserImages.user_id == user_id).order_by(desc_obj).gino.all()


class TokenMiddleware(BaseMiddleware):

    async def __call__(self,
                       handler,
                       event: types.TelegramObject,
                       data: Dict[str, Any]):
        user: User = data["user"]
        all_images = await all_user_images(user.id)
        data["all_tickets"] = all_images

        if len(all_images) < 4:
            logger.debug("here")
            tickets = 4 - len(all_images)
            data["available_tickets"] = tickets
            return await handler(event, data)

        available_tickets = list(image for image in all_images[:4]
                                 if (datetime.datetime.utcnow() - image.create_at).days != 0)
        data["available_tickets"] = len(available_tickets)
        return await handler(event, data)

    def setup(self, router, *events):
        for event in events:
            router.observers[event].outer_middleware.register(self)
