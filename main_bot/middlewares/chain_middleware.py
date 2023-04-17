from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import MessageToDeleteNotFound
from loguru import logger

from main_bot.utils.redis_static import RedisStorageStatic
from contextlib import suppress

from aiogram import Dispatcher


class ChainMiddleware(BaseMiddleware):
    async def _chain(self, message, res, exc=None):
        if not message:
            return
        if isinstance(message, types.CallbackQuery):
            id_from = message.from_user.id
            message = message.message
        else:
            id_from = message.from_user.id
        disp = Dispatcher.get_current()
        bot = disp.bot
        redis: RedisStorageStatic = disp.storage
        data = await redis.get_data_static(chat=message.chat.id,
                                           user=id_from)
                     # ┐
        if not res:  # | потенциальная
            return   # | багулина
                     # ┘

        if not isinstance(res[0], types.Message):
            res = res[0]
        res = [mes.message_id for mes in res]
        if not exc:
            if mess := data.pop(str(id_from), None):
                for mes in mess:
                    with suppress(MessageToDeleteNotFound):
                        await bot.delete_message(id_from, mes)
        if message:
            res.append(message.message_id)
        if mess := data.get(str(id_from)):
            mess.extend(res)
        else:
            data[id_from] = res
        await redis.set_data_static(chat=message.chat.id, user=id_from, data=data)

    async def on_post_process_message(self, message: types.Message, res, data):
        await self._chain(message, res)

    async def on_post_process_callback_query(self, callback: types.CallbackQuery, res, data):
        await self._chain(callback, res)

    async def on_post_process_error(self, update: types.Update, exc, res, data):
        await self._chain(update.message, res, exc)
