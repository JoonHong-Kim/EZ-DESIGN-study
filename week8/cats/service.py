from typing import Optional

from cats.entity import Cat
from nestpy.common import Injectable

cats: list[Cat] = [
    Cat(id="1", name="Garfield", gender="M"),
    Cat(id="2", name="Tom", gender="F"),
]


@Injectable()
class CatsService:
    def create(self, cat: Cat):
        for c in cats:
            if c.id == cat.id:
                raise Exception("Cat already exists")
        cats.append(cat)
        return cat

    def list(self, gender: Optional[str] = None):
        filter = lambda cat: cat.gender == gender if gender else True
        return [cat for cat in cats if filter(cat)]

    def get(self, id: str):
        for cat in cats:
            if cat.id == id:
                return cat
        raise Exception("Cat not found")
