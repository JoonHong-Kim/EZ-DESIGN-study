import logging
import time

from fastapi import Request
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_request_handler(func):
    def wrapper(
        request: Request, query: str = None, message: str = None
    ) -> JSONResponse:
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request url: {request.url}")
        logger.info(f"Client ip: {request.client.host}")
        start_time = time.time()
        response = func(request, query)
        process_time = time.time() - start_time
        logger.info(f"Request Processing time: {process_time}")
        logger.info(f"Response status code: {response.status_code}")
        return response

    return wrapper
