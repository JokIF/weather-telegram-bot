from .sql_middleware import SqlMiddleware
from .chain_middleware import ChainMiddleware
from .i18n_middleware import I18nMiddleware
from .chat_action_middleware import ChatActionMiddleware
from .token_middleware import TokenMiddleware
from .. import config

from aiogram import Dispatcher
from aiogram.utils.i18n import I18n
from loguru import logger

i18n = I18n(path=config.locales_dir, domain="SQLW")


def setup(dp: Dispatcher):
    defaulte_events = ["message", "callback_query"]
    logger.info('middlewares setup')
    logger.debug(i18n.locales)
    sql_router = dp.sub_routers[0]
    token_router = sql_router.sub_routers[0]
    list_middlewares = [ChainMiddleware(), ChatActionMiddleware(), I18nMiddleware(i18n=i18n)]
    for middleware in list_middlewares:
        middleware.setup(dp, *defaulte_events)
    SqlMiddleware().setup(sql_router, *defaulte_events)
    TokenMiddleware().setup(token_router, *defaulte_events)


__all__ = ['setup']
