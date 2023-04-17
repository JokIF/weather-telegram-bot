from .user_table import db

from aiogram import Dispatcher
from gino.exceptions import UninitializedError

from loguru import logger
from main_bot.data import config


async def on_start(dp: Dispatcher):
    logger.info(f'db connecting')
    try:
        await db.set_bind(config.POSTGRESQL_URL)
    except UninitializedError:
        logger.exception('Gino engine is not initialized')


async def on_shutdown(dp: Dispatcher):
    bind = db.pop_bind()
    if bind:
        logger.info('db unbinding')
        try:
            await bind.close()
        except UninitializedError:
            logger.exception('Gino engine is not initialized')
