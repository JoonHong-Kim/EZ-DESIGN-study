import inspect

from ..constants import CONTROLLER_WATERMARK, INJECTABLE_WATERMARK
from .application import NestApplication
from .container import Container


class NestFactory:
    @staticmethod
    def create(module_cls):
        module = module_cls()
        container = Container()
        for _, controller in inspect.getmembers(module, inspect.isclass):
            if getattr(controller, CONTROLLER_WATERMARK, False):
                container.add_controller(controller)

        for _, provider in inspect.getmembers(module, inspect.isclass):
            if getattr(provider, INJECTABLE_WATERMARK, False):
                container.add_provider(provider)
        container.inject_dependencies()
        return NestApplication(container.controllers)
