from .sql_middleware import SqlMiddleware
from .chain_middleware import ChainMiddleware
from .i18n_middleware import I18nMiddleware

from aiogram import Dispatcher
from main_bot.data import config
from loguru import logger


i18n = I18nMiddleware('SQLW', path=config.locales_dir)
def setup(dp: Dispatcher):
    logger.info('middlewares setup')
    dp.middleware.setup(i18n)
    dp.middleware.setup(SqlMiddleware())
    # dp.middleware.setup(ErrorMiddleware())
    dp.middleware.setup(ChainMiddleware())


__all__ = ['setup', 'i18n']
