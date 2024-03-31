import time
from abc import abstractmethod
from typing import Any

import requests


class SubjectWiki:
    @abstractmethod
    def search(self, query: str) -> Any:
        pass


class WikiApi(SubjectWiki):
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


class ProxyWiki(SubjectWiki):
    def __init__(self, wiki_api: WikiApi):
        self._wiki_api = wiki_api

    def search(self, query: str) -> Any:
        if self.check_access():
            return self._wiki_api.search(query)
        return None

    def check_access(self) -> bool:
        print("Proxy: Checking access prior to firing a real request.")
        return True
