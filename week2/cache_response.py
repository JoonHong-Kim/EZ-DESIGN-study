from threading import Lock
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse


class Cache:
    _instances = {}
    _lock: Lock = Lock()

    cache: dict = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value


def cache_response(func):
    def wrapper(request: Request, query: str = None) -> JSONResponse:
        cache = Cache()
        key = (
            str(request.url),
            request.method,
            request.client.host,
            query,
        )
        response = cache.get(key)
        if response is None:
            response = func(request, query)
            cache.set(key, response)
        return response

    return wrapper
