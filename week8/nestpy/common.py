import functools
from typing import Optional

from constants import (CONTROLLER_WATERMARK, INJECTABLE_WATERMARK,
                       METHOD_METADATA, PATH_METADATA)
from enums import RequestMethod, RouteParamtypes
from utils import validateModuleKeys


def Injectable(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        return cls(*args, **kwargs)

    setattr(wrapper, INJECTABLE_WATERMARK, True)

    return wrapper


def Controller(prefix_or_options: Optional[str] = None):
    def decorator(cls):
        @functools.wraps(cls)
        def wrapper(*args, **kwargs):
            return cls(*args, **kwargs)

        default_path = "/"
        if prefix_or_options is None:
            prefix = default_path
        else:
            prefix = prefix_or_options

        setattr(wrapper, CONTROLLER_WATERMARK, True)
        setattr(wrapper, PATH_METADATA, prefix)

        return wrapper

    return decorator


def Module(metadata: dict):
    keys = list(metadata.keys())
    validateModuleKeys(keys)

    def decorator(cls):
        @functools.wraps(cls)
        def wrapper(*args, **kwargs):
            return cls(*args, **kwargs)

        for key, value in metadata.items():
            setattr(wrapper, key, value)

        return wrapper

    return decorator


default_metadata = {
    "PATH_METADATA": "/",
    "METHOD_METADATA": RequestMethod.GET,
}


def RequestMapping(metadata: Optional[str] = None):
    if metadata is None:
        metadata = default_metadata

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        path = metadata.get("PATH_METADATA", "/")
        request_method = metadata.get("METHOD_METADATA", RequestMethod.GET)

        setattr(wrapper, PATH_METADATA, path)
        setattr(wrapper, METHOD_METADATA, request_method)

        return wrapper

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
