# nestpy/request_handler.py
import inspect
import json
from http.server import SimpleHTTPRequestHandler
from typing import Union, get_args, get_origin
from urllib.parse import parse_qs

from nestpy.common.request import Body, Param, Query

from ..constants import METHOD_METADATA, PATH_METADATA
from ..enums import RequestMethod


class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controllers = kwargs.pop("controllers", [])
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self._handle_request(RequestMethod.GET)

    def do_POST(self):
        self._handle_request(RequestMethod.POST)

    def _handle_request(self, method):
        for controller in self.controllers:
            prefix = getattr(controller, PATH_METADATA)
            for _, func in inspect.getmembers(controller, inspect.isfunction):
                if not hasattr(func, PATH_METADATA):
                    continue
                path = getattr(func, PATH_METADATA)
                if path and self.path.startswith(prefix + path[1:]):
                    if getattr(func, METHOD_METADATA) == method:
                        args = self._parse_args(func)
                        response = func(controller, *args.values())
                        self._send_response(response)
                        return
        self.send_error(404, "Not Found")

    def _parse_args(self, func):
        args = {}
        query_params = parse_qs(self.path.split("?")[1]) if "?" in self.path else {}
        path_params = self.path.split("/")[1:]
        for name, param in inspect.signature(func).parameters.items():
            annotation = param.annotation
            if get_origin(annotation) == Body:
                inner_type = get_args(annotation)[0]
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode()
                args[name] = annotation(inner_type(**json.loads(body)))
            elif get_origin(annotation) == Param:
                if path_params[0] == name:
                    args[name] = annotation(path_params[1])
            elif get_origin(annotation) == Query:
                args[name] = annotation(query_params.get(name, [None])[0])
            elif get_origin(annotation) == Union:
                inner_type = get_args(annotation)[0]
                if get_origin(inner_type) == Query:
                    args[name] = inner_type(query_params.get(name, [None])[0])
        return args

    def _send_response(self, response):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str(response).encode())
