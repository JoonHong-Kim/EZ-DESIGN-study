from cats.controller import CatsController
from cats.service import CatsService
from nestpy.common import Module


@Module({"controller": CatsController, "provider": CatsService})
class CatsModule:
    pass
