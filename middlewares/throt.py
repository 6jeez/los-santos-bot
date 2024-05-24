# спиздил: https://zelenka.guru/threads/6119258/

from typing import (
    Any,
    Callable,
    Dict,
    Awaitable,
)
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from cachetools import TTLCache


def throttled(rate: int, on_throttle: None):
    def decorator(func):
        setattr(func, "rate", rate)
        setattr(func, "on_throttle", on_throttle)
        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self):
        # self.cache = TTLCache(maxsize=10_000, ttl=self.delay)
        self.caches = dict()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        decorated_func = data["handler"].callback

        rate = getattr(decorated_func, "rate", None)
        on_throttle = getattr(decorated_func, "on_throttle", None)

        if rate and isinstance(rate, int):

            if id(decorated_func) not in self.caches:
                self.caches[id(decorated_func)] = TTLCache(maxsize=10_000, ttl=rate)

            if event.chat.id in self.caches[id(decorated_func)].keys():
                if callable(on_throttle):
                    return await on_throttle(event, data)
                else:
                    return
            else:
                self.caches[id(decorated_func)][event.chat.id] = event.chat.id

                return await handler(event, data)
        else:
            return await handler(event, data)
