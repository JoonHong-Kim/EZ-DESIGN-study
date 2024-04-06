from http.server import HTTPServer

from .adapter import RequestHandler


class NestApplication:
    def __init__(self, controllers):
        self.controllers = controllers

    def serve(self, port=8000):
        def handler_factory(*args, **kwargs):
            return RequestHandler(*args, controllers=self.controllers, **kwargs)

        httpd = HTTPServer(("", port), handler_factory)

        print(f"Serving on port {port}")
        httpd.serve_forever()
