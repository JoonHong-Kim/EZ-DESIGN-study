from pydantic import BaseModel


class Cat(BaseModel):
    id: str
    name: str
    gender: str
