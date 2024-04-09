from cats.module import CatsModule
from nestpy.core import NestFactory


def bootstrap():
    app = NestFactory.create(CatsModule)
    app.serve()


bootstrap()
