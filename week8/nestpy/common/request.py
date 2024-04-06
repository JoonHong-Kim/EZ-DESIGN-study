from typing import Generic, Optional, TypeVar

from ..constants import METHOD_METADATA, PATH_METADATA
from ..enums import RequestMethod


def RequestMapping(metadata: dict):

    def decorator(func):

        path = metadata.get("PATH_METADATA")
        if path is None:
            path = "/"
        request_method = metadata.get("METHOD_METADATA")
        setattr(func, PATH_METADATA, path)
        setattr(func, METHOD_METADATA, request_method)

        return func

    return decorator


def create_mapping_decorator(method):
    def decorator(path: Optional[str] = None):
        return RequestMapping(
            {
                "PATH_METADATA": path,
                "METHOD_METADATA": method,
            }
        )

    return decorator


Post = create_mapping_decorator(RequestMethod.POST)
Get = create_mapping_decorator(RequestMethod.GET)


T = TypeVar("T")


class RequestItem(Generic[T]):
    def __init__(self, data: T):
        self.data = data


class Body(RequestItem[T]):
    pass


class Param(RequestItem[T]):
    pass


class Query(RequestItem[T]):
    pass
