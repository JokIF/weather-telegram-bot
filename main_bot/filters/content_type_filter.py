from aiogram import types
from aiogram.filters import BaseFilter


class ContentType(BaseFilter):
    def __init__(self, *content_types):
        self.content_types = content_types
    
    async def __call__(self, message: types.Message):
        return any(message.content_type == content for content in self.content_types)
        