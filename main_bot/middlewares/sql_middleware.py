from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from typing import Union
from main_bot.database import User, LocationUser


class SqlMiddleware(BaseMiddleware):
    async def check_BD(self, mes: Union[types.Message, types.CallbackQuery], data: dict):
        user: User = await User.query.where(User.id == mes.from_user.id).gino.first()
        if user is None:
            user: User = await User.create(id=mes.from_user.id,
                                           first_name=mes.from_user.first_name,
                                           last_name=mes.from_user.last_name)
        user_loc: LocationUser = await LocationUser.query.where(
            LocationUser.user_id == mes.from_user.id).gino.first()
        data['user'] = user
        data['user_loc'] = user_loc
        # babel city

    async def on_process_message(self, message: types.Message, data: dict):
        await self.check_BD(message, data)

    async def on_process_callback_query(self, message: types.CallbackQuery, data: dict):
        await self.check_BD(message, data)
