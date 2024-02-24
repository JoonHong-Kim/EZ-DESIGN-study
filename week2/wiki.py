import time
from abc import abstractmethod
from threading import Lock
from typing import Any

import requests


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class SubjectWiki:
    @abstractmethod
    def search(self, query: str) -> Any:
        pass


class WikiApi(SubjectWiki, metaclass=SingletonMeta):
    def search(self, query: str) -> Any:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
        }
        time.sleep(5)
        respons = requests.get(url, params=params)
        result = respons.json()
        return result


class ProxyWiki(SubjectWiki, metaclass=SingletonMeta):
    _wiki_api: WikiApi = None

    def search(self, query: str) -> Any:
        if self._wiki_api is None:
            self._wiki_api = WikiApi()
        return self._wiki_api.search(query)
