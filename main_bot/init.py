from aiogram.utils.executor import Executor
from aiogram import types, Bot, Dispatcher

from main_bot.utils.redis_static import RedisStorageStatic
from main_bot.utils.set_commands import set_commands
from main_bot.sevices.gismeteo_service import GismeteoDraw
from main_bot import config

from loguru import logger


gismeteo = GismeteoDraw(config.GISMETEO_TOKEN)
bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorageStatic(host=config.REDIS_HOST,
                             port=config.REDIS_PORT,
                             db=config.REDIS_DB,
                             password=config.REDIS_PASSWORD)
dp = Dispatcher(bot=bot, storage=storage)
executor = Executor(dp)


async def notify_all_working(disp: Dispatcher):
    logger.info('all working')


async def close_redis(disp: Dispatcher):
    logger.info('redis closing')
    await disp.storage.close()


def setup():
    import main_bot.middlewares as middlewares
    middlewares.setup(dp)

    import main_bot.filters as filters
    filters.setup(dp)

    import main_bot.handlers

    import main_bot.database as database
    database.setup(executor)
    executor.on_startup(set_commands)
    executor.on_startup(notify_all_working)
    executor.on_shutdown(close_redis)
