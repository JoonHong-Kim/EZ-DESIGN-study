import logging

from cache_response import cache_response
from dependency_injector import containers, providers
from exception_handler import exception_handler
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from log_handler import log_request_handler
from wiki import ProxyWiki, WikiApi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


class Container(containers.DeclarativeContainer):
    wiki_api = providers.Singleton(WikiApi)
    proxy_wiki = providers.Singleton(ProxyWiki, wiki_api=wiki_api)


@app.get("/")
@exception_handler
@log_request_handler
@cache_response
def search_wiki(request: Request, query: str = None) -> JSONResponse:
    container = Container()
    wiki = container.proxy_wiki()
    result = wiki.search(query)
    return JSONResponse(content=result, status_code=200)


@app.get("/error")
def error(message: str) -> JSONResponse:
    raise Exception(message)
