from aiogram import types, Bot, Dispatcher, Router
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from main_bot.utils.redis_static import redis_main
from main_bot.utils.set_commands import set_commands
from main_bot.sevices.gismeteo_service import GismeteoDraw
from main_bot import config

from loguru import logger


gismeteo = GismeteoDraw(config.GISMETEO_TOKEN)
bot = Bot(config.BOT_TOKEN, parse_mode="HTML")
redis_static = RedisStorage(redis_main,
                            key_builder=DefaultKeyBuilder(prefix="static"))
storage = RedisStorage(redis_main)
dp = Dispatcher(storage=storage)
sql_router = Router(name="sql")
token_router = Router(name="token")
trash_router = Router(name="trash")


async def notify_all_working(bot: Bot):
    logger.info('all working')


async def close_redis(bot: Bot):
    logger.info('redis closing')
    await dp.storage.close()


def setup():
    import main_bot.handlers
    sql_router.include_router(token_router)
    dp.include_router(sql_router)
    dp.include_router(trash_router)

    import main_bot.middlewares as middlewares
    middlewares.setup(dp)

    import main_bot.database as database
    database.setup(dp)

    # dp.startup.register(set_commands)
    dp.startup.register(notify_all_working)
    dp.shutdown.register(close_redis)
