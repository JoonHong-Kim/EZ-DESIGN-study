from abc import ABC, abstractmethod
from pydantic import BaseModel


class Memory(BaseModel, ABC):
    data: list[int]

    @property
    def size(self) -> int:
        return len(self.data)

    @abstractmethod
    def read(self, idx: int) -> int:
        pass


class Ram(Memory):
    def read(self, idx: int) -> int:
        return self.data[idx]

    def write(self, idx: int, value: int):
        self.data[idx] = value


class Rom(Memory):
    def read(self, idx: int) -> int:
        return self.data[idx]


class MemoryFactory(ABC):
    @staticmethod
    @abstractmethod
    def make_memory(*args, **kwargs) -> Memory:
        pass


class RamFactory(MemoryFactory):
    @staticmethod
    def make_memory(size: int) -> Ram:
        return Ram(data=list(range(size)))


class RomFactory(MemoryFactory):
    @staticmethod
    def make_memory(data: list[int]) -> Rom:
        return Rom(data=data)
