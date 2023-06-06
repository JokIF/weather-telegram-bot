from typing import Any, Dict

from aiogram import Router
from aiogram.utils.chat_action import ChatActionMiddleware as ChatActionMiddlewareBase


class ChatActionMiddleware(ChatActionMiddlewareBase):
    def setup(self, router: Router, *events: str):
        for event in events:
            router.observers[event].middleware.register(self)
