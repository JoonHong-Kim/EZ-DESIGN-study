import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from cache_response import cache_response
from exception_handler import exception_handler
from log_handler import log_request_handler
from wiki import ProxyWiki

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


@app.get("/")
@exception_handler
@log_request_handler
@cache_response
def search_wiki(request: Request, query: str = None) -> JSONResponse:
    wiki = ProxyWiki()
    result = wiki.search(query)
    return JSONResponse(content=result, status_code=200)


@app.get("/error")
def error(message: str) -> JSONResponse:
    raise Exception(message)
