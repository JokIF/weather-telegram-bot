import json

from aiogram import Router, types
from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.exceptions import TelegramNotFound, TelegramBadRequest
from loguru import logger

from main_bot.init import redis_main
from contextlib import suppress
from typing import List, Union, Dict, Any

from aiogram import Dispatcher, Bot


class ChainMiddleware(BaseMiddleware):
    async def __call__(self, 
                       handler, 
                       message: Union[types.Message, types.CallbackQuery], 
                       data: Dict[str, Any], 
                       ):
        res_first = res = await handler(message, data)
        logger.debug(f"{res}, {type(res)}")
        if not message:
            return
        if isinstance(message, types.CallbackQuery):
            id_from = message.from_user.id
            message = message.message
        else:
            id_from = message.from_user.id
        bot = data["bot"]
        redis_key = redis_main.build_key(message.chat.id, id_from)
        logger.debug(redis_key)
        if red_data := await redis_main.get(redis_key):
            redis_data = json.loads(red_data)
        else:
            redis_data = {}
        logger.debug(redis_data)
        logger.debug("here")
        
                     # ┐
        if not res:  # | потенциальная
            return   # | багулина
                     # ┘

        if isinstance(res, types.Message):
            res = [res]
        logger.debug(f"{type(res)}, {type(res[0])}")
        res = [mes.message_id for mes in res]
        if mess := redis_data.pop(str(id_from), None):
            for mes in mess:
                with suppress(TelegramBadRequest, TelegramNotFound):
                    logger.debug("here delete")
                    await bot.delete_message(id_from, mes)
        if message:
            res.append(message.message_id)
        if mess := redis_data.get(str(id_from)):
            mess.extend(res)
        else:
            redis_data[id_from] = res
        await redis_main.set(name=redis_key, value=json.dumps(redis_data))
        return res_first

    def setup(self, router, *events):
        for event in events:
            router.observers[event].middleware.register(self)
