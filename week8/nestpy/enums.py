from enum import Enum


class MODULE_METADATA(Enum):
    CONTROLLERS = "controllers"
    PROVIDERS = "providers"


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"


class RouteParamtypes(Enum):
    BODY = "body"
    QUERY = "query"
