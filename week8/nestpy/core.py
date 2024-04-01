import importlib
import inspect
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Any, Type

from .common import Module


class NestFactory:
    @staticmethod
    def create(module: Type[Module]):
        return NestApplication(module)


class NestApplication:
    def __init__(self, module: Type[Module]):
        self.module = module
        self.controllers = []
        self.providers = {}
        self._setup_controllers_and_providers()

    def _setup_controllers_and_providers(self):
        for name, cls in inspect.getmembers(
            importlib.import_module(self.module.__module__), inspect.isclass
        ):
            if hasattr(cls, "__controller__"):
                self.controllers.append(cls)
            if hasattr(cls, "__provider__"):
                self.providers[cls.__name__] = cls()

        for controller in self.controllers:
            for _, func in inspect.getmembers(controller, inspect.isfunction):
                if hasattr(func, "__route__"):
                    args = inspect.signature(func).parameters
                    dependencies = {
                        arg: self.providers[arg]
                        for arg in args
                        if arg in self.providers
                    }
                    controller_instance = controller(**dependencies)
                    func.__func__.__self__ = controller_instance

    def serve(self, port: int = 8000):
        class RequestHandler(SimpleHTTPRequestHandler):
            def do_GET(self):
                self.handle_request("GET")

            def do_POST(self):
                self.handle_request("POST")

            def handle_request(self, method: str):
                path = self.path.split("?")[0]
                for controller in self.server.app.controllers:
                    for _, func in inspect.getmembers(controller, inspect.isfunction):
                        if hasattr(func, "__route__") and func.__route__ == path:
                            if func.__method__ == method:
                                args = inspect.signature(func).parameters
                                kwargs = {}
                                for arg in args:
                                    if hasattr(args[arg].annotation, "__origin__"):
                                        annotation = args[arg].annotation.__origin__
                                        if annotation == Query:
                                            query_params = self.path.split("?")[
                                                1
                                            ].split("&")
                                            for param in query_params:
                                                key, value = param.split("=")
                                                if key == arg:
                                                    kwargs[arg] = Query(value)
                                        elif annotation == Body:
                                            length = int(
                                                self.headers.get("Content-Length")
                                            )
                                            kwargs[arg] = Body(
                                                self.rfile.read(length).decode()
                                            )
                                        elif annotation == Param:
                                            kwargs[arg] = Param(
                                                self.path.split("/")[-1]
                                            )
                                self.send_response(200)
                                self.send_header("Content-type", "application/json")
                                self.end_headers()
                                response = func(**kwargs)
                                self.wfile.write(str(response).encode())
                                return

        handler = RequestHandler
        handler.server = self
        httpd = HTTPServer(("", port), handler)
        httpd.app = self
        httpd.serve_forever()
