import typing
from aiogram.utils import json
from aiogram.contrib.fsm_storage.redis import RedisStorage2

STATIC_DATA_KEY = 'static'


class RedisStorageStatic(RedisStorage2):
    async def set_data_static(self, *, chat: typing.Union[str, int, None] = None,
                              user: typing.Union[str, int, None] = None,
                              data: typing.Dict = None):
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, STATIC_DATA_KEY)
        if data:
            await self._redis.set(key, json.dumps(data), ex=self._data_ttl)
        else:
            await self._redis.delete(key)

    async def get_data_static(self, *, chat: typing.Union[str, int, None] = None, user: typing.Union[str, int, None] = None,
                       default: typing.Optional[dict] = None) -> typing.Dict:
        chat, user = self.check_address(chat=chat, user=user)
        key = self.generate_key(chat, user, STATIC_DATA_KEY)
        raw_result = await self._redis.get(key)
        if raw_result:
            return json.loads(raw_result)
        return default or {}
