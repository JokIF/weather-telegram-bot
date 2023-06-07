from aioredis import Redis

from main_bot import config

redis_main = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    password=config.REDIS_PASSWORD)
redis_main.build_key = lambda chat_id, user_id: ":".join(("fsm", str(chat_id), str(user_id), "static"))
