from typing import Optional

from cats.entity import Cat
from cats.service import CatsService
from nestpy.common import Body, Controller, Get, Param, Post, Query


@Controller()
class CatsController:
    def __init__(self, service: CatsService):
        self.service = service

    @Post()
    def create(self, cat: Body[Cat]):
        return self.service.create(cat.data)

    @Get()
    def list(self, gender: Optional[Query[str]] = None) -> list[Cat]:
        return self.service.list(gender=gender.data if gender else None)

    @Get(":id")
    def get(self, id: Param[str]):
        return self.service.get(id.data)
