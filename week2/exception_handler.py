from fastapi import Request, Response
from fastapi.responses import JSONResponse


def exception_handler(func):
    def wrapper(request: Request, query: str = None, message: str = None) -> Response:
        try:
            if message:
                raise Exception(message)
            response = func(request, query, message)
        except Exception as e:
            response = JSONResponse(content={"error": str(e)}, status_code=500)
        return response

    return wrapper